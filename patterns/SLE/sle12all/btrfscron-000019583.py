#!/usr/bin/python
#
# Title:       Pattern for TID000019583
# Description: After upgrading to SLES 12 SP5 BTRFS cron jobs are not working anymore.
# Source:      Package Version Pattern Template v0.3.5
# Options:     SLE,Filesystem,Btrfs,000019583,1159891,btrfscron,btrfsmaintenance,0.2-15.1,0,1
# Modified:    2021 Mar 25
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
META_CATEGORY = "Filesystem"
META_COMPONENT = "Btrfs"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019583|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1159891"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

RPM_NAME = 'btrfsmaintenance'
RPM_VERSION_FIXED = '0.2-15.1'
if( SUSE.packageInstalled(RPM_NAME) ):
	INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION_FIXED)
	if( INSTALLED_VERSION >= 0 ):
		Core.updateStatus(Core.IGNORE, "Bug fixes applied for " + RPM_NAME + "")
	else:
		Core.updateStatus(Core.WARN, "Weekly Btrfs cron jobs may fail, update system to apply fixes")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + RPM_NAME + " not installed")

Core.printPatternResults()

