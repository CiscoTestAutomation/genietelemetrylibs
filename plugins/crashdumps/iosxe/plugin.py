''' 
GenieTelemetry Crashdumps Plugin for IOSXE
'''

# ATS
from ats.utils import parser as argparse
from ats.datastructures import classproperty

from ..plugin import Plugin as BasePlugin


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
                            default=False,
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
                            default=['crashinfo', 'pxf_crashinfo', 'acecrashdum',\
                                     'vsa_ipsec'],
                            help='Specify list of crash type file checking under flash:')
        return parser