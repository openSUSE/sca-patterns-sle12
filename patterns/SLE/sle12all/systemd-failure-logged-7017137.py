#!/usr/bin/python

# Title:       Check for failed services
# Description: Check for failed systemd services
# Modified:    2016 Jan 08
#
##############################################################################
# Copyright (C) 2016 SUSE LINUX Products GmbH, Nuernberg, Germany
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
#   Jason Record (jrecord@suse.com)
#
##############################################################################

##############################################################################
# Module Definition
##############################################################################

import re
import os
import Core
import SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Core"
META_COMPONENT = "systemd"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7017137"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

FILE_OPEN = "messages.txt"
SECTION = "/var/log/messages"
CONTENT = []
SERVICE_FOUND = ''
FAILED_SERVICES = {}
CURRENT_FAILED_SERVICES = []
IDX_UNIT_NAME = -4
#find any systemd units that have failed
if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
	failedState = re.compile("systemd.*Unit .* entered failed state", re.IGNORECASE)
	for LINE in CONTENT:
		if failedState.search(LINE):
			SERVICE_FOUND = LINE.split()[IDX_UNIT_NAME]
			FAILED_SERVICES[SERVICE_FOUND] = True
FAILED_SERVICES_LIST = FAILED_SERVICES.keys()

#check to see if the failed units are currently in a failed state
for SERVICE in FAILED_SERVICES_LIST:
	SERVICE_INFO = SUSE.getServiceDInfo(SERVICE)
	if "SubState" in SERVICE_INFO:
		if( SERVICE_INFO['SubState'] == 'failed' ):
			CURRENT_FAILED_SERVICES.append(SERVICE)

if( len(FAILED_SERVICES_LIST) > 0 ):
	if( len(CURRENT_FAILED_SERVICES) > 0 ):
		Core.updateStatus(Core.CRIT, "Systemd units that logged a failed state: " + ", ".join(FAILED_SERVICES_LIST) + ". Those units still in a failed state: " + ", ".join(CURRENT_FAILED_SERVICES))
	else:
		Core.updateStatus(Core.WARN, "Systemd units that logged a failed state: " + ", ".join(FAILED_SERVICES_LIST) + ". Those units still in a failed state: None")
else:
	Core.updateStatus(Core.IGNORE, "No failed systemd units found")

Core.printPatternResults()


