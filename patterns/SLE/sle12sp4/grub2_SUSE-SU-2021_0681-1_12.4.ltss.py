#!/usr/bin/python
#
# Title:       Important Security Announcement for grub2 SUSE-SU-2021:0681-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP4 LTSS
# Source:      Security Announcement Parser v1.6.1
# Modified:    2021 Mar 31
#
##############################################################################
# Copyright (C) 2021 SUSE LLC
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
META_COMPONENT = "grub2"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2021-March/008422.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'grub2'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2021:0681-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 4 ):
		PACKAGES = {
			'grub2': '2.02-12.47.1',
			'grub2-arm64-efi': '2.02-12.47.1',
			'grub2-debuginfo': '2.02-12.47.1',
			'grub2-debugsource': '2.02-12.47.1',
			'grub2-i386-pc': '2.02-12.47.1',
			'grub2-powerpc-ieee1275': '2.02-12.47.1',
			'grub2-s390x-emu': '2.02-12.47.1',
			'grub2-snapper-plugin': '2.02-12.47.1',
			'grub2-systemd-sleep-plugin': '2.02-12.47.1',
			'grub2-x86_64-efi': '2.02-12.47.1',
			'grub2-x86_64-xen': '2.02-12.47.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

