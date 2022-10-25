#!/usr/bin/python3
#
# Title:       Important Security Announcement for SP3) SUSE-SU-2022:2281-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP3 LTSS
# URL:         https://lists.suse.com/pipermail/sle-security-updates/2022-July/011410.html
# Source:      Security Announcement Generator (sagen.py) v2.0.0-beta4
# Modified:    2022 Oct 25
#
##############################################################################
# Copyright (C) 2022 SUSE LLC
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
META_COMPONENT = "SP3)"
pattern_filename = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2022-July/011410.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, pattern_filename, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'SP3)'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2022:2281-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'kgraft-patch-4_4_180-94_147-default': '14-2.2',
			'kgraft-patch-4_4_180-94_147-default-debuginfo': '14-2.2',
			'kgraft-patch-4_4_180-94_150-default': '10-2.2',
			'kgraft-patch-4_4_180-94_150-default-debuginfo': '10-2.2',
			'kgraft-patch-4_4_180-94_153-default': '6-2.2',
			'kgraft-patch-4_4_180-94_153-default-debuginfo': '6-2.2',
			'kgraft-patch-4_4_180-94_156-default': '5-2.2',
			'kgraft-patch-4_4_180-94_156-default-debuginfo': '5-2.2',
			'kgraft-patch-4_4_180-94_161-default': '4-2.2',
			'kgraft-patch-4_4_180-94_161-default-debuginfo': '4-2.2',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

