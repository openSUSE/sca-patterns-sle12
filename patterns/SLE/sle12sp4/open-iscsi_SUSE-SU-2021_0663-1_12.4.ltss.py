#!/usr/bin/python
#
# Title:       Important Security Announcement for open-iscsi SUSE-SU-2021:0663-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP4 LTSS
# Source:      Security Announcement Parser v1.6.1
# Modified:    2021 Mar 31
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
META_COMPONENT = "open-iscsi"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2021-March/008407.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'open-iscsi'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2021:0663-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 4 ):
		PACKAGES = {
			'iscsiuio': '0.7.8.2-12.27.2',
			'iscsiuio-debuginfo': '0.7.8.2-12.27.2',
			'libopeniscsiusr0_2_0': '2.0.876-12.27.2',
			'libopeniscsiusr0_2_0-debuginfo': '2.0.876-12.27.2',
			'open-iscsi': '2.0.876-12.27.2',
			'open-iscsi-debuginfo': '2.0.876-12.27.2',
			'open-iscsi-debugsource': '2.0.876-12.27.2',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

