#!/usr/bin/python3

# Title:       LVM volume groups fail at boot time
# Description: Check for manually configured LVM volume groups
# Modified:    2013 Oct 31
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
META_COMPONENT = "Activation"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7014032"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

fileOpen = "lvm.txt"
section = "/etc/sysconfig/lvm"
content = {}
ATBOOT = {}
VALUES = 1
if Core.getSection(fileOpen, section, content):
	for line in content:
		if "LVM_VGS_ACTIVATED_ON_BOOT" in content[line]:
			ATBOOT = content[line].split('=')
			VGS = ATBOOT[VALUES].strip('"')
			break
	if( len(VGS) > 0 ):
		Core.updateStatus(Core.WARN, "LVM volume groups activated at boot time limited to: " + VGS)
	else:
		Core.updateStatus(Core.ERROR, "No LVM volume groups are limited to activation at boot")

Core.printPatternResults()


