'''
GenieMonitor InterfacesUpCheck Plugin
'''
# Python
import re
import copy
import logging

# argparse
from argparse import ArgumentParser

# ATS
from ats.log.utils import banner
from ats.utils import parser as argparse
from ats.datastructures import classproperty
from ats.utils.objects import find, R

# GenieMonitor
from genie.telemetry.status import OK, WARNING, ERRORED, PARTIAL, CRITICAL

# Genie
from genie.utils.timeout import Timeout

# module logger
logger = logging.getLogger(__name__)


class Plugin(object):

    __plugin_name__ = 'Ethernet Interfaces Status Check Plugin'

    @classproperty
    def parser(cls):
        parser = argparse.ArgsPropagationParser(add_help = False)
        parser.title = 'Ethernet Interfaces Status Check'

        # timeout
        # -------
        parser.add_argument('--interfacesupcheck_timeout',
                            action="store",
                            default=60,
                            help = "Specify poll timeout value\ndefault "
                                   "to 60 seconds")
        # interval
        # -------
        parser.add_argument('--interfacesupcheck_interval',
                            action="store",
                            default=20,
                            help = "Specify poll interval value\ndefault "
                                   "to 20 seconds")
        # interfaces_to_check
        # -------------------
        parser.add_argument('--interfaces_to_check',
                            action="store",
                            default='all',
                            help = "Specify the interfaces want to be checked\n"
                                   "default to check ALL Ethernet")
        # five_min_percentage
        # -------------------
        parser.add_argument('--expected_status',
                            action="store",
                            default='up',
                            help = "Specify expected status of "
                                   "interfaces\ndefault "
                                   "to up")
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
        
        # create timeout object
        timeout = Timeout(max_time=int(self.args.interfacesupcheck_timeout),
                          interval=int(self.args.interfacesupcheck_interval))

        # loop status
        loop_stat_ok = True

        if not hasattr(self, 'PARSER_MODULE'):
            return WARNING('Does not have interfaces related parsers to check')

        # print out message
        logger.info('Check if {} interfaces are UP'.format(
            self.args.interfaces_to_check))


        while timeout.iterate():
            # Execute command to get five minutes usage percentage
            try:
                intf_dict = self.PARSER_MODULE(device).parse()
            except Exception as e:
                return ERRORED('No output from show interface brief\n{}'.format(e))

            # will take argument for interface
            paths = [['interface', 'ethernet', '(?P<intf>Eth.*)', 'reason', 'Administratively down'],
                     ['interface', 'ethernet', '(?P<intf>Eth.*)', 'status', 'down']]
            rs = [R(path) for path in paths]
            ret = find([intf_dict], *rs, filter_=False)

            if ret:
                for item in ret:
                    # get port number
                    m = re.search('[a-zA-Z]+(.*)', item[1][2])
                    port = m.groups()[0] if m else None
                    if 'all' in self.args.interfaces_to_check or \
                       port in self.args.interfaces_to_check:
                        message = 'Interface {} is not UP, try again'.format(item[1][2])
                        status += WARNING(message)
                        loop_stat_ok = False
                        timeout.sleep()
            else:
                message = 'Interfaces {} are UP'.format(self.args.interfaces_to_check)
                status += OK(message)
                loop_stat_ok = True
                logger.info(message)
                break

        if not loop_stat_ok:
            message = ''
            for intf in ret:
                message += 'Interface {i} is not UP within givin timeout ({s} seconds)\n'.format(
                    i=item[1][2], s=self.args.interfacesupcheck_timeout)
            status += CRITICAL(message)
            logger.error(banner(message))


        # Final status
        return status
