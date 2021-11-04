#!/usr/bin/python3

# Title:       SUSEConnect failure
# Description: SUSEconnect Validation failed: Uuid should be formatted as UUID
# Modified:    2015 Apr 01
#
##############################################################################
# Copyright (C) 2015 SUSE LLC
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
import re

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Registration"
META_COMPONENT = "SUSEConnect"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7016361|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=919293"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def serverNotRegistered():
	fileOpen = "updates.txt"
	section = "/zypper.*repos"
	content = {}
	repo = re.compile("SLE.12-Updates", re.IGNORECASE)
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if repo.search(content[line]):
				return False
	return True

##############################################################################
# Main Program Execution
##############################################################################

SERVER = SUSE.getHostInfo()
if "s390" in SERVER['Architecture'].lower():
	RPM_NAME = 's390-tools'
	RPM_VERSION = '1.24.1-38.17'
	if( SUSE.packageInstalled(RPM_NAME) ):
		INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION)
		if( INSTALLED_VERSION <= 0 ):
			if( serverNotRegistered() ):
				Core.updateStatus(Core.WARN, "SUSEConnect may fail to register the server for patches, an updated " + RPM_NAME + " is needed from support")
			else:
				Core.updateStatus(Core.IGNORE, "Server is registered")
		else:
			Core.updateStatus(Core.IGNORE, "Bug fixes applied for " + RPM_NAME)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: RPM package not installed: " + RPM_NAME)
else:
	Core.updateStatus(Core.ERROR, "ERROR: Outside kernel architecture scope")

Core.printPatternResults()

