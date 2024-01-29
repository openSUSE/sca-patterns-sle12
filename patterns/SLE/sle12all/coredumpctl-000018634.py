#!/usr/bin/python3
#
# Title:       Pattern for TID000018634
# Description: How to obtain systemd service core dumps
# Source:      Basic Python Pattern Template v0.3.4
# Options:     SLE,Application,Core,coredumpctl,000018634,0,1,0,0
# Modified:    2024 Jan 29
#
##############################################################################
# Copyright (C) 2021-2024 SUSE LLC
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
META_CATEGORY = "Application"
META_COMPONENT = "Core"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000018634|META_LINK_Video=https://youtu.be/CNsuBBh3M10"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

CORE_LIST = {}

##############################################################################
# Local Function Definitions
##############################################################################

def journalAppCores():
	global CORE_LIST
	fileOpen = "crash.txt"
	section = "/coredumpctl list"
	content = []
	CONFIRMED = re.compile("", re.IGNORECASE)
	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if line.startswith("TIME"):
					continue
				elif( "No coredumps found" in line ):
					continue
				else:
					CORE_LIST[line.split()[-1]] = True

	if( len(list(CORE_LIST.keys())) > 0 ):
		return True
	else:
		return False

##############################################################################
# Main Program Execution
##############################################################################

if( journalAppCores() ):
	Core.updateStatus(Core.CRIT, "Detected application core dumps in the journal: " + ' '.join(list(CORE_LIST.keys())))
else:
	Core.updateStatus(Core.IGNORE, "No application core dumps found in the journal")

Core.printPatternResults()

