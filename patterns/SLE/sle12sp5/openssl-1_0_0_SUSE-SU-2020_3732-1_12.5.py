#!/usr/bin/python3
#
# Title:       Important Security Announcement for openssl-1_0_0 SUSE-SU-2020:3732-1
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
META_COMPONENT = "openssl-1_0_0"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-December/007953.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'openssl-1_0_0'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2020:3732-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 5 ):
		PACKAGES = {
			'libopenssl-1_0_0-devel': '1.0.2p-3.30.1',
			'libopenssl1_0_0': '1.0.2p-3.30.1',
			'libopenssl1_0_0-32bit': '1.0.2p-3.30.1',
			'libopenssl1_0_0-debuginfo': '1.0.2p-3.30.1',
			'libopenssl1_0_0-debuginfo-32bit': '1.0.2p-3.30.1',
			'libopenssl1_0_0-hmac': '1.0.2p-3.30.1',
			'libopenssl1_0_0-hmac-32bit': '1.0.2p-3.30.1',
			'openssl-1_0_0': '1.0.2p-3.30.1',
			'openssl-1_0_0-debuginfo': '1.0.2p-3.30.1',
			'openssl-1_0_0-debugsource': '1.0.2p-3.30.1',
			'openssl-1_0_0-doc': '1.0.2p-3.30.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

