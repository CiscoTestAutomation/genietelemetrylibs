'''
GenieMonitor Traceback Check Plugin.
'''

# Python
import re
import logging

# ATS
from ats.log.utils import banner
from ats.utils import parser as argparse
from ats.datastructures import classproperty
from ats.datastructures.logic import logic_str

# GenieMonitor
from geniemonitor.plugins.bases import BasePlugin
from geniemonitor.results import OK, WARNING, ERRORED, PARTIAL, CRITICAL

# module logger
logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    __plugin_name__ = 'Traceback Check Plugin'

    @classproperty
    def parser(cls):
        parser = argparse.ArgsPropagationParser(add_help = False)
        parser.title = 'Traceback Check'
        
        # logic_pattern
        # -------------
        parser.add_argument('-logic_pattern',
                            action="store",
                            default="And('Traceback')",
                            help='Specify logical expression for patterns to '
                                 'include/exclude when checking tracebacks '
                                 'following PyATS logic format. Default pattern'
                                 'is to check for Tracebacks.')
        # clean_up
        # --------
        parser.add_argument('-clean_up',
                            action="store",
                            default=False,
                            help='Specify whether to clear all warnings and '
                                 'tracebacks after reporting error')
        # timeout
        # -------
        parser.add_argument('-timeout',
                            action="store",
                            default=300,
                            help='Specify duration (in seconds) to wait before '
                                 'timing out execution of a command')
        return parser


    def execution(self, device, execution_time):

        # Init
        status = OK
        matched_lines_dict = {}

        # Execute command to check for tracebacks - timeout set to 5 mins
        output = device.execute(self.show_cmd, timeout=self.args.timeout)
        if not output:
            return ERRORED('No output from {cmd}'.format(cmd=self.show_cmd))

        # Logic pattern
        match_patterns = logic_str(self.args.logic_pattern)

        # Parse 'show logging logfile' output for keywords
        matched_lines_dict['matched_lines'] = []
        for line in output.splitlines():
            if match_patterns(line):
                matched_lines_dict['matched_lines'].append(line)
                message = "Matched pattern in line: '{line}'".format(line=line)
                status += CRITICAL(message)
                status += CRITICAL(matched_lines_dict)
                logger.error(banner(message))

        # Log message to user
        if not matched_lines_dict['matched_lines']:
            message = "***** No patterns matched *****"
            status += OK(message)
            logger.info(banner(message))

        # Clear logging (if user specified)
        if self.args.clean_up:
            try:
                device.execute(self.clear_cmd)
                message = "Successfully cleared logging"
                status += OK(message)
                logger.info(banner(message))
            except Exception as e:
                # Handle exception
                logger.warning(e)
                message = "Clear logging execution failed"
                logger.error(message)
                status += ERRORED(message)

        # Final status
        return status
