# vim: tabstop=4 shiftwidth=4 softtabstop=4
#!/usr/bin/python
#
#
#
import sys
import time
import logging
from daemon import runner
#
# An example daemon main logic application class.
# Just keep writing timestamps to a log file periodically.
#
class App:
    def __init__(self):
        # python-daemon DaemonRunner requires the below.
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        # For debug, you can use '/dev/tty' for stdout/stderr instead.
        #self.stdout_path = '/dev/tty'
        #self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5
        # The above 5 attributes are mandatory.
        #
        # The below are this App specific.
        self.foreground = False
        self.log_file = '/tmp/foobar.log'

    def run(self):
        # Here is your main logic.
        # Initializing code.
        if not self.foreground:
            logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s',
                            filename=self.log_file,
                            filemode='a')
        while True:
            # the main loop code.
            try: 
                str = time.asctime(time.localtime(time.time()))
                if self.foreground:
                    print str
                else:
                    logging.info('DEBUG: %s' % str)

                time.sleep(1)
            except:
                logging.info(sys.exc_info())
                logging.info('Terminating.')
                sys.exit(1)

if __name__ == '__main__':

    daemonize = 1
    if len(sys.argv) > 1:
        if sys.argv[1] not in ['start', 'stop', 'restart']:
            print 'Specify start or stop or restart as the first argument'
            sys.exit(0)
        for key in sys.argv[2:]:
            if key.startswith('daemonize='):
                daemonize = key.split('=')[1]
    else:
        print 'Specify start or stop or restart as the first argument'
        sys.exit(0)
    #
    #
    #
    app = App()
    if (daemonize != 0):
        daemon_runner = runner.DaemonRunner(app)
        daemon_runner.detach_process = True
        daemon_runner.do_action()
        app.foreground = True
    else:
        app.run()
