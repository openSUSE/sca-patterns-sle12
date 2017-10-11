#!/usr/bin/python

# Title:       Module is unknown
# Description: Module is unknown and cannot login at the console
# Modified:    2017 Oct 07
#
##############################################################################
# Copyright (C) 2017 SUSE LINUX Products GmbH, Nuernberg, Germany
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
import SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "PAM"
META_COMPONENT = "Module"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=7022033"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

MISSING_MODULE = re.compile("PAM unable to dlopen\(.*\): .*cannot open shared object file: No such file or directory", re.IGNORECASE)
FAILED_LOGIN = re.compile("FAILED LOGIN SESSION.*Module is unknown", re.IGNORECASE)
FILE_OPEN = "messages.txt"
MODULES = {}
FAILED = False

SECTION = "/var/log/warn"
CONTENT = []
if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
	for LINE in CONTENT:
		if MISSING_MODULE.search(LINE):
			MOD = LINE.split('(')[1].split(')')[0]
			MODULES[MOD] = True
		elif FAILED_LOGIN.search(LINE):
			FAILED = True

SECTION = "/var/log/messages"
CONTENT = []
if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
	for LINE in CONTENT:
		if MISSING_MODULE.search(LINE):
			MOD = LINE.split('(')[1].split(')')[0]
			MODULES[MOD] = True
		elif FAILED_LOGIN.search(LINE):
			FAILED = True

if( MODULES ):
	if( FAILED ):
		Core.updateStatus(Core.CRIT, "Login failures due to unknown PAM modules: " + ' '.join(MODULES))
	else:
		Core.updateStatus(Core.WARN, "Detected unknown PAM modules: " + ' '.join(MODULES))
else:
	Core.updateStatus(Core.IGNORE, "No unknown PAM modules detected.")

Core.printPatternResults()


