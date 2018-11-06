################################################################################
#                                                                              #
#                      Cisco Systems Proprietary Software                      #
#        Not to be distributed without consent from Test Technology            #
#                               Cisco Systems, Inc.                            #
#                                                                              #
################################################################################
#                            genie.libs.telemetry Internal Makefile
#
# Author:
#   pyats-support@cisco.com
#
# Support:
#   pyats-support@cisco.com
#
# Version:
#   v3.0
#
# Date:
#   November 2018
#
# About This File:
#   This script will build the genie.libs.telemetry package for
#   distribution in PyPI server
#
# Requirements:
#	1. Module name is the same as package name.
#	2. setup.py file is stored within the module folder
################################################################################

# Variables
PKG_NAME      = genie.libs.telemetry
BUILD_DIR     = $(shell pwd)/__build__
DIST_DIR      = $(BUILD_DIR)/dist
PROD_USER     = pyadm@pyats-ci
PROD_PKGS     = /auto/pyats/packages/cisco-shared/genietelemetry/libs
PYTHON        = python
TESTCMD       = ./tests/runAll --path=./tests/
BUILD_CMD     = $(PYTHON) setup.py bdist_wheel --dist-dir=$(DIST_DIR)
PYPIREPO      = pypitest

# Development pkg requirements
DEPENDENCIES  = restview psutil Sphinx wheel asynctest
DEPENDENCIES += setproctitle sphinxcontrib-napoleon sphinx-rtd-theme httplib2
DEPENDENCIES += pip-tools Cython requests

.PHONY: clean package distribute develop undevelop help devnet\
        docs test install_build_deps uninstall_build_deps

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "package               Build the package"
	@echo "test                  Test the package"
	@echo "distribute            Distribute the package to internal Cisco PyPi server"
	@echo "clean                 Remove build artifacts"
	@echo "develop               Build and install development package"
	@echo "undevelop             Uninstall development package"
	@echo "docs                  Build Sphinx documentation for this package"
	@echo "devnet                Build DevNet package."
	@echo "install_build_deps    install pyats-distutils"
	@echo "uninstall_build_deps  remove pyats-distutils"
	@echo ""
	@echo "     --- build arguments ---"
	@echo " DEVNET=true              build for devnet style (cythonized, no ut)"

devnet: package
	@echo "Completed building DevNet packages"
	@echo ""

install_build_deps:
	@echo "--------------------------------------------------------------------"
	@echo "Installing cisco-distutils"
	@pip install --index-url=http://pyats-pypi.cisco.com/simple \
	             --trusted-host=pyats-pypi.cisco.com \
	             cisco-distutils
 
uninstall_build_deps:
	@echo "--------------------------------------------------------------------"
	@echo "Uninstalling pyats-distutils"
	@pip uninstall cisco-distutils
 
docs:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "No documentation for $(PKG_NAME)"
	@echo ""
 
test:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "No tests for $(PKG_NAME)"
	@echo ""
 
package:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Building $(PKG_NAME) distributable: $@"
	@echo ""
	
	$(BUILD_CMD)
	
	@echo ""
	@echo "Completed building: $@"
	@echo ""
 
develop:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Building and installing $(PKG_NAME) development distributable: $@"
	@echo ""
	
	@pip install $(DEPENDENCIES)
	
	@$(PYTHON) setup.py develop --no-deps
	
	@pip install -e ".[dev]"
	
	@echo ""
	@echo "Completed building and installing: $@"
	@echo ""
 
undevelop:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Uninstalling $(PKG_NAME) development distributable: $@"
	@echo ""
	
	@$(PYTHON) setup.py develop --no-deps -q --uninstall
	
	@echo ""
	@echo "Completed uninstalling: $@"
	@echo ""
 
clean:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Removing make directory: $(BUILD_DIR)"
	@rm -rf $(BUILD_DIR) $(DIST_DIR)
	@echo ""
	@echo "Removing build artifacts ..."
	@$(PYTHON) setup.py clean
	@echo ""
	@echo "Done."
	@echo ""
 
distribute:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Copying all distributable to $(PROD_PKGS)"
	@test -d $(DIST_DIR) || { echo "Nothing to distribute! Exiting..."; exit 1; }
	@ssh -q $(PROD_USER) 'test -e $(PROD_PKGS)/ || mkdir $(PROD_PKGS)'
	@scp $(DIST_DIR)/* $(PROD_USER):$(PROD_PKGS)/
	@echo ""
	@echo "Done."
	@echo ""
