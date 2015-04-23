#!/usr/bin/python

# Title:       Look for unregistered products
# Description: Identify products not registered with SCC
# Modified:    2015 Apr 17
#
##############################################################################
# Copyright (C) 2015 SUSE LLC
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
import SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Updates"
META_COMPONENT = "Registration"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Register"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_SCC=https://scc.suse.com/dashboard|META_LINK_Register=https://www.suse.com/products/server/how-to-buy/"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def getZypperRepoList():
	fileOpen = "updates.txt"
	section = "/zypper\s.*\srepos"
	startRepos = re.compile("^-*\+-*\+")
	endRepos = re.compile("^#==|^$")
	REPOS = []
	IN_REPOS = False
	content = {}
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if( IN_REPOS ):
				if endRepos.search(content[line]):
					IN_REPOS = False
				else:
					
					print content[line].replace(" *", " ")
			elif startRepos.search(content[line]):
				IN_REPOS = True
	return REPOS

def getZypperProductsList():
	return False

##############################################################################
# Main Program Execution
##############################################################################

REPO = getZypperRepoList()

if( REPO ):
	Core.updateStatus(Core.IGNORE, "Repos Found")
else:
	Core.updateStatus(Core.ERROR, "ERROR: Not zypper repositories found")

Core.printPatternResults()


