''' 
GenieTelemetry Traceback Check Plugin for IOSXE.
'''

# genie.telemetry
from ..plugin import Plugin as BasePlugin

from ats.utils import parser as argparse
from ats.datastructures import classproperty

class Plugin(BasePlugin):

    show_cmd = 'show logging'
    clear_cmd = 'clear logging'


    @classproperty
    def parser(cls):
        parser = argparse.ArgsPropagationParser(add_help = False)
        parser.title = 'Traceback Check'
        
        # logic_pattern
        # -------------
        default_list = ('Traceback', 'SERVICE_CRASHED', 'BADSLOT',\
                        'out of sync', 'HA_CONFIG_SYNC\-\[1234\]',\
                        'out of spec', 'CPUHOG', 'DUPLEX_MISMATCH',\
                        'EREVENT', 'ERRMSG', 'LINECARDDS384MAJOREVENT',\
                        'fib root', 'PXF root tables', 'Invalid', \
                        'IPC failure', 'IRONBUS_FAULT', 'LCHUNG',\
                        'LINECARDSEEPROMREADFAILED', 'MALLOCFAIL',\
                        'BLOCKEDTXQUEUE', 'NOIFINDEX', 'INITFAIL',\
                        'NSE100', 'Restarting Pxf', 'PXF_CRASHINFO',\
                        'TFIB\-2\-MEMORY', 'TOASTER\-2\-FAULT')
        
        parser.add_argument('--tracebackcheck_logic_pattern',
                            action="store",
                            default="Or('Traceback')",
                            help='Specify logical expression for patterns to '
                                 'include/exclude when checking tracebacks '
                                 'following PyATS logic format. Default pattern'
                                 'is to check for Tracebacks.')
        # clean_up
        # --------
        parser.add_argument('--tracebackcheck_clean_up',
                            action="store",
                            default=False,
                            help='Specify whether to clear all warnings and '
                                 'tracebacks after reporting error')
        # timeout
        # -------
        parser.add_argument('--tracebackcheck_timeout',
                            action="store",
                            default=300,
                            help='Specify duration (in seconds) to wait before '
                                 'timing out execution of a command')
        return parser

    def parse_args(self, argv):
        '''parse_args

        parse arguments if available, store results to self.args. This follows
        the easypy argument propagation scheme, where any unknown arguments to
        this plugin is then stored back into sys.argv and untouched.

        Does nothing if a plugin doesn't come with a built-in parser.
        '''

        # do nothing when there's no parser
        super().parse_args(argv)

        # append pattern on the default list