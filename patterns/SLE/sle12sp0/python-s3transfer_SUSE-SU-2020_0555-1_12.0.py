#!/usr/bin/python
#
# Title:       Moderate Security Announcement for python-s3transfer SUSE-SU-2020:0555-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP0
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
META_COMPONENT = "python-s3transfer"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-March/006561.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'python-s3transfer'
MAIN = ''
SEVERITY = 'Moderate'
TAG = 'SUSE-SU-2020:0555-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 0 ):
		PACKAGES = {
			'cfn-lint': '0.21.4-2.3.1',
			'python-PyYAML': '5.1.2-26.9.4',
			'python-PyYAML-debuginfo': '5.1.2-26.9.4',
			'python-PyYAML-debugsource': '5.1.2-26.9.4',
			'python-asn1crypto': '0.24.0-2.5.1',
			'python-boto3': '1.9.213-14.9.1',
			'python-botocore': '1.12.213-28.12.1',
			'python-docutils': '0.15.2-3.4.2',
			'python-functools32': '3.2.3.2-2.6.1',
			'python-jsonpatch': '1.1-10.4.1',
			'python-jsonpointer': '1.0-10.3.1',
			'python-jsonschema': '2.6.0-5.3.1',
			'python-packaging': '17.1-2.5.1',
			'python-pyparsing': '2.2.0-7.6.1',
			'python-requests': '2.20.1-8.7.7',
			'python-s3transfer': '0.2.1-8.3.1',
			'python3-PyYAML': '5.1.2-26.9.4',
			'python3-asn1crypto': '0.24.0-2.5.1',
			'python3-aws-sam-translator': '1.11.0-2.3.1',
			'python3-boto3': '1.9.213-14.9.1',
			'python3-botocore': '1.12.213-28.12.1',
			'python3-cfn-lint': '0.21.4-2.3.1',
			'python3-docutils': '0.15.2-3.4.2',
			'python3-jsonpatch': '1.1-10.4.1',
			'python3-jsonpointer': '1.0-10.3.1',
			'python3-jsonschema': '2.6.0-5.3.1',
			'python3-packaging': '17.1-2.5.1',
			'python3-pyparsing': '2.2.0-7.6.1',
			'python3-requests': '2.20.1-8.7.7',
			'python3-s3transfer': '0.2.1-8.3.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

