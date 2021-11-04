#!/usr/bin/python3
#
# Title:       Important Security Announcement for libvirt SUSE-SU-2020:3039-1
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
META_COMPONENT = "libvirt"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2020-October/007628.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = False
NAME = 'libvirt'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2020:3039-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 5 ):
		PACKAGES = {
			'libvirt': '5.1.0-13.19.1',
			'libvirt-admin': '5.1.0-13.19.1',
			'libvirt-admin-debuginfo': '5.1.0-13.19.1',
			'libvirt-client': '5.1.0-13.19.1',
			'libvirt-client-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon': '5.1.0-13.19.1',
			'libvirt-daemon-config-network': '5.1.0-13.19.1',
			'libvirt-daemon-config-nwfilter': '5.1.0-13.19.1',
			'libvirt-daemon-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-driver-interface': '5.1.0-13.19.1',
			'libvirt-daemon-driver-interface-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-driver-libxl': '5.1.0-13.19.1',
			'libvirt-daemon-driver-libxl-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-driver-lxc': '5.1.0-13.19.1',
			'libvirt-daemon-driver-lxc-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-driver-network': '5.1.0-13.19.1',
			'libvirt-daemon-driver-network-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-driver-nodedev': '5.1.0-13.19.1',
			'libvirt-daemon-driver-nodedev-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-driver-nwfilter': '5.1.0-13.19.1',
			'libvirt-daemon-driver-nwfilter-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-driver-qemu': '5.1.0-13.19.1',
			'libvirt-daemon-driver-qemu-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-driver-secret': '5.1.0-13.19.1',
			'libvirt-daemon-driver-secret-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-driver-storage': '5.1.0-13.19.1',
			'libvirt-daemon-driver-storage-core': '5.1.0-13.19.1',
			'libvirt-daemon-driver-storage-core-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-driver-storage-disk': '5.1.0-13.19.1',
			'libvirt-daemon-driver-storage-disk-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-driver-storage-iscsi': '5.1.0-13.19.1',
			'libvirt-daemon-driver-storage-iscsi-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-driver-storage-logical': '5.1.0-13.19.1',
			'libvirt-daemon-driver-storage-logical-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-driver-storage-mpath': '5.1.0-13.19.1',
			'libvirt-daemon-driver-storage-mpath-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-driver-storage-rbd': '5.1.0-13.19.1',
			'libvirt-daemon-driver-storage-rbd-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-driver-storage-scsi': '5.1.0-13.19.1',
			'libvirt-daemon-driver-storage-scsi-debuginfo': '5.1.0-13.19.1',
			'libvirt-daemon-hooks': '5.1.0-13.19.1',
			'libvirt-daemon-lxc': '5.1.0-13.19.1',
			'libvirt-daemon-qemu': '5.1.0-13.19.1',
			'libvirt-daemon-xen': '5.1.0-13.19.1',
			'libvirt-debugsource': '5.1.0-13.19.1',
			'libvirt-devel': '5.1.0-13.19.1',
			'libvirt-doc': '5.1.0-13.19.1',
			'libvirt-libs': '5.1.0-13.19.1',
			'libvirt-libs-debuginfo': '5.1.0-13.19.1',
			'libvirt-lock-sanlock': '5.1.0-13.19.1',
			'libvirt-lock-sanlock-debuginfo': '5.1.0-13.19.1',
			'libvirt-nss': '5.1.0-13.19.1',
			'libvirt-nss-debuginfo': '5.1.0-13.19.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

