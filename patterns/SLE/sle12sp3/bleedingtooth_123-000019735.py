#!/usr/bin/python
#
# Title:       Pattern for TID000019735
# Description: Security Vulnerability: BleedingTooth aka CVE-2020-12351, CVE-2020-12352, and CVE-2020-24490
# Source:      Package Version Pattern Template v0.3.5
# Options:     SLE,Kernel,Bluetooth,000019735,0,bleedingtooth,kernel-default,4.4.121-92.146,0,1
# Distro:      SLES12 SP3
# Modified:    2021 Mar 25
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

import os
import Core
import SUSE

META_CLASS = "SLE"
META_CATEGORY = "Kernel"
META_COMPONENT = "Bluetooth"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019735|META_LINK_CVE1=https://www.suse.com/security/cve/CVE-2020-12351|META_LINK_CVE2=https://www.suse.com/security/cve/CVE-2020-12352|META_LINK_CVE3=https://www.suse.com/security/cve/CVE-2020-24490"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

RPM_BLUE = 'bluez'
RPM_NAME = 'kernel-default'
RPM_VERSION_FIXED = '4.4.180-94.135'
if( SUSE.packageInstalled(RPM_BLUE) ):
	if( SUSE.packageInstalled(RPM_NAME) ):
		INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION_FIXED)
		if( INSTALLED_VERSION >= 0 ):
			Core.updateStatus(Core.IGNORE, "Bug fixes applied for " + RPM_NAME + "")
		else:
			Core.updateStatus(Core.WARN, "Detected Security Vulnerability: BleedingTooth, update server to apply fixes")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + RPM_NAME + " not installed")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + RPM_BLUE + " not installed")

Core.printPatternResults()

