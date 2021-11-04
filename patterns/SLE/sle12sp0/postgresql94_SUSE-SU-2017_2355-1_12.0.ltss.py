#!/usr/bin/python3
#
# Title:       Important Security Announcement for postgresql94 SUSE-SU-2017:2355-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP0 LTSS
# Source:      Security Announcement Parser v1.3.6
# Modified:    2017 Sep 08
#
##############################################################################
# Copyright (C) 2017 SUSE LLC
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
META_COMPONENT = "postgresql94"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.opensuse.org/opensuse-security-announce/2017-09/msg00012.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'postgresql94'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2017:2355-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 0 ):
		PACKAGES = {
			'postgresql94': '9.4.13-21.5.1',
			'postgresql94-contrib': '9.4.13-21.5.1',
			'postgresql94-contrib-debuginfo': '9.4.13-21.5.1',
			'postgresql94-debuginfo': '9.4.13-21.5.1',
			'postgresql94-debugsource': '9.4.13-21.5.1',
			'postgresql94-docs': '9.4.13-21.5.1',
			'postgresql94-server': '9.4.13-21.5.1',
			'postgresql94-server-debuginfo': '9.4.13-21.5.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

