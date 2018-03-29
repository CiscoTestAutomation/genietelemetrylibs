''' 
GenieTelemetry KeepAlive Plugin for NXOS.
'''
import logging

# GenieTelemetry
from ..plugin import Plugin as BasePlugin
from genie.telemetry.status import OK

# module logger
logger = logging.getLogger(__name__)

class Plugin(BasePlugin):

    def execution(self, device):

        device.execute('\x0D', timeout=self.interval)
        return OK