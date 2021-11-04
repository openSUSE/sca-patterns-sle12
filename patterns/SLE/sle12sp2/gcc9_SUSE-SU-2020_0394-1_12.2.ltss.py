#!/usr/bin/python3
#
# Title:       Moderate Security Announcement for gcc9 SUSE-SU-2020:0394-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP2 LTSS
# Source:      Security Announcement Parser v1.5.2
# Modified:    2020 Nov 16
#
##############################################################################
# Copyright (C) 2020 SUSE LLC
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
META_COMPONENT = "gcc9"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-February/006488.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'gcc9'
MAIN = ''
SEVERITY = 'Moderate'
TAG = 'SUSE-SU-2020:0394-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 2 ):
		PACKAGES = {
			'gcc9-debuginfo': '9.2.1+r275327-1.3.9',
			'gcc9-debugsource': '9.2.1+r275327-1.3.9',
			'libasan5': '9.2.1+r275327-1.3.9',
			'libasan5-32bit': '9.2.1+r275327-1.3.9',
			'libasan5-32bit-debuginfo': '9.2.1+r275327-1.3.9',
			'libasan5-debuginfo': '9.2.1+r275327-1.3.9',
			'libatomic1': '9.2.1+r275327-1.3.9',
			'libatomic1-32bit': '9.2.1+r275327-1.3.9',
			'libatomic1-debuginfo': '9.2.1+r275327-1.3.9',
			'libgcc_s1': '9.2.1+r275327-1.3.9',
			'libgcc_s1-32bit': '9.2.1+r275327-1.3.9',
			'libgcc_s1-debuginfo': '9.2.1+r275327-1.3.9',
			'libgfortran5': '9.2.1+r275327-1.3.9',
			'libgfortran5-32bit': '9.2.1+r275327-1.3.9',
			'libgfortran5-debuginfo': '9.2.1+r275327-1.3.9',
			'libgo14': '9.2.1+r275327-1.3.9',
			'libgo14-32bit': '9.2.1+r275327-1.3.9',
			'libgo14-debuginfo': '9.2.1+r275327-1.3.9',
			'libgomp1': '9.2.1+r275327-1.3.9',
			'libgomp1-32bit': '9.2.1+r275327-1.3.9',
			'libgomp1-debuginfo': '9.2.1+r275327-1.3.9',
			'libitm1': '9.2.1+r275327-1.3.9',
			'libitm1-32bit': '9.2.1+r275327-1.3.9',
			'libitm1-debuginfo': '9.2.1+r275327-1.3.9',
			'liblsan0': '9.2.1+r275327-1.3.9',
			'liblsan0-debuginfo': '9.2.1+r275327-1.3.9',
			'libquadmath0': '9.2.1+r275327-1.3.9',
			'libquadmath0-32bit': '9.2.1+r275327-1.3.9',
			'libquadmath0-debuginfo': '9.2.1+r275327-1.3.9',
			'libstdc++6': '9.2.1+r275327-1.3.9',
			'libstdc++6-32bit': '9.2.1+r275327-1.3.9',
			'libstdc++6-debuginfo': '9.2.1+r275327-1.3.9',
			'libstdc++6-locale': '9.2.1+r275327-1.3.9',
			'libtsan0': '9.2.1+r275327-1.3.9',
			'libtsan0-debuginfo': '9.2.1+r275327-1.3.9',
			'libubsan1': '9.2.1+r275327-1.3.9',
			'libubsan1-32bit': '9.2.1+r275327-1.3.9',
			'libubsan1-32bit-debuginfo': '9.2.1+r275327-1.3.9',
			'libubsan1-debuginfo': '9.2.1+r275327-1.3.9',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

