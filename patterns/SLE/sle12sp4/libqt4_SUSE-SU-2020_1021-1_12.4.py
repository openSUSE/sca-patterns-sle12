#!/usr/bin/python
#
# Title:       Moderate Security Announcement for libqt4 SUSE-SU-2020:1021-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP4
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
META_COMPONENT = "libqt4"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-April/006715.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'libqt4'
MAIN = ''
SEVERITY = 'Moderate'
TAG = 'SUSE-SU-2020:1021-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 4 ):
		PACKAGES = {
			'libqt4': '4.8.7-8.13.1',
			'libqt4-32bit': '4.8.7-8.13.1',
			'libqt4-debuginfo': '4.8.7-8.13.1',
			'libqt4-debuginfo-32bit': '4.8.7-8.13.1',
			'libqt4-debugsource': '4.8.7-8.13.1',
			'libqt4-devel': '4.8.7-8.13.1',
			'libqt4-devel-debuginfo': '4.8.7-8.13.1',
			'libqt4-devel-doc': '4.8.7-8.13.1',
			'libqt4-devel-doc-data': '4.8.7-8.13.1',
			'libqt4-devel-doc-debuginfo': '4.8.7-8.13.1',
			'libqt4-devel-doc-debugsource': '4.8.7-8.13.1',
			'libqt4-linguist': '4.8.7-8.13.1',
			'libqt4-linguist-debuginfo': '4.8.7-8.13.1',
			'libqt4-private-headers-devel': '4.8.7-8.13.1',
			'libqt4-qt3support': '4.8.7-8.13.1',
			'libqt4-qt3support-32bit': '4.8.7-8.13.1',
			'libqt4-qt3support-debuginfo': '4.8.7-8.13.1',
			'libqt4-qt3support-debuginfo-32bit': '4.8.7-8.13.1',
			'libqt4-sql': '4.8.7-8.13.1',
			'libqt4-sql-32bit': '4.8.7-8.13.1',
			'libqt4-sql-debuginfo': '4.8.7-8.13.1',
			'libqt4-sql-debuginfo-32bit': '4.8.7-8.13.1',
			'libqt4-sql-mysql': '4.8.7-8.13.1',
			'libqt4-sql-mysql-32bit': '4.8.7-8.13.1',
			'libqt4-sql-mysql-debuginfo': '4.8.7-8.13.1',
			'libqt4-sql-mysql-debuginfo-32bit': '4.8.7-8.13.1',
			'libqt4-sql-plugins-debugsource': '4.8.7-8.13.1',
			'libqt4-sql-postgresql': '4.8.7-8.13.1',
			'libqt4-sql-postgresql-32bit': '4.8.7-8.13.1',
			'libqt4-sql-postgresql-debuginfo': '4.8.7-8.13.1',
			'libqt4-sql-postgresql-debuginfo-32bit': '4.8.7-8.13.1',
			'libqt4-sql-sqlite': '4.8.7-8.13.1',
			'libqt4-sql-sqlite-32bit': '4.8.7-8.13.1',
			'libqt4-sql-sqlite-debuginfo': '4.8.7-8.13.1',
			'libqt4-sql-sqlite-debuginfo-32bit': '4.8.7-8.13.1',
			'libqt4-sql-unixODBC': '4.8.7-8.13.1',
			'libqt4-sql-unixODBC-32bit': '4.8.7-8.13.1',
			'libqt4-sql-unixODBC-debuginfo': '4.8.7-8.13.1',
			'libqt4-sql-unixODBC-debuginfo-32bit': '4.8.7-8.13.1',
			'libqt4-x11': '4.8.7-8.13.1',
			'libqt4-x11-32bit': '4.8.7-8.13.1',
			'libqt4-x11-debuginfo': '4.8.7-8.13.1',
			'libqt4-x11-debuginfo-32bit': '4.8.7-8.13.1',
			'qt4-x11-tools': '4.8.7-8.13.1',
			'qt4-x11-tools-debuginfo': '4.8.7-8.13.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

