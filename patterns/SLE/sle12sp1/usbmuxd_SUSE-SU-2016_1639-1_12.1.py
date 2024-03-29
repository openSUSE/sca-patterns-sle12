#!/usr/bin/python3
#
# Title:       Important Security Announcement for usbmuxd SUSE-SU-2016:1639-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP1
# Source:      Security Announcement Parser v1.3.1
# Modified:    2016 Jun 27
#
##############################################################################
# Copyright (C) 2016 SUSE LLC
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
#   Jason Record (jrecord@suse.com)
#
##############################################################################

import os
import Core
import SUSE

META_CLASS = "Security"
META_CATEGORY = "SLE"
META_COMPONENT = "usbmuxd"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2016-06/msg00042.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'usbmuxd'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2016:1639-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 1 ):
		PACKAGES = {
			'libimobiledevice-debugsource': '1.1.5-6.1',
			'libimobiledevice-devel': '1.1.5-6.1',
			'libimobiledevice-tools': '1.1.5-6.1',
			'libimobiledevice-tools-debuginfo': '1.1.5-6.1',
			'libimobiledevice4': '1.1.5-6.1',
			'libimobiledevice4-debuginfo': '1.1.5-6.1',
			'libusbmuxd-devel': '1.0.8-12.1',
			'libusbmuxd2': '1.0.8-12.1',
			'libusbmuxd2-debuginfo': '1.0.8-12.1',
			'usbmuxd': '1.0.8-12.1',
			'usbmuxd-debuginfo': '1.0.8-12.1',
			'usbmuxd-debugsource': '1.0.8-12.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

