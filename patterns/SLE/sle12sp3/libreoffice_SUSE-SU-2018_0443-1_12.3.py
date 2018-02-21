#!/usr/bin/python
#
# Title:       Important Security Announcement for libreoffice SUSE-SU-2018:0443-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP3
# Source:      Security Announcement Parser v1.3.7
# Modified:    2018 Feb 20
#
##############################################################################
# Copyright (C) 2018 SUSE LLC
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
META_COMPONENT = "libreoffice"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.opensuse.org/opensuse-security-announce/2018-02/msg00024.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'libreoffice'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2018:0443-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'libreoffice': '5.4.5.1-43.19.1',
			'libreoffice-base': '5.4.5.1-43.19.1',
			'libreoffice-base-debuginfo': '5.4.5.1-43.19.1',
			'libreoffice-base-drivers-mysql': '5.4.5.1-43.19.1',
			'libreoffice-base-drivers-mysql-debuginfo': '5.4.5.1-43.19.1',
			'libreoffice-base-drivers-postgresql': '5.4.5.1-43.19.1',
			'libreoffice-base-drivers-postgresql-debuginfo': '5.4.5.1-43.19.1',
			'libreoffice-calc': '5.4.5.1-43.19.1',
			'libreoffice-calc-debuginfo': '5.4.5.1-43.19.1',
			'libreoffice-calc-extensions': '5.4.5.1-43.19.1',
			'libreoffice-debuginfo': '5.4.5.1-43.19.1',
			'libreoffice-debugsource': '5.4.5.1-43.19.1',
			'libreoffice-draw': '5.4.5.1-43.19.1',
			'libreoffice-draw-debuginfo': '5.4.5.1-43.19.1',
			'libreoffice-filters-optional': '5.4.5.1-43.19.1',
			'libreoffice-gnome': '5.4.5.1-43.19.1',
			'libreoffice-gnome-debuginfo': '5.4.5.1-43.19.1',
			'libreoffice-icon-theme-galaxy': '5.4.5.1-43.19.1',
			'libreoffice-icon-theme-tango': '5.4.5.1-43.19.1',
			'libreoffice-impress': '5.4.5.1-43.19.1',
			'libreoffice-impress-debuginfo': '5.4.5.1-43.19.1',
			'libreoffice-l10n-af': '5.4.5.1-43.19.1',
			'libreoffice-l10n-ar': '5.4.5.1-43.19.1',
			'libreoffice-l10n-bg': '5.4.5.1-43.19.1',
			'libreoffice-l10n-ca': '5.4.5.1-43.19.1',
			'libreoffice-l10n-cs': '5.4.5.1-43.19.1',
			'libreoffice-l10n-da': '5.4.5.1-43.19.1',
			'libreoffice-l10n-de': '5.4.5.1-43.19.1',
			'libreoffice-l10n-en': '5.4.5.1-43.19.1',
			'libreoffice-l10n-es': '5.4.5.1-43.19.1',
			'libreoffice-l10n-fi': '5.4.5.1-43.19.1',
			'libreoffice-l10n-fr': '5.4.5.1-43.19.1',
			'libreoffice-l10n-gu': '5.4.5.1-43.19.1',
			'libreoffice-l10n-hi': '5.4.5.1-43.19.1',
			'libreoffice-l10n-hr': '5.4.5.1-43.19.1',
			'libreoffice-l10n-hu': '5.4.5.1-43.19.1',
			'libreoffice-l10n-it': '5.4.5.1-43.19.1',
			'libreoffice-l10n-ja': '5.4.5.1-43.19.1',
			'libreoffice-l10n-ko': '5.4.5.1-43.19.1',
			'libreoffice-l10n-lt': '5.4.5.1-43.19.1',
			'libreoffice-l10n-nb': '5.4.5.1-43.19.1',
			'libreoffice-l10n-nl': '5.4.5.1-43.19.1',
			'libreoffice-l10n-nn': '5.4.5.1-43.19.1',
			'libreoffice-l10n-pl': '5.4.5.1-43.19.1',
			'libreoffice-l10n-pt_BR': '5.4.5.1-43.19.1',
			'libreoffice-l10n-pt_PT': '5.4.5.1-43.19.1',
			'libreoffice-l10n-ro': '5.4.5.1-43.19.1',
			'libreoffice-l10n-ru': '5.4.5.1-43.19.1',
			'libreoffice-l10n-sk': '5.4.5.1-43.19.1',
			'libreoffice-l10n-sv': '5.4.5.1-43.19.1',
			'libreoffice-l10n-uk': '5.4.5.1-43.19.1',
			'libreoffice-l10n-xh': '5.4.5.1-43.19.1',
			'libreoffice-l10n-zh_CN': '5.4.5.1-43.19.1',
			'libreoffice-l10n-zh_TW': '5.4.5.1-43.19.1',
			'libreoffice-l10n-zu': '5.4.5.1-43.19.1',
			'libreoffice-mailmerge': '5.4.5.1-43.19.1',
			'libreoffice-math': '5.4.5.1-43.19.1',
			'libreoffice-math-debuginfo': '5.4.5.1-43.19.1',
			'libreoffice-officebean': '5.4.5.1-43.19.1',
			'libreoffice-officebean-debuginfo': '5.4.5.1-43.19.1',
			'libreoffice-pyuno': '5.4.5.1-43.19.1',
			'libreoffice-pyuno-debuginfo': '5.4.5.1-43.19.1',
			'libreoffice-sdk': '5.4.5.1-43.19.1',
			'libreoffice-sdk-debuginfo': '5.4.5.1-43.19.1',
			'libreoffice-writer': '5.4.5.1-43.19.1',
			'libreoffice-writer-debuginfo': '5.4.5.1-43.19.1',
			'libreoffice-writer-extensions': '5.4.5.1-43.19.1',
			'libreofficekit': '5.4.5.1-43.19.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

