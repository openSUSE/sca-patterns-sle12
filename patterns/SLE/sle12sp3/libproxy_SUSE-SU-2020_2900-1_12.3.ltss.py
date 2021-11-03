#!/usr/bin/python3
#
# Title:       Important Security Announcement for libproxy SUSE-SU-2020:2900-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP3 LTSS
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
META_COMPONENT = "libproxy"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-October/007543.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'libproxy'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2020:2900-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'libproxy-debugsource': '0.4.13-18.3.1',
			'libproxy-plugins-debugsource': '0.4.13-18.3.1',
			'libproxy1': '0.4.13-18.3.1',
			'libproxy1-32bit': '0.4.13-18.3.1',
			'libproxy1-config-gnome3': '0.4.13-18.3.1',
			'libproxy1-config-gnome3-32bit': '0.4.13-18.3.1',
			'libproxy1-config-gnome3-debuginfo': '0.4.13-18.3.1',
			'libproxy1-config-gnome3-debuginfo-32bit': '0.4.13-18.3.1',
			'libproxy1-debuginfo': '0.4.13-18.3.1',
			'libproxy1-debuginfo-32bit': '0.4.13-18.3.1',
			'libproxy1-networkmanager': '0.4.13-18.3.1',
			'libproxy1-networkmanager-debuginfo': '0.4.13-18.3.1',
			'libproxy1-pacrunner-webkit': '0.4.13-18.3.1',
			'libproxy1-pacrunner-webkit-debuginfo': '0.4.13-18.3.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

