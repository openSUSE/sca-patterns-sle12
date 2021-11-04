#!/usr/bin/python3
#
# Title:       Pattern for TID000020301
# Description: SCA Appliance configuration reports ERROR 2002 HY000 Cannot connect to MySQL server
# Source:      Basic Python Pattern Template v0.3.4
# Options:     SLE,SCA,sdagent,sdagentconfig,000020301,1183464,2,1,0
# Modified:    2021 Jun 25
#
##############################################################################
# Copyright (C) 2021 SUSE LLC
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
META_COMPONENT = "sdagent"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000020301|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1183464"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def brokerConfigured():
	global fileOpen
	global CONFIRMED
	section = "sca/sdbroker.conf"
	content = []
	if Core.getRegExSection(fileOpen, section, content):
		for line in content:
			if CONFIRMED.search(line):
				return False
	return True

def agentConfigured():
	global fileOpen
	global CONFIRMED
	section = "sca/sdagent.conf"
	content = []
	if Core.getRegExSection(fileOpen, section, content):
		for line in content:
			if CONFIRMED.search(line):
				return False
	return True

##############################################################################
# Main Program Execution
##############################################################################

PACKAGE = "sca-appliance-agent"
fileOpen = "etc.txt"

if( SUSE.packageInstalled(PACKAGE) ):
	if Core.isFileActive(fileOpen):
		CONFIRMED = re.compile("INSRC=#Run", re.IGNORECASE)
		if( brokerConfigured() ):
			if( agentConfigured() ):
				Core.updateStatus(Core.IGNORE, "Both the sdbroker and sdagent are configured")
			else:
				Core.updateStatus(Core.CRIT, "Detected incomplete SCA Appliance server configuration, check MySQL bind-address")
		else:
			Core.updateStatus(Core.ERROR, "The SCA Appliance broker has not been configured")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: File not found - " + fileOPen)
else:
	Core.updateStatus(Core.ERROR, "ERROR: RPM package " + PACKAGE + " not installed")

Core.printPatternResults()

