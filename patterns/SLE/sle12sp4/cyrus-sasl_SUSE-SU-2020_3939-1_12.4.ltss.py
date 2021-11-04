#!/usr/bin/python3
#
# Title:       Important Security Announcement for cyrus-sasl SUSE-SU-2020:3939-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP4 LTSS
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
META_COMPONENT = "cyrus-sasl"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-December/008123.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'cyrus-sasl'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2020:3939-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 4 ):
		PACKAGES = {
			'cyrus-sasl': '2.1.26-8.13.1',
			'cyrus-sasl-32bit': '2.1.26-8.13.1',
			'cyrus-sasl-crammd5': '2.1.26-8.13.1',
			'cyrus-sasl-crammd5-32bit': '2.1.26-8.13.1',
			'cyrus-sasl-crammd5-debuginfo': '2.1.26-8.13.1',
			'cyrus-sasl-crammd5-debuginfo-32bit': '2.1.26-8.13.1',
			'cyrus-sasl-debuginfo': '2.1.26-8.13.1',
			'cyrus-sasl-debuginfo-32bit': '2.1.26-8.13.1',
			'cyrus-sasl-debugsource': '2.1.26-8.13.1',
			'cyrus-sasl-digestmd5': '2.1.26-8.13.1',
			'cyrus-sasl-digestmd5-debuginfo': '2.1.26-8.13.1',
			'cyrus-sasl-gssapi': '2.1.26-8.13.1',
			'cyrus-sasl-gssapi-32bit': '2.1.26-8.13.1',
			'cyrus-sasl-gssapi-debuginfo': '2.1.26-8.13.1',
			'cyrus-sasl-gssapi-debuginfo-32bit': '2.1.26-8.13.1',
			'cyrus-sasl-otp': '2.1.26-8.13.1',
			'cyrus-sasl-otp-32bit': '2.1.26-8.13.1',
			'cyrus-sasl-otp-debuginfo': '2.1.26-8.13.1',
			'cyrus-sasl-otp-debuginfo-32bit': '2.1.26-8.13.1',
			'cyrus-sasl-plain': '2.1.26-8.13.1',
			'cyrus-sasl-plain-32bit': '2.1.26-8.13.1',
			'cyrus-sasl-plain-debuginfo': '2.1.26-8.13.1',
			'cyrus-sasl-plain-debuginfo-32bit': '2.1.26-8.13.1',
			'libsasl2-3': '2.1.26-8.13.1',
			'libsasl2-3-32bit': '2.1.26-8.13.1',
			'libsasl2-3-debuginfo': '2.1.26-8.13.1',
			'libsasl2-3-debuginfo-32bit': '2.1.26-8.13.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

