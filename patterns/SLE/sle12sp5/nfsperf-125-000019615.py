#!/usr/bin/python
#
# Title:       Pattern for TID000019615
# Description: Performance loss when writing large files over NFS
# Source:      Kernel Package Version Pattern Template v0.1.2
# Options:     SLE,NFS,Performance,nfsperf-125,000019615,1163403,4.12.14-122.20,0,1
# Distro:      SLES12 SP5
# Modified:    2021 May 10
#
##############################################################################
# Copyright (C) 2021, SUSE LLC
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

import re
import os
import Core
import SUSE

META_CLASS = "SLE"
META_CATEGORY = "NFS"
META_COMPONENT = "Performance"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019615|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1163403"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

KERNEL_VERSION_FIXED = '4.12.14-122.20'
NFSMOUNTS = False

INSTALLED_VERSION = SUSE.compareKernel(KERNEL_VERSION_FIXED)
if( INSTALLED_VERSION >= 0 ):
	Core.updateStatus(Core.IGNORE, "Bug fixes applied in kernel version " + KERNEL_VERSION_FIXED + " or higher")
else:
	FSLIST = SUSE.getFileSystems()
	for FS in FSLIST:
		if( FS['Type'].lower() == 'nfs' or FS['Type'].lower() == 'nfs4' ):
			if( FS['Mounted'] ):
				NFSMOUNTS = True
	if( NFSMOUNTS ):
		Core.updateStatus(Core.WARN, "Writing large files to NFS mounts may be susceptible to performance degradation")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: NFS mounts not found")

Core.printPatternResults()

