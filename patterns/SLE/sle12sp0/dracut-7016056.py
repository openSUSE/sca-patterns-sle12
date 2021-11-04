#!/usr/bin/python3

# Title:       Missing dracut modules
# Description: Additional kernel modules not added to the initrd when specified in /etc/dracut.conf
# Modified:    2015 Jan 13
#
##############################################################################
# Copyright (C) 2015 SUSE LINUX Products GmbH, Nuernberg, Germany
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
META_COMPONENT = "Dracut"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7016056|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=911660"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def getDracutModules():
	fileOpen = "etc.txt"
	section = "dracut.conf$"
	content = {}
	DRIVERS = []
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if content[line].startswith("add_drivers"):
				DRIVERS = content[line].split("=")[-1].strip().strip('"').split()
				break
	return DRIVERS

def initrdModulesFound(moduleList):
	fileOpen = "boot.txt"
	section = "lsinitrd"
	content = {}
	FOUND = 0
	if Core.getSection(fileOpen, section, content):
		for i in range(len(moduleList)-1):
			if moduleList[i].endswith(".ko"):
				modSearch = moduleList[i]
			else:
				modSearch = moduleList[i] + ".ko"
			for line in content:
				if modSearch in content[line]:
					del moduleList[i] # module found, remove from the list
		if( len(moduleList) > 0 ):
			FOUND = -1 # a module is missing
		else:
			FOUND = 1 # all modules found
	else:
		FOUND = 0 # missing the lsinitrd section in boot.txt
	return FOUND

##############################################################################
# Main Program Execution
##############################################################################

RPM_NAME = 'dracut'
RPM_VERSION = '037-34.4'
if( SUSE.packageInstalled(RPM_NAME) ):
	INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION)
	if( INSTALLED_VERSION <= 0 ):
		DRACUT_MODULES = getDracutModules()
		if( len(DRACUT_MODULES) > 0 ):
			FOUND = initrdModulesFound(DRACUT_MODULES)
			if( FOUND > 0 ):
				Core.updateStatus(Core.IGNORE, "Found initrd modules specified in dracut.conf with add_drivers")
			elif( FOUND < 0 ):
				Core.updateStatus(Core.CRIT, "Missing initrd modules specified in dracut.conf with add_drivers: " + " ".join(DRACUT_MODULES))
			else:
				Core.updateStatus(Core.WARN, "Modules specified in dracut.conf with add_drivers may be missing from the initrd: " + " ".join(DRACUT_MODULES))
		else:
			Core.updateStatus(Core.ERROR, "ERROR: No add_drivers modules found")
	else:
		Core.updateStatus(Core.IGNORE, "Missing initrd modules specified in dracut.conf -- AVOIDED")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + RPM_NAME + " RPM not installed")

Core.printPatternResults()


