''' 
GenieMonitor Traceback Check Plugin for IOSXE.
'''

# GenieMonitor
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
        parser.add_argument('--tracebackcheck_logic_pattern',
                            action="store",
                            default="Or('Traceback', 'SERVICE_CRASHED', 'BADSLOT',\
                                        'out of sync', 'HA_CONFIG_SYNC\-\[1234\]',\
                                        'out of spec', 'CPUHOG', 'DUPLEX_MISMATCH',\
                                        'EREVENT', 'ERRMSG', 'LINECARDDS384MAJOREVENT',\
                                        'fib root', 'PXF root tables', 'Invalid', \
                                        'IPC failure', 'IRONBUS_FAULT', 'LCHUNG',\
                                        'LINECARDSEEPROMREADFAILED', 'MALLOCFAIL',\
                                        'BLOCKEDTXQUEUE', 'NOIFINDEX', 'INITFAIL',\
                                        'NSE100', 'Restarting Pxf', 'PXF_CRASHINFO',\
                                        'TFIB\-2\-MEMORY', 'TOASTER\-2\-FAULT')",
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