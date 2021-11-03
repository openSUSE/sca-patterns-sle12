#!/usr/bin/python3
#
# Title:       Pattern for TID000018705 (7017652)
# Description: What are all these Bug: soft lockup messages about?
# Source:      Basic Python Pattern Template v0.3.4
# Options:     SLE,Kernel,SoftLockups,softlock,000018705,0,1,0,0
# Modified:    2021 Apr 30
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
META_CATEGORY = "Kernel"
META_COMPONENT = "SoftLockups"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000018705"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def softLockFound():
	CONFIRMED = re.compile("kernel:.*BUG: soft lockup ", re.IGNORECASE)
	fileOpen = "messages.txt"

	section = "/var/log/warn"
	content = []
	if Core.getRegExSection(fileOpen, section, content):
		for line in content:
			if CONFIRMED.search(line):
				return True

	section = "/var/log/messages"
	content = []
	if Core.getRegExSection(fileOpen, section, content):
		for line in content:
			if CONFIRMED.search(line):
				return True

	fileOpen = "boot.txt"
	section = "journalctl.*--boot"
	content = []
	if Core.getRegExSection(fileOpen, section, content):
		for line in content:
			if CONFIRMED.search(line):
				return True

	return False

##############################################################################
# Main Program Execution
##############################################################################

if( softLockFound() ):
	Core.updateStatus(Core.WARN, "Detected soft lockup messages, evaluate  watchdog threshold")
else:
	Core.updateStatus(Core.IGNORE, "No soft lockup messages found")

Core.printPatternResults()

