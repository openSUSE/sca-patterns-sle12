#!/usr/bin/python3

# Title:       rp_filter communication issues
# Description: Applying newer SLES Causing Communication Issues
# Modified:    2014 Jan 30
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

import sys, os, Core, SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Kernel"
META_COMPONENT = "Network"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7007649"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def getRPfilter():
	fileOpen = "env.txt"
	section = "/sbin/sysctl -a"
	VALUE = -1
	VALUE_ALL = -1
	VALUE_INT = -1
	content = {}
	if Core.getSection(fileOpen, section, content):
		for line in content:
			if "net.ipv4.conf.all.rp_filter" in content[line]:
#				print content[line]
				RP_LIST = content[line].split('=')
				VALUE_ALL = int(RP_LIST[1].strip())
				break
		for line in content:
			if content[line].startswith('net.ipv4.conf'):
				if '.all.rp_filter' in content[line] or '.default.rp_filter' in content[line]:
					continue
				elif '.rp_filter' in content[line]:
#					print content[line]
					RP_LIST = content[line].split('=')
					VALUE_INT = int(RP_LIST[1].strip())
					if( VALUE_ALL < VALUE_INT ):
						VALUE_TMP = VALUE_INT
					else:
						VALUE_TMP = VALUE_ALL
					if( VALUE_TMP == 1 ):
						VALUE = 1
						break
					else:
						if( VALUE_TMP > VALUE ):
							VALUE = VALUE_TMP
#	print "VALUE = " + str(VALUE)
	return int(VALUE)

##############################################################################
# Main Program Execution
##############################################################################

CHECK_LIST = [SUSE.SLE12GA, SUSE.SLE11SP1, SUSE.SLE10SP4]
NOT_FOUND = True
for AFFECTED in CHECK_LIST:
	KERN_VER = SUSE.compareKernel(AFFECTED)
	if( KERN_VER >= 0 ):
		NOT_FOUND = False
		RP_FILTER = getRPfilter()
		if( RP_FILTER == 0 ):
			Core.updateStatus(Core.IGNORE, "RP_FILTER within known limits")
		elif( RP_FILTER == 1 ):
			Core.updateStatus(Core.WARN, "Potential network communication issues due to rp_filter")
		else:
			Core.updateStatus(Core.REC, "Potential network communication issues due to rp_filter")
		break

if( NOT_FOUND ):
	Core.updateStatus(Core.ERROR, "Outside the kernel scope, skipping rp_filter")

Core.printPatternResults()


