#!/usr/bin/python3
#
# Title:       Important Security Announcement for krb5 SUSE-SU-2015:0290-2
# Description: Security fixes for SUSE Linux Enterprise 12 SP0
# Source:      Security Announcement Parser v1.2.5
# Modified:    2015 Feb 20
#
##############################################################################
# Copyright (C) 2015 SUSE LLC
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
#   Jason Record (jrecord@suse.com)
#
##############################################################################

import os
import Core
import SUSE

META_CLASS = "Security"
META_CATEGORY = "SLE"
META_COMPONENT = "krb5"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2015-02/msg00017.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'krb5'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2015:0290-2'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 0 ):
		PACKAGES = {
			'krb5': '1.12.1-9.1',
			'krb5-32bit': '1.12.1-9.1',
			'krb5-client': '1.12.1-9.1',
			'krb5-client-debuginfo': '1.12.1-9.1',
			'krb5-debuginfo': '1.12.1-9.1',
			'krb5-debuginfo-32bit': '1.12.1-9.1',
			'krb5-debugsource': '1.12.1-9.1',
			'krb5-devel': '1.12.1-9.1',
			'krb5-doc': '1.12.1-9.1',
			'krb5-mini': '1.12.1-9.1',
			'krb5-mini-debuginfo': '1.12.1-9.1',
			'krb5-mini-debugsource': '1.12.1-9.1',
			'krb5-mini-devel': '1.12.1-9.1',
			'krb5-plugin-kdb-ldap': '1.12.1-9.1',
			'krb5-plugin-kdb-ldap-debuginfo': '1.12.1-9.1',
			'krb5-plugin-preauth-otp': '1.12.1-9.1',
			'krb5-plugin-preauth-otp-debuginfo': '1.12.1-9.1',
			'krb5-plugin-preauth-pkinit': '1.12.1-9.1',
			'krb5-plugin-preauth-pkinit-debuginfo': '1.12.1-9.1',
			'krb5-server': '1.12.1-9.1',
			'krb5-server-debuginfo': '1.12.1-9.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

