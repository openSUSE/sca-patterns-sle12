#!/usr/bin/python
#
# Title:       Important Security Announcement for samba SUSE-SU-2017:0859-1
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
META_COMPONENT = "samba"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2017-03/msg00045.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'samba'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2017:0859-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 1 ):
		PACKAGES = {
			'ctdb': '4.2.4-28.8.2',
			'ctdb-debuginfo': '4.2.4-28.8.2',
			'ctdb-devel': '4.2.4-28.8.2',
			'libdcerpc-atsvc-devel': '4.2.4-28.8.2',
			'libdcerpc-atsvc0': '4.2.4-28.8.2',
			'libdcerpc-atsvc0-debuginfo': '4.2.4-28.8.2',
			'libdcerpc-binding0': '4.2.4-28.8.2',
			'libdcerpc-binding0-32bit': '4.2.4-28.8.2',
			'libdcerpc-binding0-debuginfo': '4.2.4-28.8.2',
			'libdcerpc-binding0-debuginfo-32bit': '4.2.4-28.8.2',
			'libdcerpc-devel': '4.2.4-28.8.2',
			'libdcerpc-samr-devel': '4.2.4-28.8.2',
			'libdcerpc-samr0': '4.2.4-28.8.2',
			'libdcerpc-samr0-debuginfo': '4.2.4-28.8.2',
			'libdcerpc0': '4.2.4-28.8.2',
			'libdcerpc0-32bit': '4.2.4-28.8.2',
			'libdcerpc0-debuginfo': '4.2.4-28.8.2',
			'libdcerpc0-debuginfo-32bit': '4.2.4-28.8.2',
			'libgensec-devel': '4.2.4-28.8.2',
			'libgensec0': '4.2.4-28.8.2',
			'libgensec0-32bit': '4.2.4-28.8.2',
			'libgensec0-debuginfo': '4.2.4-28.8.2',
			'libgensec0-debuginfo-32bit': '4.2.4-28.8.2',
			'libndr-devel': '4.2.4-28.8.2',
			'libndr-krb5pac-devel': '4.2.4-28.8.2',
			'libndr-krb5pac0': '4.2.4-28.8.2',
			'libndr-krb5pac0-32bit': '4.2.4-28.8.2',
			'libndr-krb5pac0-debuginfo': '4.2.4-28.8.2',
			'libndr-krb5pac0-debuginfo-32bit': '4.2.4-28.8.2',
			'libndr-nbt-devel': '4.2.4-28.8.2',
			'libndr-nbt0': '4.2.4-28.8.2',
			'libndr-nbt0-32bit': '4.2.4-28.8.2',
			'libndr-nbt0-debuginfo': '4.2.4-28.8.2',
			'libndr-nbt0-debuginfo-32bit': '4.2.4-28.8.2',
			'libndr-standard-devel': '4.2.4-28.8.2',
			'libndr-standard0': '4.2.4-28.8.2',
			'libndr-standard0-32bit': '4.2.4-28.8.2',
			'libndr-standard0-debuginfo': '4.2.4-28.8.2',
			'libndr-standard0-debuginfo-32bit': '4.2.4-28.8.2',
			'libndr0': '4.2.4-28.8.2',
			'libndr0-32bit': '4.2.4-28.8.2',
			'libndr0-debuginfo': '4.2.4-28.8.2',
			'libndr0-debuginfo-32bit': '4.2.4-28.8.2',
			'libnetapi-devel': '4.2.4-28.8.2',
			'libnetapi0': '4.2.4-28.8.2',
			'libnetapi0-32bit': '4.2.4-28.8.2',
			'libnetapi0-debuginfo': '4.2.4-28.8.2',
			'libnetapi0-debuginfo-32bit': '4.2.4-28.8.2',
			'libregistry-devel': '4.2.4-28.8.2',
			'libregistry0': '4.2.4-28.8.2',
			'libregistry0-debuginfo': '4.2.4-28.8.2',
			'libsamba-credentials-devel': '4.2.4-28.8.2',
			'libsamba-credentials0': '4.2.4-28.8.2',
			'libsamba-credentials0-32bit': '4.2.4-28.8.2',
			'libsamba-credentials0-debuginfo': '4.2.4-28.8.2',
			'libsamba-credentials0-debuginfo-32bit': '4.2.4-28.8.2',
			'libsamba-hostconfig-devel': '4.2.4-28.8.2',
			'libsamba-hostconfig0': '4.2.4-28.8.2',
			'libsamba-hostconfig0-32bit': '4.2.4-28.8.2',
			'libsamba-hostconfig0-debuginfo': '4.2.4-28.8.2',
			'libsamba-hostconfig0-debuginfo-32bit': '4.2.4-28.8.2',
			'libsamba-passdb-devel': '4.2.4-28.8.2',
			'libsamba-passdb0': '4.2.4-28.8.2',
			'libsamba-passdb0-32bit': '4.2.4-28.8.2',
			'libsamba-passdb0-debuginfo': '4.2.4-28.8.2',
			'libsamba-passdb0-debuginfo-32bit': '4.2.4-28.8.2',
			'libsamba-policy-devel': '4.2.4-28.8.2',
			'libsamba-policy0': '4.2.4-28.8.2',
			'libsamba-policy0-debuginfo': '4.2.4-28.8.2',
			'libsamba-util-devel': '4.2.4-28.8.2',
			'libsamba-util0': '4.2.4-28.8.2',
			'libsamba-util0-32bit': '4.2.4-28.8.2',
			'libsamba-util0-debuginfo': '4.2.4-28.8.2',
			'libsamba-util0-debuginfo-32bit': '4.2.4-28.8.2',
			'libsamdb-devel': '4.2.4-28.8.2',
			'libsamdb0': '4.2.4-28.8.2',
			'libsamdb0-32bit': '4.2.4-28.8.2',
			'libsamdb0-debuginfo': '4.2.4-28.8.2',
			'libsamdb0-debuginfo-32bit': '4.2.4-28.8.2',
			'libsmbclient-devel': '4.2.4-28.8.2',
			'libsmbclient-raw-devel': '4.2.4-28.8.2',
			'libsmbclient-raw0': '4.2.4-28.8.2',
			'libsmbclient-raw0-32bit': '4.2.4-28.8.2',
			'libsmbclient-raw0-debuginfo': '4.2.4-28.8.2',
			'libsmbclient-raw0-debuginfo-32bit': '4.2.4-28.8.2',
			'libsmbclient0': '4.2.4-28.8.2',
			'libsmbclient0-32bit': '4.2.4-28.8.2',
			'libsmbclient0-debuginfo': '4.2.4-28.8.2',
			'libsmbclient0-debuginfo-32bit': '4.2.4-28.8.2',
			'libsmbconf-devel': '4.2.4-28.8.2',
			'libsmbconf0': '4.2.4-28.8.2',
			'libsmbconf0-32bit': '4.2.4-28.8.2',
			'libsmbconf0-debuginfo': '4.2.4-28.8.2',
			'libsmbconf0-debuginfo-32bit': '4.2.4-28.8.2',
			'libsmbldap-devel': '4.2.4-28.8.2',
			'libsmbldap0': '4.2.4-28.8.2',
			'libsmbldap0-32bit': '4.2.4-28.8.2',
			'libsmbldap0-debuginfo': '4.2.4-28.8.2',
			'libsmbldap0-debuginfo-32bit': '4.2.4-28.8.2',
			'libtevent-util-devel': '4.2.4-28.8.2',
			'libtevent-util0': '4.2.4-28.8.2',
			'libtevent-util0-32bit': '4.2.4-28.8.2',
			'libtevent-util0-debuginfo': '4.2.4-28.8.2',
			'libtevent-util0-debuginfo-32bit': '4.2.4-28.8.2',
			'libwbclient-devel': '4.2.4-28.8.2',
			'libwbclient0': '4.2.4-28.8.2',
			'libwbclient0-32bit': '4.2.4-28.8.2',
			'libwbclient0-debuginfo': '4.2.4-28.8.2',
			'libwbclient0-debuginfo-32bit': '4.2.4-28.8.2',
			'samba': '4.2.4-28.8.2',
			'samba-32bit': '4.2.4-28.8.2',
			'samba-client': '4.2.4-28.8.2',
			'samba-client-32bit': '4.2.4-28.8.2',
			'samba-client-debuginfo': '4.2.4-28.8.2',
			'samba-client-debuginfo-32bit': '4.2.4-28.8.2',
			'samba-core-devel': '4.2.4-28.8.2',
			'samba-debuginfo': '4.2.4-28.8.2',
			'samba-debuginfo-32bit': '4.2.4-28.8.2',
			'samba-debugsource': '4.2.4-28.8.2',
			'samba-doc': '4.2.4-28.8.2',
			'samba-libs': '4.2.4-28.8.2',
			'samba-libs-32bit': '4.2.4-28.8.2',
			'samba-libs-debuginfo': '4.2.4-28.8.2',
			'samba-libs-debuginfo-32bit': '4.2.4-28.8.2',
			'samba-test-devel': '4.2.4-28.8.2',
			'samba-winbind': '4.2.4-28.8.2',
			'samba-winbind-32bit': '4.2.4-28.8.2',
			'samba-winbind-debuginfo': '4.2.4-28.8.2',
			'samba-winbind-debuginfo-32bit': '4.2.4-28.8.2',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

