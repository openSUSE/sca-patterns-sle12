#!/usr/bin/python

# Title:       NTP fails to start
# Description: NTP Service Fails to Start or Hangs on SLES12
# Modified:    2014 Nov 10
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

META_CLASS = "SLE"
META_CATEGORY = "NTP"
META_COMPONENT = "Startup"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7015867|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=898438"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def appArmorError():
	ERROR = re.compile(r'apparmor="DENIED".*profile="/usr/sbin/ntpd"', re.IGNORECASE)

	fileOpen = "security-apparmor.txt"
	section = "audit.log"
	content = {}
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if ERROR.search(content[line]):
				return True

	fileOpen = "messages.txt"
	section = "/var/log/messages"
	content = {}
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if ERROR.search(content[line]):
				return True

	return False

##############################################################################
# Main Program Execution
##############################################################################

NTPD = SUSE.getServiceDInfo('ntpd.service')
if( len(NTPD) > 0 ):
	if( NTPD['ActiveState'].lower() == 'active' and NTPD['SubState'].lower() == 'running' ):
		Core.updateStatus(Core.IGNORE, "NTP Daemon is running, AVOIDED")
	else:
		APPARMOR = SUSE.getServiceDInfo('apparmor.service')
		if( len(APPARMOR) > 0 ):
			if( APPARMOR['ActiveState'].lower() == 'active' and APPARMOR['SubState'].lower() == 'exited' ):
				if( appArmorError() ):
					Core.updateStatus(Core.CRIT, "NTP Service Failure, Check AppArmor NTP Profile")
				else:
					Core.updateStatus(Core.WARN, "NTP Service Failure Probable, Check AppArmor NTP Profile")
			else:
				Core.updateStatus(Core.ERROR, "AppArmor not running, NTP not running but skipping NTP conflict check")
		else:
			Core.updateStatus(Core.ERROR, "AppArmor disabled, NTP not running but skipping NTP conflict check")
else:
	Core.updateStatus(Core.ERROR, "NTP Daemon disabled, not applicable")

Core.printPatternResults()


