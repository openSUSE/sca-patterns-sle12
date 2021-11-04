#!/usr/bin/python3

# Title:       chmod -R 777 /
# Description: Create a pattern checking if the chmod -R 777 / command has been run.
# Modified:    2014 Mar 06
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
#   Jason Record (jrecord@suse.com)
#
##############################################################################

##############################################################################
# Module Definition
##############################################################################

import sys, os, Core, SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

# The limits to the percentage of files found with 777 permissions
# in boot.txt and sysfs.txt
LIMIT_CRITICAL = 60
LIMIT_WARNING = 40

META_CLASS = "SLE"
META_CATEGORY = "Security"
META_COMPONENT = "Permissions"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=http://www.novell.com/support/kb/doc.php?id=7014410"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def getOpenModeFilePercent():
	TOTAL = 0
	COUNT = 0
	PERCENT = 0

	fileOpen = "boot.txt"
	section = "ls -lR"
	content = {}
	if Core.getSection(fileOpen, section, content):
		for line in content:
			LIST = content[line].split()
			if( len(LIST) > 6 ):
				TOTAL += 1
				if "lrwxrwxrwx" in LIST[0]:
					continue
				elif "rwxrwxrwx" in LIST[0]:
					COUNT += 1

	fileOpen = "sysfs.txt"
	section = "find /sys"
	content = {}
	if Core.getSection(fileOpen, section, content):
		for line in content:
			LIST = content[line].split()
			if( LIST[0].startswith("ls: ") ):
				continue
			else:
				TOTAL += 1
				if "lrwxrwxrwx" in LIST[0]:
					continue
				elif "rwxrwxrwx" in LIST[0]:
					COUNT += 1

	if( TOTAL > 0 ):
		PERCENT = COUNT * 100 / TOTAL
	return int(PERCENT)

##############################################################################
# Main Program Execution
##############################################################################

OPEN_MODE = getOpenModeFilePercent()
if( OPEN_MODE >= LIMIT_CRITICAL ):
	Core.updateStatus(Core.CRIT, "Security risk: Too many files found with 777 permissions")
elif( OPEN_MODE >= LIMIT_WARNING ):
	Core.updateStatus(Core.WARN, "Security risk: Too many files found with 777 permissions")
else:
	Core.updateStatus(Core.IGNORE, "Files with 777 mode: " + str(OPEN_MODE) + "%")

Core.printPatternResults()

