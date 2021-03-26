#!/usr/bin/python
#
# Title:       Pattern for TID000019638
# Description: System crash during a BTRFS maintenance task
# Source:      Package Version Pattern Template v0.3.5
# Options:     SLE,Btrfs,Crash,000019638,1163508,btrfscrash-124,kernel-default,4.12.14-95.51,0,1
# Distro:      SLES12 SP5
# Modified:    2021 Mar 26
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
META_CATEGORY = "Btrfs"
META_COMPONENT = "Crash"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019638|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1163508"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def btrfsInUse():
	fileOpen = "fs-btrfs.txt"
	section = "btrfs filesystem show"
	content = {}
	CONFIRMED = re.compile("Label:", re.IGNORECASE)
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if CONFIRMED.search(content[line]):
				return True
	return False

def kernelCoredumped():
	fileOpen = "crash.txt"
	section = "/var/crash"
	content = {}
	CONFIRMED = re.compile("dmesg.txt", re.IGNORECASE)
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if CONFIRMED.search(content[line]):
				return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

RPM_NAME = 'kernel-default'
RPM_VERSION_FIXED = '4.12.14-122.20'
if( SUSE.packageInstalled(RPM_NAME) ):
	INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION_FIXED)
	if( INSTALLED_VERSION >= 0 ):
		Core.updateStatus(Core.IGNORE, "Bug fixes applied for " + RPM_NAME + "")
	else:
		if( btrfsInUse() ):
			if( kernelCoredumped() ):
				Core.updateStatus(Core.CRIT, "System core detected and btrfs may be a contributor, update system")
			else:
				Core.updateStatus(Core.WARN, "Btrfs may cause the system to dump core, update system to avoid")
		else:
			Core.updateStatus(Core.IGNORE, "ERROR: No btrfs filesystems found")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + RPM_NAME + " not installed")

Core.printPatternResults()

