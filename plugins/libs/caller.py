# logging
import logging

# ats results
import ats
from ats.results import Passed

# GenieTelemetry
from genie.telemetry import Manager

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

        section.parent.healthCheck.run(section)

        # Checking the GenieTelemetry call final result
        anomallies = []

        results = section.parent.healthCheck.results.get(key, {})
        for pluginname, devices in results.items():
            results = []
            for name, device in devices.items():
                status = device.get('status', None)
                status_name = getattr(status, 'name', status)
                if str(status_name).lower() == 'ok':
                    continue
                results.append('\n\t\t'.join([name, status_name]))
            if not results:
                continue
            anomallies.append('\n\t'.join([pluginname, '\n'.join(results)]))

        # Only overwrite section result if testcase passed
        if section.result == Passed and anomallies:
            section.passx("Genie.Telemetry caught anomallies: \n{}".format(
                                                        '\n'.join(anomallies))
                                                    )
    except Exception as e:
        section.skipped("Genie.Telemetry encountered an issue: {}".format(e))
