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
    __version__ = '1.0.0'
    __supported_os__ = ['nxos', 'iosxr', 'iosxe']

    @classproperty
    def parser(cls):
        parser = argparse.ArgsPropagationParser(add_help = False)
        parser.title = 'Traceback Check'

        # tracebackcheck_keywords
        # -----------------------
        parser.add_argument('--tracebackcheck_keywords',
                            action="store",
                            help="Specify comma-separated string of keywords to"
                                 " search within the 'show logging' output.\n"
                                 "Default: 'Traceback'")

        # tracebackcheck_disable_traceback
        # --------------------------------
        parser.add_argument('--tracebackcheck_disable_traceback',
                            action="store",
                            default=False,
                            help="Disable check for 'Traceback' keyword within "
                                 "logging output.\nDefault: False")

        # tracebackcheck_clean_up
        # -----------------------
        parser.add_argument('--tracebackcheck_clean_up',
                            action="store",
                            default=True,
                            help='Specify whether to clear all warnings and '
                                 'tracebacks after reporting error')

        # tracebackcheck_timeout
        # ----------------------
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

        # Default pattern to search for
        logic_string = "\'Traceback\'"

        # Execute command to check for tracebacks - timeout set to 5 mins
        output = lookup.libs.utils.check_tracebacks(device,
            timeout=self.args.tracebackcheck_timeout)
        if not output:
            message = "No patterns {patterns} found in '{cmd}'".format(
                patterns= self.args.tracebackcheck_logic_pattern,
                cmd=self.show_cmd)
            status += OK(message)
            logger.info(message)
            return status

        # Add in user provided keywords
        if self.args.tracebackcheck_keywords:
            for item in self.args.tracebackcheck_keywords.split(', '):
                logic_string += ", \'{}\'".format(item.strip())

        # Remove keyword 'Traceback' if user requested
        if self.args.tracebackcheck_disable_traceback:
            logic_string.replace("\'Traceback\', ", "")

        # Create final logic pattern to match in 'show logging logfile' output
        match_patterns = logic_str("Or({})".format(logic_string.strip()))

        # Parse 'show logging logfile' output for keywords
        matched_lines_dict['matched_lines'] = []
        for line in output.splitlines():
            if match_patterns(line):
                matched_lines_dict['matched_lines'].append(line)
                message = "Matched pattern in line: '{line}'".format(line=line)
                status += CRITICAL(message)
                status += CRITICAL(matched_lines_dict)
                logger.error(message)

        # Log message to user
        if not matched_lines_dict['matched_lines']:
            message = "No patterns {patterns} matched".format(
                patterns= self.args.tracebackcheck_logic_pattern)
            status += OK(message)
            logger.info(message)

        # Clear logging (if user specified)
        if self.args.tracebackcheck_clean_up:
            try:
                output = lookup.libs.utils.clear_tracebacks(device,
                    timeout=self.args.tracebackcheck_timeout)
                message = "Successfully cleared logging"
                status += OK()
                logger.info(message)
            except Exception as e:
                # Handle exception
                logger.warning(e)
                message = "Clear logging execution failed"
                logger.error(message)
                status += ERRORED()

        # Final status
        return status
