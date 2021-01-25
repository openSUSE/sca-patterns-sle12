#!/usr/bin/python

# Title:       Side-channel AttackeD DNS
# Description: Security Vulnerability: SADDNS attack (CVE-2020-25705)
# Distro:      SLES12 SP2
# Modified:    2021 Jan 21
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

##############################################################################
# Module Definition
##############################################################################

import re
import os
import Core
import SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Security"
META_COMPONENT = "DNS"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019786|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1175721|META_LINK_CVE=https://www.suse.com/security/cve/CVE-2020-25705/|META_LINK_SADDNS=https://www.saddns.net/"

KERNEL_VERSION = '4.4.121-92.146'
DNS_PACKAGE = 'bind'
DNS_SERVICE = 'named'
RC_DNS_ENABLED = 1
RC_DNS_DISABLED = 0
RC_DNS_ERROR = -1

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)
##############################################################################
# Local Function Definitions
##############################################################################

def workAroundApplied():
	fileOpen = "network.txt"
	section = "iptables -t filter"
	content = {}
	IN_STATE = False
	WORK_AROUND = re.compile("DROP.*icmp.*icmptype")
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if IN_STATE:
				if "Chain" in content[line]: # we reached the end of the output chain
					return False
				elif WORK_AROUND.search(content[line]): # we find the workaround
					return True
			elif "Chain OUTPUT" in content[line]: # the workaround only applies in the output chain
				IN_STATE = True
	return False

def namedStatus():
	fileOpen = "dns.txt"
	section = "chkconfig named --list"
	content = {}
	RC = RC_DNS_ERROR
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if content[line].startswith(DNS_SERVICE):
				if ":on" in content[line]:
					RC = RC_DNS_ENABLED
				else:
					RC = RC_DNS_DISABLED
	return RC

##############################################################################
# Main Program Execution
##############################################################################

ACTIVE_VERSION = SUSE.compareKernel(KERNEL_VERSION)
if( ACTIVE_VERSION < 0 ):
	if( SUSE.packageInstalled(DNS_PACKAGE) ):
		SERVICE_INFO = namedStatus()
		if( SERVICE_INFO == RC_DNS_DISABLED ):
			if( workAroundApplied() ):
				Core.updateStatus(Core.WARN, "SAD DNS security risk detected, but workaround applied, update server for fixes")
			else:
				Core.updateStatus(Core.IGNORE, "Service is disabled: " + str(DNS_SERVICE))
		elif( SERVICE_INFO == RC_DNS_ENABLED ):
			if( workAroundApplied() ):
				Core.updateStatus(Core.WARN, "SAD DNS security risk detected, but workaround applied, update server for fixes")
			else:
				Core.updateStatus(Core.CRIT, "SAD DNS security risk detected, update server for fixes")
		else:
				Core.updateStatus(Core.WARN, "Potential SAD DNS security risk if named enabled, update server for fixes")
	else:
		Core.updateStatus(Core.ERROR, "The package " + DNS_PACKAGE + " is NOT installed")	
else:
	Core.updateStatus(Core.IGNORE, "SAD DNS security risk resolved in kernel version " + KERNEL_VERSION)

Core.printPatternResults()

