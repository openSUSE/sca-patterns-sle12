#!/usr/bin/python3
#
# Title:       Important Security Announcement for samba SUSE-SU-2023:0126-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP4 LTSS
# URL:         https://lists.suse.com/pipermail/sle-security-updates/2023-January/013514.html
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
meta_component = "samba"
pattern_filename = os.path.basename(__file__)
primary_link = "META_LINK_Security"
overall = Core.TEMP
overall_info = "NOT SET"
other_links = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2023-January/013514.html"
Core.init(meta_class, meta_category, meta_component, pattern_filename, primary_link, overall, overall_info, other_links)

def main():
	ltss = True
	name = 'samba'
	main = ''
	severity = 'Important'
	tag = 'SUSE-SU-2023:0126-1'
	packages = {}
	server = SUSE.getHostInfo()

	if ( server['DistroVersion'] == 12):
		if ( server['DistroPatchLevel'] == 4 ):
			packages = {
				'libdcerpc-binding0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libdcerpc-binding0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libdcerpc0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libdcerpc0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libndr-krb5pac0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libndr-krb5pac0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libndr-nbt0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libndr-nbt0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libndr-standard0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libndr-standard0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libndr0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libndr0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libnetapi0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libnetapi0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsamba-credentials0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsamba-credentials0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsamba-errors0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsamba-errors0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsamba-hostconfig0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsamba-hostconfig0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsamba-passdb0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsamba-passdb0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsamba-util0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsamba-util0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsamdb0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsamdb0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsmbclient0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsmbclient0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsmbconf0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsmbconf0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsmbldap0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libsmbldap0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libtevent-util0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libtevent-util0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'libwbclient0': '4.6.16+git.384.9fec958bed-3.76.1',
				'libwbclient0-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'samba': '4.6.16+git.384.9fec958bed-3.76.1',
				'samba-client': '4.6.16+git.384.9fec958bed-3.76.1',
				'samba-client-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'samba-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'samba-debugsource': '4.6.16+git.384.9fec958bed-3.76.1',
				'samba-libs': '4.6.16+git.384.9fec958bed-3.76.1',
				'samba-libs-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
				'samba-winbind': '4.6.16+git.384.9fec958bed-3.76.1',
				'samba-winbind-debuginfo': '4.6.16+git.384.9fec958bed-3.76.1',
			}
			SUSE.securityAnnouncementPackageCheck(name, main, ltss, severity, tag, packages)
		else:
			Core.updateStatus(Core.ERROR, "ERROR: " + name + " Security Announcement: Outside the service pack scope")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + name + " Security Announcement: Outside the distribution scope")

	Core.printPatternResults()

if __name__ == "__main__":
	main()

