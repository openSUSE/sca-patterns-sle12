#!/usr/bin/python3
#
# Title:       Important Security Announcement for sssd SUSE-SU-2023:0200-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP4 LTSS
# URL:         https://lists.suse.com/pipermail/sle-security-updates/2023-January/013563.html
# Source:      Security Announcement Generator (sagen.py) v2.0.6
# Modified:    2023 Jun 13
#
##############################################################################
# Copyright (C) 2023 SUSE LLC
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

meta_class = "Security"
meta_category = "SLE"
meta_component = "sssd"
pattern_filename = os.path.basename(__file__)
primary_link = "META_LINK_Security"
overall = Core.TEMP
overall_info = "NOT SET"
other_links = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2023-January/013563.html"
Core.init(meta_class, meta_category, meta_component, pattern_filename, primary_link, overall, overall_info, other_links)

def main():
	ltss = True
	name = 'sssd'
	main = ''
	severity = 'Important'
	tag = 'SUSE-SU-2023:0200-1'
	packages = {}
	server = SUSE.getHostInfo()

	if ( server['DistroVersion'] == 12):
		if ( server['DistroPatchLevel'] == 4 ):
			packages = {
				'libipa_hbac0': '1.16.1-4.43.1',
				'libipa_hbac0-debuginfo': '1.16.1-4.43.1',
				'libsss_certmap0': '1.16.1-4.43.1',
				'libsss_certmap0-debuginfo': '1.16.1-4.43.1',
				'libsss_idmap0': '1.16.1-4.43.1',
				'libsss_idmap0-debuginfo': '1.16.1-4.43.1',
				'libsss_nss_idmap0': '1.16.1-4.43.1',
				'libsss_nss_idmap0-debuginfo': '1.16.1-4.43.1',
				'libsss_simpleifp0': '1.16.1-4.43.1',
				'libsss_simpleifp0-debuginfo': '1.16.1-4.43.1',
				'python-sssd-config': '1.16.1-4.43.1',
				'python-sssd-config-debuginfo': '1.16.1-4.43.1',
				'sssd': '1.16.1-4.43.1',
				'sssd-ad': '1.16.1-4.43.1',
				'sssd-ad-debuginfo': '1.16.1-4.43.1',
				'sssd-dbus': '1.16.1-4.43.1',
				'sssd-dbus-debuginfo': '1.16.1-4.43.1',
				'sssd-debuginfo': '1.16.1-4.43.1',
				'sssd-debugsource': '1.16.1-4.43.1',
				'sssd-ipa': '1.16.1-4.43.1',
				'sssd-ipa-debuginfo': '1.16.1-4.43.1',
				'sssd-krb5': '1.16.1-4.43.1',
				'sssd-krb5-common': '1.16.1-4.43.1',
				'sssd-krb5-common-debuginfo': '1.16.1-4.43.1',
				'sssd-krb5-debuginfo': '1.16.1-4.43.1',
				'sssd-ldap': '1.16.1-4.43.1',
				'sssd-ldap-debuginfo': '1.16.1-4.43.1',
				'sssd-proxy': '1.16.1-4.43.1',
				'sssd-proxy-debuginfo': '1.16.1-4.43.1',
				'sssd-tools': '1.16.1-4.43.1',
				'sssd-tools-debuginfo': '1.16.1-4.43.1',
			}
			SUSE.securityAnnouncementPackageCheck(name, main, ltss, severity, tag, packages)
		else:
			Core.updateStatus(Core.ERROR, "ERROR: " + name + " Security Announcement: Outside the service pack scope")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + name + " Security Announcement: Outside the distribution scope")

	Core.printPatternResults()

if __name__ == "__main__":
	main()

