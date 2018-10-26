# Genie Telemetry libs

Genie is both a library framework and a test harness that facilitates rapid
development, encourage re-usable and simplify writing test automation. Genie
bundled with the modular architecture of pyATS framework accelerates and
simplifies test automation leveraging all the perks of the Python programming
language in an object-orienting fashion.

pyATS is an end-to-end testing ecosystem, specializing in data-driven and
reusable testing, and engineered to be suitable for Agile, rapid development
iterations. Extensible by design, pyATS enables developers to start with small,
simple and linear test cases, and scale towards large, complex and asynchronous
test suites.

Genie Telemetry is a testbed health status monitoring tool, this package
contains the libraries.

[Cisco Devnet]: https://developer.cisco.com/

GenieTelemetryLibs is the library location for genie.telemetry package containing
all the user developed plugins deriving the telemetry behavior during the run.

Multiple plugins have been already developed,

* crashdumps
* tracebackcheck
* alignmentcheck
* cpucheck

# Installation

Detailed installation guide can be found on [our website].

[our website]: https://developer.cisco.com/site/pyats/

```
$ pip install genie.telemetry
```

# Building Plugins Guidelines

Detailed build guide can be found in the [Plugins build guidelines](BUILD.md).