#!/usr/bin/python

# Title:       Check for openSUSE Repos
# Description: System no longer stable after updating with active openSUSE repository enabled
# Modified:    2014 Sep 23
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
META_CATEGORY = "System"
META_COMPONENT = "Update"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7015683"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def openSUSERepos():
	fileOpen = "updates.txt"
	section = "/zypper.*repos"
	content = {}
	NAME = 2
	if Core.getSection(fileOpen, section, content):
		openSUSE = re.compile(r'^openSUSE:\d+.\d+$')
		for line in content:
			new_line = re.sub(r'\s+', '', content[line]).split('|')
			if( len(new_line) > NAME ):
#				print new_line[NAME]
				if openSUSE.search(new_line[NAME]):
					return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

if( openSUSERepos() ):
	Core.updateStatus(Core.CRIT, "Detected openSUSE repositories, do not update server.")
else:
	Core.updateStatus(Core.IGNORE, "No critical openSUSE repositories found")

Core.printPatternResults()

