#!/usr/bin/python3

# Title:       Check for failed services
# Description: Check for failed systemd services
# Modified:    2021 Jul 02
#
##############################################################################
# Copyright (C) 2021 SUSE LINUX Products GmbH, Nuernberg, Germany
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

FILE_OPEN = "systemd.txt"
SECTION = "systemctl --failed"
CONTENT = []
FAILED_SERVICES = []
IDX_UNIT_NAME = 1
#find any systemd units that have failed
if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
	failedState = re.compile("loaded.*failed", re.IGNORECASE)
	for LINE in CONTENT:
		if failedState.search(LINE):
			FAILED_SERVICES.append(LINE.split()[IDX_UNIT_NAME])

if( len(FAILED_SERVICES) > 0 ):
	Core.updateStatus(Core.CRIT, "Systemd units currently in a failed state: " + ", ".join(FAILED_SERVICES))
else:
	Core.updateStatus(Core.IGNORE, "No failed systemd units found")

Core.printPatternResults()


