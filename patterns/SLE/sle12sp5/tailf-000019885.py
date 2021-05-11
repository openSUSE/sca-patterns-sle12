#!/usr/bin/python
#
# Title:       Pattern for TID000019885
# Description: Aborting tailf causes bash session to be corrupted
# Source:      Package Version Pattern Template v0.3.8
# Options:     SLE,Bash,Session,tailf,000019885,1177369,bash,4.3-83.26.4,0,0
# Modified:    2021 May 11
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

import os
import Core
import SUSE

META_CLASS = "SLE"
META_CATEGORY = "Bash"
META_COMPONENT = "Session"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019885|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1177369|META_LINK_Issue=https://github.com/kislyuk/argcomplete/issues/146"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

RPM_NAME = 'bash'
RPM_VERSION_FIXED = '4.3-83.26.4'
if( SUSE.packageInstalled(RPM_NAME) ):
	INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION_FIXED)
	if( INSTALLED_VERSION >= 0 ):
		Core.updateStatus(Core.IGNORE, "Bug fixes applied for " + RPM_NAME)
	else:
		Core.updateStatus(Core.WARN, "Aborting commands like tailf or echo may cause bash session issues")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + RPM_NAME + " not installed")


Core.printPatternResults()

