#!/usr/bin/python3

# Title:       Detect Partial LVM Volume Groups
# Description: Checks vgs output for partial volumes
# Modified:    2013 Nov 04
#
##############################################################################
# Copyright (C) 2013 SUSE LLC
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

import sys, os, Core, SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "LVM"
META_COMPONENT = "Disk"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=3803380|META_LINK_CoolSolution=http://www.novell.com/coolsolutions/appnote/19386.html#DiskBelongingtoaVolumeGroupRemoved"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def getPartialVolumes():
	fileOpen = "lvm.txt"
	section = "/sbin/vgs\n"
	content = {}
	VOLS = []
	PARTIAL_FLAG = 3
	STATUS_FIELD = 4
	VOL_NAME = 0
	START = 0
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if( START ):
				THIS_VOL = content[line].split()
				if( THIS_VOL[STATUS_FIELD][PARTIAL_FLAG] == 'p' ):
					VOLS.append(THIS_VOL[VOL_NAME])
			else:
				#skips past the command header
				if "VFree" in content[line]:
					START = 1
	return VOLS

##############################################################################
# Main Program Execution
##############################################################################

PARTIAL_VOLS = getPartialVolumes()
if( len(PARTIAL_VOLS) > 0 ):
	Core.updateStatus(Core.WARN, "Partial mode LVM volume groups found: " + " ".join(PARTIAL_VOLS))
else:
	Core.updateStatus(Core.ERROR,"No LVM volumes or all are active")

Core.printPatternResults()


