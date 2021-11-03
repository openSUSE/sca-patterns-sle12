#!/usr/bin/python3
#
# Title:       Moderate Security Announcement for librsvg SUSE-SU-2020:0604-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP4
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
META_COMPONENT = "librsvg"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-March/006583.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'librsvg'
MAIN = ''
SEVERITY = 'Moderate'
TAG = 'SUSE-SU-2020:0604-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 4 ):
		PACKAGES = {
			'gdk-pixbuf-loader-rsvg': '2.40.21-5.9.1',
			'gdk-pixbuf-loader-rsvg-debuginfo': '2.40.21-5.9.1',
			'librsvg-2-2': '2.40.21-5.9.1',
			'librsvg-2-2-32bit': '2.40.21-5.9.1',
			'librsvg-2-2-debuginfo': '2.40.21-5.9.1',
			'librsvg-2-2-debuginfo-32bit': '2.40.21-5.9.1',
			'librsvg-debugsource': '2.40.21-5.9.1',
			'librsvg-devel': '2.40.21-5.9.1',
			'rsvg-view': '2.40.21-5.9.1',
			'rsvg-view-debuginfo': '2.40.21-5.9.1',
			'typelib-1_0-Rsvg-2_0': '2.40.21-5.9.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

