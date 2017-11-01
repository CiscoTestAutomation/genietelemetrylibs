
# Python
import time
import logging
from datetime import datetime

# ATS
from ats.log.utils import banner

# GenieMonitor
from geniemonitor.results import OK, WARNING, ERRORED, PARTIAL, CRITICAL

# Parsergen
from parsergen import oper_fill_tabular

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# module logger
logger = logging.getLogger(__name__)


def check_cores(device, core_list):

    # Init
    status = OK

    # Execute command to check for cores
    header = [ "VDC", "Module", "Instance",
                "Process-name", "PID", "Date\(Year-Month-Day Time\)" ]
    output = oper_fill_tabular(device = device, 
                               show_command = 'show cores vdc-all',
                               header_fields = header, index = [5])
    if not output.entries:
        meta_info = "No cores found!"
        logger.info(banner(meta_info))
        return OK(meta_info)
    
    # Parse through output to collect core information (if any)
    for k in sorted(output.entries.keys(), reverse=True):
        row = output.entries[k]
        date = row.get("Date\(Year-Month-Day Time\)", None)
        if not date:
            continue
        date_ = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        # Save core info
        core_info = dict(module = row['Module'],
                         pid = row['PID'],
                         instance = row['Instance'],
                         process = row['Process-name'],
                         date = date.replace(" ", "_"))
        core_list.append(core_info)

        meta_info = "Core dump generated for process '{}' at {}".format(row['Process-name'], date_)
        logger.error(banner(meta_info))
        status += CRITICAL(meta_info)

    return status


def upload_to_server(device, core_list, **kwargs):

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

    # Create unicon dialog (for ftp)
    dialog = Dialog([
        Statement(pattern=r'Enter username:',
                  action='sendline({})'.format(username),
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r'Password:',
                  action='sendline({})'.format(password),
                  loop_continue=True,
                  continue_timer=False),
        ])

    # Upload each core found
    for core in core_list:
        cmd = get_upload_cmd(server = server, port = port,
                                  dest = destination, protocol = protocol,
                                  **core)
        message = "Core dump upload attempt: {}".format(cmd)
        try:
            result = device.execute(cmd, timeout = timeout, reply=dialog)
            if 'operation failed' in result:
                meta_info = "Core upload operation failed: {}".format(message)
                logger.error(banner(meta_info))
                status += ERRORED(meta_info)
            else:
                meta_info = "Core upload operation passed: {}".format(message)
                logger.info(banner(meta_info))
                status += OK(meta_info)
        except Exception as e:
            # Handle exception
            logger.warning(e)
            status += ERRORED("Failed: {}".format(message))

    return status


def get_upload_cmd(module, pid, instance, server, port, dest, date, process, protocol):

    # Sample command:
    # copy core://<module-number>/<process-id>[/instance-num]
    #      tftp:[//server[:port]][/path] vrf management
    path = '{dest}/core_{pid}_{process}_{date}_{time}'.format(
                                               dest = dest, pid = pid,
                                               process = process,
                                               date = date,
                                               time = time.time())
    if port:
        server = '{server}:{port}'.format(server = server, port = port)

    if instance:
        pid = '{pid}/{instance}'.format(pid = pid, instance = instance)

    cmd = 'copy core://{module}/{pid} ' \
          '{protocol}://{server}/{path} vrf management'

    return cmd.format(module = module, pid = pid, protocol = protocol,
                      server = server, path = path)


def clear_cores(device, core_list):

    # Execute command to delete cores
    try:
        device.execute('clear cores')
        meta_info = "Successfully cleared cores on device"
        logger.info(banner(meta_info))
        status = OK(meta_info)
    except Exception as e:
        # Handle exception
        logger.warning(e)
        meta_info = "Unable to clear cores on device"
        logger.error(meta_info)
        status = ERRORED(meta_info)

    return status
