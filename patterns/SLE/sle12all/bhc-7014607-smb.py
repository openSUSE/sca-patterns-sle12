#!/usr/bin/python

# Title:       Samba SMB Basic Service Pattern
# Description: Checks to see if the service is installed, valid and running
# Modified:    2014 Feb 21
#
##############################################################################
# Copyright (C) 2014 SUSE LLC
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

import sys, os, Core, SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "Basic Health"
META_CATEGORY = "Samba"
META_COMPONENT = "SMB"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7014607"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

PACKAGE = "samba"
SERVICE = "smb.service"

##############################################################################
# Main Program Execution
##############################################################################

if( SUSE.packageInstalled(PACKAGE) ):
	SUSE.serviceDHealth(SERVICE)
else:
	Core.updateStatus(Core.ERROR, "Basic Service Health; Package Not Installed: " + str(PACKAGE))

Core.printPatternResults()


