# -*- coding: utf-8 -*-
import requests
import re
import json
import time
import optparse

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class pyKevo(object):

    #site specific domina information
    _signin     = 'signin'
    _login      = 'login'

    _unlock     = 'user/remote_locks/command/remote_unlock.json?arguments='
    _lock       = 'user/remote_locks/command/remote_lock.json?arguments='
    _info       = 'user/remote_locks/command/lock.json?arguments='

    #base domain, set during self.__init__()
    _site       = ''

    #site credentials
    _username   = ''
    _password   = ''

    #session based information
    _token      = ''        #token issued during session
    _session    = ''        #holds the entire session information, cookies, headers etc...

    #lock information
    _lock_id    = ''
    _lock_data  = ''

    #updating state information
    _previous_lock_state = ''
    _last_refresh        = ''
    _confirmed           = False


    #TODO: Need something to check if the issued command was successful.  maybe a timer / maybe a series of checks
    #TODO: only works for one lock, as I only owns one lock so I cant test

    def __init__(self, username, password, site='https://www.mykevo.com/'):
        self._username   = username
        self._password   = password

        self._site       = site

        self._session    = requests.Session()

    def _retrieveAndSetToken(self):

        r = self._session.get(self._site + self._login, verify=False)

        page = r.text

        p = re.compile(r'input name="authenticity_token".*?value=\"(.*?)\"', re.MULTILINE | re.DOTALL)
        values = re.findall(p, page)

        self._token = values[0].strip()

    def _extractLockId(self,html):

        p = re.compile(r'<div class=\'lock_unlock_container\' data-bolt-state=\'.*?\' data-lock-id=\'(.*?)\' id', re.MULTILINE | re.DOTALL)
        values = re.findall(p, html)

        self._lock_id = values[0].strip()

    def _refreshLockInformation(self):
        r = self._session.get(self._site + self._info + self._lock_id)

        self._lock_data = json.loads(r.text)

######## ######## ######## ######## ######## ######## public definitions ######## ######## ########
    def connect(self):

        self._retrieveAndSetToken()

        r = self._session.post(self._site + self._signin,

                   data={"user[username]"       : self._username,
                         "user[password]"       : self._password,
                         "authenticity_token"   : self._token,

                         "commit"               : "Sign In",
                         "utf8"                 : "✓"})
                         # I dont think the utf8 option is required,  possibly move in future

        self._extractLockId(r.text)

        self._refreshLockInformation()

    def returnLockInfo(self):
        return self._lock_data

    def lockState(self):
        return self._lock_data["bolt_state"]

    def _action_confirmation(self):

        #TODO: timeout function needs to be included

        while self._previous_lock_state == self._lock_data["bolt_state"]:

            #TODO: This should be random.  Or based on the same functionality as the site

            time.sleep(1000)

            self._refreshLockInformation()


######## ######## ######## ######## ######## ######## action definitions ######## ######## ########


    #TODO: Lock and Unlock need a verification.  Some means of knowing they worked

    def unlockLock(self):
        self._previous_lock_state = self._lock_data["bolt_state"]

        r = self._session.get(self._site + self._unlock + self._lock_id)


    def lockLock(self):
        self._previous_lock_state = self._lock_data["bolt_state"]

        r = self._session.get(self._site + self._lock + self._lock_id)


    def toggleLock(self):
        if self.lockState() == "Unlocked":
            self.lockLock()
        else:
            self.unlockLock()

        #this needs to be implemented in the respective action call

        #time.sleep(3)
        #self._refreshLockInformation()


def main():

    p = optparse.OptionParser()

    p.add_option('--email',     '-e',   dest='email',   default="none",  help='Parameter: This is the email address you use at https://mykevo.com/')
    p.add_option('--password',  '-p',   dest='password',default="none",  help='Parameter: This is the password you use for https://mykevo.com/')

    #actions
    p.add_option('--status',    '-s',   dest='status',  default=False,  action="store_true",    help='Action: Report on current status of lock: \'Locker\' \'Unlocked\'')
    p.add_option('--info',      '-i',   dest='info',    default=False,  action="store_true",    help='Action: Get lock info')
    p.add_option('--lock',      '-l',   dest='lock',    default=False,  action="store_true",    help='Action: Issues Command to Lock Kevo Smartlock')
    p.add_option('--unlock',    '-u',   dest='unlock',  default=False,  action="store_true",    help='Action: Issues Command to UnLock Kevo Smartlock')

    options, arguments = p.parse_args()

    if valid_options(options,arguments):

        Door = pyKevo(options.email,options.password)
        Door.connect()

        if options.status:
            print Door.lockState()

        if options.info:
            print Door.returnLockInfo()

        if options.lock:
            Door.lockLock()

        if options.unlock:
            Door.unlockLock()

    else:
        p.print_help()
        print
        print "example: python pyKevo --email=\"mail@home.com\" --password=\"passw0rd\" --unlock"
        print

def valid_options(cli_options,cli_arguments):
    switch_count = cli_options.status + cli_options.info + cli_options.lock + cli_options.unlock

    if switch_count > 1:
        print "Bad Command: You can only submit one action at a time"
        return False

    if switch_count == 0:
        print "you must specify an action"
        return False

    if cli_options.email=="none" or cli_options.password == "none":
        print "You forgot to supply credentials"
        return False

    return True

if __name__ == '__main__':
    main()