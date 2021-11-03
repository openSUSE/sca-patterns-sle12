#!/usr/bin/python3

# Title:       XFS Corruption
# Description: Race between xfs_zero_eof/direct write can cause corruption
# Modified:    2016 Jan 27
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

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Filesystem"
META_COMPONENT = "XFS"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7017183|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=949744"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def xfsMounts():
	FSLIST = SUSE.getFileSystems()
	for FS in FSLIST:
		if "xfs" in FS['Type']:
			if( FS['Mounted'] ):
				return True
	return False

def directIOAllowed():
	FILE_OPEN = "modules.txt"
	SECTION = "/sbin/modinfo sg"
	CONTENT = []
	if Core.getExactSection(FILE_OPEN, SECTION, CONTENT):
		for LINE in CONTENT:
			if "/allow_dio=0" in LINE:
				return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

#KERNEL_VERSION = '3.0.101-0.47.71'		#SLE11 SP3
#KERNEL_VERSION = '3.0.101-68'			#SLE11 SP4
#KERNEL_VERSION = '3.12.51-52.31'		#SLE12 SP0
KERNEL_VERSION = '3.12.51-60.20'		#SLE12 SP1
INSTALLED_VERSION = SUSE.compareKernel(KERNEL_VERSION)
if( INSTALLED_VERSION < 0 ):
	if( xfsMounts() ):
		if( directIOAllowed() ):
			Core.updateStatus(Core.WARN, "Direct IO writes to XFS may cause filesystem damage")
		else:
			Core.updateStatus(Core.IGNORE, "Direct IO required, skipping pattern")
	else:
		Core.updateStatus(Core.IGNORE, "No XFS mounts found, skipping pattern")
else:
	Core.updateStatus(Core.IGNORE, "Bug fixes applied for " + KERNEL_VERSION)

Core.printPatternResults()


