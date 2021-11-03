#!/usr/bin/python3
#
# Title:       Important Security Announcement for git SUSE-SU-2020:0992-1
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
META_COMPONENT = "git"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-April/006709.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'git'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2020:0992-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'git-core': '2.26.0-27.27.1',
			'git-core-debuginfo': '2.26.0-27.27.1',
			'git-debugsource': '2.26.0-27.27.1',
			'libpcre2-16-0': '10.34-1.3.1',
			'libpcre2-16-0-debuginfo': '10.34-1.3.1',
			'libpcre2-32-0': '10.34-1.3.1',
			'libpcre2-32-0-debuginfo': '10.34-1.3.1',
			'libpcre2-8-0': '10.34-1.3.1',
			'libpcre2-8-0-debuginfo': '10.34-1.3.1',
			'libpcre2-posix2': '10.34-1.3.1',
			'libpcre2-posix2-debuginfo': '10.34-1.3.1',
			'perl-CGI': '4.38-1.3.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

