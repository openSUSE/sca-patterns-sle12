#!/usr/bin/python3
#
# Title:       Important Security Announcement for ceph SUSE-SU-2020:0962-1
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
META_COMPONENT = "ceph"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-April/006691.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'ceph'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2020:0962-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 5 ):
		PACKAGES = {
			'ceph-common': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'ceph-common-debuginfo': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'ceph-debugsource': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'libcephfs-devel': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'libcephfs2': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'libcephfs2-debuginfo': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'librados-devel': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'librados-devel-debuginfo': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'librados2': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'librados2-debuginfo': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'libradosstriper1': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'libradosstriper1-debuginfo': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'librbd-devel': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'librbd1': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'librbd1-debuginfo': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'librgw2': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'librgw2-debuginfo': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'python-cephfs': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'python-cephfs-debuginfo': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'python-rados': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'python-rados-debuginfo': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'python-rbd': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'python-rbd-debuginfo': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'python-rgw': '12.2.12+git.1585658687.363df3a813-2.42.4',
			'python-rgw-debuginfo': '12.2.12+git.1585658687.363df3a813-2.42.4',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

