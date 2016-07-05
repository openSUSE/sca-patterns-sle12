#!/usr/bin/python

# Title:       Systemd Service Core Dumps
# Description: systemd-coredump is not consistent in dumping systemd service cores
# Modified:    2016 Jul 05
#
##############################################################################
# Copyright (C) 2016 SUSE LINUX Products GmbH, Nuernberg, Germany
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
META_CATEGORY = "Coredump"
META_COMPONENT = "Systemd"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7017378"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

SERVER = SUSE.getHostInfo()
RPM_NAME = 'systemd'
SLE = re.compile("SUSE Linux Enterprise", re.IGNORECASE)
if SLE.search(SERVER['Distro']):
	if( SERVER['DistroVersion'] == 12 ):
		if( SERVER['DistroPatchLevel'] == 0 ):
			RPM_VERSION = '210-70.39.1'
		elif( SERVER['DistroPatchLevel'] == 1 ):
			RPM_VERSION = '210-95.1'
		else:
			RPM_VERSION = ''

		if( len(RPM_VERSION) > 0 ):
			if( SUSE.packageInstalled(RPM_NAME) ):
				INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION)
				if( INSTALLED_VERSION <= 0 ):
					Core.updateStatus(Core.CRIT, "Detected inconsistent systemd coredumping issue, update server for fixes")
				else:
					Core.updateStatus(Core.IGNORE, "Bug fixes applied for " + RPM_NAME)
		else:
			Core.updateStatus(Core.ERROR, "Error: Outside distribution patch level scope")
	else:
		Core.updateStatus(Core.ERROR, "Error: Outside distribution version scope")
else:
	Core.updateStatus(Core.ERROR, SERVER['Distro'] + ": Invalid Distribution for Test Case")

Core.printPatternResults()


