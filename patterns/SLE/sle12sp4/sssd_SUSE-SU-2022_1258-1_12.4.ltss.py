#!/usr/bin/python3
#
# Title:       Important Security Announcement for sssd SUSE-SU-2022:1258-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP4 LTSS
# Source:      Security Announcement Parser v1.6.4
# Modified:    2022 May 05
#
##############################################################################
# Copyright (C) 2022 SUSE LLC
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
META_COMPONENT = "sssd"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2022-April/010748.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'sssd'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2022:1258-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 4 ):
		PACKAGES = {
			'libipa_hbac0': '1.16.1-4.40.1',
			'libipa_hbac0-debuginfo': '1.16.1-4.40.1',
			'libsss_certmap0': '1.16.1-4.40.1',
			'libsss_certmap0-debuginfo': '1.16.1-4.40.1',
			'libsss_idmap-devel': '1.16.1-4.40.1',
			'libsss_idmap0': '1.16.1-4.40.1',
			'libsss_idmap0-debuginfo': '1.16.1-4.40.1',
			'libsss_nss_idmap-devel': '1.16.1-4.40.1',
			'libsss_nss_idmap0': '1.16.1-4.40.1',
			'libsss_nss_idmap0-debuginfo': '1.16.1-4.40.1',
			'libsss_simpleifp0': '1.16.1-4.40.1',
			'libsss_simpleifp0-debuginfo': '1.16.1-4.40.1',
			'python-sssd-config': '1.16.1-4.40.1',
			'python-sssd-config-debuginfo': '1.16.1-4.40.1',
			'sssd': '1.16.1-4.40.1',
			'sssd-32bit': '1.16.1-4.40.1',
			'sssd-ad': '1.16.1-4.40.1',
			'sssd-ad-debuginfo': '1.16.1-4.40.1',
			'sssd-dbus': '1.16.1-4.40.1',
			'sssd-dbus-debuginfo': '1.16.1-4.40.1',
			'sssd-debuginfo': '1.16.1-4.40.1',
			'sssd-debuginfo-32bit': '1.16.1-4.40.1',
			'sssd-debugsource': '1.16.1-4.40.1',
			'sssd-ipa': '1.16.1-4.40.1',
			'sssd-ipa-debuginfo': '1.16.1-4.40.1',
			'sssd-krb5': '1.16.1-4.40.1',
			'sssd-krb5-common': '1.16.1-4.40.1',
			'sssd-krb5-common-debuginfo': '1.16.1-4.40.1',
			'sssd-krb5-debuginfo': '1.16.1-4.40.1',
			'sssd-ldap': '1.16.1-4.40.1',
			'sssd-ldap-debuginfo': '1.16.1-4.40.1',
			'sssd-proxy': '1.16.1-4.40.1',
			'sssd-proxy-debuginfo': '1.16.1-4.40.1',
			'sssd-tools': '1.16.1-4.40.1',
			'sssd-tools-debuginfo': '1.16.1-4.40.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

