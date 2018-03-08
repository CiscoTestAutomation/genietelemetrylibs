# logging
import logging

# ats results
import ats
from ats.results import (Passed, Failed, Aborted, Errored,
                         Skipped, Blocked, Passx)
# GenieTelemetry
import genietelemetry
from genietelemetry.results import OK, WARNING, ERRORED, PARTIAL, CRITICAL
from genietelemetry.manager.manager import Manager

# Logger
log = logging.getLogger(__name__)


def health_check(section):
    '''Check for cores, tracebacks, carshereports or any other pattern
       specified by the user in the genietelemetry plugins provided.
       Can be controlled via sections parameters which is provided by the
       triggers/verification datafile
    '''
    # Handle disabling health check
    if 'health_check' in section.parameters and\
        section.parameters['health_check'] is False:
        # User has elected to disable running of this processor
        log.info("Skipping 'health_check' processor - user has set "
                 "'health_check' to False in trigger YAML file.")
        return

    try:
        if not hasattr(section.parent, 'healthCheck'):
            section.parent.healthCheck = Manager(
                testbed=section.parent.parameters['testbed'])

        # Check for --genietelemetry_enable value (True/False)
        if section.parent.healthCheck.args.genietelemetry_enable:
            monitor = section.parent.healthCheck.run(section,
                testbed=section.parent.parameters['testbed'])
        else:
            log.info("GenieTelemetry enable key is set to False "
                "'--genietelemetry_enable False', Set it to True or don't "
                "provide it (default value is 'True')")

        # Checking the GenieTelemetry call final result
        final_result = OK
        for plgn in section.parent.testcase_monitor_result[section].keys():
            for dev in section.parent.testcase_monitor_result[section][plgn]:
                final_result += dev['status']

        # Only overwrite section result if testcase passed
        if section.result == Passed:
            if not final_result.name == 'ok':
                section.passx("GenieTelemetry caught an anomaly {}".\
                    format(section.parent.testcase_monitor_result[section]))
    except Exception:
        # Section will skip since user didn't disable GenieTelemetry
        # and an exception has been caught
        section.skipped('Monitoring config.yaml file is missing so testbed '
            'monitoring functionality is disabled')
