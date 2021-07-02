#!/usr/bin/python
#
# Title:       Important Security Announcement for avahi SUSE-SU-2021:1494-2
# Description: Security fixes for SUSE Linux Enterprise 12 SP3 LTSS
# Source:      Security Announcement Parser v1.6.1
# Modified:    2021 Jul 02
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
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2021-June/008929.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'avahi'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2021:1494-2'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'avahi': '0.6.32-32.15.1',
			'avahi-debuginfo': '0.6.32-32.15.1',
			'avahi-debuginfo-32bit': '0.6.32-32.15.1',
			'avahi-debugsource': '0.6.32-32.15.1',
			'avahi-glib2-debugsource': '0.6.32-32.15.1',
			'avahi-lang': '0.6.32-32.15.1',
			'avahi-utils': '0.6.32-32.15.1',
			'avahi-utils-debuginfo': '0.6.32-32.15.1',
			'libavahi-client3': '0.6.32-32.15.1',
			'libavahi-client3-32bit': '0.6.32-32.15.1',
			'libavahi-client3-debuginfo': '0.6.32-32.15.1',
			'libavahi-client3-debuginfo-32bit': '0.6.32-32.15.1',
			'libavahi-common3': '0.6.32-32.15.1',
			'libavahi-common3-32bit': '0.6.32-32.15.1',
			'libavahi-common3-debuginfo': '0.6.32-32.15.1',
			'libavahi-common3-debuginfo-32bit': '0.6.32-32.15.1',
			'libavahi-core7': '0.6.32-32.15.1',
			'libavahi-core7-debuginfo': '0.6.32-32.15.1',
			'libavahi-glib1': '0.6.32-32.15.1',
			'libavahi-glib1-32bit': '0.6.32-32.15.1',
			'libavahi-glib1-debuginfo': '0.6.32-32.15.1',
			'libavahi-glib1-debuginfo-32bit': '0.6.32-32.15.1',
			'libdns_sd': '0.6.32-32.15.1',
			'libdns_sd-32bit': '0.6.32-32.15.1',
			'libdns_sd-debuginfo': '0.6.32-32.15.1',
			'libdns_sd-debuginfo-32bit': '0.6.32-32.15.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

