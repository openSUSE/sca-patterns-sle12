#!/usr/bin/python3
#
# Title:       Pattern for TID000020338
# Description: crontab - More than 1000 entries in crontab file, can&#039;t install
# Source:      Package Version Pattern Template v0.3.8
# Options:     SLE,Cron,Limits,cronlimit,000020338,1187508,cronie,0,1.5.1-6.12.2,1
# Distro:      SLES12
# Modified:    2021 Jul 22
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
META_CATEGORY = "Cron"
META_COMPONENT = "Limits"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000020338|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1187508"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def bigUserCron():
	BIG_ENTRY_LIMIT = 100

	FILE_OPEN = "cron.txt"
	CONTENT = []
	IN_STATE = False
	ENTRIES = 0
	if Core.loadFullFile(FILE_OPEN, CONTENT):
		for LINE in CONTENT:
			if( IN_STATE ):
				if LINE.startswith("#==["):
					IN_STATE = False
					if( ENTRIES >= BIG_ENTRY_LIMIT ):
						return True
				else:
					ENTRIES += 1
			elif LINE.startswith("# /var/spool/cron/tabs/"):
				IN_STATE = True
				ENTRIES = 0
	else:
		Core.updateStatus(Core.ERROR, "ERROR: Empty file - " + FILE_OPEN)

	return False

def systemLogError():
	AFFECTED_LIST = {}
	IDX_LAST = -2
	fileOpen = "cron.txt"
	section = "/bin/systemctl status cron.service"
	content = []
	CONFIRMED = re.compile("CRON.*too many entries \(.*", re.IGNORECASE)
	if Core.getRegExSection(fileOpen, section, content):
		for line in content:
			if CONFIRMED.search(line):
				FILE = re.split(r'[()]', line)
				AFFECTED_LIST[FILE[IDX_LAST]] = True
	return AFFECTED_LIST

##############################################################################
# Main Program Execution
##############################################################################

RPM_NAME = 'cronie'
RPM_VERSION_FIXED = '2.0'
RPM_VERSION_BROKE = '1.4.11-59.13.1'
if( SUSE.packageInstalled(RPM_NAME) ):
	INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION_FIXED)
	if( INSTALLED_VERSION >= 0 ):
		Core.updateStatus(Core.IGNORE, "Bug fixes applied for " + RPM_NAME)
	else:
		INSTALLED_VERSION = SUSE.compareRPM(RPM_NAME, RPM_VERSION_BROKE)
		if( INSTALLED_VERSION == 0 ):
			if( bigUserCron() ):
				Core.updateStatus(Core.WARN, "User cron table files will be limited to 1000 entries")
			else:
				CRON_TABLES = systemLogError()
				if( len(CRON_TABLES) > 0 ):
					Core.updateStatus(Core.CRIT, "User cron table files have exceeded the entry limit: " + ' '.join(list(CRON_TABLES.keys())))
				else:
					Core.updateStatus(Core.IGNORE, "No individual cron entries to worry about")
		else:
			Core.updateStatus(Core.IGNORE, "Previously unaffected version of " + RPM_NAME + " installed")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + RPM_NAME + " not installed")


Core.printPatternResults()

