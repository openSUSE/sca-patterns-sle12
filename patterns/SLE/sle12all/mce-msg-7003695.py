#!/usr/bin/python

# Title:       MCE Log Checks
# Description: Machine check exceptions in the logs
# Modified:    2017 Aug 04
#
##############################################################################
# Copyright (C) 2017 SUSE LINUX Products GmbH, Nuernberg, Germany
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
META_CATEGORY = "Kernel"
META_COMPONENT = "MCE"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7003695"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

CONTENT = []
HARDWARE_ERRORS = False
MCE_ERRORS = False
NOT_DONE = True

hardwareFailure = re.compile("\[Hardware Error\]:", re.IGNORECASE)
mceFailure = re.compile("MC\d:.*MCE|MC\d:.*Machine Check Event|MC\d:.*Machine Check Exception", re.IGNORECASE)

FILE_OPEN = "boot.txt"
SECTION = "/bin/dmesg"
if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
	for LINE in CONTENT:
		if hardwareFailure.search(LINE):
			HARDWARE_ERRORS = True
			NOT_DONE = False
		if mceFailure.search(LINE):
			MCE_ERRORS = True
			NOT_DONE = False

if( NOT_DONE ):
	FILE_OPEN = "messages.txt"
	SECTION = "/var/log/warn"
	if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
		for LINE in CONTENT:
			if hardwareFailure.search(LINE):
				HARDWARE_ERRORS = True
				NOT_DONE = False
			if mceFailure.search(LINE):
				MCE_ERRORS = True
				NOT_DONE = False

if( NOT_DONE ):
	FILE_OPEN = "messages.txt"
	SECTION = "/var/log/messages"
	if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
		for LINE in CONTENT:
			if hardwareFailure.search(LINE):
				HARDWARE_ERRORS = True
				NOT_DONE = False
			if mceFailure.search(LINE):
				MCE_ERRORS = True
				NOT_DONE = False

if( HARDWARE_ERRORS and MCE_ERRORS ):
	Core.updateStatus(Core.WARN, "Check hardware, detected hardware and MCE errors in " + str(FILE_OPEN) + ":" + str(SECTION))
elif( HARDWARE_ERRORS ):
	Core.updateStatus(Core.WARN, "Check hardware, detected hardware errors in " + str(FILE_OPEN) + ":" + str(SECTION))
elif( MCE_ERRORS ):
	Core.updateStatus(Core.WARN, "Check hardware, detected MCE errors in " + str(FILE_OPEN) + ":" + str(SECTION))
else:
	Core.updateStatus(Core.IGNORE, "IGNORE: No Hardware or MCE errors found")

Core.printPatternResults()


