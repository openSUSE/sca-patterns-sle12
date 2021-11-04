#!/usr/bin/python3
#
# Title:       Important Security Announcement for resource-agents SUSE-SU-2017:2237-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP3
# Source:      Security Announcement Parser v1.3.6
# Modified:    2017 Sep 08
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
META_COMPONENT = "resource-agents"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.opensuse.org/opensuse-security-announce/2017-08/msg00063.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'resource-agents'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2017:2237-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'ctdb': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'ctdb-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'ldirectord': '4.0.1+git.1495055229.643177f1-2.4.2',
			'libdcerpc-binding0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libdcerpc-binding0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libdcerpc-binding0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libdcerpc-binding0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libdcerpc0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libdcerpc0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libdcerpc0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libdcerpc0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr-krb5pac0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr-krb5pac0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr-krb5pac0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr-krb5pac0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr-nbt0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr-nbt0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr-nbt0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr-nbt0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr-standard0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr-standard0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr-standard0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr-standard0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libndr0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libnetapi0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libnetapi0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libnetapi0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libnetapi0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-credentials0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-credentials0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-credentials0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-credentials0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-errors0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-errors0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-errors0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-errors0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-hostconfig0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-hostconfig0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-hostconfig0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-hostconfig0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-passdb0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-passdb0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-passdb0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-passdb0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-util0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-util0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-util0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamba-util0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamdb0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamdb0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamdb0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsamdb0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsmbclient-devel': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsmbclient0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsmbclient0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsmbclient0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsmbclient0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsmbconf0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsmbconf0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsmbconf0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsmbconf0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsmbldap0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsmbldap0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsmbldap0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libsmbldap0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libtevent-util0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libtevent-util0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libtevent-util0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libtevent-util0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libwbclient-devel': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libwbclient0': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libwbclient0-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libwbclient0-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'libwbclient0-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'monitoring-plugins-metadata': '4.0.1+git.1495055229.643177f1-2.4.2',
			'resource-agents': '4.0.1+git.1495055229.643177f1-2.4.2',
			'resource-agents-debuginfo': '4.0.1+git.1495055229.643177f1-2.4.2',
			'resource-agents-debugsource': '4.0.1+git.1495055229.643177f1-2.4.2',
			'samba': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'samba-client': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'samba-client-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'samba-client-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'samba-client-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'samba-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'samba-debugsource': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'samba-doc': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'samba-libs': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'samba-libs-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'samba-libs-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'samba-libs-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'samba-winbind': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'samba-winbind-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'samba-winbind-debuginfo': '4.6.7+git.38.90b2cdb4f22-3.7.1',
			'samba-winbind-debuginfo-32bit': '4.6.7+git.38.90b2cdb4f22-3.7.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

