#!/usr/bin/python
#
# Title:       Moderate Security Announcement for postgresql12 SUSE-SU-2020:3343-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP2 LTSS
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
META_COMPONENT = "postgresql12"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-November/007780.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'postgresql12'
MAIN = ''
SEVERITY = 'Moderate'
TAG = 'SUSE-SU-2020:3343-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 2 ):
		PACKAGES = {
			'libecpg6': '12.4-3.5.1',
			'libecpg6-debuginfo': '12.4-3.5.1',
			'libpq5': '12.4-3.5.1',
			'libpq5-32bit': '12.4-3.5.1',
			'libpq5-debuginfo': '12.4-3.5.1',
			'libpq5-debuginfo-32bit': '12.4-3.5.1',
			'postgresql': '12.0.1-4.4.1',
			'postgresql-contrib': '12.0.1-4.4.1',
			'postgresql-docs': '12.0.1-4.4.1',
			'postgresql-plperl': '12.0.1-4.4.1',
			'postgresql-plpython': '12.0.1-4.4.1',
			'postgresql-pltcl': '12.0.1-4.4.1',
			'postgresql-server': '12.0.1-4.4.1',
			'postgresql10': '10.14-4.4.1',
			'postgresql10-contrib': '10.14-4.4.1',
			'postgresql10-contrib-debuginfo': '10.14-4.4.1',
			'postgresql10-debuginfo': '10.14-4.4.1',
			'postgresql10-debugsource': '10.14-4.4.1',
			'postgresql10-docs': '10.14-4.4.1',
			'postgresql10-plperl': '10.14-4.4.1',
			'postgresql10-plperl-debuginfo': '10.14-4.4.1',
			'postgresql10-plpython': '10.14-4.4.1',
			'postgresql10-plpython-debuginfo': '10.14-4.4.1',
			'postgresql10-pltcl': '10.14-4.4.1',
			'postgresql10-pltcl-debuginfo': '10.14-4.4.1',
			'postgresql10-server': '10.14-4.4.1',
			'postgresql10-server-debuginfo': '10.14-4.4.1',
			'postgresql94': '9.4.26-24.3.1',
			'postgresql94-contrib': '9.4.26-24.3.1',
			'postgresql94-contrib-debuginfo': '9.4.26-24.3.1',
			'postgresql94-debuginfo': '9.4.26-24.3.1',
			'postgresql94-debugsource': '9.4.26-24.3.1',
			'postgresql94-docs': '9.4.26-24.3.1',
			'postgresql94-plperl': '9.4.26-24.3.1',
			'postgresql94-plperl-debuginfo': '9.4.26-24.3.1',
			'postgresql94-plpython': '9.4.26-24.3.1',
			'postgresql94-plpython-debuginfo': '9.4.26-24.3.1',
			'postgresql94-pltcl': '9.4.26-24.3.1',
			'postgresql94-pltcl-debuginfo': '9.4.26-24.3.1',
			'postgresql94-server': '9.4.26-24.3.1',
			'postgresql94-server-debuginfo': '9.4.26-24.3.1',
			'postgresql96': '9.6.19-6.4.1',
			'postgresql96-contrib': '9.6.19-6.4.1',
			'postgresql96-contrib-debuginfo': '9.6.19-6.4.1',
			'postgresql96-debuginfo': '9.6.19-6.4.1',
			'postgresql96-debugsource': '9.6.19-6.4.1',
			'postgresql96-docs': '9.6.19-6.4.1',
			'postgresql96-plperl': '9.6.19-6.4.1',
			'postgresql96-plperl-debuginfo': '9.6.19-6.4.1',
			'postgresql96-plpython': '9.6.19-6.4.1',
			'postgresql96-plpython-debuginfo': '9.6.19-6.4.1',
			'postgresql96-pltcl': '9.6.19-6.4.1',
			'postgresql96-pltcl-debuginfo': '9.6.19-6.4.1',
			'postgresql96-server': '9.6.19-6.4.1',
			'postgresql96-server-debuginfo': '9.6.19-6.4.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

