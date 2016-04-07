#!/usr/bin/python
# 
# vyos-config.py : An example to work with vyos using pexpect.
#
# This script is based on an example script, monitor.py, contained in 'pexpect-2.3.tar.gz'.
# 
# Author: Masanori Itoh <masanori.itoh@gmail.com>
#
import sys
import pexpect

class VyosConfig(object):
    host = ''
    user = 'vyos'
    password = ''
    hostname = 'vyos'
    
    child = None

    COMMAND_PROMPT = '[#$] '
    TERMINAL_PROMPT = '(?i)terminal type\?'
    TERMINAL_TYPE = 'vt100'
    # This is the prompt we get if SSH does not have the remote host's public key stored in the cache.
    SSH_NEWKEY = '(?i)are you sure you want to continue connecting'

    def __init__(self, host, user, password=''):
        self.host = host
        self.user = user
        self.password = password

    def set_host(self, host):
        self.host = host

    def set_user(self, user):
        self.user = user

    def set_password(self, password):
        self.password = password

    def set_command_prompt(self, prompt):
        self.COMMAND_PROMPT = prompt

    def set_terminal_prompt(self, prompt):
        self.TERMINAL_PROMPT = prompt

    def login(self):

        self.child = pexpect.spawn('ssh -l %s %s'%(self.user, self.host))
        i = self.child.expect([pexpect.TIMEOUT, self.SSH_NEWKEY, self.COMMAND_PROMPT, '(?i)password'])
        if i == 0: # Timeout
            print 'ERROR! could not login with SSH. Here is what SSH said:'
            print self.child.before, self.child.after
            print str(self.child)
            sys.exit (1)
            # In this case SSH does not have the public key cached.
        if i == 1:
            self.child.sendline ('yes')
            self.child.expect ('(?i)password')
        if i == 2:
            # This may happen if a public key was setup to 
            # automatically login.
            # But beware, the COMMAND_PROMPT at this point is 
            # very trivial and could be fooled by some output
            # in the MOTD or login message.
            pass
        if i == 3:
            self.child.sendline(self.password)
            # Now we are either at the command prompt or
            # the login process is asking for our terminal type.
            i = self.child.expect ([self.COMMAND_PROMPT, self.TERMINAL_PROMPT])
            if i == 1:
                self.child.sendline (self.TERMINAL_TYPE)
                self.child.expect (self.COMMAND_PROMPT)
        #
        # Set command prompt to something more unique.
        #
        COMMAND_PROMPT = "\[PEXPECT\]\$ "
        self.child.sendline ("PS1='[PEXPECT]\$ '") # In case of sh-style
        i = self.child.expect ([pexpect.TIMEOUT, self.COMMAND_PROMPT], timeout=10)
        if i == 0:
            print "# Couldn't set sh-style prompt -- trying csh-style."
            self.child.sendline ("set prompt='[PEXPECT]\$ '")
            i = self.child.expect ([pexpect.TIMEOUT, self.COMMAND_PROMPT], timeout=10)
            if i == 0:
                print "Failed to set command prompt using sh or csh style."
                print "Response was:"
                print self.child.before
                sys.exit (1)
                
    def cmd(self, cmd='', debug=False):
        self.child.sendline (cmd)
        self.child.expect (self.COMMAND_PROMPT)
        if debug:
            print self.child.before

    def configure(self):
        self.set_command_prompt(self.user + '@' + self.hostname + '# ')
        self.cmd('configure')
        # disable pager for automation
        self.cmd('export VYATTA_PAGER=')

    def commit(self):
        self.cmd('commit')

    def save(self):
        self.cmd('save')

    def logout(self):
        self.cmd('exit')
        self.set_command_prompt(self.user + '@' + self.hostname + ':~$ ')
        self.cmd('exit')
        sys.exit(0)


if __name__ == '__main__':
    vyos = VyosConfig('192.168.31.129', 'vyos', 'vyos')
    vyos.login()
    vyos.configure()
    #
    # example: show all configuration
    #
    vyos.cmd('show', debug=True)
    #
    # example: set IP address and default route
    #
    #vyos.cmd('set interfaces ethernet eth1 address 10.0.0.123/24')
    #vyos.cmd('set protocols static route 0.0.0.0/0 next-hop 10.0.0.1 distance 1')
    #
    # example: reconfigure ntp server
    #
    #vyos.cmd('delete ntp')
    #vyos.cmd('set ntp server ' + '10.0.0.2')
    #
    # example: enable ssh service on tcp 22
    #
    #vyos.cmd('set service ssh port 22')

    #vyos.logout()

    sys.exit(0)

