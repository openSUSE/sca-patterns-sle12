#!/usr/bin/python3
#
# Title:       Important Security Announcement for openssl SUSE-SU-2022:0854-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP3 LTSS
# Source:      Security Announcement Parser v1.6.4
# Modified:    2022 May 05
#
##############################################################################
# Copyright (C) 2022 SUSE LLC
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
META_COMPONENT = "openssl"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2022-March/010449.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'openssl'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2022:0854-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'libopenssl-devel': '1.0.2j-60.75.1',
			'libopenssl1_0_0': '1.0.2j-60.75.1',
			'libopenssl1_0_0-32bit': '1.0.2j-60.75.1',
			'libopenssl1_0_0-debuginfo': '1.0.2j-60.75.1',
			'libopenssl1_0_0-debuginfo-32bit': '1.0.2j-60.75.1',
			'libopenssl1_0_0-hmac': '1.0.2j-60.75.1',
			'libopenssl1_0_0-hmac-32bit': '1.0.2j-60.75.1',
			'openssl': '1.0.2j-60.75.1',
			'openssl-debuginfo': '1.0.2j-60.75.1',
			'openssl-debugsource': '1.0.2j-60.75.1',
			'openssl-doc': '1.0.2j-60.75.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

