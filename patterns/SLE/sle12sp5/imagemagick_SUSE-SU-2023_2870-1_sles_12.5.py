#!/usr/bin/python3
#
# Title:       Moderate Security Announcement for ImageMagick SUSE-SU-2023:2870-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP5
# URL:         https://lists.suse.com/pipermail/sle-security-updates/2023-July/015518.html
# Source:      Security Announcement Generator (sagen.py) v2.0.13
# Modified:    2023 Aug 31
#
##############################################################################
# Copyright (C) 2023 SUSE LLC
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
#   Jason Record <jason.record@suse.com>
#
##############################################################################

import os
import Core
import SUSE

meta_class = "Security"
meta_category = "SLE"
meta_component = "ImageMagick"
pattern_filename = os.path.basename(__file__)
primary_link = "META_LINK_Security"
overall = Core.TEMP
overall_info = "NOT SET"
other_links = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2023-July/015518.html"
Core.init(meta_class, meta_category, meta_component, pattern_filename, primary_link, overall, overall_info, other_links)

def main():
	ltss = False
	name = 'ImageMagick'
	main = ''
	severity = 'Moderate'
	tag = 'SUSE-SU-2023:2870-1'
	packages = {}
	server = SUSE.getHostInfo()

	if ( server['DistroVersion'] == 12):
		if ( server['DistroPatchLevel'] == 5 ):
			packages = {
				'ImageMagick-config-6-SUSE': '6.8.8.1-71.192.1',
				'ImageMagick-config-6-upstream': '6.8.8.1-71.192.1',
				'ImageMagick-debuginfo': '6.8.8.1-71.192.1',
				'ImageMagick-debugsource': '6.8.8.1-71.192.1',
				'libMagickCore-6_Q16-1': '6.8.8.1-71.192.1',
				'libMagickCore-6_Q16-1-debuginfo': '6.8.8.1-71.192.1',
				'libMagickWand-6_Q16-1': '6.8.8.1-71.192.1',
				'libMagickWand-6_Q16-1-debuginfo': '6.8.8.1-71.192.1',
			}
			SUSE.securityAnnouncementPackageCheck(name, main, ltss, severity, tag, packages)
		else:
			Core.updateStatus(Core.ERROR, "ERROR: " + name + " Security Announcement: Outside the service pack scope")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + name + " Security Announcement: Outside the distribution scope")

	Core.printPatternResults()

if __name__ == "__main__":
	main()

