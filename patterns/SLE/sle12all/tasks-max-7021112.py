#!/usr/bin/python

# Title:       Max Tasks Exceeded
# Description: Check for TasksCurrent approaching TasksMax
# Modified:    2017 Jul 20
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
META_CATEGORY = "SystemD"
META_COMPONENT = "Tasks"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=7021112|META_LINK_DevInfo=https://github.com/systemd/systemd/pull/3753"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

FILE_OPEN = "systemd.txt"
SECTIONS = {}
CRIT_PERCENT = 90
WARN_PERCENT = 80
CRITICAL_SERVICES = {}
WARNING_SERVICES = {}
CONTENT = {}
if Core.listSections(FILE_OPEN, CONTENT):
	for LINE in CONTENT:
		if "/systemctl show" in CONTENT[LINE]:
			SERVICE_NAME = CONTENT[LINE].split("'")[1]
			SERVICE_INFO = SUSE.getServiceDInfo(SERVICE_NAME)
			if ('TasksCurrent' in SERVICE_INFO.keys()):
				TASK_RATIO = int(SERVICE_INFO['TasksCurrent'])*100/int(SERVICE_INFO['TasksMax'])
				if( TASK_RATIO > 100 ):
					TASK_RATIO = 100
				if( SERVICE_INFO['MemoryCurrent'] != SERVICE_INFO['TasksCurrent'] ): #Means TasksCurrent is set to unlimited
					if( TASK_RATIO >= CRIT_PERCENT ):
						CRITICAL_SERVICES[SERVICE_NAME] = 1
					elif( TASK_RATIO >= WARN_PERCENT ):
						WARNING_SERVICES[SERVICE_NAME] = 1
#					print "INFO: " + str(SERVICE_NAME) + ": " + str(TASK_RATIO) + "% " + str(SERVICE_INFO['TasksCurrent']) + "/" + str(SERVICE_INFO['TasksMax'])

if( len(CRITICAL_SERVICES) > 0 ):
	if( len(WARNING_SERVICES) > 0 ):
		Core.updateStatus(Core.CRIT, "Services that have run out of tasks: " + " ".join(CRITICAL_SERVICES.keys()) + " " + " ".join(WARNING_SERVICES.keys()))
	else:
		Core.updateStatus(Core.CRIT, "Services that have run out of tasks: " + " ".join(CRITICAL_SERVICES.keys()))
elif( len(WARNING_SERVICES) > 0 ):
	Core.updateStatus(Core.WARN, "Services that may be running out of tasks: " + " ".join(WARNING_SERVICES.keys()))
else:
	Core.updateStatus(Core.IGNORE, "Services are within TasksMax limits")


Core.printPatternResults()


