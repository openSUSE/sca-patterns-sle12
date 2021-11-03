#!/usr/bin/python3

# Title:       Checking securetty mode
# Description: Cannot login as root at the console, login incorrect
# Modified:    2014 Mar 06
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

import re, sys, os, Core, SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Console"
META_COMPONENT = "Login"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7014706"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def securettyModeInvalid():
	fileOpen = "pam.txt"
	section = "rpm -V pam"
	content = {}
	if Core.getSection(fileOpen, section, content):
		securettyMode = re.compile(".*M.*/etc/securetty")
		for line in content:
			if securettyMode.search(content[line]):
#				print content[line]
				return True
	return False

def failedLogin():
	fileOpen = "messages.txt"
	section = "/var/log/warn"
	content = {}
	if Core.getSection(fileOpen, section, content):
		failure = re.compile("login.*pam_securetty.*/etc/securetty.*writable")
		for line in content:
			if failure.search(content[line]):
				return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

if( securettyModeInvalid() ):
	if( failedLogin() ):
		Core.updateStatus(Core.CRIT, "Detected failed console login, invalid securetty mode")
	else:
		Core.updateStatus(Core.CRIT, "Invalid securetty mode, console logins may fail")
else:
	Core.updateStatus(Core.IGNORE, "Valid securetty mode, ignored")

Core.printPatternResults()


