#!/usr/bin/python3

# Title:       Cleaning up temporary directories
# Description: Suggest tmp cleanup when low on disk space.
# Modified:    2013 Dec 13
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

META_CLASS = "SLE"
META_CATEGORY = "Disk"
META_COMPONENT = "Space"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7002723"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def lowDiskSpace():
	fileOpen = "basic-health-check.txt"
	section = "/bin/df -h"
	content = {}
	DISK_LOW = 85
	FULL = 6
	SHORT = 5
	iFULL = 4
	iSHORT = 3
	if Core.getSection(fileOpen, section, content):
		for line in content:
			FIELDS = content[line].split()
			PERCENT = 0
			if( len(FIELDS) == FULL ):
				PERCENT = FIELDS[iFULL].rstrip('%')
				if ( PERCENT.isdigit() ):
					PERCENT = int(PERCENT)
				else:
					PERCENT = 0
			elif( len(FIELDS) == SHORT ):
				PERCENT = FIELDS[iSHORT].rstrip('%')
				if ( PERCENT.isdigit() ):
					PERCENT = int(PERCENT)
				else:
					PERCENT = 0

#			print str(len(FIELDS)) + ':' + str(PERCENT) + ':' + str(DISK_LOW) + ": " + str(FIELDS)
			if( PERCENT > DISK_LOW ):
				return True

	return False

def maxDaysInTmp():
	fileOpen = "sysconfig.txt"
	section = "/etc/sysconfig/cron"
	content = {}
	VALUE = 1
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if "MAX_DAYS_IN_TMP" in content[line]:
				PAIR = content[line].replace('"','').replace("'",'').split('=',1)
				if( int(PAIR[VALUE]) > 0 ):
					return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

if( lowDiskSpace() ):
	if( maxDaysInTmp() ):
		Core.updateStatus(Core.ERROR, "MAX_DAYS_IN_TMP already set")
	else:
		Core.updateStatus(Core.REC, "Consider setting MAX_DAYS_IN_TMP to delete old files in temporary directories")
else:
	Core.updateStatus(Core.ERROR, "No low disk space conditions")

Core.printPatternResults()


