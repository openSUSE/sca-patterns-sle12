#!/usr/bin/python3
#
# Title:       Pattern for TID000019607
# Description: System exit to emergency shell at boot with multipath enabled
# Source:      Basic Python Pattern Template v0.3.4
# Options:     SLE,MPIO,Blacklist,blacklist,000019607,0,1,0,0
# Modified:    2021 Jun 18
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

META_CLASS = "SLE"
META_CATEGORY = "MPIO"
META_COMPONENT = "Blacklist"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019607"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def ignoredMaps():
	fileOpen = "mpio.txt"
	section = "systemctl status multipathd"
	content = []
	map_list = {}
	IDX_WWID = -2
	CONFIRMED = re.compile("multipathd.*ignoring map", re.IGNORECASE)
	# Jun 18 12:51:21 server multipathd[3391]: 364cd98f0cd0b4200263d647def941d99: ignoring map
	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if CONFIRMED.search(line):
					map_list[line.split(':')[IDX_WWID]] = True
	return map_list

##############################################################################
# Main Program Execution
##############################################################################

MAPS = ignoredMaps()
if( len(MAPS) > 0 ):
	Core.updateStatus(Core.CRIT, "Detected unmapped MPIO devices, consider blacklisting: " + ' '.join(list(MAPS.keys())))
else:
	Core.updateStatus(Core.IGNORE, "No MPIO unmapped WWIDs found")

Core.printPatternResults()

