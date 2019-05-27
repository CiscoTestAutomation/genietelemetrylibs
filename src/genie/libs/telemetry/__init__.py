'''
    Module:
        genie.libs.telemetry

    Description:
        This is the library sub-component of Genie for `genie.telemetry`.

'''

# metadata
__version__ = '19.5.0'
__author__ = 'Cisco Systems Inc.'
__contact__ = ['pyats-support@cisco.com', 'pyats-support-ext@cisco.com']
__copyright__ = 'Copyright (c) 2018, Cisco Systems Inc.'

try:
    from ats.cisco.stats import CesMonitor
    CesMonitor(action = 'genietelemetrylibs', application='Genie').post()
except Exception:
    try:
        from ats.utils.stats import CesMonitor
        CesMonitor(action = 'genietelemetrylibs', application='Genie').post()
    except Exception:
        pass

# Enable abstraction; This is the root package.
from genie import abstract
abstract.declare_package(__name__)
