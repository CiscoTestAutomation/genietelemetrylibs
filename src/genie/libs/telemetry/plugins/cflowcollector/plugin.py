'''
GenieTelemetry CflowCollection Plugin
'''
# Python
import os
import copy
import logging

# argparse
from argparse import ArgumentParser

# urllib
from urllib.parse import urlparse

# ATS
from ats import topology
from ats.log.utils import banner
from ats.utils import parser as argparse
from ats.datastructures import classproperty

# GenieTelemetry
from genie.telemetry.plugin import BasePlugin
from genie.telemetry.status import OK, WARNING, ERRORED, PARTIAL, CRITICAL

# Genie
from genie.utils.timeout import Timeout

# cflow
from cflow.collector import CflowCollector

# module logger
logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    __plugin_name__ = 'Cflow Data Collection Plugin'

    @classproperty
    def parser(cls):
        parser = argparse.ArgsPropagationParser(add_help = False)
        parser.title = 'Cflow Data Collection'

        # cflowcollector_dest
        # -------------------
        parser.add_argument('--cflowcollector_dest',
                            action="store",
                            required = True,
                            default=None,
                            help = 'destination URL to copy cflow result to')


        # cflowcollector_verbose
        # ----------------------
        parser.add_argument('--cflowcollector_verbose',
                            action = 'store',
                            default = False,
                            help = 'verbose cflow copy/clear output')


        # cflowcollector_init_flag
        # ------------------------
        parser.add_argument('--cflowcollector_init_flag',
                            action = 'store',
                            default = False,
                            help = 'True if process is in the inital status'
                                   ' which needs clear the devices left cflow data')
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

        # create cflow object for clear and collect
        collector = CflowCollector(devices=[device], verbose=self.args.cflowcollector_verbose)

        if self.args.cflowcollector_init_flag:
            logger.info('clear process on device %s at the beginning' % device.name)
            collector.clear()

        logger.info('copy process on device %s' % device.name)
        collector.collect()

        logger.info('export data to %s on device %s' % (self.args.cflowcollector_dest,device.name))
        parsed = urlparse(self.args.cflowcollector_dest)
        ret = collector.export(dest=self.args.cflowcollector_dest, server=parsed.netloc)

        # update status
        files = [os.path.join(parsed.path,f) for f in ret[0]]
        message = 'device %s cflow data exported to %s' % (device.name, files)
        status += OK(message)
        logger.info(banner(message))


        logger.info('clear data on device %s' % device.name)
        collector.clear()

        # Final status
        return status
     