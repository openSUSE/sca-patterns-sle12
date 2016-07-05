#!/usr/bin/python
#
# Title:       Important Security Announcement for Firefox SUSE-SU-2016:1691-1
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
META_COMPONENT = "Firefox"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2016-06/msg00055.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'Firefox'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2016:1691-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 0 ):
		PACKAGES = {
			'MozillaFirefox': '45.2.0esr-75.2',
			'MozillaFirefox-branding-SLE': '45.0-28.2',
			'MozillaFirefox-debuginfo': '45.2.0esr-75.2',
			'MozillaFirefox-debugsource': '45.2.0esr-75.2',
			'MozillaFirefox-devel': '45.2.0esr-75.2',
			'MozillaFirefox-translations': '45.2.0esr-75.2',
			'libfreebl3': '3.21.1-46.2',
			'libfreebl3-32bit': '3.21.1-46.2',
			'libfreebl3-debuginfo': '3.21.1-46.2',
			'libfreebl3-debuginfo-32bit': '3.21.1-46.2',
			'libfreebl3-hmac': '3.21.1-46.2',
			'libfreebl3-hmac-32bit': '3.21.1-46.2',
			'libsoftokn3': '3.21.1-46.2',
			'libsoftokn3-32bit': '3.21.1-46.2',
			'libsoftokn3-debuginfo': '3.21.1-46.2',
			'libsoftokn3-debuginfo-32bit': '3.21.1-46.2',
			'libsoftokn3-hmac': '3.21.1-46.2',
			'libsoftokn3-hmac-32bit': '3.21.1-46.2',
			'mozilla-nspr': '4.12-15.2',
			'mozilla-nspr-32bit': '4.12-15.2',
			'mozilla-nspr-debuginfo': '4.12-15.2',
			'mozilla-nspr-debuginfo-32bit': '4.12-15.2',
			'mozilla-nspr-debugsource': '4.12-15.2',
			'mozilla-nspr-devel': '4.12-15.2',
			'mozilla-nss': '3.21.1-46.2',
			'mozilla-nss-32bit': '3.21.1-46.2',
			'mozilla-nss-certs': '3.21.1-46.2',
			'mozilla-nss-certs-32bit': '3.21.1-46.2',
			'mozilla-nss-certs-debuginfo': '3.21.1-46.2',
			'mozilla-nss-certs-debuginfo-32bit': '3.21.1-46.2',
			'mozilla-nss-debuginfo': '3.21.1-46.2',
			'mozilla-nss-debuginfo-32bit': '3.21.1-46.2',
			'mozilla-nss-debugsource': '3.21.1-46.2',
			'mozilla-nss-devel': '3.21.1-46.2',
			'mozilla-nss-sysinit': '3.21.1-46.2',
			'mozilla-nss-sysinit-32bit': '3.21.1-46.2',
			'mozilla-nss-sysinit-debuginfo': '3.21.1-46.2',
			'mozilla-nss-sysinit-debuginfo-32bit': '3.21.1-46.2',
			'mozilla-nss-tools': '3.21.1-46.2',
			'mozilla-nss-tools-debuginfo': '3.21.1-46.2',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

