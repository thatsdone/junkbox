#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ghlutil.py: A tiny utility to migrate repositories (especially issues) from
#             Gitlab to Github (Enterprise)
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2023/02/05 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# NOTE:
#   * UNDER DEVELOPMENT!!
import json
import yaml
import sys
import time
import github.GithubObject as gho
from github.GithubObject import NotSet

def op_gitlab_auth(url, token):
    import gitlab
    gl = gitlab.Gitlab(url=url, private_token=token)
    gl.auth()
    return gl

def op_gitlab(gl, group, project):
    nsprj = '%s/%s' % (group, project)
    project = gl.projects.get(nsprj)
    #
    # group labels
    #
    labels = project.labels.list()
    for label in labels:
        print(label)
    #
    # issues
    #
    issues = project.issues.list(all=True)
    num_issues = len(issues)
    num_opened_issues = 0
    for issue in issues:
        if issue.state == 'opened':
            notes = issue.notes.list()
            print('%s %s %s %s (#notes = %d)' % (issue.id, issue.iid, issue.title, issue.state, len(notes)))
            num_opened_issues += 1
        if issue.iid == 157:
            print(issue)
            for note in notes:
                print(note)
    print('all / opened = %d / %d' % (num_issues, num_opened_issues))


def op_gitlab_labels(gl, group, project):
    gl_labels = list()

    nsprj = '%s/%s' % (group, project)
    project = gl.projects.get(nsprj)
    labels = project.labels.list()
    for label in labels:
        print(label)
        gl_labels.append({'name': label.name,  'color': label.color, 'description': label.description, 'id': label.id})

    print(yaml.dump(gl_labels))

    gl_label_file = 'gl_labels.yaml'
    with open(gl_label_file, 'w') as fp:
        yaml.dump(gl_labels, fp, encoding='utf-8', allow_unicode=True)


def op_gitlab_issues(gl, group, project, op=None):
    nsprj = '%s/%s' % (group, project)
    #print(nsprj)
    project = gl.projects.get(nsprj)
    issues = project.issues.list(all=True)
    num_issues = len(issues)
    num_opened_issues = 0

    gl_issues = list()

    if op == 'list':
        for issue in issues:
            gl_issues.append({'id': issue.iid,
                              'title': issue.title,
                              'state': issue.state,
                              'labels': issue.labels,
                              'description': issue.description})
            num_opened_issues += 1
            if issue.iid == 170:
                print(issue)
                print(gl_issues[0])

    elif op == 'save' :
        gl_issues_file = 'gl_issues.yaml'
        with open(gl_issues_file, 'w') as fp:
            yaml.dump(gl_issues, fp, encoding='utf-8', allow_unicode=True)
#
# github
#
def op_github_auth(url, token):
    from github import Github
    gh = Github(base_url=url, login_or_token=token)
    return gh

def op_github(gh, organizatin, repository):
    return


def op_github_labels(gl, organization, repository, op=None):
    gh_labels = list()

    repo = None
    # 'group' is required. Either 'organization' or 'owner'
    repo = gh.get_repo('%s/%s' % (organization, repository))
    #
    print('repo: %s found' % (repo))
    #

    if op == 'list':
        labels = repo.get_labels()
        label_to_delte = None
        for label in labels:
            #print(label, label.name, (label.color), label.description, label.url)
            gh_labels.append({'name': label.name,  'color': label.color, 'description': label.description})
            if label.name == 'mitoh1':
                print('deleteing label: %s' % (label.name))
                label.delete()
                break
        print(yaml.dump(gh_labels))

    if op == 'delete':
        labels = repo.get_labels()
        label_to_delte = None
        for label in labels:
            print('deleteing label: %s' % (label.name))
            label.delete()

    elif op == 'save':
        print(yaml.dump(gh_labels))
        gh_label_file = 'gh_labels.yaml'
        with open(gh_label_file, 'w') as fp:
            yaml.dump(gh_labels, fp, encoding='utf-8', allow_unicode=True)

    elif op == 'migrate':
        gl_label_file = 'gl_labels.yaml'
        gl_labels_db = None
        with open(gl_label_file) as fd:
            gl_labels_db = yaml.load(fd, Loader=yaml.SafeLoader)
        if not gl_labels_db:
            print('failed to load gitlab label file')
            sys.exit()
        print(len(gl_labels_db))
        gl_labels = dict()
        for label in gl_labels_db:
            if not label['name'] in gl_labels.keys():
                gl_labels[label['name']] = {
                    'color': label['color'].replace('#', '').lower(),
                    'description': label['description']
                }
            #print('%s %s %s' % (label['name'],
            #                 label['color'],
            #                 label['description']))
        #print(len(gl_labels_db), gl_labels_db)
        #print(len(gl_labels), gl_labels)
        for k in gl_labels.keys():
            print(k, gl_labels[k]['color'], gl_labels[k]['description'])
            if gl_labels[k]['description']:
                repo.create_label(k,
                                  gl_labels[k]['color'],
                                  description=gl_labels[k]['description'])
            else:
                repo.create_label(k, gl_labels[k]['color'])

def op_github_issues(gh, organizatin, repository, op=None):

    repo = gh.get_repo('%s/%s' % (organization, repository))
    if not repo:
        print('repository: %s not found' % (repository))
        return

    # open src repository issuel list
    issues_file = 'gl_issues.yaml'
    issues_list = None
    with open(issues_file) as fd:
         issues_list = yaml.load(fd, Loader=yaml.SafeLoader)

    print('source repository issue file \'%s\' opened. %d issues. ' % (issues_file, len(issues_list)))
    # reserve issue numbers
    #op = 'reserve_issue_numbers'
    op = 'migrate_issue_bodies'
    #
    # reserve github issue 'number'
    #
    if op == 'reserve_issue_numbers':
        print('list of issues')
        new_issues = repo.get_issues(state='all')
        for issue in new_issues:
            print(issue.id, issue.number, issue)

        sys.exit()
        for num in range(1, len(issues_list) + 1):
            print('creating issue %d' % (num))
            repo.create_issue('issue %d placeholder' % num, body='')
            time.sleep(1)

        print('list of issues')
        new_issues = repo.get_issues(state='all')
        for issue in new_issues:
            print(issue)
    #
    #
    #
    elif op == 'migrate_issue_bodies':
        for issue in issues_list:
            # gitlab issue['id'] is 'number'
            # get_issue() not get_issues()
            gh_issue = repo.get_issue(issue['id'])
            print(gh_issue)
            gh_issue.edit(title=issue['title'], body=issue['description'],
                          milestone=None)
            time.sleep(1)

if __name__ == "__main__":

    config_file = 'config.yaml'
    conf = None
    url = None
    token = None
    organization = None
    repository = None
    scm_type = None
    profile = None

    if len(sys.argv) >= 2:
        profile = sys.argv[1]
    else:
        profile = 'ghe_destination'

    with open(config_file) as fd:
        conf = yaml.load(fd, Loader=yaml.SafeLoader)
    if not conf:
        print('Specify a config file')
        sys.exit()
    print('searching \'%s\' in %s' % (profile, config_file) )
    for p in conf['profiles']:
        print(p['name'], p['scm_type'], p['url'], p['organization'], p['repository'])
        if p['name'] == profile:
            url = p['url']
            token = p['token']
            organization = p['organization']
            repository = p['repository']
            scm_type = p['scm_type']
            break
    #
    #
    #
    if scm_type == 'gitlab':
        gl = op_gitlab_auth(url, token)
        #op_gitlab(gl, organization, repository)
        op_gitlab_issues(gl, organization, repository, op='list')
        #op_gitlab_labels(gl, organization, repository)
    elif scm_type == 'github':
        gh = op_github_auth(url, token)
        #op_github(gh, organization, repository)
        op_github_labels(gh, organization, repository, op='migrate')
