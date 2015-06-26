#!/usr/bin/python

# Title:       FIPS Selftest Errors
# Description: FIPS enabled, but no FIPS packages installed
# Modified:    2015 Jun 26
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
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7016637"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

FIPS = SUSE.getBasicFIPSData()
if( FIPS['Enabled'] ):
	if( FIPS['Installed'] ):
		Core.updateStatus(Core.IGNORE, "FIPS enabled and installed")
	else:
		Core.updateStatus(Core.CRIT, "FIPS enabled, but missing required FIPS packages")
else:
		Core.updateStatus(Core.ERROR, "ERROR: FIPS disabled, not applicable")

Core.printPatternResults()

