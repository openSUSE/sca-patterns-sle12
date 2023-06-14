#!/usr/bin/python3
#
# Title:       Important Security Announcement for freeradius-server SUSE-SU-2022:4621-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP5
# URL:         https://lists.suse.com/pipermail/sle-security-updates/2022-December/013345.html
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
meta_component = "freeradius-server"
pattern_filename = os.path.basename(__file__)
primary_link = "META_LINK_Security"
overall = Core.TEMP
overall_info = "NOT SET"
other_links = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2022-December/013345.html"
Core.init(meta_class, meta_category, meta_component, pattern_filename, primary_link, overall, overall_info, other_links)

def main():
	ltss = False
	name = 'freeradius-server'
	main = ''
	severity = 'Important'
	tag = 'SUSE-SU-2022:4621-1'
	packages = {}
	server = SUSE.getHostInfo()

	if ( server['DistroVersion'] == 12):
		if ( server['DistroPatchLevel'] == 5 ):
			packages = {
				'freeradius-server': '3.0.19-3.12.1',
				'freeradius-server-debuginfo': '3.0.19-3.12.1',
				'freeradius-server-debugsource': '3.0.19-3.12.1',
				'freeradius-server-doc': '3.0.19-3.12.1',
				'freeradius-server-krb5': '3.0.19-3.12.1',
				'freeradius-server-krb5-debuginfo': '3.0.19-3.12.1',
				'freeradius-server-ldap': '3.0.19-3.12.1',
				'freeradius-server-ldap-debuginfo': '3.0.19-3.12.1',
				'freeradius-server-libs': '3.0.19-3.12.1',
				'freeradius-server-libs-debuginfo': '3.0.19-3.12.1',
				'freeradius-server-mysql': '3.0.19-3.12.1',
				'freeradius-server-mysql-debuginfo': '3.0.19-3.12.1',
				'freeradius-server-perl': '3.0.19-3.12.1',
				'freeradius-server-perl-debuginfo': '3.0.19-3.12.1',
				'freeradius-server-postgresql': '3.0.19-3.12.1',
				'freeradius-server-postgresql-debuginfo': '3.0.19-3.12.1',
				'freeradius-server-python': '3.0.19-3.12.1',
				'freeradius-server-python-debuginfo': '3.0.19-3.12.1',
				'freeradius-server-sqlite': '3.0.19-3.12.1',
				'freeradius-server-sqlite-debuginfo': '3.0.19-3.12.1',
				'freeradius-server-utils': '3.0.19-3.12.1',
				'freeradius-server-utils-debuginfo': '3.0.19-3.12.1',
			}
			SUSE.securityAnnouncementPackageCheck(name, main, ltss, severity, tag, packages)
		else:
			Core.updateStatus(Core.ERROR, "ERROR: " + name + " Security Announcement: Outside the service pack scope")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + name + " Security Announcement: Outside the distribution scope")

	Core.printPatternResults()

if __name__ == "__main__":
	main()

