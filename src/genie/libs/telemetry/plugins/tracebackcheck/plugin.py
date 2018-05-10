'''
GenieTelemetry Traceback Check Plugin.
'''

# Python
import re
import logging
import copy

# argparse
from ats.utils import parser as argparse

# ATS
from ats.log.utils import banner
from ats.datastructures.logic import logic_str
from ats.datastructures import classproperty

# GenieTelemetry
from genie.telemetry.plugin import BasePlugin
from genie.telemetry.status import OK, WARNING, ERRORED, PARTIAL, CRITICAL
from genie.libs.telemetry.plugins import libs

# Abstract
from genie.abstract import Lookup

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
        parser.add_argument('--tracebackcheck_logic_pattern',
                            action="store",
                            default="And('Traceback')",
                            help='Specify logical expression for patterns to '
                                 'include/exclude when checking tracebacks '
                                 'following PyATS logic format. Default pattern'
                                 'is to check for Tracebacks.')
        # clean_up
        # --------
        parser.add_argument('--tracebackcheck_clean_up',
                            action="store",
                            default=True,
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
        if not self.parser:
            return

        argv = copy.copy(argv)

        # avoid parsing unknowns
        self.args, _ = self.parser.parse_known_args(argv)

    def execution(self, device, **kwargs):

        # Init
        status = OK
        matched_lines_dict = {}

        lookup = Lookup.from_device(device)

        # Execute command to check for tracebacks - timeout set to 5 mins
        output = lookup.libs.utils.check_tracebacks(device,
            timeout=self.args.tracebackcheck_timeout)
        if not output:
            return ERRORED('No output from {cmd}'.format(cmd=self.show_cmd))

        # Logic pattern
        match_patterns = logic_str(self.args.tracebackcheck_logic_pattern)

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
        if self.args.tracebackcheck_clean_up:
            try:
                output = lookup.libs.utils.clear_tracebacks(device,
                    timeout=self.args.tracebackcheck_timeout)
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
