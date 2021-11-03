#!/usr/bin/python3

# Title:       ssh logins not recorded in lastlog
# Description: Users logging into the server with ssh are not recorded in lastlog
# Modified:    2014 Apr 09
#
##############################################################################
# Copyright (C) 2014 SUSE LLC
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
#   Sean Barlow (sbarlow@novell.com)
#
##############################################################################

##############################################################################
# Module Definition
##############################################################################

import sys, os, Core, SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Login"
META_COMPONENT = "SSH"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=http://www.novell.com/support/kb/doc.php?id=7014881"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def logErrorsFound():
	fileOpen = "messages.txt"
	section = "/var/log/messages"
	content = {}
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if "Couldn't stat /var/log/lastlog: No such file or directory" in content[line]:
				return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

if( logErrorsFound() ):
	Core.updateStatus(Core.WARN, "SSH logins not recorded in lastlog")
else:
	Core.updateStatus(Core.IGNORE, "Ignore this pattern, not applicable")

Core.printPatternResults()


