#!/usr/bin/python

# Title:       Hostname DNS searches fail
# Description: /etc/resolv.conf Domain Search list does not use listed domains
# Modified:    2014 Nov 10
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

import re
import os
import Core

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "DNS"
META_COMPONENT = "Search"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7015868"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

fileOpen = "network.txt"
section = "nsswitch.conf"
content = {}
MSG_SEVERITY = Core.WARN
DNS_USED = re.compile("^hosts:\s*.*\sdns", re.IGNORECASE)
if Core.getSection(fileOpen, section, content):
	for line in content:
		if DNS_USED.search(content[line]):
			MSG_SEVERITY = Core.CRIT

section = "resolv.conf"
content = {}
SEARCH_COUNT = 0
SEARCH_FORMAT = False
INVALID = re.compile("search.*\s\s+\S|search.*\S,\S", re.IGNORECASE)
if Core.getSection(fileOpen, section, content):
	for line in content:
		if content[line].lower().startswith('search'):
			SEARCH_COUNT += 1
			if INVALID.search(content[line]):
				SEARCH_FORMAT = True

if( SEARCH_COUNT > 1 and SEARCH_FORMAT ):
	Core.updateStatus(MSG_SEVERITY, "Invalid DNS resolv.conf search parameter: multiple search lines and host list error")
elif( SEARCH_FORMAT ):
	Core.updateStatus(MSG_SEVERITY, "Invalid DNS resolv.conf search parameter: host list error")
elif( SEARCH_COUNT > 1 ):
	Core.updateStatus(MSG_SEVERITY, "Invalid DNS resolv.conf search parameter: multiple search lines")
else:
	Core.updateStatus(Core.IGNORE, "No invalid DNS resolv.conf search parameter detected")

Core.printPatternResults()

