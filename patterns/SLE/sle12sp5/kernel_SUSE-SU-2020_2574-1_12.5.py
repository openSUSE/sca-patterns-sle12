#!/usr/bin/python3
#
# Title:       Important Security Announcement for Kernel SUSE-SU-2020:2574-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP5
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
META_COMPONENT = "Kernel"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-September/007382.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'Kernel'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2020:2574-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 5 ):
		PACKAGES = {
			'cluster-md-kmp-default': '4.12.14-122.37.1',
			'cluster-md-kmp-default-debuginfo': '4.12.14-122.37.1',
			'dlm-kmp-default': '4.12.14-122.37.1',
			'dlm-kmp-default-debuginfo': '4.12.14-122.37.1',
			'gfs2-kmp-default': '4.12.14-122.37.1',
			'gfs2-kmp-default-debuginfo': '4.12.14-122.37.1',
			'kernel-default': '4.12.14-122.37.1',
			'kernel-default-base': '4.12.14-122.37.1',
			'kernel-default-base-debuginfo': '4.12.14-122.37.1',
			'kernel-default-debuginfo': '4.12.14-122.37.1',
			'kernel-default-debugsource': '4.12.14-122.37.1',
			'kernel-default-devel': '4.12.14-122.37.1',
			'kernel-default-devel-debuginfo': '4.12.14-122.37.1',
			'kernel-default-extra': '4.12.14-122.37.1',
			'kernel-default-extra-debuginfo': '4.12.14-122.37.1',
			'kernel-default-kgraft': '4.12.14-122.37.1',
			'kernel-default-kgraft-devel': '4.12.14-122.37.1',
			'kernel-default-man': '4.12.14-122.37.1',
			'kernel-devel': '4.12.14-122.37.1',
			'kernel-docs': '4.12.14-122.37.1',
			'kernel-macros': '4.12.14-122.37.1',
			'kernel-obs-build': '4.12.14-122.37.1',
			'kernel-obs-build-debugsource': '4.12.14-122.37.1',
			'kernel-source': '4.12.14-122.37.1',
			'kernel-syms': '4.12.14-122.37.1',
			'kgraft-patch-4_12_14-122_37-default': '1-8.5.1',
			'ocfs2-kmp-default': '4.12.14-122.37.1',
			'ocfs2-kmp-default-debuginfo': '4.12.14-122.37.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

