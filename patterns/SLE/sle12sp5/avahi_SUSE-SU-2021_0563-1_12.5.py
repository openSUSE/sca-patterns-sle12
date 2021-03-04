#!/usr/bin/python
#
# Title:       Moderate Security Announcement for avahi SUSE-SU-2021:0563-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP5
# Source:      Security Announcement Parser v1.6.1
# Modified:    2021 Mar 03
#
##############################################################################
# Copyright (C) 2021 SUSE LLC
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
META_COMPONENT = "avahi"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2021-February/008362.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'avahi'
MAIN = ''
SEVERITY = 'Moderate'
TAG = 'SUSE-SU-2021:0563-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 5 ):
		PACKAGES = {
			'avahi': '0.6.32-32.12.2',
			'avahi-debuginfo': '0.6.32-32.12.2',
			'avahi-debuginfo-32bit': '0.6.32-32.12.2',
			'avahi-debugsource': '0.6.32-32.12.2',
			'avahi-glib2-debugsource': '0.6.32-32.12.3',
			'avahi-lang': '0.6.32-32.12.2',
			'avahi-utils': '0.6.32-32.12.2',
			'avahi-utils-debuginfo': '0.6.32-32.12.2',
			'libavahi-client3': '0.6.32-32.12.2',
			'libavahi-client3-32bit': '0.6.32-32.12.2',
			'libavahi-client3-debuginfo': '0.6.32-32.12.2',
			'libavahi-client3-debuginfo-32bit': '0.6.32-32.12.2',
			'libavahi-common3': '0.6.32-32.12.2',
			'libavahi-common3-32bit': '0.6.32-32.12.2',
			'libavahi-common3-debuginfo': '0.6.32-32.12.2',
			'libavahi-common3-debuginfo-32bit': '0.6.32-32.12.2',
			'libavahi-core7': '0.6.32-32.12.2',
			'libavahi-core7-debuginfo': '0.6.32-32.12.2',
			'libavahi-glib1': '0.6.32-32.12.3',
			'libavahi-glib1-32bit': '0.6.32-32.12.3',
			'libavahi-glib1-debuginfo': '0.6.32-32.12.3',
			'libavahi-glib1-debuginfo-32bit': '0.6.32-32.12.3',
			'libdns_sd': '0.6.32-32.12.2',
			'libdns_sd-32bit': '0.6.32-32.12.2',
			'libdns_sd-debuginfo': '0.6.32-32.12.2',
			'libdns_sd-debuginfo-32bit': '0.6.32-32.12.2',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

