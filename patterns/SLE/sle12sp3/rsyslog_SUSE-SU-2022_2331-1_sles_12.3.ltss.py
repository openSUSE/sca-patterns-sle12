#!/usr/bin/python3
#
# Title:       Important Security Announcement for rsyslog SUSE-SU-2022:2331-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP3 LTSS
# URL:         https://lists.suse.com/pipermail/sle-security-updates/2022-July/011474.html
# Source:      Security Announcement Generator (sagen.py) v2.0.0-beta4
# Modified:    2022 Oct 25
#
##############################################################################
# Copyright (C) 2022 SUSE LLC
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

META_CLASS = "Security"
META_CATEGORY = "SLE"
META_COMPONENT = "rsyslog"
pattern_filename = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2022-July/011474.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, pattern_filename, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'rsyslog'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2022:2331-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'rsyslog': '8.24.0-3.58.2',
			'rsyslog-debuginfo': '8.24.0-3.58.2',
			'rsyslog-debugsource': '8.24.0-3.58.2',
			'rsyslog-diag-tools': '8.24.0-3.58.2',
			'rsyslog-diag-tools-debuginfo': '8.24.0-3.58.2',
			'rsyslog-doc': '8.24.0-3.58.2',
			'rsyslog-module-gssapi': '8.24.0-3.58.2',
			'rsyslog-module-gssapi-debuginfo': '8.24.0-3.58.2',
			'rsyslog-module-gtls': '8.24.0-3.58.2',
			'rsyslog-module-gtls-debuginfo': '8.24.0-3.58.2',
			'rsyslog-module-mysql': '8.24.0-3.58.2',
			'rsyslog-module-mysql-debuginfo': '8.24.0-3.58.2',
			'rsyslog-module-pgsql': '8.24.0-3.58.2',
			'rsyslog-module-pgsql-debuginfo': '8.24.0-3.58.2',
			'rsyslog-module-relp': '8.24.0-3.58.2',
			'rsyslog-module-relp-debuginfo': '8.24.0-3.58.2',
			'rsyslog-module-snmp': '8.24.0-3.58.2',
			'rsyslog-module-snmp-debuginfo': '8.24.0-3.58.2',
			'rsyslog-module-udpspoof': '8.24.0-3.58.2',
			'rsyslog-module-udpspoof-debuginfo': '8.24.0-3.58.2',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

