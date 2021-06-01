#!/usr/bin/python
#
# Title:       Pattern for TID000020240
# Description: XFS nobarrier option has been completely deprecated starting from SLES15 SP2
# Source:      Basic Python Pattern Template v0.3.4
# Options:     SLE,XFS,Nobarrier,nobarrier,000020240,1176375,1,0,0
# Modified:    2021 Jun 01
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
META_CATEGORY = "XFS"
META_COMPONENT = "Nobarrier"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000020240|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1176375"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

RC_NOTFOUND = 0
RC_DEPRECATED = 1
RC_UNSUPPORTED = 2

##############################################################################
# Local Function Definitions
##############################################################################

def findMsgs():
	# 0 = Not found, 1 = deprecated messages, 2 = unsupported messages
	global RC_NOTFOUND
	global RC_DEPRECATED
	global RC_UNSUPPORTED
	fileOpen = "boot.txt"
	section = "dmesg -T"
	content = []
	RCODE = RC_NOTFOUND
	DEPRECATED = re.compile("XFS.*nobarrier option is deprecated", re.IGNORECASE)
	UNSUPPORTED = re.compile("XFS.*unknown mount option.*nobarrier", re.IGNORECASE)
	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if DEPRECATED.search(line):
					if( RCODE < RC_DEPRECATED ):
						RCODE = RC_DEPRECATED
				if UNSUPPORTED.search(line):
					if( RCODE < RC_UNSUPPORTED ):
						RCODE = RC_UNSUPPORTED
	else:
		Core.updateStatus(Core.ERROR, "ERROR: File not found - " + fileOpen)

	return RCODE

##############################################################################
# Main Program Execution
##############################################################################

NOBARRIERS = []
FSLIST = SUSE.getFileSystems()
XFS_FOUND = False
for FS in FSLIST:
	if( 'xfs' in FS['Type'] ):
		XFS_FOUND = True
		if( 'nobarrier' in FS['FstabOptions'] ):
			NOBARRIERS.append(FS['MountPoint'])

if( NOBARRIERS ):
	SERVER = SUSE.getHostInfo()
	if( SERVER['DistroVersion'] >= 15 and SERVER['DistroPatchLevel'] >= 2 ):
		Core.updateStatus(Core.CRIT, "Detected XFS filesystems with unsupported nobarriers option: " + ' '.join(NOBARRIERS))
	else:
		Core.updateStatus(Core.WARN, "Detected XFS filesystems with deprecated nobarriers option: " + ' '.join(NOBARRIERS))
else:
	STATUS = findMsgs()
	if( STATUS == RC_DEPRECATED ):
		Core.updateStatus(Core.WARN, "Detected XFS filesystem messages for deprecated nobarriers option")
	elif( STATUS == RC_UNSUPPORTED ):
		Core.updateStatus(Core.CRIT, "Detected XFS filesystem messages for unsupported nobarriers option")
	else:
		Core.updateStatus(Core.IGNORE, "No XFS filesystem messages for nobarriers option found")

Core.printPatternResults()

