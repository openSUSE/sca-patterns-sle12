#!/usr/bin/python
#
# Title:       Important Security Announcement for mozilla-nss SUSE-SU-2016:3014-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP1
# Source:      Security Announcement Parser v1.3.6
# Modified:    2016 Dec 14
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
META_COMPONENT = "mozilla-nss"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2016-12/msg00011.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'mozilla-nss'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2016:3014-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 1 ):
		PACKAGES = {
			'MozillaFirefox': '45.5.0esr-88.1',
			'MozillaFirefox-debuginfo': '45.5.0esr-88.1',
			'MozillaFirefox-debugsource': '45.5.0esr-88.1',
			'MozillaFirefox-devel': '45.5.0esr-88.1',
			'MozillaFirefox-translations': '45.5.0esr-88.1',
			'libfreebl3': '3.21.3-50.1',
			'libfreebl3-32bit': '3.21.3-50.1',
			'libfreebl3-debuginfo': '3.21.3-50.1',
			'libfreebl3-debuginfo-32bit': '3.21.3-50.1',
			'libfreebl3-hmac': '3.21.3-50.1',
			'libfreebl3-hmac-32bit': '3.21.3-50.1',
			'libsoftokn3': '3.21.3-50.1',
			'libsoftokn3-32bit': '3.21.3-50.1',
			'libsoftokn3-debuginfo': '3.21.3-50.1',
			'libsoftokn3-debuginfo-32bit': '3.21.3-50.1',
			'libsoftokn3-hmac': '3.21.3-50.1',
			'libsoftokn3-hmac-32bit': '3.21.3-50.1',
			'mozilla-nss': '3.21.3-50.1',
			'mozilla-nss-32bit': '3.21.3-50.1',
			'mozilla-nss-certs': '3.21.3-50.1',
			'mozilla-nss-certs-32bit': '3.21.3-50.1',
			'mozilla-nss-certs-debuginfo': '3.21.3-50.1',
			'mozilla-nss-certs-debuginfo-32bit': '3.21.3-50.1',
			'mozilla-nss-debuginfo': '3.21.3-50.1',
			'mozilla-nss-debuginfo-32bit': '3.21.3-50.1',
			'mozilla-nss-debugsource': '3.21.3-50.1',
			'mozilla-nss-devel': '3.21.3-50.1',
			'mozilla-nss-sysinit': '3.21.3-50.1',
			'mozilla-nss-sysinit-32bit': '3.21.3-50.1',
			'mozilla-nss-sysinit-debuginfo': '3.21.3-50.1',
			'mozilla-nss-sysinit-debuginfo-32bit': '3.21.3-50.1',
			'mozilla-nss-tools': '3.21.3-50.1',
			'mozilla-nss-tools-debuginfo': '3.21.3-50.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

