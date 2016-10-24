#!/usr/bin/python
#
# Title:       Important Security Announcement for systemd SUSE-SU-2016:2476-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP1
# Source:      Security Announcement Parser v1.3.2
# Modified:    2016 Oct 24
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
#   Jason Record (jason.record@suse.com)
#
##############################################################################

import os
import Core
import SUSE

META_CLASS = "Security"
META_CATEGORY = "SLE"
META_COMPONENT = "systemd"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2016-10/msg00016.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'systemd'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2016:2476-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 1 ):
		PACKAGES = {
			'libgudev-1_0-0': '210-114.1',
			'libgudev-1_0-0-32bit': '210-114.1',
			'libgudev-1_0-0-debuginfo': '210-114.1',
			'libgudev-1_0-0-debuginfo-32bit': '210-114.1',
			'libgudev-1_0-devel': '210-114.1',
			'libudev-devel': '210-114.1',
			'libudev1': '210-114.1',
			'libudev1-32bit': '210-114.1',
			'libudev1-debuginfo': '210-114.1',
			'libudev1-debuginfo-32bit': '210-114.1',
			'systemd': '210-114.1',
			'systemd-32bit': '210-114.1',
			'systemd-bash-completion': '210-114.1',
			'systemd-debuginfo': '210-114.1',
			'systemd-debuginfo-32bit': '210-114.1',
			'systemd-debugsource': '210-114.1',
			'systemd-devel': '210-114.1',
			'systemd-sysvinit': '210-114.1',
			'typelib-1_0-GUdev-1_0': '210-114.1',
			'udev': '210-114.1',
			'udev-debuginfo': '210-114.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

