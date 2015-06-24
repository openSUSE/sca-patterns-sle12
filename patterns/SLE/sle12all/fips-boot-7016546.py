#!/usr/bin/python

# Title:       Boot Failure with FIPS
# Description: Server will not boot when fips=1 is in the kernel parameter and /boot is a separate partition
# Modified:    2015 Jun 24
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

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Boot"
META_COMPONENT = "FIPS"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7016546|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=924393"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def separateBootPartition():
	return True
	fileOpen = "filename.txt"
	section = "CommandToIdentifyFileSection"
	content = {}
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if "something" in content[line]:
				return True
	return False

def checkSomething():
	fileOpen = "filename.txt"
	section = "CommandToIdentifyFileSection"
	content = {}
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if "something" in content[line]:
				return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

if( SUSE.packageInstalled('dracut-fips') ):
	if( separateBootPartition() ):
		FIPS_ENABLED = False
		BOOT_DEFINED = False
		CMDLINE = SUSE.getProcCmdLine()
		for OPTION in CMDLINE:
			TEST = OPTION.lower()
			if "fips=1" in TEST:
				FIPS_ENABLED = True
			elif "boot=" in TEST:
				BOOT_DEFINED = True

		if( BOOT_DEFINED ):
			Core.updateStatus(Core.IGNORE, "Boot works regardless of FIPS enablement")
		else:
			if( FIPS_ENABLED ):
				Core.updateStatus(Core.CRIT, "Boot failure probable, configure boot device")
			else:
				Core.updateStatus(Core.WARN, "Enabling FIPS may cause server boot failure, configure boot device first.")
	else:
		Core.updateStatus(Core.ERROR, "Separate boot partiton not found")
else:
	Core.updateStatus(Core.ERROR, "FIPS not installed, not applicable")

Core.printPatternResults()


