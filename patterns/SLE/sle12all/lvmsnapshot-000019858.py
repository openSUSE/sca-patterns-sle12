#!/usr/bin/python
#
# Title:       Pattern for TID000019858
# Description: LVM snapshot changed state to Invalid and should be removed
# Source:      Package Version Pattern Template v0.3.3
# Options:     SLE,LVM,Snapshot,lvmsnapshot,000019858,0,2,0,0
# Modified:    2021 Apr 28
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
META_CATEGORY = "LVM"
META_COMPONENT = "Snapshot"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019858|META_LINK_TLDP=https://tldp.org/HOWTO/LVM-HOWTO/snapshotintro.html"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

LIMIT_CRIT = 90
LIMIT_WARN = 80
SNAPS = {}
SS_INVALID = []
SS_CRIT = []
SS_WARN = []
SS_MAX = ''
SS_MAX_VALUE = 0

##############################################################################
# Local Function Definitions
##############################################################################

def getLVMSnapshots():
	global SNAPS

	fileOpen = "lvm.txt"
	section = "lvs"
	content = []
	ATTRIBUTES = 2
	SNAPDATA = 5
	VOLTYPE = 0
	LVM_LV = 0
	LVM_VG = 1

	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				ENTRY = line.split()
				if( ENTRY[ATTRIBUTES][VOLTYPE].lower() == 's' ): # Snapshot found
					LVM_KEY = str(ENTRY[LVM_LV]) + "-" + str(ENTRY[LVM_VG])
					if( len(ENTRY) > SNAPDATA ): # Checks for the snapshot data field
						SNAPS[LVM_KEY] = [ENTRY[ATTRIBUTES],int(ENTRY[SNAPDATA].split('.')[0])]
					else:
						SNAPS[LVM_KEY] = [ENTRY[ATTRIBUTES],0]
	if( len(SNAPS) > 0 ):
		return True
	else:
		return False

def parseSnapshots():
	global SNAPS
	global LIMIT_CRIT
	global LIMIT_WARN
	global SS_MAX
	global SS_MAX_VALUE
	global SS_INVALID
	global SS_CRIT
	global SS_WARN

	ATTRIBUTES = 0
	USED_DATA = 1
	LVM_STATE = 4
	LVM_STATE_INVALID = 'I'

#	print(SNAPS)
	for key in SNAPS:
#		print(key)
#		print(SNAPS[key][ATTRIBUTES])
#		print(SNAPS[key][USED_DATA])
#		print(SNAPS[key][ATTRIBUTES][LVM_STATE])
		if( SNAPS[key][USED_DATA] > SS_MAX_VALUE ):
			SS_MAX = key
			SS_MAX_VALUE = SNAPS[key][USED_DATA]
		if( SNAPS[key][ATTRIBUTES][LVM_STATE] == LVM_STATE_INVALID ):
			SS_INVALID.append(key)
		elif( SNAPS[key][USED_DATA] >= LIMIT_CRIT ):
			SS_CRIT.append(key)
		elif( SNAPS[key][USED_DATA] >= LIMIT_WARN ):
			SS_WARN.append(key)

##############################################################################
# Main Program Execution
##############################################################################

if( getLVMSnapshots() ):
	parseSnapshots()
	if( len(SS_INVALID) > 0 ):
		Core.updateStatus(Core.CRIT, "Detected invalid LVM snapshot(s): " + ' '.join(SS_INVALID))
	elif( len(SS_CRIT) > 0 ):
		Core.updateStatus(Core.CRIT, "Fullest snapshot " + SS_MAX + " at " + str(SNAPS[SS_MAX][1]) + "%, Reaching space capacity: " + ' '.join(SS_CRIT))
	elif( len(SS_WARN) > 0 ):
		Core.updateStatus(Core.WARN, "Fullest snapshot " + SS_MAX + " at " + str(SNAPS[SS_MAX][1]) + "%, Monitor snapshots: " + ' '.join(SS_WARN))
	else:
		Core.updateStatus(Core.IGNORE, "Fullest snapshot " + SS_MAX + " at " + str(SNAPS[SS_MAX][1]) + "%")
else:
	Core.updateStatus(Core.ERROR, "ERROR: No LVM snapshots found")

Core.printPatternResults()

