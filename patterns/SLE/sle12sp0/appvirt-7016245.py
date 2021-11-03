#!/usr/bin/python3

# Title:       Virtual Guests Fail to Start
# Description: libvirtd apparmor profile prevents Xen domains from starting
# Modified:    2015 Mar 07
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
META_CATEGORY = "Virtualization"
META_COMPONENT = "Apparmor"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7016245|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=913799"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def apparmorActive():
	SERVICE = 'apparmor.service'
	SERVICE_INFO = SUSE.getServiceDInfo(SERVICE)
	if( SERVICE_INFO['LoadState'].lower() == 'loaded' ):
		return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

RPM_NAME = 'libvirt-daemon'
RPM_VERSION = '1.2.5-21.1'
if( SUSE.packageInstalled(RPM_NAME) ):
	if( apparmorActive() ):
		INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION)
		if( INSTALLED_VERSION == 0 ):
			Core.updateStatus(Core.CRIT, "SLES 12 virtual guests will fail to load, update system to apply newest " + RPM_NAME + " package.")
		else:
			Core.updateStatus(Core.IGNORE, "No known conflict between Apparmor and " + RPM_NAME)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: AppArmor not active, skipping")
else:
	Core.updateStatus(Core.ERROR, "ERROR: RPM package not installed: " + RPM_NAME)

Core.printPatternResults()


