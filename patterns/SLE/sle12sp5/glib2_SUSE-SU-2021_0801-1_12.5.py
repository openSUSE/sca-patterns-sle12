#!/usr/bin/python3
#
# Title:       Important Security Announcement for glib2 SUSE-SU-2021:0801-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP5
# Source:      Security Announcement Parser v1.6.1
# Modified:    2021 Mar 31
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
META_COMPONENT = "glib2"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2021-March/008493.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'glib2'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2021:0801-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 5 ):
		PACKAGES = {
			'glib2-debugsource': '2.48.2-12.22.1',
			'glib2-lang': '2.48.2-12.22.1',
			'glib2-tools': '2.48.2-12.22.1',
			'glib2-tools-debuginfo': '2.48.2-12.22.1',
			'libgio-2_0-0': '2.48.2-12.22.1',
			'libgio-2_0-0-32bit': '2.48.2-12.22.1',
			'libgio-2_0-0-debuginfo': '2.48.2-12.22.1',
			'libgio-2_0-0-debuginfo-32bit': '2.48.2-12.22.1',
			'libglib-2_0-0': '2.48.2-12.22.1',
			'libglib-2_0-0-32bit': '2.48.2-12.22.1',
			'libglib-2_0-0-debuginfo': '2.48.2-12.22.1',
			'libglib-2_0-0-debuginfo-32bit': '2.48.2-12.22.1',
			'libgmodule-2_0-0': '2.48.2-12.22.1',
			'libgmodule-2_0-0-32bit': '2.48.2-12.22.1',
			'libgmodule-2_0-0-debuginfo': '2.48.2-12.22.1',
			'libgmodule-2_0-0-debuginfo-32bit': '2.48.2-12.22.1',
			'libgobject-2_0-0': '2.48.2-12.22.1',
			'libgobject-2_0-0-32bit': '2.48.2-12.22.1',
			'libgobject-2_0-0-debuginfo': '2.48.2-12.22.1',
			'libgobject-2_0-0-debuginfo-32bit': '2.48.2-12.22.1',
			'libgthread-2_0-0': '2.48.2-12.22.1',
			'libgthread-2_0-0-32bit': '2.48.2-12.22.1',
			'libgthread-2_0-0-debuginfo': '2.48.2-12.22.1',
			'libgthread-2_0-0-debuginfo-32bit': '2.48.2-12.22.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

