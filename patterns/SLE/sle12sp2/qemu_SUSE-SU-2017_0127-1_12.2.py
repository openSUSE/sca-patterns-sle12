#!/usr/bin/python3
#
# Title:       Important Security Announcement for qemu SUSE-SU-2017:0127-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP2
# Source:      Security Announcement Parser v1.3.6
# Modified:    2017 Apr 04
#
##############################################################################
# Copyright (C) 2017 SUSE LLC
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
OTHER_LINKS = "META_LINK_Security=http://lists.opensuse.org/opensuse-security-announce/2017-01/msg00017.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'qemu'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2017:0127-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 2 ):
		PACKAGES = {
			'qemu': '2.6.2-39.1',
			'qemu-arm': '2.6.2-39.1',
			'qemu-arm-debuginfo': '2.6.2-39.1',
			'qemu-block-curl': '2.6.2-39.1',
			'qemu-block-curl-debuginfo': '2.6.2-39.1',
			'qemu-block-rbd': '2.6.2-39.1',
			'qemu-block-rbd-debuginfo': '2.6.2-39.1',
			'qemu-block-ssh': '2.6.2-39.1',
			'qemu-block-ssh-debuginfo': '2.6.2-39.1',
			'qemu-debugsource': '2.6.2-39.1',
			'qemu-guest-agent': '2.6.2-39.1',
			'qemu-guest-agent-debuginfo': '2.6.2-39.1',
			'qemu-ipxe': '1.0.0-39.1',
			'qemu-kvm': '2.6.2-39.1',
			'qemu-lang': '2.6.2-39.1',
			'qemu-ppc': '2.6.2-39.1',
			'qemu-ppc-debuginfo': '2.6.2-39.1',
			'qemu-seabios': '1.9.1-39.1',
			'qemu-sgabios': '8-39.1',
			'qemu-tools': '2.6.2-39.1',
			'qemu-tools-debuginfo': '2.6.2-39.1',
			'qemu-vgabios': '1.9.1-39.1',
			'qemu-x86': '2.6.2-39.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

