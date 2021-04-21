#!/usr/bin/python
#
# Title:       Pattern for TID000019643
# Description: Security Vulnerability: Special Register Buffer Data Sampling aka CrossTalk (CVE-2020-0543)
# Source:      Kernel Package Version Pattern Template v0.1.1
# Options:     SLE,Security,Crosstalk,crosstalk_151,000019643,1154824,4.12.14-197.45,0,1
# Distro:      SLES12 SP5
# Modified:    2021 Apr 21
#
##############################################################################
# Copyright (C) 2021, SUSE LLC
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
META_CATEGORY = "Security"
META_COMPONENT = "Crosstalk"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019643|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1154824|META_LINK_CVE-2020-0543=https://www.suse.com/security/cve/CVE-2020-0543/"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def intelCPU():
	fileOpen = "hardware.txt"
	section = "/proc/cpuinfo"
	content = []
	CONFIRMED = re.compile("vendor_id.*GenuineIntel", re.IGNORECASE)
	if Core.getRegExSection(fileOpen, section, content):
		for line in content:
			if CONFIRMED.search(line):
				return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

RPM_NAME = 'ucode-intel'
RPM_VERSION_FIXED = '20200602-3.12.1'
KERNEL_VERSION_FIXED = '4.12.14-122.23'

if( SUSE.packageInstalled(RPM_NAME) ):
	if( intelCPU() ):
		INSTALLED_VERSION_RPM = SUSE.compareRPM(RPM_NAME, RPM_VERSION_FIXED)
		INSTALLED_VERSION_KERN = SUSE.compareKernel(KERNEL_VERSION_FIXED)
		if( INSTALLED_VERSION_RPM >= 0 ):
			if( INSTALLED_VERSION_KERN >= 0 ):
				Core.updateStatus(Core.IGNORE, "Bug fixes applied for " + RPM_NAME + " and kernel version")
			else:
				Core.updateStatus(Core.WARN, "Risk of L1D data cache eviction and vector register sampling, update kernel to avoid")
		else:
			if( INSTALLED_VERSION_KERN >= 0 ):
				Core.updateStatus(Core.WARN, "Risk of L1D data cache eviction and vector register sampling, update " + RPM_NAME + " to avoid")
			else:
				Core.updateStatus(Core.WARN, "Risk of L1D data cache eviction and vector register sampling, update system to avoid")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: Intel CPU not found")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + RPM_NAME + " not installed")

Core.printPatternResults()

