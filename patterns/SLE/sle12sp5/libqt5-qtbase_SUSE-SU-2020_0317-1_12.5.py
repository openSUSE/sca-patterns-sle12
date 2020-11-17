#!/usr/bin/python
#
# Title:       Important Security Announcement for libqt5-qtbase SUSE-SU-2020:0317-1
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
META_COMPONENT = "libqt5-qtbase"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-February/006448.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'libqt5-qtbase'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2020:0317-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 5 ):
		PACKAGES = {
			'libQt5Bootstrap-devel-static': '5.6.2-6.22.1',
			'libQt5Concurrent-devel': '5.6.2-6.22.1',
			'libQt5Concurrent5': '5.6.2-6.22.1',
			'libQt5Concurrent5-debuginfo': '5.6.2-6.22.1',
			'libQt5Core-devel': '5.6.2-6.22.1',
			'libQt5Core-private-headers-devel': '5.6.2-6.22.1',
			'libQt5Core5': '5.6.2-6.22.1',
			'libQt5Core5-debuginfo': '5.6.2-6.22.1',
			'libQt5DBus-devel': '5.6.2-6.22.1',
			'libQt5DBus-devel-debuginfo': '5.6.2-6.22.1',
			'libQt5DBus-private-headers-devel': '5.6.2-6.22.1',
			'libQt5DBus5': '5.6.2-6.22.1',
			'libQt5DBus5-debuginfo': '5.6.2-6.22.1',
			'libQt5Gui-devel': '5.6.2-6.22.1',
			'libQt5Gui-private-headers-devel': '5.6.2-6.22.1',
			'libQt5Gui5': '5.6.2-6.22.1',
			'libQt5Gui5-debuginfo': '5.6.2-6.22.1',
			'libQt5Network-devel': '5.6.2-6.22.1',
			'libQt5Network-private-headers-devel': '5.6.2-6.22.1',
			'libQt5Network5': '5.6.2-6.22.1',
			'libQt5Network5-debuginfo': '5.6.2-6.22.1',
			'libQt5OpenGL-devel': '5.6.2-6.22.1',
			'libQt5OpenGL-private-headers-devel': '5.6.2-6.22.1',
			'libQt5OpenGL5': '5.6.2-6.22.1',
			'libQt5OpenGL5-debuginfo': '5.6.2-6.22.1',
			'libQt5OpenGLExtensions-devel-static': '5.6.2-6.22.1',
			'libQt5PlatformHeaders-devel': '5.6.2-6.22.1',
			'libQt5PlatformSupport-devel-static': '5.6.2-6.22.1',
			'libQt5PlatformSupport-private-headers-devel': '5.6.2-6.22.1',
			'libQt5PrintSupport-devel': '5.6.2-6.22.1',
			'libQt5PrintSupport-private-headers-devel': '5.6.2-6.22.1',
			'libQt5PrintSupport5': '5.6.2-6.22.1',
			'libQt5PrintSupport5-debuginfo': '5.6.2-6.22.1',
			'libQt5Sql-devel': '5.6.2-6.22.1',
			'libQt5Sql-private-headers-devel': '5.6.2-6.22.1',
			'libQt5Sql5': '5.6.2-6.22.1',
			'libQt5Sql5-debuginfo': '5.6.2-6.22.1',
			'libQt5Sql5-mysql': '5.6.2-6.22.1',
			'libQt5Sql5-mysql-debuginfo': '5.6.2-6.22.1',
			'libQt5Sql5-postgresql': '5.6.2-6.22.1',
			'libQt5Sql5-postgresql-debuginfo': '5.6.2-6.22.1',
			'libQt5Sql5-sqlite': '5.6.2-6.22.1',
			'libQt5Sql5-sqlite-debuginfo': '5.6.2-6.22.1',
			'libQt5Sql5-unixODBC': '5.6.2-6.22.1',
			'libQt5Sql5-unixODBC-debuginfo': '5.6.2-6.22.1',
			'libQt5Test-devel': '5.6.2-6.22.1',
			'libQt5Test-private-headers-devel': '5.6.2-6.22.1',
			'libQt5Test5': '5.6.2-6.22.1',
			'libQt5Test5-debuginfo': '5.6.2-6.22.1',
			'libQt5Widgets-devel': '5.6.2-6.22.1',
			'libQt5Widgets-private-headers-devel': '5.6.2-6.22.1',
			'libQt5Widgets5': '5.6.2-6.22.1',
			'libQt5Widgets5-debuginfo': '5.6.2-6.22.1',
			'libQt5Xml-devel': '5.6.2-6.22.1',
			'libQt5Xml5': '5.6.2-6.22.1',
			'libQt5Xml5-debuginfo': '5.6.2-6.22.1',
			'libqt5-qtbase-common-devel': '5.6.2-6.22.1',
			'libqt5-qtbase-common-devel-debuginfo': '5.6.2-6.22.1',
			'libqt5-qtbase-debugsource': '5.6.2-6.22.1',
			'libqt5-qtbase-devel': '5.6.2-6.22.1',
			'libqt5-qtbase-private-headers-devel': '5.6.2-6.22.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

