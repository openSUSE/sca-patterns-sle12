#!/usr/bin/python3
#
# Title:       Pattern for TID000018798
# Description: How to resize/extend a btrfs formatted root partition
# Source:      Basic Python Pattern Template v0.3.4
# Options:     SLE,Filesystem,Btrfs,sizingbtrfs,000018798,0,1,0,0
# Modified:    2021 Jun 14
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
META_CATEGORY = "Filesystem"
META_COMPONENT = "Btrfs"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000018798|META_LINK_MASTER=https://www.suse.com/support/kb/doc/?id=000018779"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)


##############################################################################
# Main Program Execution
##############################################################################

THRESHOLD = 85
ROOT_BTRFS = False
FSLIST = SUSE.getFileSystems()
for FS in FSLIST:
	if( FS['MountPoint'] == '/' ):
		if( 'btrfs' in FS['Type'] ):
			ROOT_BTRFS = True
			break


if( ROOT_BTRFS ):
	if( FS['PercentUsed'] >= THRESHOLD ):
		Core.updateStatus(Core.REC, "How to resize Btrfs root filesystem if needed")
	else:
		Core.updateStatus(Core.IGNORE, "Used space " + str(FS['PercentUsed']) + "% less than " + str(THRESHOLD) + "%")
else:
	Core.updateStatus(Core.ERROR, "ERROR: Root btrfs filesystem not found")


Core.printPatternResults()

