#!/usr/bin/python
#
# Title:       Important Security Announcement for qemu SUSE-SU-2020:2743-1
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
META_COMPONENT = "qemu"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-September/007481.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'qemu'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2020:2743-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 5 ):
		PACKAGES = {
			'qemu': '3.1.1.1-45.1',
			'qemu-arm': '3.1.1.1-45.1',
			'qemu-arm-debuginfo': '3.1.1.1-45.1',
			'qemu-audio-alsa': '3.1.1.1-45.1',
			'qemu-audio-alsa-debuginfo': '3.1.1.1-45.1',
			'qemu-audio-oss': '3.1.1.1-45.1',
			'qemu-audio-oss-debuginfo': '3.1.1.1-45.1',
			'qemu-audio-pa': '3.1.1.1-45.1',
			'qemu-audio-pa-debuginfo': '3.1.1.1-45.1',
			'qemu-audio-sdl': '3.1.1.1-45.1',
			'qemu-audio-sdl-debuginfo': '3.1.1.1-45.1',
			'qemu-block-curl': '3.1.1.1-45.1',
			'qemu-block-curl-debuginfo': '3.1.1.1-45.1',
			'qemu-block-iscsi': '3.1.1.1-45.1',
			'qemu-block-iscsi-debuginfo': '3.1.1.1-45.1',
			'qemu-block-rbd': '3.1.1.1-45.1',
			'qemu-block-rbd-debuginfo': '3.1.1.1-45.1',
			'qemu-block-ssh': '3.1.1.1-45.1',
			'qemu-block-ssh-debuginfo': '3.1.1.1-45.1',
			'qemu-debugsource': '3.1.1.1-45.1',
			'qemu-guest-agent': '3.1.1.1-45.1',
			'qemu-guest-agent-debuginfo': '3.1.1.1-45.1',
			'qemu-ipxe': '1.0.0+-45.1',
			'qemu-kvm': '3.1.1.1-45.1',
			'qemu-lang': '3.1.1.1-45.1',
			'qemu-ppc': '3.1.1.1-45.1',
			'qemu-ppc-debuginfo': '3.1.1.1-45.1',
			'qemu-s390': '3.1.1.1-45.1',
			'qemu-s390-debuginfo': '3.1.1.1-45.1',
			'qemu-seabios': '1.12.0-45.1',
			'qemu-sgabios': '8-45.1',
			'qemu-tools': '3.1.1.1-45.1',
			'qemu-tools-debuginfo': '3.1.1.1-45.1',
			'qemu-ui-curses': '3.1.1.1-45.1',
			'qemu-ui-curses-debuginfo': '3.1.1.1-45.1',
			'qemu-ui-gtk': '3.1.1.1-45.1',
			'qemu-ui-gtk-debuginfo': '3.1.1.1-45.1',
			'qemu-ui-sdl': '3.1.1.1-45.1',
			'qemu-ui-sdl-debuginfo': '3.1.1.1-45.1',
			'qemu-vgabios': '1.12.0-45.1',
			'qemu-x86': '3.1.1.1-45.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

