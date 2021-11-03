#!/usr/bin/python3
#
# Title:       Important Security Announcement for libqt5-qtbase SUSE-SU-2020:2751-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP3 LTSS
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
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-September/007486.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'libqt5-qtbase'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2020:2751-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'libQt5Concurrent5': '5.6.2-6.25.1',
			'libQt5Concurrent5-debuginfo': '5.6.2-6.25.1',
			'libQt5Core5': '5.6.2-6.25.1',
			'libQt5Core5-debuginfo': '5.6.2-6.25.1',
			'libQt5DBus5': '5.6.2-6.25.1',
			'libQt5DBus5-debuginfo': '5.6.2-6.25.1',
			'libQt5Gui5': '5.6.2-6.25.1',
			'libQt5Gui5-debuginfo': '5.6.2-6.25.1',
			'libQt5Network5': '5.6.2-6.25.1',
			'libQt5Network5-debuginfo': '5.6.2-6.25.1',
			'libQt5OpenGL5': '5.6.2-6.25.1',
			'libQt5OpenGL5-debuginfo': '5.6.2-6.25.1',
			'libQt5PrintSupport5': '5.6.2-6.25.1',
			'libQt5PrintSupport5-debuginfo': '5.6.2-6.25.1',
			'libQt5Sql5': '5.6.2-6.25.1',
			'libQt5Sql5-debuginfo': '5.6.2-6.25.1',
			'libQt5Sql5-mysql': '5.6.2-6.25.1',
			'libQt5Sql5-mysql-debuginfo': '5.6.2-6.25.1',
			'libQt5Sql5-postgresql': '5.6.2-6.25.1',
			'libQt5Sql5-postgresql-debuginfo': '5.6.2-6.25.1',
			'libQt5Sql5-sqlite': '5.6.2-6.25.1',
			'libQt5Sql5-sqlite-debuginfo': '5.6.2-6.25.1',
			'libQt5Sql5-unixODBC': '5.6.2-6.25.1',
			'libQt5Sql5-unixODBC-debuginfo': '5.6.2-6.25.1',
			'libQt5Test5': '5.6.2-6.25.1',
			'libQt5Test5-debuginfo': '5.6.2-6.25.1',
			'libQt5Widgets5': '5.6.2-6.25.1',
			'libQt5Widgets5-debuginfo': '5.6.2-6.25.1',
			'libQt5Xml5': '5.6.2-6.25.1',
			'libQt5Xml5-debuginfo': '5.6.2-6.25.1',
			'libqt5-qtbase-debugsource': '5.6.2-6.25.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

