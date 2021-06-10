#!/usr/bin/python
#
# Title:       Pattern for TID000020275
# Description: zypper commands return Error code HTTP response 0
# Source:      Basic Python Pattern Template v0.3.4
# Options:     SLE,Zypper,Proxy,zypproxy,000020275,0,2,0,0
# Modified:    2021 Jun 10
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

META_CLASS = "SLE"
META_CATEGORY = "Zypper"
META_COMPONENT = "Proxy"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000020275"
Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def proxyActive():
	FILE_OPEN = "updates.txt"
	SECTION = "bin/env"
	CONTENT = []
	if Core.isFileActive(FILE_OPEN):
		if Core.getRegExSection(FILE_OPEN, SECTION, CONTENT):
			CONFIRMED = re.compile("^http_proxy=|^https_proxy=", re.IGNORECASE)
			for LINE in CONTENT:
				if CONFIRMED.search(LINE):
					return True
	else:
		Core.updateStatus(Core.ERROR, "ERROR: File not found - " + FILE_OPEN)

	return False

def proxyAuthFailed():
	FILE_OPEN = "updates.txt"
	IDX_FILEPATH = 4
	IDX_SERVER_ID = 4
	IDX_FILENAME = -1
	CURL_TESTS = []
	PROXY_FAILURES = []
	PROXY_AUTH_REQUIRED = False
	PROXY_AUTH_FAILED = False

	SECTION_DICT = {}
	if Core.listSections(FILE_OPEN, SECTION_DICT):
		for LINE in SECTION_DICT:
			if "bin/curl --connect-timeout" in SECTION_DICT[LINE]:
#				print(CONTENT[LINE])
				CURL_TESTS.append(SECTION_DICT[LINE].split()[IDX_FILEPATH].split("/")[IDX_FILENAME])

	if( len(CURL_TESTS) > 0 ):
#		print(CURL_TESTS)
		PROXY_AUTH_FAILED_MSG = re.compile("HTTP/1.1 403 Forbidden|== Info: Authentication problem. Ignoring this", re.IGNORECASE)
		for FILE_OPEN in CURL_TESTS:
#			print(FILE_OPEN)
			CONTENT = []
			if Core.loadFullFile(FILE_OPEN, CONTENT):
				PROXY_SERVER = "Unknown"
				for LINE in CONTENT:
					if "Info: Connected to" in LINE:
						PROXY_SERVER = LINE.split()[IDX_SERVER_ID]
					if "Proxy-Authorization:" in LINE:
						PROXY_AUTH_REQUIRED = True
					if PROXY_AUTH_FAILED_MSG.search(LINE):
						PROXY_AUTH_FAILED = True

			if( PROXY_AUTH_REQUIRED and PROXY_AUTH_FAILED ):
				PROXY_FAILURES.append(PROXY_SERVER)

	return PROXY_FAILURES

##############################################################################
# Main Program Execution
##############################################################################

if( proxyActive() ):
	FAILED_PROXY_LIST = proxyAuthFailed()
	if( len(FAILED_PROXY_LIST) > 0 ):
		Core.updateStatus(Core.CRIT, "Zypper proxy authorization failed, check proxy credentials for: " + ' '.join(FAILED_PROXY_LIST))
	else:
		Core.updateStatus(Core.IGNORE, "Proxy authorization failure not found")
else:
	Core.updateStatus(Core.ERROR, "ERROR: Proxy servers not in use")

Core.printPatternResults()

