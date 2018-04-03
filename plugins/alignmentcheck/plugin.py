'''
GenieMonitor Alignment Check Plugin.
'''

# Python
import re
import logging

# ATS
from ats.log.utils import banner
from ats.utils import parser as argparse
from ats.datastructures import classproperty

# GenieMonitor
from genietelemetry.plugins.bases import BasePlugin
from genietelemetry.results import OK, WARNING, ERRORED, PARTIAL, CRITICAL

# module logger
logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    __plugin_name__ = 'Alignment Check Plugin'

    @classproperty
    def parser(cls):
        parser = argparse.ArgsPropagationParser(add_help = False)
        parser.title = 'Alignment Check'
        
        # timeout
        # -------
        parser.add_argument('--timeout',
                            action="store",
                            default=300,
                            help='Specify duration (in seconds) to wait before '
                                 'timing out execution of a command')
        return parser


    def execution(self, device, execution_time):

        # Init
        status = OK
        message = ''

        # Execute command to check for tracebacks - timeout set to 5 mins
        output = device.execute(self.show_cmd, timeout=self.args.timeout)
        if not output:
            return ERRORED('No output from {cmd}'.format(cmd=self.show_cmd))

        # Check for alignment errors. Hex values = problems.
        if '0x' in output:
            message = "Device {d} Alignment error detected: '{o}'"\
                .format(d=device.name, o=output)
            status += CRITICAL(message)
            logger.error(banner(message))

        # Log message to user
        if not message:
            message = "***** No alignment error found *****"
            status += OK(message)
            logger.info(banner(message))

        # Final status
        return status
