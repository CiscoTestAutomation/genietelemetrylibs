''' 
GenieTelemetry Crashdumps Plugin for IOSXE
'''

# ATS
from ats.utils import parser as argparse
from ats.datastructures import classproperty

from ..plugin import Plugin as BasePlugin


class Plugin(BasePlugin):

    @classproperty
    def parser(cls):
        super().parser()

        # upload
        # ------
        parser.add_argument('--crashdumps_flash_crash_file ',
                            action="store",
                            default=['crashinfo', 'pxf_crashinfo', 'acecrashdum',\
                                     'vsa_ipsec'],
                            help='Specify list of crash type file checking under flash:')
        return parser