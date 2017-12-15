
# Python
import re
import logging

# ATS
from ats.log.utils import banner

# GenieMonitor
from geniemonitor.results import OK, WARNING, ERRORED, PARTIAL, CRITICAL

# ConnectionUnifier
from connectionunifier import unifier

# module logger
logger = logging.getLogger(__name__)


def check_cores(device, core_list, crashreport_list, timeout):

    # Init
    status = OK

    # Execute command to check for cores and crashinfo reports
    for location in ['flash:/core', 'bootflash:/core', 'harddisk:/core', 'crashinfo:']:
        try:
            output = device.execute('dir {}'.format(location), timeout=timeout)
        except Exception as e:
            if any(isinstance(item, TimeoutError) for item in e.args):
                # Handle exception
                logger.warning(e)
                logger.warning(banner("dir {} execution exceeded the timeout value {}".format(location, timeout)))
            else:
                # Handle exception
                logger.warning(e)
                logger.warning(banner("Location '{}' does not exist on device".format(location)))

            continue
        
        if 'Invalid input detected' in output:
            logger.warning(banner("Location '{}' does not exist on device".format(location)))
            continue
        elif not output:
            meta_info = "Unable to check for cores"
            logger.error(banner(meta_info))
            return ERRORED(meta_info)

        for line in output.splitlines():
            line = line.strip()

            # Parse through output to collect core information (if any)
            # 1613827  -rw-         56487348  Oct 17 2017 15:56:59 +17:00  PE1_RP_0_x86_64_crb_linux_iosd-universalk9-ms_15866_20171016-155604-PDT.core.gz
            core_pattern = re.compile(r'(?P<number>(\d+)) '
                '+(?P<permissions>(\S+)) +(?P<filesize>(\d+)) '
                '+(?P<month>(\S+)) +(?P<date>(\d+)) +(?P<year>(\d+)) '
                '+(?P<time>(\S+)) +(?P<timezone>(\S+)) +(?P<core>(.*core\.gz))$', re.IGNORECASE)
            m = core_pattern.match(line)
            if m:
                core = m.groupdict()['core']
                meta_info = "Core dump generated:\n'{}'".format(core)
                logger.error(banner(meta_info))
                status += CRITICAL(meta_info)
                core_info = dict(location = location,
                                 core = core)
                core_list.append(core_info)
                continue

            # Parse through output to collect crashinfo reports (if any)
            # 62  -rw-           125746  Jul 30 2016 05:47:28 +00:00  crashinfo_RP_00_00_20160730-054724-UTC
            crashinfo_pattern = re.compile(r'(?P<number>(\d+)) '
                '+(?P<permissions>(\S+)) +(?P<filesize>(\d+)) '
                '+(?P<month>(\S+)) +(?P<date>(\d+)) +(?P<year>(\d+)) '
                '+(?P<time>(\S+)) +(?P<timezone>(\S+)) '
                '+(?P<core>(crashinfo.*))$', re.IGNORECASE)
            m = crashinfo_pattern.match(line)
            if m:
                crashreport = m.groupdict()['core']
                meta_info = "Crashinfo report generated:\n'{}'".format(crashreport)
                logger.error(banner(meta_info))
                status += CRITICAL(meta_info)
                crashreport_info = dict(location = location,
                    core = crashreport)
                crashreport_list.append(crashreport_info)
                continue

        if not core_list:
            meta_info = "No cores found at location: {}".format(location)
            logger.info(banner(meta_info))
            status += OK(meta_info)

        if not crashreport_list:
            meta_info = "No crashreports found at location: {}".format(location)
            logger.info(banner(meta_info))
            status += OK(meta_info)

    return status


def upload_to_server(device, core_list, crashreport_list, **kwargs):

    # Init
    status= OK

    # Get info
    port = kwargs['port']
    server = kwargs['server']
    timeout = kwargs['timeout']
    destination = kwargs['destination']
    protocol = kwargs['protocol']
    username = kwargs['username']
    password = kwargs['password']

    # Check values are not None
    for item in [protocol, server, destination, username, password]:
        if item is None:
            meta_info = "Unable to upload core dump - parameters not provided"
            return ERRORED(meta_info)

    # Define the pattern to construct the connection dialog
    pattern =\
        {"Address or name of remote host.*": "sendline()",
         "Destination filename.*": "sendline()"}

    # Construct the dialog as per the device connection
    dialog = unifier.handle_dialog(device, pattern)

    # preparing the full list to iterate over
    full_list = core_list + crashreport_list

    # Upload each core found
    for item in full_list:
        cmd = get_upload_cmd(server = server, port = port, dest = destination, 
                             protocol = protocol, core = item['core'], 
                             location = item['location'])

        if 'crashinfo' in item['core']:
            file_type = 'Crashreport'
        else:
            file_type = 'Core'

        message = "{} upload attempt: {}".format(file_type, cmd)
        try:
            result = device.execute(cmd, timeout = timeout, reply=dialog)
            if 'operation failed' in result or 'Error' in result:
                meta_info = "{} upload operation failed: {}".format(file_type, message)
                logger.error(banner(meta_info))
                status += ERRORED(meta_info)
            else:
                meta_info = "{} upload operation passed: {}".format(file_type, message)
                logger.info(banner(meta_info))
                status += OK(meta_info)
        except Exception as e:
            # Handle exception
            logger.warning(e)
            status += ERRORED("Failed: {}".format(message))

    return status


def get_upload_cmd(server, port, dest, protocol, core, location):
    
    if port:
        server = '{server}:{port}'.format(server = server, port = port)

    cmd = 'copy {location}/{core} {protocol}://{server}/{dest}/{core}'

    return cmd.format(location=location, core=core, protocol=protocol,
                      server=server, dest=dest)


def clear_cores(device, core_list, crashreport_list):

    # define the pattern to construct the connection dialog
    pattern =\
        {"Delete.*": "sendline()"}

    # Construct the dialog as per the device connection
    dialog = unifier.handle_dialog(device, pattern)

    # preparing the full list to iterate over
    full_list = core_list + crashreport_list

    # Delete cores from the device
    for item in full_list:
        try:
            # Execute delete command for this core
            cmd = 'delete {location}/{core}'.format(
                    core=item['core'],location=item['location'])
            output = device.execute(cmd, timeout=300, reply=dialog)
            # Log to user
            meta_info = 'Successfully deleted {location}/{core}'.format(
                        core=item['core'],location=item['location'])
            logger.info(banner(meta_info))
            return OK(meta_info)
        except Exception as e:
            # Handle exception
            logger.warning(e)
            meta_info = 'Unable to delete {location}/{core}'.format(
                        core=item['core'],location=item['location'])
            logger.error(banner(meta_info))
            return ERRORED(meta_info)
