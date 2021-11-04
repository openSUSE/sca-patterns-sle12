#!/usr/bin/python3

# Title:       yast clone_system fails on ntp.conf
# Description: YaST clone_system module errors on ntp.conf changes
# Modified:    2017 Oct 11
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

import os
import Core
import SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "YaST"
META_COMPONENT = "Cloning"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=7021385|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1058510"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def cloneSystemAttempted():
	FILE_OPEN = "y2log.txt"
	SECTION = "/var/log/YaST2/y2log"
	CONTENT = []
	if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
		for LINE in CONTENT:
			if "clone_system.rb" in LINE:
				return True
	return False

def validAutoinst():
	FILE_OPEN = "y2log.txt"
	SECTION = "/root/autoinst.xml"
	CONTENT = []
	if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
		for LINE in CONTENT:
			if '<peer>' in LINE:
				return True
	return False

def susceptibleNTPConfig():
	FILE_OPEN = "ntp.txt"
	SECTION = "/etc/ntp.conf"
	CONTENT = []
	SERVER = False
	FUDGE = False
	if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
		for LINE in CONTENT:
			if 'server' in LINE.lower():
				SERVER = True
			if 'fudge' in LINE.lower():
				FUDGE = True
	if( SERVER and FUDGE ):
		return True
	else:
		return False

##############################################################################
# Main Program Execution
##############################################################################

RPM_NAME = 'yast2-ntp-client'
RPM_VERSION = '3.2.14-2.5.11'
if( SUSE.packageInstalled(RPM_NAME) ):
	INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION)
	if( INSTALLED_VERSION <= 0 ):
		if( susceptibleNTPConfig() ):
			if( cloneSystemAttempted() ):
				Core.updateStatus(Core.CRIT, "Detected NTP configuration issue when cloning system, update server for fixes")
			else:
				Core.updateStatus(Core.WARN, "Susceptible to NTP configuration issue when cloning system, update server for fixes")
		else:
			Core.updateStatus(Core.WARN, "NTP configuration okay, but could fail if modified before cloning")
	else:
		Core.updateStatus(Core.IGNORE, "NTP Configuration issue resolved with system update")
else:
	Core.updateStatus(Core.ERROR, "ERROR: RPM package not installed: " + RPM_NAME)

Core.printPatternResults()


