'''
GenieMonitor HelloWorld Plugin Template.
'''

# Python Imports
import logging
import argparse
import datetime

# ATS
from ats.utils import parser as argparse
from ats.datastructures import classproperty

# GenieMonitor
from geniemonitor.plugins.bases import BasePlugin
from geniemonitor.results import OK, WARNING, ERRORED, PARTIAL, CRITICAL
from geniemonitor_libs.plugins import libs

logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    '''HelloWorld Plugin

        Saluting the world and printing the device name and runtime if a custom
        flag is used.
    '''

    # Each plugin may have a unique name
    # Set the plugin name by setting the 'name' class variable.
    # (defaults to the current class name)
    __plugin_name__ = 'HelloWorld'

    @classproperty
    def parser(cls):

        # Each plugin may have a parser to parse its own command line arguments.
        # These parsers are invoked automatically by the parser engine during
        # easypy startup (always use add_help=False).
        parser = argparse.ArgsPropagationParser(add_help = False)
        
        parser.title = 'HelloWorld'

        # Custom arguments shall always use '--'' as prefix.
        # Positional custom arguments are NOT allowed.
        parser.add_argument('--print_timestamp',
                            action = 'store',
                            default = False)
        return parser

    # Plugins may define its own class constructor __init__, though, it
    # must respect the parent __init__, so super() needs to be called.
    # Any additional arguments defined in the plugin config file would be
    # passed to here as keyword arguments
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
