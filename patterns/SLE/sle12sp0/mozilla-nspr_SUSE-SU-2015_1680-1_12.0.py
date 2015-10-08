#!/usr/bin/python
#
# Title:       Important Security Announcement for mozilla-nspr SUSE-SU-2015:1680-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP0
# Source:      Security Announcement Parser v1.3.0
# Modified:    2015 Oct 08
#
##############################################################################
# Copyright (C) 2015 SUSE LLC
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
META_COMPONENT = "mozilla-nspr"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2015-10/msg00004.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'mozilla-nspr'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2015:1680-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 0 ):
		PACKAGES = {
			'MozillaFirefox': '38.3.0esr-48.1',
			'MozillaFirefox-debuginfo': '38.3.0esr-48.1',
			'MozillaFirefox-debugsource': '38.3.0esr-48.1',
			'MozillaFirefox-devel': '38.3.0esr-48.1',
			'MozillaFirefox-translations': '38.3.0esr-48.1',
			'mozilla-nspr': '4.10.9-6.1',
			'mozilla-nspr-32bit': '4.10.9-6.1',
			'mozilla-nspr-debuginfo': '4.10.9-6.1',
			'mozilla-nspr-debuginfo-32bit': '4.10.9-6.1',
			'mozilla-nspr-debugsource': '4.10.9-6.1',
			'mozilla-nspr-devel': '4.10.9-6.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

