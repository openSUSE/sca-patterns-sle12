#!/usr/bin/python
#
# Title:       Important Security Announcement for Kernel-rt SUSE-SU-2016:1937-1
# Description: Security fixes for SUSE Linux Enterprise Real Time Kernel 12 SP1
# Source:      Security Announcement Parser v1.3.2
# Modified:    2016 Aug 23
#
##############################################################################
# Copyright (C) 2016 SUSE LLC
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
#   Jason Record (jason.record@suse.com)
#
##############################################################################

import os
import Core
import SUSE

META_CLASS = "Security"
META_CATEGORY = "SLE"
META_COMPONENT = "Kernel-rt"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2016-08/msg00000.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'Kernel-rt'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2016:1937-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 1 ):
		PACKAGES = {
			'kernel-compute': '3.12.61-60.18.1',
			'kernel-compute-base': '3.12.61-60.18.1',
			'kernel-compute-base-debuginfo': '3.12.61-60.18.1',
			'kernel-compute-debuginfo': '3.12.61-60.18.1',
			'kernel-compute-debugsource': '3.12.61-60.18.1',
			'kernel-compute-devel': '3.12.61-60.18.1',
			'kernel-compute_debug-debuginfo': '3.12.61-60.18.1',
			'kernel-compute_debug-debugsource': '3.12.61-60.18.1',
			'kernel-compute_debug-devel': '3.12.61-60.18.1',
			'kernel-compute_debug-devel-debuginfo': '3.12.61-60.18.1',
			'kernel-devel-rt': '3.12.61-60.18.1',
			'kernel-rt': '3.12.61-60.18.1',
			'kernel-rt-base': '3.12.61-60.18.1',
			'kernel-rt-base-debuginfo': '3.12.61-60.18.1',
			'kernel-rt-debuginfo': '3.12.61-60.18.1',
			'kernel-rt-debugsource': '3.12.61-60.18.1',
			'kernel-rt-devel': '3.12.61-60.18.1',
			'kernel-rt_debug-debuginfo': '3.12.61-60.18.1',
			'kernel-rt_debug-debugsource': '3.12.61-60.18.1',
			'kernel-rt_debug-devel': '3.12.61-60.18.1',
			'kernel-rt_debug-devel-debuginfo': '3.12.61-60.18.1',
			'kernel-source-rt': '3.12.61-60.18.1',
			'kernel-syms-rt': '3.12.61-60.18.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

