#!/usr/bin/python
#
# Title:       Moderate Security Announcement for texlive SUSE-SU-2020:1581-1
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
META_COMPONENT = "texlive"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-June/006915.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'texlive'
MAIN = ''
SEVERITY = 'Moderate'
TAG = 'SUSE-SU-2020:1581-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 4 ):
		PACKAGES = {
			'libkpathsea6': '6.2.0dev-22.8.2',
			'libkpathsea6-debuginfo': '6.2.0dev-22.8.2',
			'libptexenc1': '1.3.2dev-22.8.2',
			'libptexenc1-debuginfo': '1.3.2dev-22.8.2',
			'texlive': '2013.20130620-22.8.2',
			'texlive-bibtex-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-bibtex-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-bin-devel': '2013.20130620-22.8.2',
			'texlive-checkcites-bin': '2013.20130620.svn25623-22.8.2',
			'texlive-collection-basic': '2013.74.svn30372-16.12.1',
			'texlive-collection-fontsrecommended': '2013.74.svn30307-16.12.1',
			'texlive-collection-htmlxml': '2013.74.svn30307-16.12.1',
			'texlive-collection-latex': '2013.74.svn30308-16.12.1',
			'texlive-collection-latexrecommended': '2013.74.svn30811-16.12.1',
			'texlive-collection-luatex': '2013.74.svn30790-16.12.1',
			'texlive-collection-xetex': '2013.74.svn30396-16.12.1',
			'texlive-context-bin': '2013.20130620.svn29741-22.8.2',
			'texlive-cweb-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-cweb-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-debugsource': '2013.20130620-22.8.2',
			'texlive-devel': '2013.74-16.12.1',
			'texlive-dviasm-bin': '2013.20130620.svn8329-22.8.2',
			'texlive-dvidvi-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-dvidvi-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-dviljk-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-dviljk-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-dvipdfmx-bin': '2013.20130620.svn30845-22.8.2',
			'texlive-dvipdfmx-bin-debuginfo': '2013.20130620.svn30845-22.8.2',
			'texlive-dvipng-bin': '2013.20130620.svn30845-22.8.2',
			'texlive-dvipng-bin-debuginfo': '2013.20130620.svn30845-22.8.2',
			'texlive-dvips-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-dvips-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-dvisvgm-bin': '2013.20130620.svn30613-22.8.2',
			'texlive-dvisvgm-bin-debuginfo': '2013.20130620.svn30613-22.8.2',
			'texlive-extratools': '2013.74-16.12.1',
			'texlive-filesystem': '2013.74-16.12.1',
			'texlive-gsftopk-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-gsftopk-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-jadetex-bin': '2013.20130620.svn3006-22.8.2',
			'texlive-kpathsea-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-kpathsea-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-kpathsea-devel': '6.2.0dev-22.8.2',
			'texlive-lacheck-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-lacheck-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-latex-bin-bin': '2013.20130620.svn14050-22.8.2',
			'texlive-lua2dox-bin': '2013.20130620.svn29053-22.8.2',
			'texlive-luaotfload-bin': '2013.20130620.svn30313-22.8.2',
			'texlive-luatex-bin': '2013.20130620.svn30845-22.8.2',
			'texlive-luatex-bin-debuginfo': '2013.20130620.svn30845-22.8.2',
			'texlive-makeindex-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-makeindex-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-metafont-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-metafont-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-metapost-bin': '2013.20130620.svn30845-22.8.2',
			'texlive-metapost-bin-debuginfo': '2013.20130620.svn30845-22.8.2',
			'texlive-mfware-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-mfware-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-mptopdf-bin': '2013.20130620.svn18674-22.8.2',
			'texlive-pdftex-bin': '2013.20130620.svn30845-22.8.2',
			'texlive-pdftex-bin-debuginfo': '2013.20130620.svn30845-22.8.2',
			'texlive-pstools-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-pstools-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-ptexenc-devel': '1.3.2dev-22.8.2',
			'texlive-seetexk-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-seetexk-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-splitindex-bin': '2013.20130620.svn29688-22.8.2',
			'texlive-tetex-bin': '2013.20130620.svn29741-22.8.2',
			'texlive-tex-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-tex-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-tex4ht-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-tex4ht-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-texconfig-bin': '2013.20130620.svn29741-22.8.2',
			'texlive-thumbpdf-bin': '2013.20130620.svn6898-22.8.2',
			'texlive-vlna-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-vlna-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-web-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-web-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-xdvi-bin': '2013.20130620.svn30088-22.8.2',
			'texlive-xdvi-bin-debuginfo': '2013.20130620.svn30088-22.8.2',
			'texlive-xetex-bin': '2013.20130620.svn30845-22.8.2',
			'texlive-xetex-bin-debuginfo': '2013.20130620.svn30845-22.8.2',
			'texlive-xmltex-bin': '2013.20130620.svn3006-22.8.2',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

