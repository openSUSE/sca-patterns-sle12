#!/usr/bin/python3
#
# Title:       Important Security Announcement for gstreamer-plugins-bad SUSE-SU-2021:1875-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP5
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
META_COMPONENT = "gstreamer-plugins-bad"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2021-June/008942.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'gstreamer-plugins-bad'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2021:1875-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 5 ):
		PACKAGES = {
			'gstreamer-plugins-bad': '1.8.3-18.3.5',
			'gstreamer-plugins-bad-debuginfo': '1.8.3-18.3.5',
			'gstreamer-plugins-bad-debugsource': '1.8.3-18.3.5',
			'gstreamer-plugins-bad-lang': '1.8.3-18.3.5',
			'libgstadaptivedemux-1_0-0': '1.8.3-18.3.5',
			'libgstadaptivedemux-1_0-0-debuginfo': '1.8.3-18.3.5',
			'libgstbadaudio-1_0-0': '1.8.3-18.3.5',
			'libgstbadaudio-1_0-0-debuginfo': '1.8.3-18.3.5',
			'libgstbadbase-1_0-0': '1.8.3-18.3.5',
			'libgstbadbase-1_0-0-debuginfo': '1.8.3-18.3.5',
			'libgstbadvideo-1_0-0': '1.8.3-18.3.5',
			'libgstbadvideo-1_0-0-debuginfo': '1.8.3-18.3.5',
			'libgstbasecamerabinsrc-1_0-0': '1.8.3-18.3.5',
			'libgstbasecamerabinsrc-1_0-0-debuginfo': '1.8.3-18.3.5',
			'libgstcodecparsers-1_0-0': '1.8.3-18.3.5',
			'libgstcodecparsers-1_0-0-debuginfo': '1.8.3-18.3.5',
			'libgstgl-1_0-0': '1.8.3-18.3.5',
			'libgstgl-1_0-0-debuginfo': '1.8.3-18.3.5',
			'libgstmpegts-1_0-0': '1.8.3-18.3.5',
			'libgstmpegts-1_0-0-debuginfo': '1.8.3-18.3.5',
			'libgstphotography-1_0-0': '1.8.3-18.3.5',
			'libgstphotography-1_0-0-debuginfo': '1.8.3-18.3.5',
			'libgsturidownloader-1_0-0': '1.8.3-18.3.5',
			'libgsturidownloader-1_0-0-debuginfo': '1.8.3-18.3.5',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

