#!/usr/bin/python3
#
# Title:       Important Security Announcement for openldap2 SUSE-SU-2020:1859-1
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
META_COMPONENT = "openldap2"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-July/007077.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'openldap2'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2020:1859-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'libldap-2_4-2': '2.4.41-18.71.2',
			'libldap-2_4-2-32bit': '2.4.41-18.71.2',
			'libldap-2_4-2-debuginfo': '2.4.41-18.71.2',
			'libldap-2_4-2-debuginfo-32bit': '2.4.41-18.71.2',
			'openldap2': '2.4.41-18.71.2',
			'openldap2-back-meta': '2.4.41-18.71.2',
			'openldap2-back-meta-debuginfo': '2.4.41-18.71.2',
			'openldap2-client': '2.4.41-18.71.2',
			'openldap2-client-debuginfo': '2.4.41-18.71.2',
			'openldap2-debuginfo': '2.4.41-18.71.2',
			'openldap2-debugsource': '2.4.41-18.71.2',
			'openldap2-doc': '2.4.41-18.71.2',
			'openldap2-ppolicy-check-password': '1.2-18.71.2',
			'openldap2-ppolicy-check-password-debuginfo': '1.2-18.71.2',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

