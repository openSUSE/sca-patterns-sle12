#!/usr/bin/python3
#
# Title:       Pattern for TID000020680
# Description: trace_printk() Messages in System Logs
# Source:      Basic Python Pattern Template v1.0.0
# Options:     SLE,Kernel,Debug,traceprintk,000020680,0,1,0,0
# Modified:    2022 Jul 06
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

import re
import os
import Core

META_CLASS = "SLE"
META_CATEGORY = "Kernel"
META_COMPONENT = "Debug"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000020680|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1200133"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def traceFound():
	fileOpen = "boot.txt"
	section = "dmesg -T"
	content = []
	CONFIRMED = re.compile("trace_printk()", re.IGNORECASE)
	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if CONFIRMED.search(line):
					return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

if( traceFound() ):
	Core.updateStatus(Core.WARN, "Detected trace_printk debug kernel which is unsafe for production use")
else:
	Core.updateStatus(Core.IGNORE, "trace_printk not found")

Core.printPatternResults()

