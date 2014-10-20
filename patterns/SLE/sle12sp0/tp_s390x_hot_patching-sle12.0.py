#!/usr/bin/python

# Title:       Technology Preview: s390x 1.4.2.13.4 Hot-patching Support
# Description: Identify SLE12 technology preview features
# Modified:    2014 Oct 20
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

import os
import Core
import SUSE

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Technology"
META_COMPONENT = "Preview"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_Note"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_Note=https://www.suse.com/releasenotes/x86_64/SUSE-SLES/12/#Intro.Support.Techpreviews|META_LINK_Support=https://www.suse.com/releasenotes/x86_64/SUSE-SLES/12/#fate-315333|META_LINK_Fate=https://fate.suse.com/315333|META_LINK_Docs=http://gcc.gnu.org/onlinedocs/gcc/"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

SERVER = SUSE.getHostInfo()
PACKAGE = 'gcc'
if "s390x" in SERVER['Architecture'].lower():
	if( SUSE.packageInstalled(PACKAGE) ):
		Core.updateStatus(Core.WARN, "Hot Patching support in gcc on s390x is unsupported technology preview software")
	else:
		Core.updateStatus(Core.ERROR, "Package not installed: " + str(PACKAGE))
else:
	Core.updateStatus(Core.ERROR, "Invalid architecture: " + str(SERVER['Architecture']))

Core.printPatternResults()


