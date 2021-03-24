#!/usr/bin/python

# Title:       Pattern for TID000019595
# Description: plymouth hang - login to console not possible
# Modified:    2021 Mar 24
#
##############################################################################
# Copyright (C) 2021, SUSE LLC
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

##############################################################################
# Module Definition
##############################################################################

import os
import re
import Core
import SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Login"
META_COMPONENT = "Plymouth"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019595|META_LINK_TID2=https://www.suse.com/support/kb/doc/?id=000019853"


Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)
##############################################################################
# Local Function Definitions
##############################################################################

def workAroundApplied():
	fileOpen = "boot.txt"
	section = "/proc/cmdline"
	content = {}
	CONFIRMED = re.compile("plymouth.enable=0", re.IGNORECASE)
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if CONFIRMED.search(content[line]):
				return True
	return False

def graphicalTarget():
	fileOpen = "systemd.txt"
	section = "/bin/ls -alR /etc/systemd/"
	content = {}
	CONFIRMED = re.compile("default\.target.*graphical\.target", re.IGNORECASE)
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if CONFIRMED.search(content[line]):
				return True
	return False

def plymouthRunning():
	fileOpen = "systemd.txt"
	section = "/bin/systemctl.*list-units"
	content = {}
	CONFIRMED = re.compile("plymouth-quit-wait.service.*start.*running", re.IGNORECASE)
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if CONFIRMED.search(content[line]):
				return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

if( workAroundApplied() ):
	Core.updateStatus(Core.IGNORE, "Workaround applied")
else:
	if( graphicalTarget() ):
		if( plymouthRunning() ):
			Core.updateStatus(Core.WARN, "Plymouth hang may cause console login failure, consider disabling plymouth")
		else:
			Core.updateStatus(Core.WARN, "Console login issue may occur, disable plymouth if needed")
	else:
		Core.updateStatus(Core.ERROR, "Not using graphical.target as default")

Core.printPatternResults()


