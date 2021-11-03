#!/usr/bin/python3
#
# Title:       Important Security Announcement for postgresql13 SUSE-SU-2021:0217-1
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
META_COMPONENT = "postgresql13"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2021-January/008245.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'postgresql13'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2021:0217-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 5 ):
		PACKAGES = {
			'libecpg6': '13.1-3.3.1',
			'libecpg6-debuginfo': '13.1-3.3.1',
			'libpq5': '13.1-3.3.1',
			'libpq5-32bit': '13.1-3.3.1',
			'libpq5-debuginfo': '13.1-3.3.1',
			'libpq5-debuginfo-32bit': '13.1-3.3.1',
			'postgresql': '13-4.7.1',
			'postgresql-contrib': '13-4.7.1',
			'postgresql-docs': '13-4.7.1',
			'postgresql-plperl': '13-4.7.1',
			'postgresql-plpython': '13-4.7.1',
			'postgresql-pltcl': '13-4.7.1',
			'postgresql-server': '13-4.7.1',
			'postgresql12': '12.5-3.12.3',
			'postgresql12-contrib': '12.5-3.12.3',
			'postgresql12-contrib-debuginfo': '12.5-3.12.3',
			'postgresql12-debuginfo': '12.5-3.12.3',
			'postgresql12-debugsource': '12.5-3.12.3',
			'postgresql12-docs': '12.5-3.12.3',
			'postgresql12-plperl': '12.5-3.12.3',
			'postgresql12-plperl-debuginfo': '12.5-3.12.3',
			'postgresql12-plpython': '12.5-3.12.3',
			'postgresql12-plpython-debuginfo': '12.5-3.12.3',
			'postgresql12-pltcl': '12.5-3.12.3',
			'postgresql12-pltcl-debuginfo': '12.5-3.12.3',
			'postgresql12-server': '12.5-3.12.3',
			'postgresql12-server-debuginfo': '12.5-3.12.3',
			'postgresql13': '13.1-3.3.1',
			'postgresql13-contrib': '13.1-3.3.1',
			'postgresql13-contrib-debuginfo': '13.1-3.3.1',
			'postgresql13-debuginfo': '13.1-3.3.1',
			'postgresql13-debugsource': '13.1-3.3.1',
			'postgresql13-docs': '13.1-3.3.1',
			'postgresql13-plperl': '13.1-3.3.1',
			'postgresql13-plperl-debuginfo': '13.1-3.3.1',
			'postgresql13-plpython': '13.1-3.3.1',
			'postgresql13-plpython-debuginfo': '13.1-3.3.1',
			'postgresql13-pltcl': '13.1-3.3.1',
			'postgresql13-pltcl-debuginfo': '13.1-3.3.1',
			'postgresql13-server': '13.1-3.3.1',
			'postgresql13-server-debuginfo': '13.1-3.3.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

