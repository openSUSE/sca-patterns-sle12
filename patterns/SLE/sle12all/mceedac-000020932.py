#!/usr/bin/python3
#
# Title:       mce EDAC memory scrubbing error
# Description: Pattern for TID000020932
# Template:    SCA Tool Python Pattern Generator v1.0.10
# Modified:    2023 Jan 18
#
##############################################################################
# Copyright (C) 2023 SUSE LLC
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

meta_class = "SLE"
meta_category = "Kernel"
meta_component = "MCE"
pattern_id = os.path.basename(__file__)
primary_link = "META_LINK_TID"
overall = Core.TEMP
overall_info = "NOT SET"
other_links = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000020932|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1078655|META_LINK_Cisco=https://quickview.cloudapps.cisco.com/quickview/bug/CSCvf14908"
Core.init(meta_class, meta_category, meta_component, pattern_id, primary_link, overall, overall_info, other_links)

##############################################################################
# Local Function Definitions
##############################################################################

def hardware_affected():
	system_info = SUSE.getBasicVirtualization()
	if 'Manufacturer' in system_info.keys():
		if "cisco systems" in system_info['Manufacturer'].lower():
			if 'Hardware' in system_info.keys():
				if re.search("^ucsc-|^ucsb-", system_info['Hardware'], re.IGNORECASE):
					return True

	return False

def mce_event_found():
	file_open = "boot.txt"
	section = "dmesg -T"
	content = []
	mcevent = re.compile("mce:.*Hardware Error.*Machine check events logged", re.IGNORECASE)
	if Core.isFileActive(file_open):
		if Core.getRegExSection(file_open, section, content):
			for line in content:
				if mcevent.search(line):
					return True
	
	return False

def edac_error_found():
	file_open = "messages.txt"
	section = "/var/log/warn"
	content = []
	confirmed = re.compile("EDAC.*CE memory scrubbing error on.*DIMM|EDAC.*CE memory read error on.*DIMM", re.IGNORECASE)
	if Core.isFileActive(file_open):
		if Core.getRegExSection(file_open, section, content):
			for line in content:
				if confirmed.search(line):
					return True
	
	return False

##############################################################################
# Main
##############################################################################

def main():
	driver_name = "sb_edac"
	driver = SUSE.getDriverInfo(driver_name)
	if( driver['loaded'] ):
		if( hardware_affected() ):
			if( mce_event_found() ):
				if( edac_error_found() ):
					Core.updateStatus(Core.CRIT, "MCE event logged with " + driver_name + " driver loaded, the system may crash with Cisco hardware")
				else:
					Core.updateStatus(Core.WARN, "MCE events detected while " + driver_name + " driver loaded, conflicts may occur with Cisco hardware")
			else:
				Core.updateStatus(Core.IGNORE, "No MCE events found even though " + driver_name + " driver loaded on Ciscso hardware")
		else:
			Core.updateStatus(Core.ERROR, "ERROR: Hardware does not apply")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + driver_name + " module not loaded")

	Core.printPatternResults()

# Entry point
if __name__ == "__main__":
	main()

