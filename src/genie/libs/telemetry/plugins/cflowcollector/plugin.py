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

        # cflow_dest
        # -------------------
        parser.add_argument('--cflow_dest',
                            action="store",
                            required = True,
                            default=None,
                            help = 'destination URL to copy cflow result to.'
                                   'example: tftp:/10.1.0.111/temp/')


        # cflow_verbose
        # ----------------------
        parser.add_argument('--cflow_verbose',
                            action = 'store_true',
                            default = False,
                            help = 'verbose cflow copy/clear output')


        # cflow_init_flag
        # ------------------------
        parser.add_argument('--cflow_init_flag',
                            action = 'store_true',
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

        # check cflow dest values
        parsed = urlparse(self.args.cflow_dest)

        try:
            assert parsed.scheme == 'tftp'
        except AssertionError as e:
            log.error(banner(str(e)))
            return ERRORED(str(e))

        try:
            assert parsed.path != ''
        except AssertionError as e:
            log.error(banner(str(e)))
            return ERRORED(str(e))

        try:
            assert self.args.cflow_dest.endswith('/')
        except AssertionError as e:
            log.error(banner(str(e)))
            return ERRORED(str(e))

        # get server address
        self.server = parsed.netloc
        # get path
        self.path = parsed.path

    def execution(self, device, **kwargs):

        # Init
        status = OK

        # get tftp server from testbed yaml
        tb = device.testbed

        # cflow package currently only supports tftp
        tftp = tb.servers.get('tftp', {}).get('address', None)

        # if provided server is not same as tb yaml, use yaml one
        if tftp and tftp not in self.server:
            logger.info('Provided tftp is %s, not same as the one in testbed yaml. '
                        'Will use testbed yaml server %s' % (self.server, tftp))
            self.server = tftp

        # create cflow object for clear and collect
        collector = CflowCollector(devices=[device], verbose=self.args.cflow_verbose)

        if self.args.cflow_init_flag:
            logger.info('clear process on device %s at the beginning' % device.name)
            collector.clear()

        # collect data
        logger.info('copy process on device %s' % device.name)
        try:
            collector.collect()
        except Exception as e:
            status += WARNING('Cannot collect data from device %s \n %s' % (device.name, str(e)))
            return status

        logger.info('export data to %s on device %s' % (self.args.cflow_dest,device.name))
        try:        
            ret = collector.export(dest=self.args.cflow_dest, server=self.server)
            assert ret
        except AssertionError as e:
            status += WARNING('There is no files are successfully exported from device %s' % device.name)
            return status
        except Exception as e:
            status += WARNING(str(e))
            return status

        # update status
        files = [os.path.join(self.path, f) for f in ret[0]]

        message = 'device %s cflow data exported to %s' % (device.name, files)
        status += OK(message)
        logger.info(banner(message))


        logger.info('clear data on device %s' % device.name)
        collector.clear()

        # Final status
        return status
     