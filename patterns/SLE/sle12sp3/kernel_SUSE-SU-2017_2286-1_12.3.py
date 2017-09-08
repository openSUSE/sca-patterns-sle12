#!/usr/bin/python
#
# Title:       Important Security Announcement for Kernel SUSE-SU-2017:2286-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP3
# Source:      Security Announcement Parser v1.3.6
# Modified:    2017 Sep 08
#
##############################################################################
# Copyright (C) 2017 SUSE LLC
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
OTHER_LINKS = "META_LINK_Security=https://lists.opensuse.org/opensuse-security-announce/2017-08/msg00071.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'Kernel'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2017:2286-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'cluster-md-kmp-default': '4.4.82-6.3.1',
			'cluster-md-kmp-default-debuginfo': '4.4.82-6.3.1',
			'dlm-kmp-default': '4.4.82-6.3.1',
			'dlm-kmp-default-debuginfo': '4.4.82-6.3.1',
			'gfs2-kmp-default': '4.4.82-6.3.1',
			'gfs2-kmp-default-debuginfo': '4.4.82-6.3.1',
			'kernel-default': '4.4.82-6.3.1',
			'kernel-default-base': '4.4.82-6.3.1',
			'kernel-default-base-debuginfo': '4.4.82-6.3.1',
			'kernel-default-debuginfo': '4.4.82-6.3.1',
			'kernel-default-debugsource': '4.4.82-6.3.1',
			'kernel-default-devel': '4.4.82-6.3.1',
			'kernel-default-extra': '4.4.82-6.3.1',
			'kernel-default-extra-debuginfo': '4.4.82-6.3.1',
			'kernel-default-man': '4.4.82-6.3.1',
			'kernel-devel': '4.4.82-6.3.1',
			'kernel-docs': '4.4.82-6.3.5',
			'kernel-macros': '4.4.82-6.3.1',
			'kernel-obs-build': '4.4.82-6.3.3',
			'kernel-obs-build-debugsource': '4.4.82-6.3.3',
			'kernel-source': '4.4.82-6.3.1',
			'kernel-syms': '4.4.82-6.3.1',
			'kgraft-patch-4_4_82-6_3-default': '1-2.1',
			'kgraft-patch-4_4_82-6_3-default-debuginfo': '1-2.1',
			'ocfs2-kmp-default': '4.4.82-6.3.1',
			'ocfs2-kmp-default-debuginfo': '4.4.82-6.3.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

