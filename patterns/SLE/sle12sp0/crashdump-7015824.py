#!/usr/bin/python

# Title:       Crashdump Failure
# Description: System fails to generate a kernel crashdump and drops into bash shell after triggering kdump
# Modified:    2014 Nov 6
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
import Core
import SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Kernel"
META_COMPONENT = "Core"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7015824|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=900134"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def getKdumpInfo():
	INFO = {'Installed': False, 'Active': False}
	if( SUSE.packageInstalled('kdump') and SUSE.packageInstalled('kexec-tools') ):
		INFO['Installed'] = True
		SERVICE_NAME = 'kdump.service'
		SERVICE = SUSE.getServiceDInfo(SERVICE_NAME)
		if( len(SERVICE) > 0 and SERVICE['ActiveState'].lower() == 'active' ):
			INFO['Active'] = True
	return INFO

##############################################################################
# Main Program Execution
##############################################################################

SERVER = SUSE.getHostInfo()
if 'ppc64le' in SERVER['Architecture'].lower():
	if( SERVER['DistroVersion'] == 12 and SERVER['DistroPatchLevel'] < 1 ):
		PACKAGE = 'kexec-tools'
		AFFECTED_PACKAGE_VER = '2.0.5-9.22'
		KDUMP = getKdumpInfo()
		if( KDUMP['Active'] ):
			if( Core.compareVersions(SUSE.getRpmInfo(PACKAGE)['version'], AFFECTED_PACKAGE_VER) <= 0 ):
				Core.updateStatus(Core.CRIT, "Triggering kdump will fail to create a crashdump, consider makedumpfile")
			else:
				Core.updateStatus(Core.IGNORE, "Active Kdump crash issue resolved, not applicable")
		else:
			Core.updateStatus(Core.ERROR, "Kdump disabled, not applicable")
	else:
		Core.updateStatus(Core.ERROR, "Outside distribution and patchlevel scope, not applicable")
else:
	Core.updateStatus(Core.ERROR, "Outside architecture scope, not applicable")

Core.printPatternResults()


