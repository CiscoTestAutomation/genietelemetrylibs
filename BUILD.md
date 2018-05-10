## Creating a GenieTelemetry Plugin

To develop a new plugin,

* Clone genietelemetrylibs repo under your pyAts environment then
activate __develop__ mode to contribute.

```bash
  git clone <git_repo>
  cd genietelemetrylibs/
  make develop
```

* Create a new plugin folder under genietelemetrylibs/src/genie/libs/telemetry/plugins/<mynewplugin> following the structure shown below:

```
    mynewplugin
    |-- __init__.py
    |-- iosxe
    |   |-- __init__.py
    |   `-- plugin.py
    |-- iosxr
    |   |-- __init__.py
    |   `-- plugin.py
    |-- nxos
    |   |-- __init__.py
    |   `-- plugin.py
    `-- plugin.py
```

The plugin class should consist of 2 methods that need to be implemented by the plugin developer:

* parser()
* execution()

These methods must be implemented in the <mynewplugin>/plugin.py file and/or the <mnewplugin>/<OS>/plugin.py file.

```
    <mynewplugin>/plugin.py:
        parser() -
            Contains implementation for any argument the plugin needs to allow the plugin specific arguments propagation.
        execution() -
            Contains implementation for the device level execution steps that the plugin should perform when it is executed.
            If the device execution steps are varied for each OS (as is generally the case), the code should be abstracted into its appropriate OS folder.

    <mynewplugin>/<OS>/plugin.py:
        execution() -
            Contains implementation for OS specific execution steps that the plugin should perform when executed.
```

## Executing a GenieTelemetry Plugin
Configuration YAML

Create a YAML file containing the details of the newly created plugin as shown below:

```
plugins:
    mynewplugin:
        interval: 30
        enabled: True
        module: genie.libs.telemetry.plugins.crashdumps
        devices: ['R1',]  ----- > If left empty, plugin will run on all the devices defined in the testbed yaml file
```

## GenieTelemetry Usage

The following options are available by default to execute a Genietelemetry Plugin:

Plugin specific arguments (defined in the plugin parser() method) should be supplied in addition to the arguments below

```
\ssr-sucs-lnx7:/ws/karmoham-sjc/pyats/pypi/genietelemetrylibs/src/genie/libs/telemetry/plugins\>:genietelemetry -h -configuration /ws/karmoham-sjc/pyats/xr_jb/config_genie.yaml 
usage: genietelemetry [TESTBEDFILE]
                      [-h] [-loglevel] [-configuration FILE] [-uid UID]
                      [-runinfo_dir RUNINFO_DIR]
                      [-callback_notify CALLBACK_NOTIFY] [-timeout TIMEOUT]
                      [-connection_timeout CONNECTION_TIMEOUT] [-no_mail]
                      [-no_notify] [-mailto] [-mail_subject] [-notify_subject]
                      [-email_domain] [-smtp_host] [-smtp_port]
                      [-smtp_username] [-smtp_password]
                      [--alignmentcheck_timeout ALIGNMENTCHECK_TIMEOUT]
                      [--cpucheck_timeout CPUCHECK_TIMEOUT]
                      [--cpucheck_interval CPUCHECK_INTERVAL]
                      [--cpucheck_fivemin_pcnt CPUCHECK_FIVEMIN_PCNT]
                      [--tracebackcheck_logic_pattern TRACEBACKCHECK_LOGIC_PATTERN]
                      [--tracebackcheck_clean_up TRACEBACKCHECK_CLEAN_UP]
                      [--tracebackcheck_timeout TRACEBACKCHECK_TIMEOUT]
                      [--crashdumps_upload CRASHDUMPS_UPLOAD]
                      [--crashdumps_clean_up CRASHDUMPS_CLEAN_UP]
                      [--crashdumps_protocol CRASHDUMPS_PROTOCOL]
                      [--crashdumps_server CRASHDUMPS_SERVER]
                      [--crashdumps_port CRASHDUMPS_PORT]
                      [--crashdumps_username CRASHDUMPS_USERNAME]
                      [--crashdumps_password CRASHDUMPS_PASSWORD]
                      [--crashdumps_destination CRASHDUMPS_DESTINATION]
                      [--crashdumps_timeout CRASHDUMPS_TIMEOUT]
                      [--crashdumps_flash_crash_file CRASHDUMPS_FLASH_CRASH_FILE]

genie telemetry command line arguments.

Example
-------
  genietelemetry /path/to/testbed.yaml

--------------------------------------------------------------------------------

Positional Arguments:
  TESTBEDFILE           testbed file to be monitored

Help:
  -h, -help             show this help message and exit

Logging:
  -loglevel             genie telemetry logging level
                        eg: -loglevel="INFO"

Configuration:
  -configuration FILE   configuration yaml file for plugins and settings
  -uid UID              Specify monitoring job uid
  -runinfo_dir RUNINFO_DIR
                        Specify directory to store execution logs
  -callback_notify CALLBACK_NOTIFY
                        Specify Liveview callback notify URI
  -timeout TIMEOUT      Specify plugin maximum execution length
                        Default to 300 seconds
  -connection_timeout CONNECTION_TIMEOUT
                        Specify connection timeout

Mailing:
  -no_mail              disable final email report
  -no_notify            disable notification on device health status other than "ok"
  -mailto               list of email recipients
  -mail_subject         report email subject header
  -notify_subject       notification email subject header
  -email_domain         default email domain
  -smtp_host            specify smtp host
  -smtp_port            specify smtp server port
  -smtp_username        specify smtp username
  -smtp_password        specify smtp password

Alignment Check:
  --alignmentcheck_timeout ALIGNMENTCHECK_TIMEOUT
                        Specify duration <in seconds> to wait before timing out execution of a command

CPU utilization Check:
  --cpucheck_timeout CPUCHECK_TIMEOUT
                        Specify poll timeout value
                        default to 120 seconds
  --cpucheck_interval CPUCHECK_INTERVAL
                        Specify poll interval value
                        default to 20 seconds
  --cpucheck_fivemin_pcnt CPUCHECK_FIVEMIN_PCNT
                        Specify limited 5 minutes percentage of cpu usage
                        default to 60

Traceback Check:
  --tracebackcheck_logic_pattern TRACEBACKCHECK_LOGIC_PATTERN
                        Specify logical expression for patterns to include/exclude when checking tracebacks following PyATS logic format. Default patternis to check for Tracebacks.
  --tracebackcheck_clean_up TRACEBACKCHECK_CLEAN_UP
                        Specify whether to clear all warnings and tracebacks after reporting error
  --tracebackcheck_timeout TRACEBACKCHECK_TIMEOUT
                        Specify duration (in seconds) to wait before timing out execution of a command

Crash Dumps:
  --crashdumps_upload CRASHDUMPS_UPLOAD
                        Specify whether upload core dumps
  --crashdumps_clean_up CRASHDUMPS_CLEAN_UP
                        Specify whether clear core after upload
  --crashdumps_protocol CRASHDUMPS_PROTOCOL
                        Specify upload protocol
                        default to TFTP
  --crashdumps_server CRASHDUMPS_SERVER
                        Specify upload Server
                        default uses servers information from yaml file
  --crashdumps_port CRASHDUMPS_PORT
                        Specify upload Port
                        default uses servers information from yaml file
  --crashdumps_username CRASHDUMPS_USERNAME
                        Specify upload username credentials
  --crashdumps_password CRASHDUMPS_PASSWORD
                        Specify upload password credentials
  --crashdumps_destination CRASHDUMPS_DESTINATION
                        Specify destination folder at remote server
                        default to '/'
  --crashdumps_timeout CRASHDUMPS_TIMEOUT
                        Specify upload timeout value
                        default to 300 seconds
  --crashdumps_flash_crash_file CRASHDUMPS_FLASH_CRASH_FILE
                        Specify list of crash type file checking under flash:
\ssr-sucs-lnx7:/ws/karmoham-sjc/pyats/pypi/genietelemetrylibs/src/genie/libs/telemetry/plugins\>:

```

## CLI Execution

Execute your GenieTelemetry plugin as shown below:

* Standalone run

    ```
    [pyats] asg-lnx-1:6:55> genietelemetry -configuration <somepath>/config.yaml -testbed_file <somepath>/testbed.yaml --mynewplugin_arg1 True

    Ex:
    --
    genietelemetry config_genie.yaml -testbed_file edison_tb6.yaml --crashdumps_upload True
    ```

* Within Genie run

    ```
    [pyats] asg-lnx-1:6:55> easypy <somepath>/job.py -testbed_file <somepath>/testbed.yaml --genietelemetry <somepath>/config.yaml --mynewplugin_arg1 True

    Ex:
    --
    easypy job_xe.py -testbed_file edison_tb3.yaml --genietelemetry config_genie.yaml --crashdumps_upload True
    ```

Detailed instructions guide can be found on [our website].

[our website]: https://pubhub.devnetcloud.com/media/pyats-packages/docs/genietelemetry/index.html