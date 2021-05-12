#!/usr/bin/python
#
# Title:       Pattern for TID000019618
# Description: Timeout when attempting NFS mount over IPv6
# Source:      Basic Python Pattern Template v0.3.4
# Options:     SLE,NFS,Timeout,nfsipv6,000019618,1144162,0,1,0
# Distro:      SLES12 SP5
# Modified:    2021 May 12
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

META_CLASS = "SLE"
META_CATEGORY = "NFS"
META_COMPONENT = "Timeout"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019618|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1144162"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

PACKAGE = "nfs-client"
KERNEL_VERSION = '4.12.14-122.20'
FEATURE = 'scatter-gather'
IPV6_DEVICES = []
FEATURELESS_IPV6_DEVICES = []

if( SUSE.packageInstalled(PACKAGE) ): # nfs package for mounting installed
	INSTALLED_VERSION = SUSE.compareKernel(KERNEL_VERSION)
	if( INSTALLED_VERSION < 0 ): # Running the affected kernel version
		NETWORKS = SUSE.getNetworkInterfaces()
		for DEVICE in NETWORKS.keys():
			if( len(NETWORKS[DEVICE]['addr6']) > 0 ): # Find IPv6 enabled interfaces
				IPV6_DEVICES.append(DEVICE)
				if( FEATURE in NETWORKS[DEVICE] ):
					if( not NETWORKS[DEVICE][FEATURE] ): # With scatter-gather disabled
						FEATURELESS_IPV6_DEVICES.append(DEVICE)
		if( len(IPV6_DEVICES) > 0 ):
			if( len(FEATURELESS_IPV6_DEVICES) > 0 ):
				Core.updateStatus(Core.WARN, "Timeouts may occur attempting NFS mounts over IPv6 on: " + ' '.join(FEATURELESS_IPV6_DEVICES))
			else:
				Core.updateStatus(Core.IGNORE, "All IPv6 network devices have " + str(FEATURE) + " enabled")
		else:
			Core.updateStatus(Core.ERROR, "ERROR: No IPv6 network devices found")
	else:
		Core.updateStatus(Core.IGNORE, "Bug fixes applied in kernel version " + KERNEL_VERSION + " or higher")
else:
	Core.updateStatus(Core.ERROR, "ERROR: RPM package " + PACKAGE + " not installed")

Core.printPatternResults()

