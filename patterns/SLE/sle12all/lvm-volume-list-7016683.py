#!/usr/bin/python

# Title:       Check for volume_list exit status
# Description: Validate volume_list does not generate exit 5
# Modified:    2015 Jul 30
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
	if( LVM_CONFIG ): # a valid lvm config file exists
		if( 'volume_list' in LVM_CONFIG.keys() ): # there is a volume_list entry in lvm.conf
			if( len(LVM_CONFIG['volume_list']) > 0 ): # there are values associated with the volume_list entry
				if( 'auto_activation_volume_list' in LVM_CONFIG.keys() ): # there is an auto_activation_volume_list entry in lvm.conf
					if( len(LVM_CONFIG['auto_activation_volume_list']) > 0 ): # there are values associated with the auto_activation_volume_list entry
						if set(LVM_CONFIG['volume_list']).issubset(LVM_CONFIG['auto_activation_volume_list']): # all required entries found in auto_activation_volume_list
							Core.updateStatus(Core.IGNORE, "All volume_list entries are found within the auto_activation_volume_list, ignore")
						else: # some volume_list entries are missing from the auto_activation_volume_list
							if( SERVICE_INFO['ExecMainStatus'] == '5' ): # found the error associated with missing auto_activation_volume_list entries
								Core.updateStatus(Core.WARN, "Missing auto_activation_volume_list entries in lvm.conf")
							else: # didn't fine the error associated with missing auto_activation_volume_list entries
								Core.updateStatus(Core.WARN, "An auto_activation_volume_list entry in lvm.conf may be needed to avoid errors")
					else: # no auto_activation_volume_list entries found
						if( SERVICE_INFO['ExecMainStatus'] == '5' ): # found the error associated with missing auto_activation_volume_list entries
							Core.updateStatus(Core.WARN, "Missing auto_activation_volume_list entries in lvm.conf")
						else: # didn't fine the error associated with missing auto_activation_volume_list entries
							Core.updateStatus(Core.WARN, "An auto_activation_volume_list entry in lvm.conf may be needed to avoid errors")
				else: # no auto_activation_volume_list entries found
					if( SERVICE_INFO['ExecMainStatus'] == '5' ): # found the error associated with missing auto_activation_volume_list entries
						Core.updateStatus(Core.WARN, "Missing auto_activation_volume_list entries in lvm.conf")
					else: # didn't fine the error associated with missing auto_activation_volume_list entries
						Core.updateStatus(Core.WARN, "An auto_activation_volume_list entry in lvm.conf may be needed to avoid errors")
			else: # volume_list is empty
				Core.updateStatus(Core.IGNORE, "The volume_list values are empty, ignore")
		elif( 'auto_activation_volume_list' in LVM_CONFIG.keys() ): # found auto_activation_volume_list that is used for vgchange -aay
			Core.updateStatus(Core.IGNORE, "The auto_activation_volume_list key matches the use of vgchange -aay, ignore")
		else:
			Core.updateStatus(Core.ERROR, "ERROR: LVM configuration file missing activation volume_list and auto_activation_volume_list")
	else: # no lvm.conf activation section found
		Core.updateStatus(Core.ERROR, "ERROR: LVM configuration file missing activation section")
else: # vgchange -aay auto activation is not in use
	Core.updateStatus(Core.ERROR, "ERROR: LVM auto activation required")

Core.printPatternResults()


