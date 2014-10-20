#!/usr/bin/python

# Title:       Technology Preview: 1.4.2.5 QEMU: virtio-blk-data-plane
# Description: Identify SLE12 technology preview features
# Modified:    2014 Oct 20
#
##############################################################################
# Copyright (C) 2014 SUSE LLC
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
import re
import Core

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Technology"
META_COMPONENT = "Preview"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Note"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Note=https://www.suse.com/releasenotes/x86_64/SUSE-SLES/12/#Intro.Support.Techpreviews|META_LINK_Support=https://www.suse.com/releasenotes/x86_64/SUSE-SLES/12/#fate-316355|META_LINK_Fate=https://fate.suse.com/316355"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def dataPlaneEnabled():
	fileOpen = "basic-health-check.txt"
	section = "/ps a"
	content = {}
	DATA_PLANE = re.compile('bin/qemu.*-device.*virtio-blk-pci.*x-data-plane=on|bin/qemu.*-device.*x-data-plane=on.*virtio-blk-pci', re.IGNORECASE)

	if Core.getSection(fileOpen, section, content):
		for line in content:
			if DATA_PLANE.search(content[line]):
				return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

if( dataPlaneEnabled() ):
	Core.updateStatus(Core.WARN, "Virtual machines with virtio-blk-data-plane enabled are unsupported technology preview software")
else:
	Core.updateStatus(Core.ERROR, "No KVM virtural machines running with virtio-blk-data-plane")

Core.printPatternResults()


