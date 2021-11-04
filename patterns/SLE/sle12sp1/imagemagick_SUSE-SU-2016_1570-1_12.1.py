#!/usr/bin/python3
#
# Title:       Important Security Announcement for ImageMagick SUSE-SU-2016:1570-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP1
# Source:      Security Announcement Parser v1.3.1
# Modified:    2016 Jun 15
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
META_COMPONENT = "ImageMagick"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2016-06/msg00021.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'ImageMagick'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2016:1570-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 1 ):
		PACKAGES = {
			'ImageMagick': '6.8.8.1-25.1',
			'ImageMagick-debuginfo': '6.8.8.1-25.1',
			'ImageMagick-debugsource': '6.8.8.1-25.1',
			'ImageMagick-devel': '6.8.8.1-25.1',
			'libMagick++-6_Q16-3': '6.8.8.1-25.1',
			'libMagick++-6_Q16-3-debuginfo': '6.8.8.1-25.1',
			'libMagick++-devel': '6.8.8.1-25.1',
			'libMagickCore-6_Q16-1': '6.8.8.1-25.1',
			'libMagickCore-6_Q16-1-32bit': '6.8.8.1-25.1',
			'libMagickCore-6_Q16-1-debuginfo': '6.8.8.1-25.1',
			'libMagickCore-6_Q16-1-debuginfo-32bit': '6.8.8.1-25.1',
			'libMagickWand-6_Q16-1': '6.8.8.1-25.1',
			'libMagickWand-6_Q16-1-debuginfo': '6.8.8.1-25.1',
			'perl-PerlMagick': '6.8.8.1-25.1',
			'perl-PerlMagick-debuginfo': '6.8.8.1-25.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

