#!/usr/bin/python3
#
# Title:       Pattern for TID000020694
# Description: Azure Accelerated Networking fails
# Source:      Basic Python Pattern Template v1.0.0
# Options:     SLE,Network,Acceleration,azurenetaccel,000020694,1199853,3,0,0
# Modified:    2022 Jul 14
#
##############################################################################
# Copyright (C) 2022 SUSE LLC
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
import SUSE

META_CLASS = "SLE"
META_CATEGORY = "Network"
META_COMPONENT = "Acceleration"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000020694|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1199853"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def acceleratedNetworking():
#	Source: https://docs.microsoft.com/en-us/azure/virtual-network/create-vm-accelerated-networking-cli#confirm-that-accelerated-networking-is-enabled
	fileOpen = "hardware.txt"
	section = "bin/lspci -b"
	content = []
	CONFIRMED = re.compile("Ethernet controller: Mellanox Technologies MT27500/MT27520 Family \[ConnectX-3/ConnectX-3 Pro Virtual Function\]", re.IGNORECASE)
	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if CONFIRMED.search(line):
					return True
	return True

def networkError():
	global IFACE
	global DRIVER_NAME
	NET_DOWN = []
	fileOpen = "boot.txt"
	section = "bin/dmesg -T"
	content = []
	IDX_IFACE = 6

	NETWORKS = SUSE.getNetworkInterfaces()
	#print("IFACE = " + str(IFACE))
	for DEVICE in NETWORKS.keys():
		if( NETWORKS[DEVICE]['state'] == 'DOWN'):
			NET_DOWN.append(DEVICE)

	if( len(NET_DOWN) > 0 ):
		CONFIRMED = re.compile(str(DRIVER_NAME) + ".*Close port called", re.IGNORECASE)
		if Core.isFileActive(fileOpen):
			if Core.getRegExSection(fileOpen, section, content):
				for line in content:
					if CONFIRMED.search(line):
						IFACE = line.split()[IDX_IFACE][:-1]
						if IFACE in NET_DOWN:
							return True

	return False

##############################################################################
# Main Program Execution
##############################################################################

IFACE = ''
DRIVER_NAME = 'mlx4_en'
DRIVER_INFO = SUSE.getDriverInfo(DRIVER_NAME)
if( DRIVER_INFO['loaded'] ):
	if( acceleratedNetworking() ):
		if( networkError() ):
			Core.updateStatus(Core.WARN, "Detected accelerated networking failure on " + str(IFACE))
		else:
			Core.updateStatus(Core.IGNORE, "IGNORE: No networking errors found")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: Accelerated networking not configured")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + str(DRIVER_NAME) + ": Mellanox driver not loaded")

Core.printPatternResults()

