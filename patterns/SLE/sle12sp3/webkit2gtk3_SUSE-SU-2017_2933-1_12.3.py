#!/usr/bin/python3
#
# Title:       Important Security Announcement for webkit2gtk3 SUSE-SU-2017:2933-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP3
# Source:      Security Announcement Parser v1.3.6
# Modified:    2018 Jan 05
#
##############################################################################
# Copyright (C) 2018 SUSE LLC
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
META_COMPONENT = "webkit2gtk3"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.opensuse.org/opensuse-security-announce/2017-11/msg00005.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'webkit2gtk3'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2017:2933-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'libjavascriptcoregtk-4_0-18': '2.18.0-2.9.1',
			'libjavascriptcoregtk-4_0-18-debuginfo': '2.18.0-2.9.1',
			'libwebkit2gtk-4_0-37': '2.18.0-2.9.1',
			'libwebkit2gtk-4_0-37-debuginfo': '2.18.0-2.9.1',
			'libwebkit2gtk3-lang': '2.18.0-2.9.1',
			'typelib-1_0-JavaScriptCore-4_0': '2.18.0-2.9.1',
			'typelib-1_0-WebKit2-4_0': '2.18.0-2.9.1',
			'webkit2gtk-4_0-injected-bundles': '2.18.0-2.9.1',
			'webkit2gtk-4_0-injected-bundles-debuginfo': '2.18.0-2.9.1',
			'webkit2gtk3-debugsource': '2.18.0-2.9.1',
			'webkit2gtk3-devel': '2.18.0-2.9.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

