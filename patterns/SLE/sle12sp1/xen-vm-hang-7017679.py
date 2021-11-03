#!/usr/bin/python3

# Title:       XEN VM Hangs on Shutdown
# Description: virsh/xl domu shutdown hangs domain, name changes to null
# Modified:    2016 Jun 17
#
##############################################################################
# Copyright (C) 2016 SUSE LINUX Products GmbH, Nuernberg, Germany
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
import Xen

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "XEN"
META_COMPONENT = "VM"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc?id=7017679|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=978094"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def nullVM():
	FILE_OPEN = "xen.txt"
	SECTION = "xl list$"
	CONTENT = []
	if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
		for LINE in CONTENT:
			if LINE.startswith('(null)'):
				return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

KERNEL_VERSION = '3.12.57-60.35'
INSTALLED_VERSION = SUSE.compareKernel(KERNEL_VERSION)
if( INSTALLED_VERSION == 0 ):
	if( Xen.isDom0() ):
		if( nullVM() ):
			Core.updateStatus(Core.CRIT, "Detected null VM in xl list: Update system to apply XEN Kernel fix")
		else:
			Core.updateStatus(Core.WARN, "Susceptible to null VMs in xl list: Update system to apply XEN Kernel fix")
	else:
		Core.updateStatus(Core.ERROR, "XEN Dom0 Not Found")		
else:
	Core.updateStatus(Core.IGNORE, "Bug fix applied for " + KERNEL_VERSION)

Core.printPatternResults()


