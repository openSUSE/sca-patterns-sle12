#!/usr/bin/python
#
# Title:       Pattern for TID000020356
# Description: Postfix fails to start with IPv6 disabled
# Source:      Basic Python Pattern Template v0.3.4
# Options:     SLE,Postfix,Configuration,postfix,000020356,0,2,1,1
# Modified:    2021 Aug 05
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
META_CATEGORY = "Postfix"
META_COMPONENT = "Configuration"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000020356"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def ipv6inHosts():
	fileOpen = "network.txt"
	section = "/etc/hosts"
	content = []
	CONFIRMED = re.compile("::1.*localhost", re.IGNORECASE)
	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if CONFIRMED.search(line):
					return True
	else:
		Core.updateStatus(Core.ERROR, "ERROR: File not found - " + fileOpen)

	return False

def ipv6Disabled():
	fileOpen = "network.txt"
	section = "/usr/sbin/wicked ifstatus --verbose all"
	content = []
	CONFIRMED = re.compile("addr.*ipv6.*::1/", re.IGNORECASE)
	if Core.getRegExSection(fileOpen, section, content):
		for line in content:
			if CONFIRMED.search(line):
				return False
	return True

##############################################################################
# Main Program Execution
##############################################################################

PACKAGE = "postfix"
SERVICE_NAME = 'postfix.service'

if( SUSE.packageInstalled(PACKAGE) ):
	SERVICE_INFO = SUSE.getServiceDInfo(SERVICE_NAME)
	if( SERVICE_INFO ):
		if( SERVICE_INFO['UnitFileState'] == 'enabled' ):
			if( SERVICE_INFO['SubState'] == 'failed' ):
				if( ipv6inHosts() ):
					if( ipv6Disabled() ):
						Core.updateStatus(Core.CRIT, "Postfix failure due to mismatched IPv6 configuration")
					else:
						Core.updateStatus(Core.IGNORE, "IPv6 enabled and configured")
				else:
					Core.updateStatus(Core.IGNORE, "No IPv6 loopback entry found")
			else:
				Core.updateStatus(Core.ERROR, "Service did not fail: " + str(SERVICE_NAME))
		else:
			Core.updateStatus(Core.ERROR, "Service is disabled: " + str(SERVICE_NAME))
	else:
		Core.updateStatus(Core.ERROR, "Service details not found: " + str(SERVICE_NAME))
else:
	Core.updateStatus(Core.ERROR, "ERROR: RPM package " + PACKAGE + " not installed")

Core.printPatternResults()

