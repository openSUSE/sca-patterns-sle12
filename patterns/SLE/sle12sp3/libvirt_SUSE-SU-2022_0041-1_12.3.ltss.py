#!/usr/bin/python3
#
# Title:       Important Security Announcement for libvirt SUSE-SU-2022:0041-1
# Description: Security fixes for SUSE Linux Enterprise 12 SP3 LTSS
# Source:      Security Announcement Parser v1.6.4
# Modified:    2022 May 06
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
META_COMPONENT = "libvirt"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Security"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Security=https://lists.suse.com/pipermail/sle-security-updates/2022-January/009983.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LTSS = True
NAME = 'libvirt'
MAIN = ''
SEVERITY = 'Important'
TAG = 'SUSE-SU-2022:0041-1'
PACKAGES = {}
SERVER = SUSE.getHostInfo()

if ( SERVER['DistroVersion'] == 12):
	if ( SERVER['DistroPatchLevel'] == 3 ):
		PACKAGES = {
			'libvirt': '3.3.0-5.49.1',
			'libvirt-admin': '3.3.0-5.49.1',
			'libvirt-admin-debuginfo': '3.3.0-5.49.1',
			'libvirt-client': '3.3.0-5.49.1',
			'libvirt-client-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon': '3.3.0-5.49.1',
			'libvirt-daemon-config-network': '3.3.0-5.49.1',
			'libvirt-daemon-config-nwfilter': '3.3.0-5.49.1',
			'libvirt-daemon-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-driver-interface': '3.3.0-5.49.1',
			'libvirt-daemon-driver-interface-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-driver-libxl': '3.3.0-5.49.1',
			'libvirt-daemon-driver-libxl-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-driver-lxc': '3.3.0-5.49.1',
			'libvirt-daemon-driver-lxc-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-driver-network': '3.3.0-5.49.1',
			'libvirt-daemon-driver-network-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-driver-nodedev': '3.3.0-5.49.1',
			'libvirt-daemon-driver-nodedev-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-driver-nwfilter': '3.3.0-5.49.1',
			'libvirt-daemon-driver-nwfilter-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-driver-qemu': '3.3.0-5.49.1',
			'libvirt-daemon-driver-qemu-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-driver-secret': '3.3.0-5.49.1',
			'libvirt-daemon-driver-secret-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-driver-storage': '3.3.0-5.49.1',
			'libvirt-daemon-driver-storage-core': '3.3.0-5.49.1',
			'libvirt-daemon-driver-storage-core-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-driver-storage-disk': '3.3.0-5.49.1',
			'libvirt-daemon-driver-storage-disk-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-driver-storage-iscsi': '3.3.0-5.49.1',
			'libvirt-daemon-driver-storage-iscsi-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-driver-storage-logical': '3.3.0-5.49.1',
			'libvirt-daemon-driver-storage-logical-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-driver-storage-mpath': '3.3.0-5.49.1',
			'libvirt-daemon-driver-storage-mpath-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-driver-storage-rbd': '3.3.0-5.49.1',
			'libvirt-daemon-driver-storage-rbd-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-driver-storage-scsi': '3.3.0-5.49.1',
			'libvirt-daemon-driver-storage-scsi-debuginfo': '3.3.0-5.49.1',
			'libvirt-daemon-hooks': '3.3.0-5.49.1',
			'libvirt-daemon-lxc': '3.3.0-5.49.1',
			'libvirt-daemon-qemu': '3.3.0-5.49.1',
			'libvirt-daemon-xen': '3.3.0-5.49.1',
			'libvirt-debugsource': '3.3.0-5.49.1',
			'libvirt-doc': '3.3.0-5.49.1',
			'libvirt-libs': '3.3.0-5.49.1',
			'libvirt-libs-debuginfo': '3.3.0-5.49.1',
			'libvirt-lock-sanlock': '3.3.0-5.49.1',
			'libvirt-lock-sanlock-debuginfo': '3.3.0-5.49.1',
			'libvirt-nss': '3.3.0-5.49.1',
			'libvirt-nss-debuginfo': '3.3.0-5.49.1',
		}
		SUSE.securityAnnouncementPackageCheck(NAME, MAIN, LTSS, SEVERITY, TAG, PACKAGES)
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the service pack scope")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + NAME + " Security Announcement: Outside the distribution scope")
Core.printPatternResults()

