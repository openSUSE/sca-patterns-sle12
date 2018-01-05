#!/usr/bin/python
#
# Title:       Important Security Announcement for evince SUSE-SU-2017:3428-1
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
META_COMPONENT = "evince"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.opensuse.org/opensuse-security-announce/2017-12/msg00089.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'evince'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2017:3428-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'evince': '3.20.2-6.19.15',
			'evince-browser-plugin': '3.20.2-6.19.15',
			'evince-browser-plugin-debuginfo': '3.20.2-6.19.15',
			'evince-debuginfo': '3.20.2-6.19.15',
			'evince-debugsource': '3.20.2-6.19.15',
			'evince-devel': '3.20.2-6.19.15',
			'evince-lang': '3.20.2-6.19.15',
			'evince-plugin-djvudocument': '3.20.2-6.19.15',
			'evince-plugin-djvudocument-debuginfo': '3.20.2-6.19.15',
			'evince-plugin-dvidocument': '3.20.2-6.19.15',
			'evince-plugin-dvidocument-debuginfo': '3.20.2-6.19.15',
			'evince-plugin-pdfdocument': '3.20.2-6.19.15',
			'evince-plugin-pdfdocument-debuginfo': '3.20.2-6.19.15',
			'evince-plugin-psdocument': '3.20.2-6.19.15',
			'evince-plugin-psdocument-debuginfo': '3.20.2-6.19.15',
			'evince-plugin-tiffdocument': '3.20.2-6.19.15',
			'evince-plugin-tiffdocument-debuginfo': '3.20.2-6.19.15',
			'evince-plugin-xpsdocument': '3.20.2-6.19.15',
			'evince-plugin-xpsdocument-debuginfo': '3.20.2-6.19.15',
			'libevdocument3-4': '3.20.2-6.19.15',
			'libevdocument3-4-debuginfo': '3.20.2-6.19.15',
			'libevview3-3': '3.20.2-6.19.15',
			'libevview3-3-debuginfo': '3.20.2-6.19.15',
			'nautilus-evince': '3.20.2-6.19.15',
			'nautilus-evince-debuginfo': '3.20.2-6.19.15',
			'typelib-1_0-EvinceDocument-3_0': '3.20.2-6.19.15',
			'typelib-1_0-EvinceView-3_0': '3.20.2-6.19.15',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

