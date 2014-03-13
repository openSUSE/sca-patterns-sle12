#!/usr/bin/python

# Title:       Basic Health Check - CPU Load
# Description: Processes Waiting for Run Queue (Kernel Load)
# Modified:    2013 Dec 09
#
##############################################################################
# Copyright (C) 2013 SUSE LLC
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

import sys, os, Core, SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "Basic Health"
META_CATEGORY = "SLE"
META_COMPONENT = "Kernel"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7002722|META_LINK_Web=http://blog.scoutapp.com/articles/2009/07/31/understanding-load-averages|META_LINK_Wikipedia=http://en.wikipedia.org/wiki/Load_%28computing%29"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def getCPUCount():
	fileOpen = "proc.txt"
	section = "/proc/cpuinfo"
	content = {}
	CPUS = 0
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if "processor" in content[line]:
				CPUS += 1
	return CPUS

def getAverageLoads():
	fileOpen = "basic-health-check.txt"
	section = "/usr/bin/uptime"
	content = {}
	CPU_AVG = []
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if "load average" in content[line]:
				NUM = content[line].split()
				for VALUE in [NUM[-3], NUM[-2], NUM[-1]]:
					if( VALUE[-1] == ',' ):
						VALUE = VALUE[:-1]
					VALUE = VALUE.replace(',','.')
					CPU_AVG.append(float(VALUE))
	return CPU_AVG

##############################################################################
# Main Program Execution
##############################################################################

CPU_COUNT = getCPUCount()
CPU_LOADS = getAverageLoads()
OPTIMAL = 75
WARNING = 90
CRITICAL = 110
if( len(CPU_LOADS) == 0 ):
	Core.updateStatus(Core.ERROR, "ERROR: Invalid CPU load calculation, no CPU loads found")
else:
	CPU_LOAD = round(sum(CPU_LOADS)/len(CPU_LOADS), 2)
	CPU_LOAD_PERCENT = int(CPU_LOAD * 100 / CPU_COUNT)

if( CPU_LOAD_PERCENT <= OPTIMAL ):
	Core.updateStatus(Core.SUCC, str(CPU_LOAD_PERCENT) + "% CPU load within limits, CPUs: " + str(CPU_COUNT) + ", Load Average: " + str(CPU_LOAD))
elif( CPU_LOAD_PERCENT >= CRITICAL ):
	Core.updateStatus(Core.CRIT, str(CPU_LOAD_PERCENT) + "% CPU load is excessive, CPUs: " + str(CPU_COUNT) + ", Load Average: " + str(CPU_LOAD))
elif( CPU_LOAD_PERCENT >= WARNING ):
	Core.updateStatus(Core.WARN, str(CPU_LOAD_PERCENT) + "% CPU load is heavy, CPUs: " + str(CPU_COUNT) + ", Load Average: " + str(CPU_LOAD))
elif( CPU_LOAD_PERCENT > OPTIMAL ):
	Core.updateStatus(Core.WARN, str(CPU_LOAD_PERCENT) + "% CPU load is full, CPUs: " + str(CPU_COUNT) + ", Load Average: " + str(CPU_LOAD))
else:
	Core.updateStatus(Core.SUCC, str(CPU_LOAD_PERCENT) + "% CPU load, CPUs: " + str(CPU_COUNT) + ", Load Average: " + str(CPU_LOAD))

Core.printPatternResults()


