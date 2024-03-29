#!/usr/bin/python3
#
# Title:       Important Security Announcement for Kernel SUSE-SU-2016:2912-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP1
# Source:      Security Announcement Parser v1.3.6
# Modified:    2016 Nov 28
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
META_COMPONENT = "Kernel"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2016-11/msg00041.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'Kernel'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2016:2912-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 1 ):
		PACKAGES = {
			'kernel-default': '3.12.67-60.64.18.1',
			'kernel-default-base': '3.12.67-60.64.18.1',
			'kernel-default-base-debuginfo': '3.12.67-60.64.18.1',
			'kernel-default-debuginfo': '3.12.67-60.64.18.1',
			'kernel-default-debugsource': '3.12.67-60.64.18.1',
			'kernel-default-devel': '3.12.67-60.64.18.1',
			'kernel-default-extra': '3.12.67-60.64.18.1',
			'kernel-default-extra-debuginfo': '3.12.67-60.64.18.1',
			'kernel-default-man': '3.12.67-60.64.18.1',
			'kernel-devel': '3.12.67-60.64.18.1',
			'kernel-docs': '3.12.67-60.64.18.3',
			'kernel-macros': '3.12.67-60.64.18.1',
			'kernel-obs-build': '3.12.67-60.64.18.1',
			'kernel-obs-build-debugsource': '3.12.67-60.64.18.1',
			'kernel-source': '3.12.67-60.64.18.1',
			'kernel-syms': '3.12.67-60.64.18.1',
			'kernel-xen': '3.12.67-60.64.18.1',
			'kernel-xen-base': '3.12.67-60.64.18.1',
			'kernel-xen-base-debuginfo': '3.12.67-60.64.18.1',
			'kernel-xen-debuginfo': '3.12.67-60.64.18.1',
			'kernel-xen-debugsource': '3.12.67-60.64.18.1',
			'kernel-xen-devel': '3.12.67-60.64.18.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

