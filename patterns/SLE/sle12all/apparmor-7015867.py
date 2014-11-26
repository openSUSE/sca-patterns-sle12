#!/usr/bin/python

# Title:       AppArmor Rejects Can Cause Unexpected Application Behavior
# Description: Make sure AppArmor is not rejecting application functionality
# Modified:    2014 Nov 26
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

import re
import os
import Core
import SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "Security"
META_CATEGORY = "SLE"
META_COMPONENT = "AppArmor"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID1"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID1=https://www.suse.com/support/kb/doc.php?id=7015867|META_LINK_TID2=http://www.suse.com/support/kb/doc.php?id=7006073|Docs=https://www.suse.com/documentation/sles-12/book_security/data/part_apparmor.html"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def checkRejectMessages():
	ERROR = re.compile(r'apparmor="DENIED".*profile="(.+?)"\s', re.IGNORECASE)
	DENIED = {}
	DENIED_COUNT = 0

	fileOpen = "security-apparmor.txt"
	section = "audit.log"
	content = {}
	if Core.getSection(fileOpen, section, content):
		for line in content:
			MATCHED = ERROR.search(content[line])
			if MATCHED:
				try:
					DENIED[MATCHED.group(1)] = True
					DENIED_COUNT += 1
				except:
					True

	if( DENIED_COUNT == 0 ):
		fileOpen = "messages.txt"
		section = "/var/log/messages"
		content = {}
		if Core.getSection(fileOpen, section, content):
			for line in content:
				MATCHED = ERROR.search(content[line])
				if MATCHED:
					try:
						DENIED[MATCHED.group(1)] = True
						DENIED_COUNT += 1
					except:
						True

	if( DENIED_COUNT > 0 ):
		Core.updateStatus(Core.WARN, "Observed " + str(DENIED_COUNT) + " AppArmor denial messages for profiles(s): " + str(DENIED.keys()))
	else:
		Core.updateStatus(Core.SUCC, "No AppArmor denial messages found")

##############################################################################
# Main Program Execution
##############################################################################

APPARMOR = SUSE.getServiceDInfo('apparmor.service')
if( len(APPARMOR) > 0 ):
	if( APPARMOR['ActiveState'].lower() == 'active' and APPARMOR['SubState'].lower() == 'exited' ):
		checkRejectMessages()
	else:
		Core.updateStatus(Core.ERROR, "AppArmor not running, skipping profile check")
else:
	Core.updateStatus(Core.ERROR, "AppArmor disabled, skipping profile check")

Core.printPatternResults()


