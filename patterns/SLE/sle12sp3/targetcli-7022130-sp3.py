#!/usr/bin/python

# Title:       targetcli fails in console mode
# Description: iSCSI LIO configuration with targetcli fails to saveconfig or exit
# OS:          SLES12 SP3
# Modified:    2017 Oct 19
#
##############################################################################
# Copyright (C) 2017 SUSE LINUX Products GmbH, Nuernberg, Germany
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

import os
import Core
import SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "iSCSI"
META_COMPONENT = "Target"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7022130|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1058995"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

RPM_NAME = 'targetcli'
RPM_VERSION = '2.1-17.1'
if( SUSE.packageInstalled(RPM_NAME) ):
	INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION)
	if( INSTALLED_VERSION <= 0 ):
		Core.updateStatus(Core.CRIT, "Targetcli exit issue detected, replace targetcli package with targetcli-fb")
	else:
		Core.updateStatus(Core.WARN, "Deprecated targetcli package, replace with targetcli-fb")
else:
	Core.updateStatus(Core.ERROR, "ERROR: RPM package not installed: " + RPM_NAME)

Core.printPatternResults()


