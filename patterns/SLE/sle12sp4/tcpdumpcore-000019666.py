#!/usr/bin/python
#
# Title:       Pattern for TID000019666
# Description: Running tcpdump on a SLES12 SP4 System with Kernel 4.12.14-95.48-default may crash the system
# Source:      Package Version Pattern Template v0.3.7
# Options:     SLE,Kernel,Core,000019666,0,tcpdumpcore,kernel-default,4.12.14-95.54,4.12.14-95.48,1
# Distro:      SLES12 SP4
# Modified:    2021 Mar 31
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

import os
import Core
import SUSE

META_CLASS = "SLE"
META_CATEGORY = "Kernel"
META_COMPONENT = "Core"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019666"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

RPM_TCPCUMP = 'tcpdump'
RPM_NAME = 'kernel-default'
RPM_VERSION_FIXED = '4.12.14-95.54'
RPM_VERSION_BROKE = '4.12.14-95.48'
if( SUSE.packageInstalled(RPM_TCPCUMP) ):
	INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION_FIXED)
	if( INSTALLED_VERSION >= 0 ):
		Core.updateStatus(Core.IGNORE, "Bug fixes applied for " + RPM_NAME + "")
	else:
		INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION_BROKE)
		if( INSTALLED_VERSION == 0 ):
			Core.updateStatus(Core.WARN, "The tcpdump command may cause a system crash, update system to avoid issues")
		else:
			Core.updateStatus(Core.IGNORE, "Previously unaffected version of " + RPM_NAME + " installed")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + RPM_TCPCUMP + " not installed")

Core.printPatternResults()

