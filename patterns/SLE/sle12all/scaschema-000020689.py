#!/usr/bin/python3
#
# Title:       Pattern for TID000020689
# Description: Schema file not found when running setup-sca or setup-sdp
# Source:      Basic Python Pattern Template v1.0.0
# Options:     SLE,SCA,Setup,scaschema,000020689,0,2,1,0
# Modified:    2022 Jul 06
#
##############################################################################
# Copyright (C) 2022 SUSE LLC
##############################################################################
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
#  Authors/Contributors:
#   Jason Record <jason.record@suse.com>
#
##############################################################################

import re
import os
import Core
import SUSE

META_CLASS = "SLE"
META_CATEGORY = "SCA"
META_COMPONENT = "Setup"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000020689"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def scaConfigured():
	fileOpen = "etc.txt"
	CONFIGURED = True
	CONFIRMED = re.compile("#Run s", re.IGNORECASE)
	CONF_FILES = ["/etc/sca/sdbroker.conf", "/etc/sca/sdagent.conf", "/etc/sca/sdp.conf"]
	for section in CONF_FILES:
		content = []
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if CONFIRMED.search(line):
					CONFIGURED = False
	return CONFIGURED

def docsExcluded():
	fileOpen = "updates.txt"
	section = "/etc/zypp/zypp.conf"
	content = []
	CONFIRMED = re.compile("rpm.install.excludedocs.*yes", re.IGNORECASE)
	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if CONFIRMED.search(line):
					return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

PACKAGE = "sca-appliance-common"

if( SUSE.packageInstalled(PACKAGE) ):
	if( scaConfigured() ):
		Core.updateStatus(Core.IGNORE, "SCA configuration complete")
	else:
		if( docsExcluded() ):
			Core.updateStatus(Core.WARN, "Invalid SCA schema file installation")
		else:
			Core.updateStatus(Core.IGNORE, "SCA Schema files were installed")
else:
	Core.updateStatus(Core.ERROR, "ERROR: RPM package " + PACKAGE + " not installed")

Core.printPatternResults()

