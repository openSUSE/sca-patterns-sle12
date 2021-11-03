#!/usr/bin/python3
#
# Title:       Important Security Announcement for spice-gtk SUSE-SU-2020:3841-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP2 LTSS
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
META_COMPONENT = "spice-gtk"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-December/008078.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'spice-gtk'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2020:3841-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 2 ):
		PACKAGES = {
			'libspice-client-glib-2_0-8': '0.31-9.10.1',
			'libspice-client-glib-2_0-8-debuginfo': '0.31-9.10.1',
			'libspice-client-glib-helper': '0.31-9.10.1',
			'libspice-client-glib-helper-debuginfo': '0.31-9.10.1',
			'libspice-client-gtk-2_0-4': '0.31-9.10.1',
			'libspice-client-gtk-2_0-4-debuginfo': '0.31-9.10.1',
			'libspice-client-gtk-3_0-4': '0.31-9.10.1',
			'libspice-client-gtk-3_0-4-debuginfo': '0.31-9.10.1',
			'libspice-controller0': '0.31-9.10.1',
			'libspice-controller0-debuginfo': '0.31-9.10.1',
			'spice-gtk-debuginfo': '0.31-9.10.1',
			'spice-gtk-debugsource': '0.31-9.10.1',
			'typelib-1_0-SpiceClientGlib-2_0': '0.31-9.10.1',
			'typelib-1_0-SpiceClientGtk-3_0': '0.31-9.10.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

