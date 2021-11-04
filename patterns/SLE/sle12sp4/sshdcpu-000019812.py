#!/usr/bin/python3

# Title:       SSHD High CPU Load
# Description: The sshd process is having high CPU load
# Modified:    2021 Feb 11
# Distro:      SLES12 SP4, SLES12 SP5
#
##############################################################################
# Copyright (C) 2021, SUSE LLC
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
META_CATEGORY = "SSHD"
META_COMPONENT = "CPU"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019812|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1179242"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def highCPU():
	fileOpen = "basic-health-check.txt"
	section = "/ps axwwo"
	content = {}
	CPUTIL_WHOLE_IDX = 3
	CPUTIL_INTEGER_IDX = 0
	MAX_CPUTIL = 70
	CPU_CURRENT = 0
	CPU_MAX = 0	
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if " sshd: " in content[line]:
				CPU_CURRENT = content[line].split()[CPUTIL_WHOLE_IDX].split('.')[CPUTIL_INTEGER_IDX]
				if( int(CPU_CURRENT) > CPU_MAX ):
					CPU_MAX = CPU_CURRENT
		if( CPU_MAX >= MAX_CPUTIL ):
			return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

RPM_NAME = 'openssh'
RPM_VERSION_BROKE = '7.2p2-78.4.2'
RPM_VERSION_FIXED = '7.2p2-78.7.1'
if( SUSE.packageInstalled(RPM_NAME) ):
	INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION_BROKE)
	if( INSTALLED_VERSION == 0 ):
		if( highCPU() ):
			Core.updateStatus(Core.CRIT, "Detected high CPU utilization for sshd processes, update server for fixes")
		else:
			Core.updateStatus(Core.WARN, "High CPU utilization on sshd connections possible, update server for fixes")
	else:
		INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION_FIXED)
		if( INSTALLED_VERSION >= 0 ):
			Core.updateStatus(Core.IGNORE, "Bug fixes applied for " + RPM_NAME + " and high CPU utilization")
		else:
			Core.updateStatus(Core.IGNORE, "Previously unaffected version of " + RPM_NAME + " installed")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + RPM_NAME + " not installed")

Core.printPatternResults()

