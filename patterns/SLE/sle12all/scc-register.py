#!/usr/bin/python

# Title:       Look for unregistered products
# Description: Identify products not registered with SCC
# Modified:    2015 Apr 17
#
##############################################################################
# Copyright (C) 2015 SUSE LLC
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
META_CATEGORY = "Updates"
META_COMPONENT = "Registration"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Register"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_SCC=https://scc.suse.com/dashboard|META_LINK_Register=https://www.suse.com/products/server/how-to-buy/"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

##############################################################################
# Main Program Execution
##############################################################################

REQUIRED_VERSION = '2.25-173';
SC_INFO = SUSE.getSCCInfo();
if( Core.compareVersions(SC_INFO['version'], REQUIRED_VERSION) >= 0 ):
	Core.updateStatus(Core.IGNORE, "Supportconfig v" + str(SC_INFO['version']) + " meets minimum requirement")
else:
	Core.updateStatus(Core.WARN, "Supportconfig v" + str(SC_INFO['version']) + " NOT sufficient, " + str(REQUIRED_VERSION) + " or higher needed")	

Core.printPatternResults()


