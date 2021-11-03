#!/usr/bin/python3

# Title:       vNUMA vs.VCPU hotplug on VMware
# Description: checks for vNUMA vs.VCPU hotplug on VMware
# Modified:    2014 Oct 29
#
##############################################################################
# Copyright (C) 2014 SUSE LLC
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
#   Jason Record (jrecord@suse.com)
#
##############################################################################

##############################################################################
# Module Definition
##############################################################################

import re
import os
import Core

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Memory"
META_COMPONENT = "NUMA"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7015827|META_LINK_VMware=http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=2040375"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def VMwareFound():
	fileOpen = "basic-environment.txt"
	section = "Virtualization"
	content = {}
	STATE = False
	MAN = re.compile("^Manufacturer:.*VMware", re.IGNORECASE)
	ID = re.compile("^Identity:.*Virtual Machine", re.IGNORECASE)
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if( STATE ):
				if ID.search(content[line]):
					return True
			elif MAN.search(content[line]):
				STATE = True
	return False

def getCPUCount():
	fileOpen = "hardware.txt"
	section = "/proc/cpuinfo"
	content = {}
	COUNT = 0
	CPU = re.compile("^processor\s*:")
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if CPU.search(content[line]):
				COUNT += 1
#	print "Processor count: " + str(COUNT)
	return COUNT

def getNUMAInfo():
	fileOpen = "memory.txt"
	section = "numactl --hardware"
	content = {}
	INFO = {'Enabled': False, 'MaxNode': -1}
	NODE_COUNT = 0
	NODE = re.compile("^node \d cpus:")
	if Core.getSection(fileOpen, section, content):
		for line in content:
#			print "Checking => " + str(content[line])
			if NODE.search(content[line]):
				NODE_COUNT += 1
				LINE_LIST = content[line].split()
				del LINE_LIST[0]
				del LINE_LIST[0]
				del LINE_LIST[0]
				if( len(LINE_LIST) > INFO['MaxNode'] ):
					INFO['MaxNode'] = len(LINE_LIST)
#	print "Node Count: " + str(NODE_COUNT)
	if( NODE_COUNT > 1 ):
		INFO['Enabled'] = True
#	print "Numa info: " + str(INFO)
	return INFO

##############################################################################
# Main Program Execution
##############################################################################

if( VMwareFound() ):
	NUMA = getNUMAInfo()
	if( NUMA['Enabled'] ):
		CPUS = getCPUCount()
		if( NUMA['MaxNode'] == CPUS ):
			Core.updateStatus(Core.WARN, "Detected potential VCPU and vNUMA conflict, consider diabling one")
		else:
			Core.updateStatus(Core.IGNORE, "No vNUMA conflict detected")
	else:
		Core.updateStatus(Core.ERROR, "NUMA disabled, skipping vNUMA conflict check")
else:
	Core.updateStatus(Core.ERROR, "Not VMware, skipping vNUMA conflict check")
Core.printPatternResults()

