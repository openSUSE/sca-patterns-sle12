#!/usr/bin/python
#
# Title:       Important Security Announcement for kgraft-patch SUSE-SU-2021:2060-1
# Description: Security fixes for SUSE Linux Kernel Live Patch 12 SP3 LTSS
# Source:      Security Announcement Parser v1.6.1
# Modified:    2021 Jul 02
#
##############################################################################
# Copyright (C) 2021 SUSE LLC
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
#   Jason Record <jason.record@suse.com>
#
##############################################################################

import os
import Core
import SUSE

META_CLASS = "Security"
META_CATEGORY = "SLE"
META_COMPONENT = "kgraft-patch"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2021-June/009049.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'kgraft-patch'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2021:2060-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'kgraft-patch-4_4_180-94_124-default': '11-2.3',
			'kgraft-patch-4_4_180-94_124-default-debuginfo': '11-2.3',
			'kgraft-patch-4_4_180-94_127-default': '11-2.2',
			'kgraft-patch-4_4_180-94_127-default-debuginfo': '11-2.2',
			'kgraft-patch-4_4_180-94_130-default': '10-2.2',
			'kgraft-patch-4_4_180-94_130-default-debuginfo': '10-2.2',
			'kgraft-patch-4_4_180-94_135-default': '8-2.2',
			'kgraft-patch-4_4_180-94_135-default-debuginfo': '8-2.2',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

