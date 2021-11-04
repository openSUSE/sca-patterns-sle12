#!/usr/bin/python3
#
# Title:       Important Security Announcement for mariadb SUSE-SU-2017:1315-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP2
# Source:      Security Announcement Parser v1.3.6
# Modified:    2017 May 18
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
META_COMPONENT = "mariadb"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2017-05/msg00051.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'mariadb'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2017:1315-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 2 ):
		PACKAGES = {
			'libmysqlclient-devel': '10.0.30-25.1',
			'libmysqlclient18': '10.0.30-25.1',
			'libmysqlclient18-32bit': '10.0.30-25.1',
			'libmysqlclient18-debuginfo': '10.0.30-25.1',
			'libmysqlclient18-debuginfo-32bit': '10.0.30-25.1',
			'libmysqlclient_r18': '10.0.30-25.1',
			'libmysqlclient_r18-32bit': '10.0.30-25.1',
			'libmysqld-devel': '10.0.30-25.1',
			'libmysqld18': '10.0.30-25.1',
			'libmysqld18-debuginfo': '10.0.30-25.1',
			'mariadb': '10.0.30-25.1',
			'mariadb-client': '10.0.30-25.1',
			'mariadb-client-debuginfo': '10.0.30-25.1',
			'mariadb-debuginfo': '10.0.30-25.1',
			'mariadb-debugsource': '10.0.30-25.1',
			'mariadb-errormessages': '10.0.30-25.1',
			'mariadb-tools': '10.0.30-25.1',
			'mariadb-tools-debuginfo': '10.0.30-25.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

