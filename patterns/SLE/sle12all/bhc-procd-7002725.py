#!/usr/bin/python

# Title:       Basic Health Check - Uninterruptible Processes
# Description: Checks for excessive Uninterruptible processes
# Modified:    2013 Nov 26
#
##############################################################################
# Copyright (C) 2013 SUSE LLC
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

import sys, os, Core, SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "Basic Health"
META_CATEGORY = "SLE"
META_COMPONENT = "Processes"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7002725"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LIMIT_RED = 5
LIMIT_YELLOW = 3

##############################################################################
# Local Function Definitions
##############################################################################

def getDStateProcs():
	STATE = 7
	D_COUNT = 0
	fileOpen = "basic-health-check.txt"
	section = "egrep"
	content = {}
	if Core.getSection(fileOpen, section, content):
		for line in content:
			FIELDS = content[line].split()
			if "D" in FIELDS[STATE]:
				D_COUNT += 1
	return D_COUNT

##############################################################################
# Main Program Execution
##############################################################################

DPROCS = getDStateProcs()
if( DPROCS >= LIMIT_RED ):
	Core.updateStatus(Core.CRIT, str(DPROCS) + " meets or exceeds " + str(LIMIT_RED) + " Uninterruptible processes")
elif( DPROCS >= LIMIT_YELLOW ):
	Core.updateStatus(Core.WARN, str(DPROCS) + " meets or exceeds " + str(LIMIT_YELLOW) + " Uninterruptible processes")
else:
	Core.updateStatus(Core.SUCC, str(DPROCS) + " Uninterruptible processes observed")

Core.printPatternResults()

