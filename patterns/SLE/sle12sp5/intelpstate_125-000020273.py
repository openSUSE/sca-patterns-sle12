#!/usr/bin/python3
#
# Title:       Pattern for TID000020273
# Description: Frequency scaling driver intel_pstate not loading on some Intel Xeon Scalable processors
# Source:      Basic Python Pattern Template v0.3.4
# Options:     SLE,Kernel,Drivers,intelpstate,000020273,1185758,3,0,0
# Distro:      SLES12 SP5
# Modified:    2021 Jun 09
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
META_CATEGORY = "Kernel"
META_COMPONENT = "Drivers"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000020273|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1185758"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def cpuModelAffected():
	fileOpen = "hardware.txt"
	section = "/proc/cpuinfo"
	content = []
	CPU = False
	FAM = False
	MOD = False
	CONFIRM_CPU = re.compile("^model name.*:.*Intel.*Xeon", re.IGNORECASE)
	CONFIRM_FAM = re.compile("^cpu family.*:.*6", re.IGNORECASE)
	CONFIRM_MOD = re.compile("^model.*:.*106", re.IGNORECASE)
	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if CONFIRM_CPU.search(line):
					CPU = True
				if CONFIRM_FAM.search(line):
					FAM = True
				if CONFIRM_MOD.search(line):
					MOD = True
	else:
		Core.updateStatus(Core.ERROR, "ERROR: File not found - " + fileOpen)

	if( CPU and FAM and MOD ):
		return True
	else:
		return False

def noWorkAround():
	fileOpen = "hardware.txt"
	section = "/proc/cmdline"
	content = []
	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if( 'intel_pstate=no_hwp' in line ):
					return False
	else:
		Core.updateStatus(Core.ERROR, "ERROR: File not found - " + fileOpen)

	return True

def errorMsgFound():
	fileOpen = "boot.txt"
	section = "dmesg -T"
	content = []
	CONFIRMED = re.compile("intel_pstate: CPU model not supported", re.IGNORECASE)
	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if CONFIRMED.search(line):
					return True
	else:
		Core.updateStatus(Core.ERROR, "ERROR: File not found - " + fileOpen)

	return False

##############################################################################
# Main Program Execution
##############################################################################

KERNEL_VERSION = '4.12.14-122.74'
INSTALLED_VERSION = SUSE.compareKernel(KERNEL_VERSION)
if( INSTALLED_VERSION >= 0 ):
	Core.updateStatus(Core.IGNORE, "Bug fixes applied in kernel version " + KERNEL_VERSION + " or higher")
else:
	if( cpuModelAffected() ):
		if( noWorkAround() ):
			if( errorMsgFound() ):
				Core.updateStatus(Core.CRIT, "Frequency scaling driver intel_pstate not loading")
			else:
				Core.updateStatus(Core.WARN, "Possible for frequency scaling driver intel_pstate to not load")
		else:
			Core.updateStatus(Core.IGNORE, "Workaround intel_pstate=no_hwp detected")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: Invalid CPU Model")

Core.printPatternResults()

