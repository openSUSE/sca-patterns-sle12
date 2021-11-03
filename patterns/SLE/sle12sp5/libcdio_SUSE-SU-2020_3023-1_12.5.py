#!/usr/bin/python3
#
# Title:       Low Security Announcement for libcdio SUSE-SU-2020:3023-1
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
META_COMPONENT = "libcdio"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-October/007617.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'libcdio'
MAIN = ''
SEVERITY = 'Low'
TAG = 'SUSE-SU-2020:3023-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 5 ):
		PACKAGES = {
			'libcdio++0': '0.90-6.6.5',
			'libcdio++0-debuginfo': '0.90-6.6.5',
			'libcdio-debugsource': '0.90-6.6.5',
			'libcdio-devel': '0.90-6.6.5',
			'libcdio14': '0.90-6.6.5',
			'libcdio14-32bit': '0.90-6.6.5',
			'libcdio14-debuginfo': '0.90-6.6.5',
			'libcdio14-debuginfo-32bit': '0.90-6.6.5',
			'libiso9660-8': '0.90-6.6.5',
			'libiso9660-8-debuginfo': '0.90-6.6.5',
			'libudf0': '0.90-6.6.5',
			'libudf0-debuginfo': '0.90-6.6.5',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

