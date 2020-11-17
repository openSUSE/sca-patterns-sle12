#!/usr/bin/python
#
# Title:       Moderate Security Announcement for LibreOffice SUSE-SU-2020:0372-1
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
META_COMPONENT = "LibreOffice"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-February/006474.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'LibreOffice'
MAIN = ''
SEVERITY = 'Moderate'
TAG = 'SUSE-SU-2020:0372-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 5 ):
		PACKAGES = {
			'bluez': '5.13-5.20.6',
			'bluez-cups': '5.13-5.20.6',
			'bluez-cups-debuginfo': '5.13-5.20.6',
			'bluez-debuginfo': '5.13-5.20.6',
			'bluez-debugsource': '5.13-5.20.6',
			'bluez-devel': '5.13-5.20.6',
			'cmis-client-debuginfo': '0.5.2-9.3.1',
			'cmis-client-debugsource': '0.5.2-9.3.1',
			'gperf': '3.1-19.4.1',
			'gperf-debuginfo': '3.1-19.4.1',
			'gperf-debugsource': '3.1-19.4.1',
			'libbluetooth3': '5.13-5.20.6',
			'libbluetooth3-debuginfo': '5.13-5.20.6',
			'libcmis-0_5-5': '0.5.2-9.3.1',
			'libcmis-0_5-5-debuginfo': '0.5.2-9.3.1',
			'libcmis-c-0_5-5': '0.5.2-9.3.1',
			'libcmis-c-0_5-5-debuginfo': '0.5.2-9.3.1',
			'libcmis-c-devel': '0.5.2-9.3.1',
			'libcmis-devel': '0.5.2-9.3.1',
			'libixion-0_15-0': '0.15.0-13.12.1',
			'libixion-0_15-0-debuginfo': '0.15.0-13.12.1',
			'libixion-debugsource': '0.15.0-13.12.1',
			'libixion-devel': '0.15.0-13.12.1',
			'libmwaw-0_3-3': '0.3.15-7.15.1',
			'libmwaw-0_3-3-debuginfo': '0.3.15-7.15.1',
			'libmwaw-debugsource': '0.3.15-7.15.1',
			'libmwaw-devel': '0.3.15-7.15.1',
			'libmwaw-devel-doc': '0.3.15-7.15.1',
			'liborcus-0_15-0': '0.15.3-10.15.1',
			'liborcus-0_15-0-debuginfo': '0.15.3-10.15.1',
			'liborcus-debugsource': '0.15.3-10.15.1',
			'liborcus-devel': '0.15.3-10.15.1',
			'libreoffice': '6.3.3.2-43.59.5',
			'libreoffice-base': '6.3.3.2-43.59.5',
			'libreoffice-base-debuginfo': '6.3.3.2-43.59.5',
			'libreoffice-base-drivers-postgresql': '6.3.3.2-43.59.5',
			'libreoffice-base-drivers-postgresql-debuginfo': '6.3.3.2-43.59.5',
			'libreoffice-branding-upstream': '6.3.3.2-43.59.5',
			'libreoffice-calc': '6.3.3.2-43.59.5',
			'libreoffice-calc-debuginfo': '6.3.3.2-43.59.5',
			'libreoffice-calc-extensions': '6.3.3.2-43.59.5',
			'libreoffice-debuginfo': '6.3.3.2-43.59.5',
			'libreoffice-debugsource': '6.3.3.2-43.59.5',
			'libreoffice-draw': '6.3.3.2-43.59.5',
			'libreoffice-draw-debuginfo': '6.3.3.2-43.59.5',
			'libreoffice-filters-optional': '6.3.3.2-43.59.5',
			'libreoffice-gnome': '6.3.3.2-43.59.5',
			'libreoffice-gnome-debuginfo': '6.3.3.2-43.59.5',
			'libreoffice-icon-themes': '6.3.3.2-43.59.5',
			'libreoffice-impress': '6.3.3.2-43.59.5',
			'libreoffice-impress-debuginfo': '6.3.3.2-43.59.5',
			'libreoffice-l10n-af': '6.3.3.2-43.59.5',
			'libreoffice-l10n-ar': '6.3.3.2-43.59.5',
			'libreoffice-l10n-bg': '6.3.3.2-43.59.5',
			'libreoffice-l10n-ca': '6.3.3.2-43.59.5',
			'libreoffice-l10n-cs': '6.3.3.2-43.59.5',
			'libreoffice-l10n-da': '6.3.3.2-43.59.5',
			'libreoffice-l10n-de': '6.3.3.2-43.59.5',
			'libreoffice-l10n-en': '6.3.3.2-43.59.5',
			'libreoffice-l10n-es': '6.3.3.2-43.59.5',
			'libreoffice-l10n-fi': '6.3.3.2-43.59.5',
			'libreoffice-l10n-fr': '6.3.3.2-43.59.5',
			'libreoffice-l10n-gu': '6.3.3.2-43.59.5',
			'libreoffice-l10n-hi': '6.3.3.2-43.59.5',
			'libreoffice-l10n-hr': '6.3.3.2-43.59.5',
			'libreoffice-l10n-hu': '6.3.3.2-43.59.5',
			'libreoffice-l10n-it': '6.3.3.2-43.59.5',
			'libreoffice-l10n-ja': '6.3.3.2-43.59.5',
			'libreoffice-l10n-ko': '6.3.3.2-43.59.5',
			'libreoffice-l10n-lt': '6.3.3.2-43.59.5',
			'libreoffice-l10n-nb': '6.3.3.2-43.59.5',
			'libreoffice-l10n-nl': '6.3.3.2-43.59.5',
			'libreoffice-l10n-nn': '6.3.3.2-43.59.5',
			'libreoffice-l10n-pl': '6.3.3.2-43.59.5',
			'libreoffice-l10n-pt_BR': '6.3.3.2-43.59.5',
			'libreoffice-l10n-pt_PT': '6.3.3.2-43.59.5',
			'libreoffice-l10n-ro': '6.3.3.2-43.59.5',
			'libreoffice-l10n-ru': '6.3.3.2-43.59.5',
			'libreoffice-l10n-sk': '6.3.3.2-43.59.5',
			'libreoffice-l10n-sv': '6.3.3.2-43.59.5',
			'libreoffice-l10n-uk': '6.3.3.2-43.59.5',
			'libreoffice-l10n-xh': '6.3.3.2-43.59.5',
			'libreoffice-l10n-zh_CN': '6.3.3.2-43.59.5',
			'libreoffice-l10n-zh_TW': '6.3.3.2-43.59.5',
			'libreoffice-l10n-zu': '6.3.3.2-43.59.5',
			'libreoffice-librelogo': '6.3.3.2-43.59.5',
			'libreoffice-mailmerge': '6.3.3.2-43.59.5',
			'libreoffice-math': '6.3.3.2-43.59.5',
			'libreoffice-math-debuginfo': '6.3.3.2-43.59.5',
			'libreoffice-officebean': '6.3.3.2-43.59.5',
			'libreoffice-officebean-debuginfo': '6.3.3.2-43.59.5',
			'libreoffice-pyuno': '6.3.3.2-43.59.5',
			'libreoffice-pyuno-debuginfo': '6.3.3.2-43.59.5',
			'libreoffice-sdk': '6.3.3.2-43.59.5',
			'libreoffice-sdk-debuginfo': '6.3.3.2-43.59.5',
			'libreoffice-writer': '6.3.3.2-43.59.5',
			'libreoffice-writer-debuginfo': '6.3.3.2-43.59.5',
			'libreoffice-writer-extensions': '6.3.3.2-43.59.5',
			'myspell-af_NA': '20191016-16.21.1',
			'myspell-af_ZA': '20191016-16.21.1',
			'myspell-ar': '20191016-16.21.1',
			'myspell-ar_AE': '20191016-16.21.1',
			'myspell-ar_BH': '20191016-16.21.1',
			'myspell-ar_DZ': '20191016-16.21.1',
			'myspell-ar_EG': '20191016-16.21.1',
			'myspell-ar_IQ': '20191016-16.21.1',
			'myspell-ar_JO': '20191016-16.21.1',
			'myspell-ar_KW': '20191016-16.21.1',
			'myspell-ar_LB': '20191016-16.21.1',
			'myspell-ar_LY': '20191016-16.21.1',
			'myspell-ar_MA': '20191016-16.21.1',
			'myspell-ar_OM': '20191016-16.21.1',
			'myspell-ar_QA': '20191016-16.21.1',
			'myspell-ar_SA': '20191016-16.21.1',
			'myspell-ar_SD': '20191016-16.21.1',
			'myspell-ar_SY': '20191016-16.21.1',
			'myspell-ar_TN': '20191016-16.21.1',
			'myspell-ar_YE': '20191016-16.21.1',
			'myspell-be_BY': '20191016-16.21.1',
			'myspell-bg_BG': '20191016-16.21.1',
			'myspell-bn_BD': '20191016-16.21.1',
			'myspell-bn_IN': '20191016-16.21.1',
			'myspell-bs': '20191016-16.21.1',
			'myspell-bs_BA': '20191016-16.21.1',
			'myspell-ca': '20191016-16.21.1',
			'myspell-ca_AD': '20191016-16.21.1',
			'myspell-ca_ES': '20191016-16.21.1',
			'myspell-ca_ES_valencia': '20191016-16.21.1',
			'myspell-ca_FR': '20191016-16.21.1',
			'myspell-ca_IT': '20191016-16.21.1',
			'myspell-cs_CZ': '20191016-16.21.1',
			'myspell-da_DK': '20191016-16.21.1',
			'myspell-de': '20191016-16.21.1',
			'myspell-de_AT': '20191016-16.21.1',
			'myspell-de_CH': '20191016-16.21.1',
			'myspell-de_DE': '20191016-16.21.1',
			'myspell-dictionaries': '20191016-16.21.1',
			'myspell-el_GR': '20191016-16.21.1',
			'myspell-en': '20191016-16.21.1',
			'myspell-en_AU': '20191016-16.21.1',
			'myspell-en_BS': '20191016-16.21.1',
			'myspell-en_BZ': '20191016-16.21.1',
			'myspell-en_CA': '20191016-16.21.1',
			'myspell-en_GB': '20191016-16.21.1',
			'myspell-en_GH': '20191016-16.21.1',
			'myspell-en_IE': '20191016-16.21.1',
			'myspell-en_IN': '20191016-16.21.1',
			'myspell-en_JM': '20191016-16.21.1',
			'myspell-en_MW': '20191016-16.21.1',
			'myspell-en_NA': '20191016-16.21.1',
			'myspell-en_NZ': '20191016-16.21.1',
			'myspell-en_PH': '20191016-16.21.1',
			'myspell-en_TT': '20191016-16.21.1',
			'myspell-en_US': '20191016-16.21.1',
			'myspell-en_ZA': '20191016-16.21.1',
			'myspell-en_ZW': '20191016-16.21.1',
			'myspell-es': '20191016-16.21.1',
			'myspell-es_AR': '20191016-16.21.1',
			'myspell-es_BO': '20191016-16.21.1',
			'myspell-es_CL': '20191016-16.21.1',
			'myspell-es_CO': '20191016-16.21.1',
			'myspell-es_CR': '20191016-16.21.1',
			'myspell-es_CU': '20191016-16.21.1',
			'myspell-es_DO': '20191016-16.21.1',
			'myspell-es_EC': '20191016-16.21.1',
			'myspell-es_ES': '20191016-16.21.1',
			'myspell-es_GT': '20191016-16.21.1',
			'myspell-es_HN': '20191016-16.21.1',
			'myspell-es_MX': '20191016-16.21.1',
			'myspell-es_NI': '20191016-16.21.1',
			'myspell-es_PA': '20191016-16.21.1',
			'myspell-es_PE': '20191016-16.21.1',
			'myspell-es_PR': '20191016-16.21.1',
			'myspell-es_PY': '20191016-16.21.1',
			'myspell-es_SV': '20191016-16.21.1',
			'myspell-es_UY': '20191016-16.21.1',
			'myspell-es_VE': '20191016-16.21.1',
			'myspell-et_EE': '20191016-16.21.1',
			'myspell-fr_BE': '20191016-16.21.1',
			'myspell-fr_CA': '20191016-16.21.1',
			'myspell-fr_CH': '20191016-16.21.1',
			'myspell-fr_FR': '20191016-16.21.1',
			'myspell-fr_LU': '20191016-16.21.1',
			'myspell-fr_MC': '20191016-16.21.1',
			'myspell-gu_IN': '20191016-16.21.1',
			'myspell-he_IL': '20191016-16.21.1',
			'myspell-hi_IN': '20191016-16.21.1',
			'myspell-hr_HR': '20191016-16.21.1',
			'myspell-hu_HU': '20191016-16.21.1',
			'myspell-id': '20191016-16.21.1',
			'myspell-id_ID': '20191016-16.21.1',
			'myspell-it_IT': '20191016-16.21.1',
			'myspell-lightproof-en': '20191016-16.21.1',
			'myspell-lightproof-hu_HU': '20191016-16.21.1',
			'myspell-lightproof-pt_BR': '20191016-16.21.1',
			'myspell-lightproof-ru_RU': '20191016-16.21.1',
			'myspell-lo_LA': '20191016-16.21.1',
			'myspell-lt_LT': '20191016-16.21.1',
			'myspell-lv_LV': '20191016-16.21.1',
			'myspell-nb_NO': '20191016-16.21.1',
			'myspell-nl_BE': '20191016-16.21.1',
			'myspell-nl_NL': '20191016-16.21.1',
			'myspell-nn_NO': '20191016-16.21.1',
			'myspell-no': '20191016-16.21.1',
			'myspell-pl_PL': '20191016-16.21.1',
			'myspell-pt_AO': '20191016-16.21.1',
			'myspell-pt_BR': '20191016-16.21.1',
			'myspell-pt_PT': '20191016-16.21.1',
			'myspell-ro': '20191016-16.21.1',
			'myspell-ro_RO': '20191016-16.21.1',
			'myspell-ru_RU': '20191016-16.21.1',
			'myspell-sk_SK': '20191016-16.21.1',
			'myspell-sl_SI': '20191016-16.21.1',
			'myspell-sr': '20191016-16.21.1',
			'myspell-sr_CS': '20191016-16.21.1',
			'myspell-sr_Latn_CS': '20191016-16.21.1',
			'myspell-sr_Latn_RS': '20191016-16.21.1',
			'myspell-sr_RS': '20191016-16.21.1',
			'myspell-sv_FI': '20191016-16.21.1',
			'myspell-sv_SE': '20191016-16.21.1',
			'myspell-te': '20191016-16.21.1',
			'myspell-te_IN': '20191016-16.21.1',
			'myspell-th_TH': '20191016-16.21.1',
			'myspell-uk_UA': '20191016-16.21.1',
			'myspell-vi': '20191016-16.21.1',
			'myspell-vi_VN': '20191016-16.21.1',
			'myspell-zu_ZA': '20191016-16.21.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

