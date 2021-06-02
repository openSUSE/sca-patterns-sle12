#!/usr/bin/python
#
# Title:       Pattern for TID000019943
# Description: Delayed outgoing packets causing NFS timeouts
# Source:      Kernel Package Version Pattern Template v0.1.2
# Options:     SLE,NFS,Timeout,nfstimeout_152,000019943,1183405,5.3.18-24.61,0,1
# Distro:      SLES12 SP5
# Modified:    2021 Jun 02
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
META_COMPONENT = "Timeout"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019943|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1183405"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def nfsMountsFound():
	fileOpen = "fs-diskio.txt"
	IDX_TYPE = 2
	if Core.isFileActive(fileOpen):
		content = []
		section = "bin/mount"
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if( ' type nfs ' in line ):
					return True
				elif( ' type nfs4 ' in line ):
					return True
	else:
		Core.updateStatus(Core.ERROR, "ERROR: File not found - " + fileOpen)
		
	return False

def invalidDefaultQdisc():
	fileOpen = "env.txt"
	section = "sysctl -a"
	content = []
	CONFIRMED = re.compile("net.core.default_qdisc = fq_codel", re.IGNORECASE)
	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if CONFIRMED.search(line):
					return False
	else:
		Core.updateStatus(Core.ERROR, "ERROR: File not found - " + fileOpen)

	return True

def pendingMessagesFound():
	fileOpen = "messages.txt"
	section = "/var/log/messages"
	content = []
	SERVERS = {}
	IDX_LAST = -1
	IDX_HOSTNAME = 1
	CONFIRMED = re.compile("kernel.*nfs.*server.*not responding, still trying", re.IGNORECASE)
	#2021-03-07T16:19:31.800974+00:00 vsa8173953 kernel: [1050705.946742] nfs: server hostname not responding, still trying
	if Core.getRegExSection(fileOpen, section, content):
		for line in content:
			if CONFIRMED.search(line):
				SERVERS[line.split(':')[IDX_LAST].split()[IDX_HOSTNAME]] = True

	return SERVERS

##############################################################################
# Main Program Execution
##############################################################################

KERNEL_VERSION_FIXED = '4.12.14-122.66'

INSTALLED_VERSION = SUSE.compareKernel(KERNEL_VERSION_FIXED)
if( INSTALLED_VERSION >= 0 ):
	Core.updateStatus(Core.IGNORE, "Bug fixes applied in kernel version " + KERNEL_VERSION_FIXED + " or higher")
else:
	if( nfsMountsFound() ):
		if( invalidDefaultQdisc() ):
			CONNECTIONS_DELAYED = pendingMessagesFound()
			if( len(CONNECTIONS_DELAYED) > 0 ):
				Core.updateStatus(Core.CRIT, "Detected NFS timeouts from delayed packets: " + ' '.join(CONNECTIONS_DELAYED.keys()))
			else:
				Core.updateStatus(Core.WARN, "NFS timeouts possible from delayed packets")
		else:
			Core.updateStatus(Core.IGNORE, "Work around net.core.default_qdisc=fq_codel applied")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: No NFS mounts found")

Core.printPatternResults()

