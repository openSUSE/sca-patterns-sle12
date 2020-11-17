#!/usr/bin/python
#
# Title:       Moderate Security Announcement for Mesa SUSE-SU-2020:0145-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP4
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
META_COMPONENT = "Mesa"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-January/006389.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'Mesa'
MAIN = ''
SEVERITY = 'Moderate'
TAG = 'SUSE-SU-2020:0145-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 4 ):
		PACKAGES = {
			'Mesa': '18.0.2-8.3.2',
			'Mesa-32bit': '18.0.2-8.3.2',
			'Mesa-debugsource': '18.0.2-8.3.2',
			'Mesa-devel': '18.0.2-8.3.2',
			'Mesa-dri': '18.0.2-8.3.2',
			'Mesa-dri-32bit': '18.0.2-8.3.2',
			'Mesa-dri-debuginfo': '18.0.2-8.3.2',
			'Mesa-dri-debuginfo-32bit': '18.0.2-8.3.2',
			'Mesa-dri-devel': '18.0.2-8.3.2',
			'Mesa-drivers-debugsource': '18.0.2-8.3.2',
			'Mesa-libEGL-devel': '18.0.2-8.3.2',
			'Mesa-libEGL1': '18.0.2-8.3.2',
			'Mesa-libEGL1-32bit': '18.0.2-8.3.2',
			'Mesa-libEGL1-debuginfo': '18.0.2-8.3.2',
			'Mesa-libEGL1-debuginfo-32bit': '18.0.2-8.3.2',
			'Mesa-libGL-devel': '18.0.2-8.3.2',
			'Mesa-libGL1': '18.0.2-8.3.2',
			'Mesa-libGL1-32bit': '18.0.2-8.3.2',
			'Mesa-libGL1-debuginfo': '18.0.2-8.3.2',
			'Mesa-libGL1-debuginfo-32bit': '18.0.2-8.3.2',
			'Mesa-libGLESv1_CM-devel': '18.0.2-8.3.2',
			'Mesa-libGLESv1_CM1': '18.0.2-8.3.2',
			'Mesa-libGLESv1_CM1-debuginfo': '18.0.2-8.3.2',
			'Mesa-libGLESv2-2': '18.0.2-8.3.2',
			'Mesa-libGLESv2-2-32bit': '18.0.2-8.3.2',
			'Mesa-libGLESv2-2-debuginfo': '18.0.2-8.3.2',
			'Mesa-libGLESv2-2-debuginfo-32bit': '18.0.2-8.3.2',
			'Mesa-libGLESv2-devel': '18.0.2-8.3.2',
			'Mesa-libGLESv3-devel': '18.0.2-8.3.2',
			'Mesa-libglapi-devel': '18.0.2-8.3.2',
			'Mesa-libglapi0': '18.0.2-8.3.2',
			'Mesa-libglapi0-32bit': '18.0.2-8.3.2',
			'Mesa-libglapi0-debuginfo': '18.0.2-8.3.2',
			'Mesa-libglapi0-debuginfo-32bit': '18.0.2-8.3.2',
			'libOSMesa-devel': '18.0.2-8.3.2',
			'libOSMesa8': '18.0.2-8.3.2',
			'libOSMesa8-32bit': '18.0.2-8.3.2',
			'libOSMesa8-debuginfo': '18.0.2-8.3.2',
			'libOSMesa8-debuginfo-32bit': '18.0.2-8.3.2',
			'libgbm-devel': '18.0.2-8.3.2',
			'libgbm1': '18.0.2-8.3.2',
			'libgbm1-32bit': '18.0.2-8.3.2',
			'libgbm1-debuginfo': '18.0.2-8.3.2',
			'libgbm1-debuginfo-32bit': '18.0.2-8.3.2',
			'libxatracker-devel': '1.0.0-8.3.2',
			'libxatracker2': '1.0.0-8.3.2',
			'libxatracker2-debuginfo': '1.0.0-8.3.2',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

