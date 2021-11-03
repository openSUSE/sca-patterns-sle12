#!/usr/bin/python3
#
# Title:       Important Security Announcement for libvirt SUSE-SU-2018:0861-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP2
# Source:      Security Announcement Parser v1.3.7
# Modified:    2018 May 02
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
META_COMPONENT = "libvirt"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.opensuse.org/opensuse-security-announce/2018-04/msg00000.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'libvirt'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2018:0861-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 2 ):
		PACKAGES = {
			'libvirt': '2.0.0-27.34.1',
			'libvirt-client': '2.0.0-27.34.1',
			'libvirt-client-32bit': '2.0.0-27.34.1',
			'libvirt-client-debuginfo': '2.0.0-27.34.1',
			'libvirt-client-debuginfo-32bit': '2.0.0-27.34.1',
			'libvirt-daemon': '2.0.0-27.34.1',
			'libvirt-daemon-config-network': '2.0.0-27.34.1',
			'libvirt-daemon-config-nwfilter': '2.0.0-27.34.1',
			'libvirt-daemon-debuginfo': '2.0.0-27.34.1',
			'libvirt-daemon-driver-interface': '2.0.0-27.34.1',
			'libvirt-daemon-driver-interface-debuginfo': '2.0.0-27.34.1',
			'libvirt-daemon-driver-libxl': '2.0.0-27.34.1',
			'libvirt-daemon-driver-libxl-debuginfo': '2.0.0-27.34.1',
			'libvirt-daemon-driver-lxc': '2.0.0-27.34.1',
			'libvirt-daemon-driver-lxc-debuginfo': '2.0.0-27.34.1',
			'libvirt-daemon-driver-network': '2.0.0-27.34.1',
			'libvirt-daemon-driver-network-debuginfo': '2.0.0-27.34.1',
			'libvirt-daemon-driver-nodedev': '2.0.0-27.34.1',
			'libvirt-daemon-driver-nodedev-debuginfo': '2.0.0-27.34.1',
			'libvirt-daemon-driver-nwfilter': '2.0.0-27.34.1',
			'libvirt-daemon-driver-nwfilter-debuginfo': '2.0.0-27.34.1',
			'libvirt-daemon-driver-qemu': '2.0.0-27.34.1',
			'libvirt-daemon-driver-qemu-debuginfo': '2.0.0-27.34.1',
			'libvirt-daemon-driver-secret': '2.0.0-27.34.1',
			'libvirt-daemon-driver-secret-debuginfo': '2.0.0-27.34.1',
			'libvirt-daemon-driver-storage': '2.0.0-27.34.1',
			'libvirt-daemon-driver-storage-debuginfo': '2.0.0-27.34.1',
			'libvirt-daemon-hooks': '2.0.0-27.34.1',
			'libvirt-daemon-lxc': '2.0.0-27.34.1',
			'libvirt-daemon-qemu': '2.0.0-27.34.1',
			'libvirt-daemon-xen': '2.0.0-27.34.1',
			'libvirt-debugsource': '2.0.0-27.34.1',
			'libvirt-devel': '2.0.0-27.34.1',
			'libvirt-doc': '2.0.0-27.34.1',
			'libvirt-lock-sanlock': '2.0.0-27.34.1',
			'libvirt-lock-sanlock-debuginfo': '2.0.0-27.34.1',
			'libvirt-nss': '2.0.0-27.34.1',
			'libvirt-nss-debuginfo': '2.0.0-27.34.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

