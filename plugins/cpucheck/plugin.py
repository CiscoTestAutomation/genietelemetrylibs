'''
GenieMonitor CpuUtilizationCheck Plugin
'''

# Python
import logging

# ATS
from ats.log.utils import banner
from ats.utils import parser as argparse
from ats.datastructures import classproperty

# GenieMonitor
from genietelemetry.plugins.bases import BasePlugin
from genietelemetry.results import OK, WARNING, ERRORED, PARTIAL, CRITICAL

# Genie
from genie.utils.timeout import Timeout

# module logger
logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    __plugin_name__ = 'CPU utilization Check Plugin'

    @classproperty
    def parser(cls):
        parser = argparse.ArgsPropagationParser(add_help = False)
        parser.title = 'CPU utilization Check'

        # timeout
        # -------
        parser.add_argument('--timeout',
                            action="store",
                            default=120,
                            help = "Specify poll timeout value\ndefault "
                                   "to 120 seconds")
        # interval
        # -------
        parser.add_argument('--interval',
                            action="store",
                            default=20,
                            help = "Specify poll interval value\ndefault "
                                   "to 20 seconds")
        # five_min_percentage
        # -------------------
        parser.add_argument('--five_min_percentage',
                            action="store",
                            default=60,
                            help = "Specify limited 5 minutes percentage of "
                                   "cpu usage\ndefault "
                                   "to 60 seconds")
        return parser


    def execution(self, device, execution_time):

        # Init
        status = OK
        
        # create timeout object
        timeout = Timeout(max_time=int(self.args.timeout),
                          interval=int(self.args.interval))

        # loop status
        loop_stat_ok = True

        if not hasattr(self, 'PARSER_MODULE'):
            return WARNING('Does not have CPU related parsers to check')

        while timeout.iterate():
            # Execute command to get five minutes usage percentage
            try:
                cpu_dict = self.PARSER_MODULE(device).parse(
                    sort_time='5min', key_word='CPU')
            except Exception as e:
                return ERRORED('No output from show processes cpu\n{}'.format(e))

            # Check 5 minutes percentage smaller than five_min_percentage
            if int(cpu_dict['five_min_cpu']) >= int(self.args.five_min_percentage):
                message = "****** Device {d}*****\n".format(d=device.name)
                message += "Excessive CPU utilization detected for 5 min interval\n"
                message += "Allowed: {e}%\n".format(e=self.args.five_min_percentage)
                message += "Measured: FiveMin: {r}%".format(r=cpu_dict['five_min_cpu'])
                loop_stat_ok = False
                timeout.sleep()
            else:
                message = "***** CPU usage is Expected ***** \n"
                message += "Allowed threashold: {e} \n"\
                                .format(e=self.args.five_min_percentage)
                message += "Measured from device: {r}"\
                                .format(r=cpu_dict['five_min_cpu'])
                loop_stat_ok = True
                status += OK(message)
                logger.info(banner(message))
                break

        if not loop_stat_ok:
            status += CRITICAL(message)
            logger.error(banner(message))

        # Final status
        return status
