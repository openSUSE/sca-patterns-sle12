#!/usr/bin/python

# Title:       Check for volume_list exit status
# Description: Validate volume_list does not generate exit 5
# Modified:    2015 Jul 15
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
# Overriden (eventually or in part) from Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "LVM"
META_COMPONENT = "Activation"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7016683|https://bugzilla.suse.com/show_bug.cgi?id=938098"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################


##############################################################################
# Main Program Execution
##############################################################################

SERVICE = 'lvm2-activation.service'
SERVICE_INFO = SUSE.getServiceDInfo(SERVICE)
LVM_CONFIG = SUSE.getConfigFileLVM('activation')
if "vgchange -aay" in SERVICE_INFO['ExecStart']: #auto activation detected
	print 'HERE'
else:
	Core.updateStatus(Core.ERROR, "LVM auto activation required")

Core.printPatternResults()


