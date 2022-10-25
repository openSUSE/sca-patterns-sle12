#!/usr/bin/python3
#
# Title:       Server Fails to Dump a Kernel Core after NMI Received
# Description: Pattern for TID000020754
# Template:    SCA Tool Python Pattern Generator v1.0.7
# Modified:    2022 Oct 25
#
##############################################################################
# Copyright (C) 2022 SUSE LLC
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
meta_component = "NMI"
pattern_id = os.path.basename(__file__)
primary_link = "META_LINK_TID"
overall = Core.TEMP
overall_info = "NOT SET"
other_links = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000020754"
Core.init(meta_class, meta_category, meta_component, pattern_id, primary_link, overall, overall_info, other_links)

##############################################################################
# Local Function Definitions
##############################################################################

def nmi_found():
	file_open = "boot.txt"
	section = "dmesg -T"
	content = []
	confirmed = re.compile("NMI.*reason .* on CPU", re.IGNORECASE)
	if Core.isFileActive(file_open):
		if Core.getRegExSection(file_open, section, content):
			for line in content:
				if confirmed.search(line):
					return True
	return False

def nmi_not_configured():
	file_open = "env.txt"
	section = "sysctl -a"
	content = []
	confirmed = re.compile("kernel.panic_on_io_nmi|kernel.panic_on_unrecovered_nmi|kernel.unknown_nmi_panic", re.IGNORECASE)
	if Core.isFileActive(file_open):
		if Core.getRegExSection(file_open, section, content):
			for line in content:
				if confirmed.search(line):
					if line.endswith("0"):
						return True
	return False

##############################################################################
# Main
##############################################################################

service_name = 'kdump.service'

service_info = SUSE.getServiceDInfo(service_name)
if( service_info ):
	if( service_info['UnitFileState'] == 'enabled' ): # We can reasonably assume they want NMI to dump core
		if( nmi_found() ):
			if( nmi_not_configured() ):
				Core.updateStatus(Core.WARN, "Not all kernel NMI options are configured to trigger a core dump")
			else:
				Core.updateStatus(Core.IGNORE, "Kernel configured for core dump on NMI")
		else:
			Core.updateStatus(Core.ERROR, "No NMI messages found in dmesg")
	else:
		Core.updateStatus(Core.ERROR, "Service is disabled: " + str(service_name))
else:
	Core.updateStatus(Core.ERROR, "Service details not found: " + str(service_name))

Core.printPatternResults()
