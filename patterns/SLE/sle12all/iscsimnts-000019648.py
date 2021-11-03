#!/usr/bin/python3
#
# Title:       Pattern for TID000019648
# Description: Proper mount options for iSCSI drives
# Source:      Basic Python Pattern Template v0.3.4
# Options:     SLE,Storage,iSCSI,iscsimnts,000019648,0,2,1,0
# Modified:    2021 May 04
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
import SUSE

META_CLASS = "SLE"
META_CATEGORY = "Storage"
META_COMPONENT = "iSCSI"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019648"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

DISPLAY_DEVICE = ''
FILESYSTEMS = {}

##############################################################################
# Local Function Definitions
##############################################################################

def iscsiDevice(DEV):
#	print(" iscsiDevice Evaluating: " + str(DEV))
	fileOpen = "fs-diskio.txt"
	section = "ls -lR.*/dev/disk/"
	content = []
	CONFIRMED = re.compile(" ip-.*-iscsi-.*/" + str(DEV) + "$", re.IGNORECASE)

	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if CONFIRMED.search(line):
					return True
	return False

def getLinkedDMDevice(CHECK_DEV):
#	print(" getLinkedDMDevice Processing: " + str(CHECK_DEV))
	fileOpen = "fs-diskio.txt"
	section = "ls -lR.*/dev/disk/"
	content = []
	CONFIRMED = re.compile("dm-name-.* -> ../../" + str(CHECK_DEV) + "$", re.IGNORECASE)
	DEV_INDEX = 7
	DEV_FULL = ''

	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if CONFIRMED.search(line):
					DEV_FULL = line.split()[DEV_INDEX].replace('dm-name-', '')

#	print(" getLinkedDMDevice Returns: " + str(DEV_FULL))
	return DEV_FULL

def getDeviceLinked(CHECK_DEV):
#	print(" getDeviceLinked Processing: " + str(CHECK_DEV))
	fileOpen = "fs-diskio.txt"
	section = "ls -lR.*/dev/disk/"
	content = []
	CONFIRMED = re.compile(str(CHECK_DEV) + " -> ../../", re.IGNORECASE)
	LAST_FIELD = -1
	DEV_FULL = ''

	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if CONFIRMED.search(line):
					DEV_FULL = line.split('/')[LAST_FIELD]

#	print(" getDeviceLinked Returns: " + str(DEV_FULL))
	return DEV_FULL

def getLVMDevice(LVM_DEV):
	FIRST_FIELD = 0
	LAST_FIELD = -1
	LVM_VG = LVM_DEV.split('/')[LAST_FIELD].split('-')[FIRST_FIELD]
#	print(" getLVMDevice Processing: " + str(LVM_DEV) + ", VG: " + str(LVM_VG))

	fileOpen = "lvm.txt"
	section = "/pvs"
	content = []
	CONFIRMED = re.compile(" " + str(LVM_VG) + " ")

	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if CONFIRMED.search(line):
					return line.split()[FIRST_FIELD]
	return ''

def getMPIODevice(MPIO_DEV):
	LAST_FIELD = -1
	DEV_INDEX = 2
	FIRST_MPIO_DEV = ''
#	print(" getMPIODevice Processing: " + str(MPIO_DEV))
	fileOpen = "mpio.txt"
	section_devices = "ls -lR.*/dev/disk/"
	section_mpiolist = "/multipath -ll"
	content = []

	MPIO_DEV_BASE = MPIO_DEV.split('/')[LAST_FIELD]
	if( '-part' in MPIO_DEV ): # The LUN without a partition designation is needed to find the device in multipath -ll
		MPIO_DEV_PARTS = MPIO_DEV_BASE.split('-')
		MPIO_DEV_PARTS.pop()
		CHECK_DEV = '-'.join(MPIO_DEV_PARTS)
	else:
		CHECK_DEV = MPIO_DEV_BASE

	MPIO_LINK = re.compile("dm-name-" + str(CHECK_DEV) + " -> ../../", re.IGNORECASE)
	DM_MPIO_DEV = ''
	STATE = False

	content = []
	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section_devices, content):
			for line in content:
				if MPIO_LINK.search(line):
					DM_MPIO_DEV = line.split('/')[LAST_FIELD]
		if( 'dm-' in DM_MPIO_DEV ):
			WWID_LIST = re.compile(" " + str(DM_MPIO_DEV) + " ")
			FIND_DEV = re.compile(r'\d+:\d+:\d+:\d+')
			content = []
			if Core.getRegExSection(fileOpen, section_mpiolist, content):
				for line in content:
					if( STATE ):
						if FIND_DEV.search(line):
							DEV_PARTS = line.split()
							for DEV_INDEX, PART in enumerate(DEV_PARTS):
								if FIND_DEV.search(PART):
									DEV_INDEX += 1
									break

							FIRST_MPIO_DEV = line.split()[DEV_INDEX]
							STATE = False
							break
					elif WWID_LIST.search(line):
						STATE = True

	return FIRST_MPIO_DEV

def processDMDevice(DM_DEV):
#	print(" processDMDevice Processing: " + str(DM_DEV))
	global DISPLAY_DEVICE
	LAST_FIELD = -1

	if( DM_DEV.startswith('dm-') ):
		DEV_LINKED = getLinkedDMDevice(DM_DEV)
	else:
		DEV_LINKED = DM_DEV

	LVM_DEVICE = getLVMDevice(DEV_LINKED)
	if( len(LVM_DEVICE) > 0 ):
#		print(" Found LVM Device Mapper: " + str(LVM_DEVICE))
		if( iscsiDevice(LVM_DEVICE.split('/')[LAST_FIELD]) ):
#			print(" + Adding iSCSI LVM device: " + str(DISPLAY_DEVICE))
			ISCSI_DEVS[DISPLAY_DEVICE] = True
		elif( LVM_DEVICE.startswith('/dev/mapper/') ):
			MPIO_DEVICE = getMPIODevice(LVM_DEVICE)
			if( len(MPIO_DEVICE) > 0 ):
#				print(" Found MPIO Device Mapper: " + str(MPIO_DEVICE))
				if( iscsiDevice(MPIO_DEVICE) ):
#					print(" + Adding iSCSI MPIO device: " + str(DISPLAY_DEVICE))
					ISCSI_DEVS[DISPLAY_DEVICE] = True
#			else:
#				print("  PUNT DM device: " + str(DISPLAY_DEVICE))
	else:
		DM_DEVICE = getMPIODevice(DEV_LINKED)
		if( len(DM_DEVICE) > 0 ):
#			print(" Found MPIO Device Mapper: " + str(DM_DEVICE))
			if( iscsiDevice(DM_DEVICE) ):
#				print(" + Adding iSCSI MPIO device: " + str(DISPLAY_DEVICE))
				ISCSI_DEVS[DISPLAY_DEVICE] = True
#		else:
#			print("  PUNT DM device: " + str(DISPLAY_DEVICE))

def iscsiMounts():
	global DISPLAY_DEVICE
	global ISCSI_DEVS
	global FILESYSTEMS
	LAST_FIELD = -1
	POSSIBLE_DM_DEVICE = 4
	POSSIBLE_RAW_DEVICE = 3

	for FS in FILESYSTEMS:
		if( len(FS['FstabDevice']) > 0 ):
			DISPLAY_DEVICE = FS['FstabDevice']
#			DISPLAY_DEVICE = FS['ActiveDevice']
#			print(FS['FstabDevice'], FS['ActiveDevice'], FS['Mounted'], FS['Type'], FS['FstabOptions'])
#			print(FS['FstabDevice'], FS['ActiveDevice'], FS['FstabOptions'])

			# Check for device mapper devices
			if( FS['ActiveDevice'].startswith('/dev/mapper/') ):
				DM_DEV_RAW = processDMDevice(FS['ActiveDevice'])
				if( iscsiDevice(DM_DEV_RAW) ):
#					print(" + Adding iSCSI DM device: " + str(DISPLAY_DEVICE))
					ISCSI_DEVS[DISPLAY_DEVICE] = True

			# Check for unmounted devices
			elif( FS['ActiveDevice'] == FS['FstabDevice'] ):
				RAWDEV_ELEMENTS = FS['ActiveDevice'].split('/')
				if( FS['Type'] != 'swap' ):
					if( FS['ActiveDevice'].startswith('LABEL=')):
#						print(" Identify LABEL " + str(FS['ActiveDevice']))
						LABEL_DEVICE = getDeviceLinked(FS['ActiveDevice'].split('=')[LAST_FIELD])
						if( len(LABEL_DEVICE) > 0 ):
							if( LABEL_DEVICE.startswith('/dev/mapper/')):
								processDMDevice(LABEL_DEVICE)
							elif( LABEL_DEVICE.startswith('dm-')):
								processDMDevice(LABEL_DEVICE)
							else:
								if( iscsiDevice(LABEL_DEVICE) ):
#									print(" + Adding iSCSI LABEL device: " + str(LABEL_DEVICE))
									ISCSI_DEVS[DISPLAY_DEVICE] = True
					elif( FS['ActiveDevice'].startswith('UUID=')):
#						print(" Identify UUID device " + str(FS['ActiveDevice']))
						UUID_DEVICE = getDeviceLinked(FS['ActiveDevice'].split('=')[LAST_FIELD])
						if( len(UUID_DEVICE) > 0 ):
							if( UUID_DEVICE.startswith('/dev/mapper/')):
								processDMDevice(UUID_DEVICE)
							elif( UUID_DEVICE.startswith('dm-')):
								processDMDevice(UUID_DEVICE)
							else:
								if( iscsiDevice(UUID_DEVICE) ):
#									print(" + Adding iSCSI UUID device: " + str(UUID_DEVICE))
									ISCSI_DEVS[DISPLAY_DEVICE] = True
					elif( FS['ActiveDevice'].startswith('/dev/disk/')):
#						print(" Identify disk by device " + str(FS['ActiveDevice']))
						LINKED_DEVICE = getDeviceLinked(FS['ActiveDevice'].split('/')[LAST_FIELD])
						if( len(LINKED_DEVICE) > 0 ):
							if( LINKED_DEVICE.startswith('/dev/mapper/')):
								processDMDevice(LINKED_DEVICE)
							elif( LINKED_DEVICE.startswith('dm-')):
								processDMDevice(LINKED_DEVICE)
							else:
								if( iscsiDevice(LINKED_DEVICE) ):
#									print(" + Adding iSCSI disk by device: " + str(LINKED_DEVICE))
									ISCSI_DEVS[DISPLAY_DEVICE] = True
					elif( FS['ActiveDevice'].startswith('/dev/') and len(RAWDEV_ELEMENTS) == POSSIBLE_DM_DEVICE ): # Assume DM device
#						print(" Identify disk device " + str(FS['ActiveDevice']))
						RAWDEV_ELEMENTS.pop(0)
						RAWDEV_ELEMENTS.pop(0)
						RAWDEV = '-'.join(RAWDEV_ELEMENTS)
						LINKED_DEVICE = getDeviceLinked(RAWDEV)
						if( len(LINKED_DEVICE) > 0 ):
							if( LINKED_DEVICE.startswith('/dev/mapper/')):
								processDMDevice(LINKED_DEVICE)
							elif( LINKED_DEVICE.startswith('dm-')):
								processDMDevice(LINKED_DEVICE)
							else:
								if( iscsiDevice(LINKED_DEVICE) ):
#									print(" + Adding iSCSI disk device: " + str(LINKED_DEVICE))
									ISCSI_DEVS[DISPLAY_DEVICE] = True
					elif( FS['ActiveDevice'].startswith('/dev/') and len(RAWDEV_ELEMENTS) == POSSIBLE_RAW_DEVICE ): # Assume raw device
#						print(" Identify raw disk device " + str(FS['ActiveDevice']))
						RAWDEV_ELEMENTS.pop(0)
						RAWDEV_ELEMENTS.pop(0)
						LINKED_DEVICE = RAWDEV_ELEMENTS[0]
						if( len(LINKED_DEVICE) > 0 ):
							if( iscsiDevice(LINKED_DEVICE) ):
#								print(" + Adding iSCSI raw disk device: " + str(LINKED_DEVICE))
								ISCSI_DEVS[DISPLAY_DEVICE] = True
#					else:
#						print(" PUNT Unmounted device " + str(FS['ActiveDevice']))
#				else:
#					print(" Swap device ignored " + str(FS['ActiveDevice']))

			# Confirm all other devices are iSCSI
			else:
				if( iscsiDevice(FS['ActiveDevice'].split('/')[LAST_FIELD]) ):
#					print(" + Adding iSCSI device: " + str(DISPLAY_DEVICE))
					ISCSI_DEVS[DISPLAY_DEVICE] = True

	if( len(ISCSI_DEVS) > 0 ):
#		print("\nISCSI_DEVS = " + str(ISCSI_DEVS) + "\n")
		return True
	else:
		return False

def checkMountingOptions():
	global FILESYSTEMS
	global ISCSI_DEVS
	global ISCSI_DEVS_NOPT
	global ISCSI_DEVS_PARTIAL
	global ISCSI_DEVS_NOFAIL

	for key in list(ISCSI_DEVS.keys()):
		OPT_NETDEV = False
		OPT_SYSD = False
		for FS in FILESYSTEMS:
			if( FS['FstabDevice'] == key ):
				if( 'nofail' in FS['FstabOptions'] ):
					ISCSI_DEVS_NOFAIL[key] = True
				else:
					if( '_netdev' in FS['FstabOptions'] ):
						OPT_NETDEV = True
					if( 'x-systemd.requires=iscsi.service' in FS['FstabOptions'] ):
						OPT_SYSD = True
				if( not OPT_NETDEV and not OPT_SYSD ):
					ISCSI_DEVS_NOPT[key] = True
				elif( OPT_NETDEV and OPT_SYSD ):
					True # This is the correct option
				else:
					ISCSI_DEVS_PARTIAL[key] = True

	if( len(ISCSI_DEVS_NOPT) > 0 or len(ISCSI_DEVS_NOFAIL) > 0 or len(ISCSI_DEVS_PARTIAL) > 0):
		return True
	else:
		return False

##############################################################################
# Main Program Execution
##############################################################################

PACKAGE = "open-iscsi"
ISCSI_DEVS = {}
ISCSI_DEVS_NOPT = {}
ISCSI_DEVS_PARTIAL = {}
ISCSI_DEVS_NOFAIL = {}

FILESYSTEMS = SUSE.getFileSystems()

if( SUSE.packageInstalled(PACKAGE) ):
	if( iscsiMounts() ):
		if( checkMountingOptions() ):
			if( len(ISCSI_DEVS_NOFAIL) > 0 ):
				Core.updateStatus(Core.CRIT, "iSCSI devices with invalid nofail fstab mount option: " + ' '.join(list(ISCSI_DEVS_NOFAIL.keys())))
			else:
				if( len(ISCSI_DEVS_NOPT) > 0 ):
					if( len(ISCSI_DEVS_PARTIAL) > 0 ):
						Core.updateStatus(Core.CRIT, "iSCSI devices with missing fstab mount options: " + ' '.join(list(ISCSI_DEVS_NOPT.keys())) + ", and those with one option: " + ' '.join(list(ISCSI_DEVS_PARTIAL.keys())))
					else:
						Core.updateStatus(Core.CRIT, "iSCSI devices with missing fstab mount options: " + ' '.join(list(ISCSI_DEVS_NOPT.keys())))
				else:
					Core.updateStatus(Core.WARN, "Please confirm iSCSI devices with partial fstab mount options: " + ' '.join(list(ISCSI_DEVS_PARTIAL.keys())))
		else:
			Core.updateStatus(Core.IGNORE, "All iSCSI devices have correct mount options")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: No iSCSI devices found in /etc/fstab")
else:
	Core.updateStatus(Core.ERROR, "ERROR: RPM package " + PACKAGE + " not installed")

Core.printPatternResults()

