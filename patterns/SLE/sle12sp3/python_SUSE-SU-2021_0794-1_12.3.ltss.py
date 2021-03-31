#!/usr/bin/python
#
# Title:       Moderate Security Announcement for python SUSE-SU-2021:0794-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP3 LTSS
# Source:      Security Announcement Parser v1.6.1
# Modified:    2021 Mar 31
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
META_COMPONENT = "python"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2021-March/008491.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'python'
MAIN = ''
SEVERITY = 'Moderate'
TAG = 'SUSE-SU-2021:0794-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'libpython2_7-1_0': '2.7.18-28.67.1',
			'libpython2_7-1_0-32bit': '2.7.18-28.67.1',
			'libpython2_7-1_0-debuginfo': '2.7.18-28.67.1',
			'libpython2_7-1_0-debuginfo-32bit': '2.7.18-28.67.1',
			'python': '2.7.18-28.67.1',
			'python-32bit': '2.7.18-28.67.1',
			'python-base': '2.7.18-28.67.1',
			'python-base-32bit': '2.7.18-28.67.1',
			'python-base-debuginfo': '2.7.18-28.67.1',
			'python-base-debuginfo-32bit': '2.7.18-28.67.1',
			'python-base-debugsource': '2.7.18-28.67.1',
			'python-curses': '2.7.18-28.67.1',
			'python-curses-debuginfo': '2.7.18-28.67.1',
			'python-debuginfo': '2.7.18-28.67.1',
			'python-debuginfo-32bit': '2.7.18-28.67.1',
			'python-debugsource': '2.7.18-28.67.1',
			'python-demo': '2.7.18-28.67.1',
			'python-devel': '2.7.18-28.67.1',
			'python-doc': '2.7.18-28.67.1',
			'python-doc-pdf': '2.7.18-28.67.1',
			'python-gdbm': '2.7.18-28.67.1',
			'python-gdbm-debuginfo': '2.7.18-28.67.1',
			'python-idle': '2.7.18-28.67.1',
			'python-tk': '2.7.18-28.67.1',
			'python-tk-debuginfo': '2.7.18-28.67.1',
			'python-xml': '2.7.18-28.67.1',
			'python-xml-debuginfo': '2.7.18-28.67.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

