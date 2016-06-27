#!/usr/bin/python
#
# Title:       Important Security Announcement for php53 SUSE-SU-2016:1638-1
# Description: Security fixes for SUSE Linux Enterprise 11 SP2 LTSS
# Source:      Security Announcement Parser v1.3.1
# Modified:    2016 Jun 27
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
META_COMPONENT = "php53"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2016-06/msg00041.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'php53'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2016:1638-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 11):
	if ( SERVER['DistroPatchLevel'] == 2 ):
		PACKAGES = {
			'apache2-mod_php53': '5.3.17-47.1',
			'php53': '5.3.17-47.1',
			'php53-bcmath': '5.3.17-47.1',
			'php53-bz2': '5.3.17-47.1',
			'php53-calendar': '5.3.17-47.1',
			'php53-ctype': '5.3.17-47.1',
			'php53-curl': '5.3.17-47.1',
			'php53-dba': '5.3.17-47.1',
			'php53-dom': '5.3.17-47.1',
			'php53-exif': '5.3.17-47.1',
			'php53-fastcgi': '5.3.17-47.1',
			'php53-fileinfo': '5.3.17-47.1',
			'php53-ftp': '5.3.17-47.1',
			'php53-gd': '5.3.17-47.1',
			'php53-gettext': '5.3.17-47.1',
			'php53-gmp': '5.3.17-47.1',
			'php53-iconv': '5.3.17-47.1',
			'php53-intl': '5.3.17-47.1',
			'php53-json': '5.3.17-47.1',
			'php53-ldap': '5.3.17-47.1',
			'php53-mbstring': '5.3.17-47.1',
			'php53-mcrypt': '5.3.17-47.1',
			'php53-mysql': '5.3.17-47.1',
			'php53-odbc': '5.3.17-47.1',
			'php53-openssl': '5.3.17-47.1',
			'php53-pcntl': '5.3.17-47.1',
			'php53-pdo': '5.3.17-47.1',
			'php53-pear': '5.3.17-47.1',
			'php53-pgsql': '5.3.17-47.1',
			'php53-pspell': '5.3.17-47.1',
			'php53-shmop': '5.3.17-47.1',
			'php53-snmp': '5.3.17-47.1',
			'php53-soap': '5.3.17-47.1',
			'php53-suhosin': '5.3.17-47.1',
			'php53-sysvmsg': '5.3.17-47.1',
			'php53-sysvsem': '5.3.17-47.1',
			'php53-sysvshm': '5.3.17-47.1',
			'php53-tokenizer': '5.3.17-47.1',
			'php53-wddx': '5.3.17-47.1',
			'php53-xmlreader': '5.3.17-47.1',
			'php53-xmlrpc': '5.3.17-47.1',
			'php53-xmlwriter': '5.3.17-47.1',
			'php53-xsl': '5.3.17-47.1',
			'php53-zip': '5.3.17-47.1',
			'php53-zlib': '5.3.17-47.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

