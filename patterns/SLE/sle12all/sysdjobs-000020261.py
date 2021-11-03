#!/usr/bin/python3
#
# Title:       Pattern for TID000020261
# Description: Troubleshooting systemd jobs that are hung or stuck
# Source:      Basic Python Pattern Template v0.3.4
# Options:     SLE,SystemD,Jobs,sysdjobs,000020261,0,1,0,0
# Modified:    2021 May 27
#
##############################################################################
# Copyright (C) 2021 SUSE LLC
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
META_CATEGORY = "SystemD"
META_COMPONENT = "Jobs"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000020261"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def getJobsStuck():
	global JOBS_RUNNING
	global JOBS_WAITING
	fileOpen = "systemd.txt"
	section = "systemctl.*list-jobs"
	content = []
	RC = False
	STATE = False
	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if( STATE ):
					PARTS = line.split()
					if "running" in PARTS[-1]:
						JOBS_RUNNING.append(PARTS[1])
						RC = True
					elif "waiting" in PARTS[-1]:
						JOBS_WAITING.append(PARTS[1])
						RC = True
				elif( line.startswith("JOB")):
					STATE = True
	return RC

##############################################################################
# Main Program Execution
##############################################################################

JOBS_RUNNING = []
JOBS_WAITING = []

if( getJobsStuck() ):
	if( len(JOBS_RUNNING) > 0 ):
		if( len(JOBS_WAITING) > 0 ):
			Core.updateStatus(Core.CRIT, "Detected running and waiting systemd jobs, still running: " + ' '.join(JOBS_RUNNING))
		else:
			Core.updateStatus(Core.WARN, "Detected running systemd jobs: " + ' '.join(JOBS_RUNNING))
	else:
		Core.updateStatus(Core.IGNORE, "No running jobs to process")
else:
	Core.updateStatus(Core.ERROR, "No systemd jobs found")

Core.printPatternResults()

