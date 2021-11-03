#!/usr/bin/python3
#
# Title:       Important Security Announcement for kgraft-patch SUSE-SU-2021:2451-1
# Description: Security fixes for SUSE Linux Kernel Live Patch 12 SP3 LTSS
# Source:      Security Announcement Parser v1.6.1
# Modified:    2021 Aug 05
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
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2021-July/009203.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'kgraft-patch'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2021:2451-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'kernel-default': '4.4.180-94.147.1',
			'kernel-default-base': '4.4.180-94.147.1',
			'kernel-default-base-debuginfo': '4.4.180-94.147.1',
			'kernel-default-debuginfo': '4.4.180-94.147.1',
			'kernel-default-debugsource': '4.4.180-94.147.1',
			'kernel-default-devel': '4.4.180-94.147.1',
			'kernel-default-kgraft': '4.4.180-94.147.1',
			'kernel-default-man': '4.4.180-94.147.1',
			'kernel-devel': '4.4.180-94.147.1',
			'kernel-macros': '4.4.180-94.147.1',
			'kernel-source': '4.4.180-94.147.1',
			'kernel-syms': '4.4.180-94.147.1',
			'kgraft-patch-4_4_180-94_147-default': '1-4.3.1',
			'kgraft-patch-4_4_180-94_147-default-debuginfo': '1-4.3.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

