# ghlutil.py

This tiny utility is intended for issue migration **from** Gitlab **to** Github (Enterprise).

Under development.

# TODO

* issues
* save
* delete all the labels of a github repo.
* create 
* Look into this: https://github.com/piceaTech/node-gitlab-2-github


```
$ python3 ghlutil.py -h
usage: ghlutil.py [-h] [--profile PROFILE] [-c CONFIG] [-t TARGET]
                  [-o OPERATION]

ghlutil.py

optional arguments:
  -h, --help            show this help message and exit
  --profile PROFILE
  -c CONFIG, --config CONFIG
  -t TARGET, --target TARGET
  -o OPERATION, --operation OPERATION
```


```yaml
profiles:
  - name: 'ghe_destination'
    url: 'https://ghe.example.com/api/v3'
    scm_type: 'github'
    organization: 'some_organization_at_destination'
    repository: 'your_ghe_repository'
    token: 'ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

  - name: 'gitlab_source'
    url: 'http://gitlab.example.com'
    scm_type: 'gitlab'
    organization: 'some_organization_at_source'
    repository: 'general'
    token: 'GITLABTOKENGITLABTOK'


```
