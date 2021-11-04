#!/usr/bin/python3

# Title:       Orarun install fails
# Description: orarun on SLES 12 SP1 ORACLE
# Modified:    2016 Aug 22
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
META_CATEGORY = "Installation"
META_COMPONENT = "Orarun"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc?id=7017965|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=992364"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def errorMessagesFound():
	FILE_OPEN = "messages.txt"
	ERROR_MSG = re.compile("OraInstall.*libmawt.so.*cannot open shared object file.*No such file or directory", re.IGNORECASE)
	SECTION = "/var/log/warn"
	CONTENT = []
	if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
		for LINE in CONTENT:
			if ERROR_MSG.search(LINE):
				return True
	SECTION = "/var/log/messages"
	CONTENT = []
	if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
		for LINE in CONTENT:
			if ERROR_MSG.search(LINE):
				return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

if( SUSE.packageInstalled('orarun') ):
	if( SUSE.packageInstalled('libXi6') ):
		if( SUSE.packageInstalled('libcap1') ):
			Core.updateStatus(Core.IGNORE, "Orarun required packages installed, not applicable")
		else:
			if( errorMessagesFound() ):
				Core.updateStatus(Core.CRIT, "Failed oraran installation, missing required package: libcap1")
			else:
				Core.updateStatus(Core.WARN, "Oraran installation will fail, missing required package: libcap1")
	else:
		if( SUSE.packageInstalled('libcap1') ):
			if( errorMessagesFound() ):
				Core.updateStatus(Core.CRIT, "Failed oraran installation, missing required package: libXi6")
			else:
				Core.updateStatus(Core.WARN, "Oraran installation will fail, missing required package: libXi6")
		else:
			if( errorMessagesFound() ):
				Core.updateStatus(Core.CRIT, "Failed oraran installation, missing required packages: libXi6, libcap1")
			else:
				Core.updateStatus(Core.WARN, "Oraran installation will fail, missing required packages: libXi6, libcap1")
else:
	Core.updateStatus(Core.IGNORE, "Orarun package not installed, not applicable")

Core.printPatternResults()


