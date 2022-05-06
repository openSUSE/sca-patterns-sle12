#!/usr/bin/python3
#
# Title:       Important Security Announcement for kgraft-patch SUSE-SU-2022:0653-1
# Description: Security fixes for SUSE Linux Kernel Live Patch 12 SP3 LTSS
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
META_COMPONENT = "kgraft-patch"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2022-March/010322.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'kgraft-patch'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2022:0653-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'cyrus-sasl': '2.1.26-8.17.1',
			'cyrus-sasl-32bit': '2.1.26-8.17.1',
			'cyrus-sasl-crammd5': '2.1.26-8.17.1',
			'cyrus-sasl-crammd5-32bit': '2.1.26-8.17.1',
			'cyrus-sasl-crammd5-debuginfo': '2.1.26-8.17.1',
			'cyrus-sasl-crammd5-debuginfo-32bit': '2.1.26-8.17.1',
			'cyrus-sasl-debuginfo': '2.1.26-8.17.1',
			'cyrus-sasl-debuginfo-32bit': '2.1.26-8.17.1',
			'cyrus-sasl-debugsource': '2.1.26-8.17.1',
			'cyrus-sasl-digestmd5': '2.1.26-8.17.1',
			'cyrus-sasl-digestmd5-debuginfo': '2.1.26-8.17.1',
			'cyrus-sasl-gssapi': '2.1.26-8.17.1',
			'cyrus-sasl-gssapi-32bit': '2.1.26-8.17.1',
			'cyrus-sasl-gssapi-debuginfo': '2.1.26-8.17.1',
			'cyrus-sasl-gssapi-debuginfo-32bit': '2.1.26-8.17.1',
			'cyrus-sasl-otp': '2.1.26-8.17.1',
			'cyrus-sasl-otp-32bit': '2.1.26-8.17.1',
			'cyrus-sasl-otp-debuginfo': '2.1.26-8.17.1',
			'cyrus-sasl-otp-debuginfo-32bit': '2.1.26-8.17.1',
			'cyrus-sasl-plain': '2.1.26-8.17.1',
			'cyrus-sasl-plain-32bit': '2.1.26-8.17.1',
			'cyrus-sasl-plain-debuginfo': '2.1.26-8.17.1',
			'cyrus-sasl-plain-debuginfo-32bit': '2.1.26-8.17.1',
			'libsasl2-3': '2.1.26-8.17.1',
			'libsasl2-3-32bit': '2.1.26-8.17.1',
			'libsasl2-3-debuginfo': '2.1.26-8.17.1',
			'libsasl2-3-debuginfo-32bit': '2.1.26-8.17.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

