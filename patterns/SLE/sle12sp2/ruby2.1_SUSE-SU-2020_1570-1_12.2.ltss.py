#!/usr/bin/python
#
# Title:       Important Security Announcement for ruby2.1 SUSE-SU-2020:1570-1
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
META_COMPONENT = "ruby2.1"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-June/006905.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'ruby2.1'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2020:1570-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 2 ):
		PACKAGES = {
			'libruby2_1-2_1': '2.1.9-19.3.2',
			'libruby2_1-2_1-debuginfo': '2.1.9-19.3.2',
			'ruby2.1': '2.1.9-19.3.2',
			'ruby2.1-debuginfo': '2.1.9-19.3.2',
			'ruby2.1-debugsource': '2.1.9-19.3.2',
			'ruby2.1-stdlib': '2.1.9-19.3.2',
			'ruby2.1-stdlib-debuginfo': '2.1.9-19.3.2',
			'yast2-ruby-bindings': '3.1.53-9.8.1',
			'yast2-ruby-bindings-debuginfo': '3.1.53-9.8.1',
			'yast2-ruby-bindings-debugsource': '3.1.53-9.8.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()
