#!/usr/bin/python3
#
# Title:       Important Security Announcement for openldap2 SUSE-SU-2016:0224-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP1
# Source:      Security Announcement Parser v1.3.0
# Modified:    2016 Jan 27
#
##############################################################################
# Copyright (C) 2016 SUSE LLC
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
#   Jason Record (jrecord@suse.com)
#
##############################################################################

import os
import Core
import SUSE

META_CLASS = "Security"
META_CATEGORY = "SLE"
META_COMPONENT = "openldap2"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2016-01/msg00031.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'openldap2'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2016:0224-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 1 ):
		PACKAGES = {
			'libldap-2_4-2': '2.4.41-18.13.1',
			'libldap-2_4-2-32bit': '2.4.41-18.13.1',
			'libldap-2_4-2-debuginfo': '2.4.41-18.13.1',
			'libldap-2_4-2-debuginfo-32bit': '2.4.41-18.13.1',
			'openldap2': '2.4.41-18.13.4',
			'openldap2-back-meta': '2.4.41-18.13.4',
			'openldap2-back-meta-debuginfo': '2.4.41-18.13.4',
			'openldap2-back-perl': '2.4.41-18.13.4',
			'openldap2-back-perl-debuginfo': '2.4.41-18.13.4',
			'openldap2-client': '2.4.41-18.13.1',
			'openldap2-client-debuginfo': '2.4.41-18.13.1',
			'openldap2-client-debugsource': '2.4.41-18.13.1',
			'openldap2-debuginfo': '2.4.41-18.13.4',
			'openldap2-debugsource': '2.4.41-18.13.4',
			'openldap2-devel': '2.4.41-18.13.1',
			'openldap2-devel-static': '2.4.41-18.13.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

