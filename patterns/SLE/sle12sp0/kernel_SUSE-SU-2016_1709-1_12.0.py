#!/usr/bin/python3
#
# Title:       Important Security Announcement for Kernel SUSE-SU-2016:1709-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP0
# Source:      Security Announcement Parser v1.3.1
# Modified:    2016 Jul 05
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
#   Jason Record (jrecord@suse.com)
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
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2016-06/msg00060.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'Kernel'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2016:1709-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 0 ):
		PACKAGES = {
			'kernel-default': '3.12.59-60.45.2',
			'kernel-default-base': '3.12.59-60.45.2',
			'kernel-default-base-debuginfo': '3.12.59-60.45.2',
			'kernel-default-debuginfo': '3.12.59-60.45.2',
			'kernel-default-debugsource': '3.12.59-60.45.2',
			'kernel-default-devel': '3.12.59-60.45.2',
			'kernel-default-extra': '3.12.59-60.45.2',
			'kernel-default-extra-debuginfo': '3.12.59-60.45.2',
			'kernel-default-man': '3.12.59-60.45.2',
			'kernel-devel': '3.12.59-60.45.1',
			'kernel-docs': '3.12.59-60.45.4',
			'kernel-ec2': '3.12.59-60.45.2',
			'kernel-ec2-debuginfo': '3.12.59-60.45.2',
			'kernel-ec2-debugsource': '3.12.59-60.45.2',
			'kernel-ec2-devel': '3.12.59-60.45.2',
			'kernel-ec2-extra': '3.12.59-60.45.2',
			'kernel-ec2-extra-debuginfo': '3.12.59-60.45.2',
			'kernel-macros': '3.12.59-60.45.1',
			'kernel-obs-build': '3.12.59-60.45.3',
			'kernel-obs-build-debugsource': '3.12.59-60.45.3',
			'kernel-source': '3.12.59-60.45.1',
			'kernel-syms': '3.12.59-60.45.1',
			'kernel-xen': '3.12.59-60.45.2',
			'kernel-xen-base': '3.12.59-60.45.2',
			'kernel-xen-base-debuginfo': '3.12.59-60.45.2',
			'kernel-xen-debuginfo': '3.12.59-60.45.2',
			'kernel-xen-debugsource': '3.12.59-60.45.2',
			'kernel-xen-devel': '3.12.59-60.45.2',
			'kgraft-patch-3_12_59-60_45-default': '1-2.3',
			'kgraft-patch-3_12_59-60_45-xen': '1-2.3',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

