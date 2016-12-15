#!/usr/bin/python

# Title:       Insufficient Disk Space on Boot
# Description: Kernel upgrade fails due to insufficient space on boot partition
# Distro:      SLE12
# Modified:    2016 Dec 14
#
##############################################################################
# Copyright (C) 2016 SUSE LINUX Products GmbH, Nuernberg, Germany
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
META_CATEGORY = "Update"
META_COMPONENT = "Disk Space"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc?id=7018350"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def errorFound():
	FILE_OPEN = "updates.txt"
	SECTION = "/var/log/zypp/history"
	CONTENT = []
	FAILED_UPDATE = re.compile("installing package.*needs.*on.*/boot filesystem", re.IGNORECASE)
	if Core.getRegExSectionRaw(FILE_OPEN, SECTION, CONTENT):
		for LINE in CONTENT[::-1]: #reverse the list order
			if FAILED_UPDATE.search(LINE):
				return True
	return False

def DeHumanize(ConvertString):
	MATCH = re.match(r"([0-9.]+)([a-zA-Z]+)", ConvertString, re.I)
	if ( MATCH ):
		AMOUNT = MATCH.group(1)
		TYPE = MATCH.group(2).lower()
	else:
		MATCH = re.match(r"([0-9.]+)", ConvertString, re.I)
		if ( MATCH ):
			AMOUNT = MATCH.group(1)
			TYPE = "b"
		else:
			TYPE = "Failed"

	CONVERTED_AMOUNT = 0
	if( TYPE == "b" ):
		CONVERTED_AMOUNT = int(float(AMOUNT) * 1024 ** 0)
	elif( TYPE == "k" ):
		CONVERTED_AMOUNT = int(float(AMOUNT) * 1024 ** 1)
	elif( TYPE == "m" ):
		CONVERTED_AMOUNT = int(float(AMOUNT) * 1024 ** 2)
	elif( TYPE == "g" ):
		CONVERTED_AMOUNT = int(float(AMOUNT) * 1024 ** 3)
	elif( TYPE == "t" ):
		CONVERTED_AMOUNT = int(float(AMOUNT) * 1024 ** 4)
	elif( TYPE == "p" ):
		CONVERTED_AMOUNT = int(float(AMOUNT) * 1024 ** 5)
	elif( TYPE == "e" ):
		CONVERTED_AMOUNT = int(float(AMOUNT) * 1024 ** 6)
	elif( TYPE == "z" ):	
		CONVERTED_AMOUNT = int(float(AMOUNT) * 1024 ** 7)
	else:
		CONVERTED_AMOUNT = -1
#	print "ConvertString: " + str(ConvertString) + " => " + str(AMOUNT) + ", " + str(TYPE) + " = " + str(CONVERTED_AMOUNT)

	return CONVERTED_AMOUNT

def BootDetails():
	FSLIST = SUSE.getFileSystems()
	for FS in FSLIST:
		if ("/boot" == FS['MountPoint']):
			C_TOTAL = DeHumanize(FS['Size'])
			C_USED  = DeHumanize(FS['UsedSpace'])
			C_FREE  = DeHumanize(FS['AvailSpace'])
			return {'total': C_TOTAL, 'used': C_USED, 'free': C_FREE}
	return {}

##############################################################################
# Main Program Execution
##############################################################################

AVAIL_REQUIRED =  52428800    #50M
AVAIL_RECOMMENDED = 104857600 #100M
if( errorFound() ):
	Core.updateStatus(Core.CRIT, "Update failure from insufficient disk space on /boot")
else:
	BOOT_INFO = BootDetails()
	if( BOOT_INFO ):
		if ( BOOT_INFO['free'] == -1 ):
			Core.updateStatus(Core.ERROR, "Unknown /boot free space value")
		elif ( BOOT_INFO['free'] < AVAIL_REQUIRED ):
			Core.updateStatus(Core.CRIT, "Update failure probible from insufficient disk space on /boot")
		elif ( BOOT_INFO['free'] < AVAIL_RECOMMENDED ):
			Core.updateStatus(Core.WARN, "Sever update may fail from insufficient disk space on /boot")
		else:
			Core.updateStatus(Core.IGNORE, "Sufficient disk space on /boot for update")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: No /boot partition, ignore")

Core.printPatternResults()


