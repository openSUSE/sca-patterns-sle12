#!/usr/bin/python3
#
# Title:       Important Security Announcement for libqt5-qtbase SUSE-SU-2023:2816-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP5
# URL:         https://lists.suse.com/pipermail/sle-security-updates/2023-July/015475.html
# Source:      Security Announcement Generator (sagen.py) v2.0.13
# Modified:    2023 Aug 31
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
meta_component = "libqt5-qtbase"
pattern_filename = os.path.basename(__file__)
primary_link = "META_LINK_Security"
overall = Core.TEMP
overall_info = "NOT SET"
other_links = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2023-July/015475.html"
Core.init(meta_class, meta_category, meta_component, pattern_filename, primary_link, overall, overall_info, other_links)

def main():
	ltss = False
	name = 'libqt5-qtbase'
	main = ''
	severity = 'Important'
	tag = 'SUSE-SU-2023:2816-1'
	packages = {}
	server = SUSE.getHostInfo()

	if ( server['DistroVersion'] == 12):
		if ( server['DistroPatchLevel'] == 5 ):
			packages = {
				'libQt5Concurrent5': '5.6.2-6.33.1',
				'libQt5Concurrent5-debuginfo': '5.6.2-6.33.1',
				'libQt5Core5': '5.6.2-6.33.1',
				'libQt5Core5-debuginfo': '5.6.2-6.33.1',
				'libQt5DBus5': '5.6.2-6.33.1',
				'libQt5DBus5-debuginfo': '5.6.2-6.33.1',
				'libQt5Gui5': '5.6.2-6.33.1',
				'libQt5Gui5-debuginfo': '5.6.2-6.33.1',
				'libQt5Network5': '5.6.2-6.33.1',
				'libQt5Network5-debuginfo': '5.6.2-6.33.1',
				'libQt5OpenGL5': '5.6.2-6.33.1',
				'libQt5OpenGL5-debuginfo': '5.6.2-6.33.1',
				'libQt5PrintSupport5': '5.6.2-6.33.1',
				'libQt5PrintSupport5-debuginfo': '5.6.2-6.33.1',
				'libQt5Sql5': '5.6.2-6.33.1',
				'libQt5Sql5-debuginfo': '5.6.2-6.33.1',
				'libQt5Sql5-mysql': '5.6.2-6.33.1',
				'libQt5Sql5-mysql-debuginfo': '5.6.2-6.33.1',
				'libQt5Sql5-postgresql': '5.6.2-6.33.1',
				'libQt5Sql5-postgresql-debuginfo': '5.6.2-6.33.1',
				'libQt5Sql5-sqlite': '5.6.2-6.33.1',
				'libQt5Sql5-sqlite-debuginfo': '5.6.2-6.33.1',
				'libQt5Sql5-unixODBC': '5.6.2-6.33.1',
				'libQt5Sql5-unixODBC-debuginfo': '5.6.2-6.33.1',
				'libQt5Test5': '5.6.2-6.33.1',
				'libQt5Test5-debuginfo': '5.6.2-6.33.1',
				'libQt5Widgets5': '5.6.2-6.33.1',
				'libQt5Widgets5-debuginfo': '5.6.2-6.33.1',
				'libQt5Xml5': '5.6.2-6.33.1',
				'libQt5Xml5-debuginfo': '5.6.2-6.33.1',
				'libqt5-qtbase-debugsource': '5.6.2-6.33.1',
			}
			SUSE.securityAnnouncementPackageCheck(name, main, ltss, severity, tag, packages)
		else:
			Core.updateStatus(Core.ERROR, "ERROR: " + name + " Security Announcement: Outside the service pack scope")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + name + " Security Announcement: Outside the distribution scope")

	Core.printPatternResults()

if __name__ == "__main__":
	main()

