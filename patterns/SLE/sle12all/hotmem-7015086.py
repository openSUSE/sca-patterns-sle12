#!/usr/bin/python3

# Title:       Check ACPI with memory hotplug
# Description: Memory hotplug fails with ACPI error messages
# Modified:    2014 May 22
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

import sys, os, Core, SUSE, re

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Memory"
META_COMPONENT = "ACPI"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7015086"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def errorsFound():
	fileOpen = "messages.txt"
	err1Found = False
	err2Found = False
	err3Found = False
	err1 = re.compile("acpi_memhotplug.*probe.*failed with error")
	err2 = re.compile("API:memory_.*add_memory failed")
	err3 = re.compile("ACPI:memory_hp:Error in acpi_memory_enable_device")
	sections = ['/var/log/warn', '/var/log/messages']

	for section in sections:
		content = {}
		if Core.getSection(fileOpen, section, content):
			for line in content:
				if err1.search(content[line]):
					err1Found = True
				elif err2.search(content[line]):
					err2Found = True
				elif err3.search(content[line]):
					err3Found = True
				if( err1Found and err2Found and err3Found ):
#					print "Found in " + str(section)
					return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

if( errorsFound() ):
	Core.updateStatus(Core.WARN, "Detected hotplug add memory failure")
else:
	Core.updateStatus(Core.IGNORE, "No hotplug memory errors found")

Core.printPatternResults()

