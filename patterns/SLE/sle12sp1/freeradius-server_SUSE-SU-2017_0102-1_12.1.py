#!/usr/bin/python3
#
# Title:       Important Security Announcement for freeradius-server SUSE-SU-2017:0102-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP1
# Source:      Security Announcement Parser v1.3.6
# Modified:    2017 Apr 04
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
META_COMPONENT = "freeradius-server"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2017-01/msg00010.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'freeradius-server'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2017:0102-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 1 ):
		PACKAGES = {
			'freeradius-server': '3.0.3-14.1',
			'freeradius-server-debuginfo': '3.0.3-14.1',
			'freeradius-server-debugsource': '3.0.3-14.1',
			'freeradius-server-devel': '3.0.3-14.1',
			'freeradius-server-doc': '3.0.3-14.1',
			'freeradius-server-krb5': '3.0.3-14.1',
			'freeradius-server-krb5-debuginfo': '3.0.3-14.1',
			'freeradius-server-ldap': '3.0.3-14.1',
			'freeradius-server-ldap-debuginfo': '3.0.3-14.1',
			'freeradius-server-libs': '3.0.3-14.1',
			'freeradius-server-libs-debuginfo': '3.0.3-14.1',
			'freeradius-server-mysql': '3.0.3-14.1',
			'freeradius-server-mysql-debuginfo': '3.0.3-14.1',
			'freeradius-server-perl': '3.0.3-14.1',
			'freeradius-server-perl-debuginfo': '3.0.3-14.1',
			'freeradius-server-postgresql': '3.0.3-14.1',
			'freeradius-server-postgresql-debuginfo': '3.0.3-14.1',
			'freeradius-server-python': '3.0.3-14.1',
			'freeradius-server-python-debuginfo': '3.0.3-14.1',
			'freeradius-server-sqlite': '3.0.3-14.1',
			'freeradius-server-sqlite-debuginfo': '3.0.3-14.1',
			'freeradius-server-utils': '3.0.3-14.1',
			'freeradius-server-utils-debuginfo': '3.0.3-14.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

