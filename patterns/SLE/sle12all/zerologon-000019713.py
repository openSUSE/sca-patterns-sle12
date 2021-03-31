#!/usr/bin/python
#
# Title:       Pattern for TID000019713
# Description: Security Vulnerability: Zerologon aka CVE-2020-1472
# Source:      Package Version Pattern Template v0.3.1
# Options:     SLE,Security,Zerologon,zerologon,000019713,1176579,1,1,1
# Modified:    2021 Mar 31
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
META_CATEGORY = "Security"
META_COMPONENT = "Zerologon"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019713|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1176579|META_LINK_CVE=https://www.suse.com/security/cve/CVE-2020-1472/|META_LINK_ZeroLogon=https://www.secura.com/blog/zero-logon"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def schannel():
	fileOpen = "samba.txt"
	section = "testparm"
	content = []
	SETTING = re.compile("server schannel", re.IGNORECASE)
	CONFIRMED = re.compile("server schannel.*Yes", re.IGNORECASE)
	if Core.isFileActive(fileOpen):
		if Core.getRegExSection(fileOpen, section, content):
			for line in content:
				if SETTING.search(line):
					if CONFIRMED.search(line):
						return 1
					else:
						return 0
	return -1

##############################################################################
# Main Program Execution
##############################################################################

PACKAGE = "samba"
SERVICE_NAME = 'smb.service'

if( SUSE.packageInstalled(PACKAGE) ):
	SERVICE_INFO = SUSE.getServiceDInfo(SERVICE_NAME)
	if( SERVICE_INFO ):
		if( SERVICE_INFO['UnitFileState'] == 'enabled' or SERVICE_INFO['SubState'] == 'running' ):
			STATUS = int(schannel())
			if( STATUS > 0 ):
				Core.updateStatus(Core.IGNORE, "Zerologon avoided with schannel set to yes")
			elif( STATUS < 0 ):
				Core.updateStatus(Core.ERROR, "Unable to detect server schannel setting")
			else:
				Core.updateStatus(Core.CRIT, "Detected Zerologon vulnerability, set server schannel to yes")
		else:
			Core.updateStatus(Core.ERROR, "Service is disabled: " + str(SERVICE_NAME))
	else:
		Core.updateStatus(Core.ERROR, "Service details not found: " + str(SERVICE_NAME))
else:
	Core.updateStatus(Core.ERROR, "ERROR: RPM package " + PACKAGE + " not installed")

Core.printPatternResults()

