#!/usr/bin/python3
#
# Title:       Important Security Announcement for glibc SUSE-SU-2017:1611-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP0
# Source:      Security Announcement Parser v1.3.6
# Modified:    2017 Jul 24
#
##############################################################################
# Copyright (C) 2017 SUSE LLC
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
META_COMPONENT = "glibc"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.opensuse.org/opensuse-security-announce/2017-06/msg00011.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'glibc'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2017:1611-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 0 ):
		PACKAGES = {
			'glibc': '2.19-22.21.1',
			'glibc-32bit': '2.19-22.21.1',
			'glibc-debuginfo': '2.19-22.21.1',
			'glibc-debuginfo-32bit': '2.19-22.21.1',
			'glibc-debugsource': '2.19-22.21.1',
			'glibc-devel': '2.19-22.21.1',
			'glibc-devel-32bit': '2.19-22.21.1',
			'glibc-devel-debuginfo': '2.19-22.21.1',
			'glibc-devel-debuginfo-32bit': '2.19-22.21.1',
			'glibc-html': '2.19-22.21.1',
			'glibc-i18ndata': '2.19-22.21.1',
			'glibc-info': '2.19-22.21.1',
			'glibc-locale': '2.19-22.21.1',
			'glibc-locale-32bit': '2.19-22.21.1',
			'glibc-locale-debuginfo': '2.19-22.21.1',
			'glibc-locale-debuginfo-32bit': '2.19-22.21.1',
			'glibc-profile': '2.19-22.21.1',
			'glibc-profile-32bit': '2.19-22.21.1',
			'nscd': '2.19-22.21.1',
			'nscd-debuginfo': '2.19-22.21.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

