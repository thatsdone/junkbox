#!/usr/bin/python
# 
# vyatta1.py : An example to work with vyatta using pexpect.
#
# This script is based on an example script, monitor.py,
# contained in 'pexpect-2.3.tar.gz'.
#
import sys
import pexpect

host = 'HOSTNAME_OR_IPADDRESS'
user = 'vyatta' # Usually no need to rewrite.
password = 'PASSWORD'

COMMAND_PROMPT = '[#$] ' ### This is way too simple for industrial use -- we will change is ASAP.
TERMINAL_PROMPT = '(?i)terminal type\?'
TERMINAL_TYPE = 'vt100'
# This is the prompt we get if SSH does not have the remote host's public key stored in the cache.
SSH_NEWKEY = '(?i)are you sure you want to continue connecting'

def config_main():
    global COMMAND_PROMPT, TERMINAL_PROMPT, TERMINAL_TYPE, SSH_NEWKEY
    #
    # Login via SSH
    #
    child = pexpect.spawn('ssh -l %s %s'%(user, host))
    i = child.expect([pexpect.TIMEOUT, SSH_NEWKEY, COMMAND_PROMPT, '(?i)password'])
    if i == 0: # Timeout
        print 'ERROR! could not login with SSH. Here is what SSH said:'
        print child.before, child.after
        print str(child)
        sys.exit (1)
    if i == 1: # In this case SSH does not have the public key cached.
        child.sendline ('yes')
        child.expect ('(?i)password')
    if i == 2:
        # This may happen if a public key was setup to automatically login.
        # But beware, the COMMAND_PROMPT at this point is very trivial and
        # could be fooled by some output in the MOTD or login message.
        pass
    if i == 3:
        child.sendline(password)
        # Now we are either at the command prompt or
        # the login process is asking for our terminal type.
        i = child.expect ([COMMAND_PROMPT, TERMINAL_PROMPT])
        if i == 1:
            child.sendline (TERMINAL_TYPE)
            child.expect (COMMAND_PROMPT)
    #
    # Set command prompt to something more unique.
    #
    COMMAND_PROMPT = "\[PEXPECT\]\$ "
    child.sendline ("PS1='[PEXPECT]\$ '") # In case of sh-style
    i = child.expect ([pexpect.TIMEOUT, COMMAND_PROMPT], timeout=10)
    if i == 0:
        print "# Couldn't set sh-style prompt -- trying csh-style."
        child.sendline ("set prompt='[PEXPECT]\$ '")
        i = child.expect ([pexpect.TIMEOUT, COMMAND_PROMPT], timeout=10)
        if i == 0:
            print "Failed to set command prompt using sh or csh style."
            print "Response was:"
            print child.before
            sys.exit (1)

    #
    # Debug: show uname
    #
    child.sendline ('uname -a')
    child.expect (COMMAND_PROMPT)
    print child.before

    #
    # Debug: tty information
    #
    child.sendline ('tty')
    child.expect (COMMAND_PROMPT)
    print child.before

    #
    # Example: Get configuration mode. (IMPORANT)
    #
    # change prompt string at first. (work around)
    # Note: 'vyatta' of '@vyatta' should be re-written.
    COMMAND_PROMPT = "vyatta@vyatta# "
    child.sendline ('configure')
    child.expect (COMMAND_PROMPT)
    print child.before

    #
    # Example: suppress pager to automation. (IMPORANT)
    #
    child.sendline ('export VYATTA_PAGER=')
    child.expect (COMMAND_PROMPT)
    print child.before

    #
    # Example: show ntp servers, and show multi lines result so that
    #          we can parse it and handle them appropriately.
    child.sendline ('show system ntp server')
    child.expect (COMMAND_PROMPT)
    result = child.before
    print result
    # we get '^M' (\r) in each line, so throw it away.
    result = result.replace('\r', '')
    for l in result.split('\n'):
        print '  ', l

    # Initlally, vyatta installation refeers (1|2|3).vyatta.pool.ntp.org
    child.sendline ('delete system ntp server 2.vyatta.pool.ntp.org')
    child.expect (COMMAND_PROMPT)
    print child.before
    child.sendline ('delete system ntp server 1.vyatta.pool.ntp.org')
    child.expect (COMMAND_PROMPT)
    print child.before
    child.sendline ('delete system ntp server 0.vyatta.pool.ntp.org')
    child.expect (COMMAND_PROMPT)
    print child.before
    #
    # Example: show the result
    #
    child.sendline ('show system ntp server')
    child.expect (COMMAND_PROMPT)
    print child.before

    #
    # Example: save your changes (IMPORANT)
    #
    child.sendline ('save')
    child.expect (COMMAND_PROMPT)
    print child.before

    #
    # Example: commit your changes (IMPORANT)
    #
    child.sendline ('commit')
    child.expect (COMMAND_PROMPT)
    print child.before
#
#
#
config_main()


