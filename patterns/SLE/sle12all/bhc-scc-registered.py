#!/usr/bin/python
#
# Title:       Pattern for TID000018546
# Description: Check system registration status
# Source:      Basic Python Pattern Template v0.3.4
# Options:     Basic Health,Registration,Status,registration-scc,000018546,0,2,0,0
# Distro:      SLES1[2,5] All
# Modified:    2021 Sep 13
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

META_CLASS = "Basic Health"
META_CATEGORY = "SLE"
META_COMPONENT = "Registration"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000018546|META_LINK_SCC=https://scc.suse.com/dashboard|META_LINK_Register=https://www.suse.com/support/|META_LINK_Video=https://youtu.be/um4XQFG_nCo"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

OES_TAG = 'Microfocus'

##############################################################################
# Local Function Definitions
##############################################################################

def getRegService():
	global OES_TAG
	fileOpen = "updates.txt"
	content = []
	IDX_NUM = 0
	IDX_ALIAS = 1
	SERVICE_TAG = ''
	SMT = re.compile("SMT-.*suse", re.IGNORECASE)
	SUSE = re.compile("/updates.suse.com/|/scc.suse.com/", re.IGNORECASE)
	OES = re.compile("/nu.novell.com/", re.IGNORECASE)
	if Core.isFileActive(fileOpen):
		section = "zypper --non-interactive --no-gpg-checks repos -d"
		if Core.getRegExSection(fileOpen, "zypper --non-interactive --no-gpg-checks repos -d", content):
			IDX_URI = 8
			for line in content:
				PARTS = line.split('|')
				PARTS = [x.strip(' ') for x in PARTS]
				if( PARTS[IDX_NUM].isdigit() ):
					REPO_ALIAS = PARTS[IDX_ALIAS].strip()
					REPO_URI = PARTS[IDX_URI].strip()
					if SUSE.search(PARTS[IDX_URI]):
						SERVICE_TAG = 'SCC'
					elif( PARTS[IDX_ALIAS].startswith('susemanager:') ):
						SERVICE_TAG = 'SUMA'
					elif( PARTS[IDX_ALIAS].startswith('spacewalk:') ):
						SERVICE_TAG = 'SUMA'
					elif SMT.search(PARTS[IDX_ALIAS]):
						SERVICE_TAG = 'SMT'
					elif OES.search(PARTS[IDX_URI]):
						SERVICE_TAG = OES_TAG
#					print(str(len(PARTS)) + ":" + str(SERVICE_TAG) + ": " + str(REPO_NUM) + '|' + str(REPO_ALIAS) + '\n  ' + str(REPO_URI))
#					print(PARTS)
		elif Core.getRegExSection(fileOpen, "zypper --non-interactive --no-gpg-checks repos -u", content):
			IDX_URI = 6
			for line in content:
				PARTS = line.split('|')
				PARTS = [x.strip(' ') for x in PARTS]
				if( PARTS[IDX_NUM].isdigit() ):
					REPO_ALIAS = PARTS[IDX_ALIAS].strip()
					REPO_URI = PARTS[IDX_URI].strip()
					if SUSE.search(PARTS[IDX_URI]):
						SERVICE_TAG = 'SCC'
					elif( PARTS[IDX_ALIAS].startswith('susemanager:') ):
						SERVICE_TAG = 'SUMA'
					elif( PARTS[IDX_ALIAS].startswith('spacewalk:') ):
						SERVICE_TAG = 'SUMA'
					elif SMT.search(PARTS[IDX_ALIAS]):
						SERVICE_TAG = 'SMT'
					elif OES.search(PARTS[IDX_URI]):
						SERVICE_TAG = OES_TAG
#					print(str(len(PARTS)) + ":" + str(SERVICE_TAG) + ": " + str(REPO_NUM) + '|' + str(REPO_ALIAS) + '\n  ' + str(REPO_URI))
#					print(PARTS)
	return SERVICE_TAG

def foundCredentials():
	FILE_OPEN = "updates.txt"
	CONTENT = []
	IN_STATE = False
	if Core.loadFullFile(FILE_OPEN, CONTENT):
		for LINE in CONTENT:
			if( IN_STATE ):
#				print(LINE)
				if LINE.startswith('#==['):
					IN_STATE = False
#					print(' OUT_STATE')
				elif LINE.startswith('username='):
					return True
			elif LINE.startswith('# /etc/zypp/credentials.d/'):
#				print('IN_STATE')
				IN_STATE = True

	return False


##############################################################################
# Main Program Execution
##############################################################################

REG_LIST = []
REG_ACTIVE = []
REG_NOREG = []
SCC_INFO = SUSE.getSCCInfo()
REG_SERVICE = getRegService()
REG_AUTH = foundCredentials()
#print(REG_AUTH)
if( SCC_INFO ):
	for I in range(len(SCC_INFO)):
		if( SCC_INFO[I]['status'] ):
			if( SCC_INFO[I]['status'].lower() == "registered" ):
				REG_LIST.append(SCC_INFO[I]['identifier'])
			elif( SCC_INFO[I]['status'].lower() == "not registered" ):
				REG_NOREG.append(SCC_INFO[I]['identifier'])
			if 'subscription_status' in SCC_INFO[I]:
				if( SCC_INFO[I]['subscription_status'].lower() == "active" ):
					REG_ACTIVE.append(SCC_INFO[I]['identifier'])
#		print(str(SCC_INFO[I]['identifier']) + ": " + str(SCC_INFO[I]['status']))
#		print(SCC_INFO[I])
#	print("\n")
	if( len(REG_ACTIVE) > 0 ):
		Core.updateStatus(Core.SUCC, "System Registered through " + str(REG_SERVICE) + ": " + ' '.join(REG_LIST))
	elif( len(REG_LIST) > 0 ):
		if( len(REG_SERVICE) > 0 ):
			Core.updateStatus(Core.SUCC, "System Remotely Registered through " + str(REG_SERVICE) + ": " + ' '.join(REG_LIST))
		else:
			Core.updateStatus(Core.SUCC, "System Remotely Registered: " + ' '.join(REG_LIST))
	elif( len(REG_NOREG) > 0 ):
		if( len(REG_SERVICE) > 0 ):
			if( REG_AUTH ):
				Core.updateStatus(Core.SUCC, "System Remotely Registered through " + str(REG_SERVICE) + ": " + ' '.join(REG_NOREG))
			else:
				Core.updateStatus(Core.WARN, "Validate Remote Registration through " + str(REG_SERVICE) + ", missing credentials: " + ' '.join(REG_NOREG))
		else:
			if( REG_AUTH ):
				Core.updateStatus(Core.WARN, "Invalid System Registration, Found credentials but no registration server")
			else:
				Core.updateStatus(Core.CRIT, "System Not Registered and Unsupported")
	else:
		Core.updateStatus(Core.WARN, "Validate System Registration")
else:
	if( len(REG_SERVICE) > 0 ):
		if( REG_AUTH ):
			if( REG_SERVICE == OES_TAG ):
				Core.updateStatus(Core.WARN, "System Registered through " + str(REG_SERVICE) + ", Secondary Support Only")
			else:
				Core.updateStatus(Core.SUCC, "System Registered through " + str(REG_SERVICE))
		else:
			Core.updateStatus(Core.CRIT, "System Not Registered and Unsupported - No Credentials")
	else:
		Core.updateStatus(Core.CRIT, "System Not Registered and Unsupported")

Core.printPatternResults()

