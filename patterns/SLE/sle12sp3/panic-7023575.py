#!/usr/bin/python

# Title:       Check update_group_capacity on SLES12 SP3
# Description: System panic in update_group_capacity() due to a divide error
# Modified:    2018 Dec 13
#
##############################################################################
# Copyright (C) 2018 SUSE LLC
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

import os
import re
import Core
import SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Kernel"
META_COMPONENT = "Panic"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=7023575|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1096254"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def panicDetected():
	PANIC = re.compile("exception RIP.*update_group_capacity", re.IGNORECASE)
	FILE_OPEN = "boot.txt"
	SECTION = "dmesg"
	CONTENT = []
	if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
		for LINE in CONTENT:
			if PANIC.search(LINE):
				return True

	FILE_OPEN = "messages.txt"
	SECTION = "/var/log/warn"
	CONTENT = []
	if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
		for LINE in CONTENT:
			if PANIC.search(LINE):
				return True
	return False

##############################################################################
# Main Program Execution
##############################################################################

KERNEL_VERSION = '4.4.155-94.50'
INSTALLED_VERSION = SUSE.compareKernel(KERNEL_VERSION)
if( INSTALLED_VERSION < 0 ):
	if( panicDetected() ):
		Core.updateStatus(Core.CRIT, "A system panic from update_group_capacity detected, update system to resolve")
	else:
		Core.updateStatus(Core.WARN, "System panic may result from benmarks, update system to avoid")
else:
	Core.updateStatus(Core.IGNORE, "Kernel version is sufficient to avoid update_group_capacity panic")

Core.printPatternResults()


