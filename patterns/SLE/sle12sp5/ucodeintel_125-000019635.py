#!/usr/bin/python
#
# Title:       Pattern for TID000019635
# Description: Security vulnerability: L1D data cache eviction and Vector Register sampling - CVE-2020-0548, CVE-2020-0549
# Source:      Package Version Pattern Template v0.3.7
# Options:     SLE,Security,CPU,000019635,1156353,ucodeintel_151,ucode-intel,20200602-3.25.1,0,1
# Distro:      SLES12 SP5
# Modified:    2021 Apr 07
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
META_CATEGORY = "Security"
META_COMPONENT = "CPU"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019635|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1156353|META_LINK_CVE-2020-0548=https://www.suse.com/security/cve/CVE-2020-0548/|META_LINK_CVE-2020-0549=https://www.suse.com/security/cve/CVE-2020-0549/|META_LINK_Intel=https://www.intel.com/content/www/us/en/security-center/advisory/intel-sa-00329.html"

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
if( SUSE.packageInstalled(RPM_NAME) ):
	INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION_FIXED)
	if( INSTALLED_VERSION >= 0 ):
		Core.updateStatus(Core.IGNORE, "Bug fixes applied for " + RPM_NAME + "")
	else:
		if( intelCPU() ):
			Core.updateStatus(Core.WARN, "Risk of L1D data cache eviction and vector register sampling, update system to avoid")
		else:
			Core.updateStatus(Core.IGNORE, "No Genuine Intel CPUs found")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + RPM_NAME + " not installed")

Core.printPatternResults()

