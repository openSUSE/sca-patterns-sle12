#!/usr/bin/python

# Title:       Check for multiple cron processes
# Description: Expected cron daemon behavior change from SLES11 to SLES12
# Modified:    2018 Dec 20
#
##############################################################################
# Copyright (C) 2018 SUSE
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

import os
import Core
import SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Basesystem"
META_COMPONENT = "Cron"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=7023601|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1017160"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def multipleCrons():
	FILE_OPEN = "basic-health-check.txt"
	SECTION = "ps axwwo"
	CONTENT = []
	CRONS = 0
	if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
		for LINE in CONTENT:
			if "cron" in LINE:
				CRONS += 1
				if( CRONS > 1 ):
					return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

if( SUSE.packageInstalled('cronie') ):
	if( SUSE.packageInstalled('cron') ):
		CRONIE_VERSION = SUSE.compareRPM('cronie', '1.4.11-59')
		CRON_VERSION = SUSE.compareRPM('cron', '4.2-59')
		if( CRONIE_VERSION < 0 ):
			if( CRON_VERSION < 0 ):
				if( multipleCrons() ):
					Core.updateStatus(Core.CRIT, "Multiple instances of cron running, update system to resolve")
				else:
					Core.updateStatus(Core.WARN, "Multiple instances of cron will incorrectly be allowed to run, update system to avoid")
			else:
				Core.updateStatus(Core.WARN, "Both cronie and cron packages should be updated together")
		else:
			if( CRON_VERSION < 0 ):
				Core.updateStatus(Core.WARN, "Both cronie and cron packages should be updated together")
			else:
				Core.updateStatus(Core.IGNORE, "Updated cronie and cron packages avoid bsc#1017160")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: RPM package not installed: cron")
else:
	Core.updateStatus(Core.ERROR, "ERROR: RPM package not installed: cronie")

Core.printPatternResults()


