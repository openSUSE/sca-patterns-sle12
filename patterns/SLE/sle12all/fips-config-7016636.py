#!/usr/bin/python

# Title:       FIPS Installed but Fails
# Description: FIPS installed but not working in kernel mode
# Modified:    2015 Jun 25
#
##############################################################################
# Copyright (C) 2015 SUSE LINUX Products GmbH, Nuernberg, Germany
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
META_CATEGORY = "Config"
META_COMPONENT = "FIPS"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7016636"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def getBasicFIPSData():
	FIPS = {'Installed': False, 'Enabled': False, 'Grub': False, 'Initrd': None}
	
	if( SUSE.packageInstalled('dracut-fips') ):
		FIPS['Installed'] = True
		CONTENT = []
		if Core.getRegExSection('proc.txt', '/proc/sys/crypto/fips_enabled', CONTENT):
			for LINE in CONTENT:
				if( LINE.isdigit() ):
					if( int(LINE) > 0 ):
						FIPS['Enabled'] = True
		GRUB2 = SUSE.getGrub2Config()
		if( "fips=1" in GRUB2['GRUB_CMDLINE_LINUX_DEFAULT'].lower() ):
			FIPS['Grub'] = True
		if Core.getRegExSection('boot.txt', '/bin/lsinitrd', CONTENT):
			FOUND = False
			MODS = False
			for LINE in CONTENT:
				TEST = LINE.lower()
				if( MODS ):
					if TEST.startswith("=="):
						MODS = False
						break
					elif TEST.startswith("fips"):
						FOUND = True
						break
				elif TEST.startswith("dracut modules:"):
					MODS = True

	return FIPS

##############################################################################
# Main Program Execution
##############################################################################

FIPS = getBasicFIPSData()
if( FIPS['Installed'] ):
	print "FIPS", FIPS
else:
	Core.updateStatus(Core.ERROR, "FIPS packages missing, not applicable")

Core.printPatternResults()

