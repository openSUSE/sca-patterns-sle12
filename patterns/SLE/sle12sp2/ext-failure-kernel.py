#!/usr/bin/python3

# Title:       kernel update causes ext4 failure
# Description: ext4: first meta block group too large
# Modified:    2017 May 10
#
##############################################################################
# Copyright (C) 2017 SUSE LINUX Products GmbH, Nuernberg, Germany
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
META_COMPONENT = "Failure"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc?id=7018898|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1029986"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def checkSomething():
	fileOpen = "filename.txt"
	section = "CommandToIdentifyFileSection"
	content = {}
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if "something" in content[line]:
				return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

BROKEN_KERNEL_VERSION = '4.4.49-92.11.1'
FIXED_KERNEL_VERSION = '4.4.59-92.17.3'
BROKEN_RESULT = SUSE.compareKernel(BROKEN_KERNEL_VERSION)
FIXED_RESULT = SUSE.compareKernel(FIXED_KERNEL_VERSION)

if BROKEN_RESULT >= 0 and FIXED_RESULT < 0:
	EXT_FOUND = False
	FSLIST = SUSE.getFileSystems()
	for FS in FSLIST:
		if( "ext" in FS['Type'].lower() ):
			EXT_FOUND = True
	if( EXT_FOUND ):
		Core.updateStatus(Core.WARN, "Detected possible ext3/4 mount issue with the kernel, update kernel to resolve.")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: No ext3/4 filesystems found")
else:
	Core.updateStatus(Core.IGNORE, "Outside the kernel scope: EXT3/4 bug not applicable")

Core.printPatternResults()


