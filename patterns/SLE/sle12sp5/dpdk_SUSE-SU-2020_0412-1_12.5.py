#!/usr/bin/python
#
# Title:       Moderate Security Announcement for dpdk SUSE-SU-2020:0412-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP5
# Source:      Security Announcement Parser v1.5.2
# Modified:    2020 Nov 16
#
##############################################################################
# Copyright (C) 2020 SUSE LLC
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
META_COMPONENT = "dpdk"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-February/006497.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'dpdk'
MAIN = ''
SEVERITY = 'Moderate'
TAG = 'SUSE-SU-2020:0412-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 5 ):
		PACKAGES = {
			'dpdk': '18.11.3-3.6.1',
			'dpdk-debuginfo': '18.11.3-3.6.1',
			'dpdk-debugsource': '18.11.3-3.6.1',
			'dpdk-devel': '18.11.3-3.6.1',
			'dpdk-devel-debuginfo': '18.11.3-3.6.1',
			'dpdk-kmp-default': '18.11.3_k4.12.14_122.12-3.6.1',
			'dpdk-kmp-default-debuginfo': '18.11.3_k4.12.14_122.12-3.6.1',
			'dpdk-thunderx': '18.11.3-3.6.1',
			'dpdk-thunderx-debuginfo': '18.11.3-3.6.1',
			'dpdk-thunderx-debugsource': '18.11.3-3.6.1',
			'dpdk-thunderx-devel': '18.11.3-3.6.1',
			'dpdk-thunderx-devel-debuginfo': '18.11.3-3.6.1',
			'dpdk-thunderx-kmp-default': '18.11.3_k4.12.14_122.12-3.6.1',
			'dpdk-thunderx-kmp-default-debuginfo': '18.11.3_k4.12.14_122.12-3.6.1',
			'dpdk-tools': '18.11.3-3.6.1',
			'dpdk-tools-debuginfo': '18.11.3-3.6.1',
			'libdpdk-18_11': '18.11.3-3.6.1',
			'libdpdk-18_11-debuginfo': '18.11.3-3.6.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

