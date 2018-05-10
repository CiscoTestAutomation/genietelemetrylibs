'''
GenieTelemetry Crashdumps Plugin
'''

# Python
import copy

# argparse
from argparse import ArgumentParser

# ATS
from ats.utils import parser as argparse
from ats.datastructures import classproperty

# GenieTelemetry
from genie.telemetry.plugin import BasePlugin
from genie.telemetry.status import OK, CRITICAL
from genie.libs.telemetry.plugins import libs

# Abstract
from genie.abstract import Lookup


class Plugin(BasePlugin):

    __plugin_name__ = 'Crash Dumps Plugin'

    @classproperty
    def parser(cls):
        parser = argparse.ArgsPropagationParser(add_help = False)
        parser.title = 'Crash Dumps'

        # upload
        # ------
        parser.add_argument('--crashdumps_upload',
                            action="store",
                            default=False,
                            help='Specify whether upload core dumps')
        # clean_up
        # --------
        parser.add_argument('--crashdumps_clean_up',
                            action="store",
                            default=True,
                            help='Specify whether clear core after upload')
        # protocol
        # --------
        parser.add_argument('--crashdumps_protocol',
                            action="store",
                            default=None,
                            help = 'Specify upload protocol\ndefault to TFTP')
        # server
        # ------
        parser.add_argument('--crashdumps_server',
                            action="store",
                            default=None,
                            help = 'Specify upload Server\ndefault uses '
                                   'servers information from yaml file')
        # port
        # ----
        parser.add_argument('--crashdumps_port',
                            action="store",
                            default=None,
                            help = 'Specify upload Port\ndefault uses '
                                   'servers information from yaml file')
        # username
        # --------
        parser.add_argument('--crashdumps_username',
                            action="store",
                            default=None,
                            help = 'Specify upload username credentials')
        # password
        # --------
        parser.add_argument('--crashdumps_password',
                            action="store",
                            default=None,
                            help = 'Specify upload password credentials')
        # destination
        # -----------
        parser.add_argument('--crashdumps_destination',
                            action="store",
                            default="/",
                            help = "Specify destination folder at remote "
                                   "server\ndefault to '/'")
        # timeout
        # -------
        parser.add_argument('--crashdumps_timeout',
                            action="store",
                            default=300,
                            help = "Specify upload timeout value\ndefault "
                                   "to 300 seconds")
        # flash_crash_file
        # ----------------
        parser.add_argument('--crashdumps_flash_crash_file',
                            action="store",
                            default=None,
                            help='Specify list of crash type file checking under flash:')
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
        lookup = Lookup.from_device(device)

        # List to hold cores
        self.core_list = []
        self.crashreport_list = []

        crash_type = getattr(self.args, 'crashdumps_flash_crash_file', [])
        if crash_type is None:
            crash_type = []

        # Execute command to check for cores
        status += lookup.libs.utils.check_cores(device, self.core_list,
                                                crashreport_list=self.crashreport_list,
                                                timeout=self.args.crashdumps_timeout,
                                                crash_type=crash_type)

        # User requested upload cores to server
        if self.args.crashdumps_upload and status == CRITICAL:
            kwargs = {'protocol': self.args.crashdumps_protocol,
                      'server': self.args.crashdumps_server,
                      'port': self.args.crashdumps_port,
                      'username': self.args.crashdumps_username,
                      'password': self.args.crashdumps_password,
                      'destination': self.args.crashdumps_destination,
                      'timeout': self.args.crashdumps_timeout}

            # Will make sure that manadtory keys exist for uploading to server
            # [protocol, server, destination, username, password]
            if not kwargs['protocol']:
                valid_protocols_list = ['tftp', 'ftp', 'scp']
                if hasattr(device.testbed, 'servers'):
                    for item in device.testbed.servers.keys():
                        if item in valid_protocols_list:
                            kwargs['protocol'] = item

                            if not kwargs['server']:
                                kwargs['server'] = \
                                    device.testbed.servers[item].address

                            if not kwargs['destination'] or kwargs['destination'] == '/':
                                kwargs['destination'] = \
                                    device.testbed.servers[item].path

                            if not kwargs['username']:
                                kwargs['username'] = \
                                    device.testbed.servers[item].username

                            if not kwargs['password']:
                                kwargs['password'] = \
                                    device.testbed.servers[item].password

                        break

            status += lookup.libs.utils.upload_to_server(device,
                self.core_list, self.crashreport_list, **kwargs)

        # User requested clean up of cores
        if self.args.crashdumps_clean_up and status == CRITICAL:
            status += lookup.libs.utils.clear_cores(device, self.core_list,
                self.crashreport_list)

        # Final status
        return status
