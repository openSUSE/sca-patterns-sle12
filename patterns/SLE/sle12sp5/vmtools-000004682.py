#!/usr/bin/python3
#
# Title:       Pattern for TID000004682
# Description: Extensive logging in vmware-vmsvc-root.log with open-vm-tools
# Source:      Package Version Pattern Template v0.3.3
# Options:     SLE,VMware,Tools,vmtools,000004682,1162119,1,1,0
# Distros:     SLES12 SP4/5
# Modified:    2021 Apr 22
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

import re
import os
import Core
import SUSE

META_CLASS = "SLE"
META_CATEGORY = "VMware"
META_COMPONENT = "Tools"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000004682|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1162119"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def VMwareVM():
	fileOpen = "basic-environment.txt"
	section = "Virtualization"
	VMWARE = False
	VMSERVER = False

	content = []
	HYPERVM = re.compile("Manufacturer.*VMware.*Inc", re.IGNORECASE)
	VM = re.compile("Identity.*Virtual Machine", re.IGNORECASE)
	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if HYPERVM.search(line):
					VMWARE = True
				elif VM.search(line):
					VMSERVER = True
	if( VMWARE and VMSERVER ):
		return True
	else:
		return False

##############################################################################
# Main Program Execution
##############################################################################

PACKAGE = "open-vm-tools"
VERSION_FIXED = '11.0.0-4.18.3'
VERSION_FIXED_OLD = '10'

if( SUSE.packageInstalled(PACKAGE) ):
	INSTALLED_VERSION = SUSE.compareRPM(PACKAGE, VERSION_FIXED)
	if( INSTALLED_VERSION >= 0 ):
		Core.updateStatus(Core.IGNORE, "Bug fixes applied for " + PACKAGE)
	else:
		INSTALLED_VERSION_OLD = SUSE.compareRPM(PACKAGE, VERSION_FIXED_OLD)
		if( INSTALLED_VERSION_OLD == 0 ):
			Core.updateStatus(Core.IGNORE, "Early versions of " + PACKAGE + " are unaffected")
		else:
			if( VMwareVM() ):
				Core.updateStatus(Core.WARN, "Excessive logging may ocurr in vmware-vmsvc-root.log")
			else:
				Core.updateStatus(Core.ERROR, "ERROR: Not a VMware VM")
else:
	Core.updateStatus(Core.ERROR, "ERROR: RPM package " + PACKAGE + " not installed")

Core.printPatternResults()

