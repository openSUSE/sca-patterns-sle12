#!/usr/bin/python3
#
# Title:       Moderate Security Announcement for gcc10 SUSE-SU-2020:3263-1
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
META_COMPONENT = "gcc10"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-November/007739.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'gcc10'
MAIN = ''
SEVERITY = 'Moderate'
TAG = 'SUSE-SU-2020:3263-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 2 ):
		PACKAGES = {
			'gcc10-debuginfo': '10.2.1+git583-1.3.5',
			'gcc10-debugsource': '10.2.1+git583-1.3.5',
			'libasan6': '10.2.1+git583-1.3.5',
			'libasan6-32bit': '10.2.1+git583-1.3.5',
			'libasan6-32bit-debuginfo': '10.2.1+git583-1.3.5',
			'libasan6-debuginfo': '10.2.1+git583-1.3.5',
			'libatomic1': '10.2.1+git583-1.3.5',
			'libatomic1-32bit': '10.2.1+git583-1.3.5',
			'libatomic1-32bit-debuginfo': '10.2.1+git583-1.3.5',
			'libatomic1-debuginfo': '10.2.1+git583-1.3.5',
			'libgcc_s1': '10.2.1+git583-1.3.5',
			'libgcc_s1-32bit': '10.2.1+git583-1.3.5',
			'libgcc_s1-32bit-debuginfo': '10.2.1+git583-1.3.5',
			'libgcc_s1-debuginfo': '10.2.1+git583-1.3.5',
			'libgfortran5': '10.2.1+git583-1.3.5',
			'libgfortran5-32bit': '10.2.1+git583-1.3.5',
			'libgfortran5-32bit-debuginfo': '10.2.1+git583-1.3.5',
			'libgfortran5-debuginfo': '10.2.1+git583-1.3.5',
			'libgo16': '10.2.1+git583-1.3.5',
			'libgo16-32bit': '10.2.1+git583-1.3.5',
			'libgo16-32bit-debuginfo': '10.2.1+git583-1.3.5',
			'libgo16-debuginfo': '10.2.1+git583-1.3.5',
			'libgomp1': '10.2.1+git583-1.3.5',
			'libgomp1-32bit': '10.2.1+git583-1.3.5',
			'libgomp1-32bit-debuginfo': '10.2.1+git583-1.3.5',
			'libgomp1-debuginfo': '10.2.1+git583-1.3.5',
			'libitm1': '10.2.1+git583-1.3.5',
			'libitm1-32bit': '10.2.1+git583-1.3.5',
			'libitm1-32bit-debuginfo': '10.2.1+git583-1.3.5',
			'libitm1-debuginfo': '10.2.1+git583-1.3.5',
			'liblsan0': '10.2.1+git583-1.3.5',
			'liblsan0-debuginfo': '10.2.1+git583-1.3.5',
			'libobjc4': '10.2.1+git583-1.3.5',
			'libobjc4-32bit': '10.2.1+git583-1.3.5',
			'libobjc4-32bit-debuginfo': '10.2.1+git583-1.3.5',
			'libobjc4-debuginfo': '10.2.1+git583-1.3.5',
			'libquadmath0': '10.2.1+git583-1.3.5',
			'libquadmath0-32bit': '10.2.1+git583-1.3.5',
			'libquadmath0-32bit-debuginfo': '10.2.1+git583-1.3.5',
			'libquadmath0-debuginfo': '10.2.1+git583-1.3.5',
			'libstdc++6': '10.2.1+git583-1.3.5',
			'libstdc++6-32bit': '10.2.1+git583-1.3.5',
			'libstdc++6-32bit-debuginfo': '10.2.1+git583-1.3.5',
			'libstdc++6-debuginfo': '10.2.1+git583-1.3.5',
			'libstdc++6-locale': '10.2.1+git583-1.3.5',
			'libstdc++6-pp-gcc10': '10.2.1+git583-1.3.5',
			'libstdc++6-pp-gcc10-32bit': '10.2.1+git583-1.3.5',
			'libtsan0': '10.2.1+git583-1.3.5',
			'libtsan0-debuginfo': '10.2.1+git583-1.3.5',
			'libubsan1': '10.2.1+git583-1.3.5',
			'libubsan1-32bit': '10.2.1+git583-1.3.5',
			'libubsan1-32bit-debuginfo': '10.2.1+git583-1.3.5',
			'libubsan1-debuginfo': '10.2.1+git583-1.3.5',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

