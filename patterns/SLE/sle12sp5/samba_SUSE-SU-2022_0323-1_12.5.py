#!/usr/bin/python3
#
# Title:       Critical Security Announcement for samba SUSE-SU-2022:0323-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP5
# Source:      Security Announcement Parser v1.6.4
# Modified:    2022 May 06
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
META_COMPONENT = "samba"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2022-February/010181.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'samba'
MAIN = ''
SEVERITY = 'Critical'
TAG = 'SUSE-SU-2022:0323-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 5 ):
		PACKAGES = {
			'apache2-mod_apparmor': '2.8.2-56.6.3',
			'apache2-mod_apparmor-debuginfo': '2.8.2-56.6.3',
			'apparmor-debugsource': '2.8.2-56.6.3',
			'apparmor-docs': '2.8.2-56.6.3',
			'apparmor-parser': '2.8.2-56.6.3',
			'apparmor-parser-debuginfo': '2.8.2-56.6.3',
			'apparmor-profiles': '2.8.2-56.6.3',
			'apparmor-utils': '2.8.2-56.6.3',
			'ca-certificates': '1_201403302107-15.3.3',
			'gnutls-debugsource': '3.4.17-8.4.1',
			'libapparmor1': '2.8.2-56.6.3',
			'libapparmor1-32bit': '2.8.2-56.6.3',
			'libapparmor1-debuginfo': '2.8.2-56.6.3',
			'libapparmor1-debuginfo-32bit': '2.8.2-56.6.3',
			'libgnutls30': '3.4.17-8.4.1',
			'libgnutls30-32bit': '3.4.17-8.4.1',
			'libgnutls30-debuginfo': '3.4.17-8.4.1',
			'libgnutls30-debuginfo-32bit': '3.4.17-8.4.1',
			'libhogweed4': '3.1-21.3.2',
			'libhogweed4-32bit': '3.1-21.3.2',
			'libhogweed4-debuginfo': '3.1-21.3.2',
			'libhogweed4-debuginfo-32bit': '3.1-21.3.2',
			'libipa_hbac0': '1.16.1-7.28.9',
			'libipa_hbac0-debuginfo': '1.16.1-7.28.9',
			'libnettle-debugsource': '3.1-21.3.2',
			'libnettle6': '3.1-21.3.2',
			'libnettle6-32bit': '3.1-21.3.2',
			'libnettle6-debuginfo': '3.1-21.3.2',
			'libnettle6-debuginfo-32bit': '3.1-21.3.2',
			'libp11-kit0': '0.23.2-8.3.2',
			'libp11-kit0-32bit': '0.23.2-8.3.2',
			'libp11-kit0-debuginfo': '0.23.2-8.3.2',
			'libp11-kit0-debuginfo-32bit': '0.23.2-8.3.2',
			'libsamba-policy-python3-devel': '4.15.4+git.324.8332acf1a63-3.54.1',
			'libsamba-policy0-python3': '4.15.4+git.324.8332acf1a63-3.54.1',
			'libsamba-policy0-python3-32bit': '4.15.4+git.324.8332acf1a63-3.54.1',
			'libsamba-policy0-python3-debuginfo': '4.15.4+git.324.8332acf1a63-3.54.1',
			'libsamba-policy0-python3-debuginfo-32bit': '4.15.4+git.324.8332acf1a63-3.54.1',
			'libsss_certmap0': '1.16.1-7.28.9',
			'libsss_certmap0-debuginfo': '1.16.1-7.28.9',
			'libsss_idmap0': '1.16.1-7.28.9',
			'libsss_idmap0-debuginfo': '1.16.1-7.28.9',
			'libsss_nss_idmap-devel': '1.16.1-7.28.9',
			'libsss_nss_idmap0': '1.16.1-7.28.9',
			'libsss_nss_idmap0-debuginfo': '1.16.1-7.28.9',
			'libsss_simpleifp0': '1.16.1-7.28.9',
			'libsss_simpleifp0-debuginfo': '1.16.1-7.28.9',
			'p11-kit': '0.23.2-8.3.2',
			'p11-kit-32bit': '0.23.2-8.3.2',
			'p11-kit-debuginfo': '0.23.2-8.3.2',
			'p11-kit-debuginfo-32bit': '0.23.2-8.3.2',
			'p11-kit-debugsource': '0.23.2-8.3.2',
			'p11-kit-nss-trust': '0.23.2-8.3.2',
			'p11-kit-tools': '0.23.2-8.3.2',
			'p11-kit-tools-debuginfo': '0.23.2-8.3.2',
			'pam_apparmor': '2.8.2-56.6.3',
			'pam_apparmor-32bit': '2.8.2-56.6.3',
			'pam_apparmor-debuginfo': '2.8.2-56.6.3',
			'pam_apparmor-debuginfo-32bit': '2.8.2-56.6.3',
			'perl-apparmor': '2.8.2-56.6.3',
			'perl-apparmor-debuginfo': '2.8.2-56.6.3',
			'python-sssd-config': '1.16.1-7.28.9',
			'python-sssd-config-debuginfo': '1.16.1-7.28.9',
			'samba': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-client': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-client-32bit': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-client-debuginfo': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-client-debuginfo-32bit': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-client-libs': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-client-libs-32bit': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-client-libs-debuginfo': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-client-libs-debuginfo-32bit': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-debuginfo': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-debugsource': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-devel': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-doc': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-ldb-ldap': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-ldb-ldap-debuginfo': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-libs': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-libs-32bit': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-libs-debuginfo': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-libs-debuginfo-32bit': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-libs-python3': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-libs-python3-32bit': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-libs-python3-debuginfo': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-libs-python3-debuginfo-32bit': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-python3': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-python3-debuginfo': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-tool': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-winbind': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-winbind-debuginfo': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-winbind-libs': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-winbind-libs-32bit': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-winbind-libs-debuginfo': '4.15.4+git.324.8332acf1a63-3.54.1',
			'samba-winbind-libs-debuginfo-32bit': '4.15.4+git.324.8332acf1a63-3.54.1',
			'sssd': '1.16.1-7.28.9',
			'sssd-ad': '1.16.1-7.28.9',
			'sssd-ad-debuginfo': '1.16.1-7.28.9',
			'sssd-common': '1.16.1-7.28.9',
			'sssd-common-debuginfo': '1.16.1-7.28.9',
			'sssd-dbus': '1.16.1-7.28.9',
			'sssd-dbus-debuginfo': '1.16.1-7.28.9',
			'sssd-debugsource': '1.16.1-7.28.9',
			'sssd-ipa': '1.16.1-7.28.9',
			'sssd-ipa-debuginfo': '1.16.1-7.28.9',
			'sssd-krb5': '1.16.1-7.28.9',
			'sssd-krb5-common': '1.16.1-7.28.9',
			'sssd-krb5-common-debuginfo': '1.16.1-7.28.9',
			'sssd-krb5-debuginfo': '1.16.1-7.28.9',
			'sssd-ldap': '1.16.1-7.28.9',
			'sssd-ldap-debuginfo': '1.16.1-7.28.9',
			'sssd-proxy': '1.16.1-7.28.9',
			'sssd-proxy-debuginfo': '1.16.1-7.28.9',
			'sssd-tools': '1.16.1-7.28.9',
			'sssd-tools-debuginfo': '1.16.1-7.28.9',
			'yast2-samba-client': '3.1.23-3.3.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

