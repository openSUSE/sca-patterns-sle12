#!/usr/bin/python

# Title:       System down type
# Description: Detects the last system down type
# Modified:    2013 Dec 11
#
##############################################################################
# Copyright (C) 2013 SUSE LLC
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
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#  Authors/Contributors:
#   Jason Record (jrecord@suse.com)
#
##############################################################################

##############################################################################
# Module Definition
##############################################################################

import sys, os, Core, SUSE
from datetime import date, timedelta
from time import strptime

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "Basic Health"
META_CATEGORY = "SLE"
META_COMPONENT = "System"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID1"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=http://www.novell.com/support/kb/doc.php?id=3301593|META_LINK_TID1=http://www.novell.com/support/kb/doc.php?id=7010249"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Local Function Definitions
##############################################################################

def getRunLevelLineDate(EXISTING_DATE, LINE, RUN_LEVEL):
	if( len(EXISTING_DATE) == 0 ):
		LINE_ARRAY = LINE.split()
		TMP_ARRAY = []
		for I in range(11, 16):
			TMP_ARRAY.append(LINE_ARRAY[I])
		EXISTING_DATE = ' '.join(TMP_ARRAY)
		EXISTING_DATE = EXISTING_DATE + RUN_LEVEL

	return EXISTING_DATE

def getRebootLineDate(EXISTING_DATE, LINE):
	if( len(EXISTING_DATE) == 0 ):
		LINE_ARRAY = LINE.split()
		TMP_ARRAY = []
		for I in range(4, 9):
			TMP_ARRAY.append(LINE_ARRAY[I])
		EXISTING_DATE = ' '.join(TMP_ARRAY)

	return EXISTING_DATE

def getSupportconfigRunDate():
	fileOpen = "basic-environment.txt"
	section = "/bin/date"
	content = {}
	if Core.getSection(fileOpen, section, content):
		for line in content:
			DATE_TMP = content[line].split()
			if( len(DATE_TMP) > 0 ):
				del DATE_TMP[4]
				SC_RUN_DATE = ' '.join(DATE_TMP)
#	print "SC_RUN_DATE =     " + SC_RUN_DATE
	return SC_RUN_DATE

def daysPassed(RUN_DATE, COMPARE_DATE):
	iYEAR = 4
	iMONTH = 1
	iDAY = 2
#	print "RUN_DATE     = " + RUN_DATE
#	print "COMPARE_DATE = " + COMPARE_DATE

	RUN_LIST = RUN_DATE.split()
#	print "RUN_LIST     = " + str(RUN_LIST)

	YEAR = RUN_LIST[iYEAR]
	MONTH = RUN_LIST[iMONTH]
	DAY = RUN_LIST[iDAY]
#	print YEAR + ' ' + MONTH + ' ' + DAY
	if not ( len(YEAR) == 4 and YEAR.isdigit() ):
#		print "Invalid Year"
		return 0
	if not ( len(MONTH) == 3 and MONTH.isalpha() ):
#		print "Invalid Month"
		return 0
	if not ( DAY.isdigit() ):
#		print "Invalid Day"
		return 0

	RUN_DATE_OBJ = date(strptime(YEAR,'%Y').tm_year, strptime(MONTH,'%b').tm_mon, strptime(DAY,'%d').tm_mday)
#	print "RUN_DATE_OBJ = " + str(RUN_DATE_OBJ)

	CMP_LIST = COMPARE_DATE.split()
#	print "CMP_LIST     = " + str(CMP_LIST)

	YEAR = CMP_LIST[iYEAR]
	MONTH = CMP_LIST[iMONTH]
	DAY = CMP_LIST[iDAY]
#	print YEAR + ' ' + MONTH + ' ' + DAY
	if not ( len(YEAR) == 4 and YEAR.isdigit() ):
#		print "Invalid Year"
		return 0
	if not ( len(MONTH) == 3 and MONTH.isalpha() ):
#		print "Invalid Month"
		return 0
	if not ( DAY.isdigit() ):
#		print "Invalid Day"
		return 0

	CMP_DATE_OBJ = date(strptime(YEAR,'%Y').tm_year, strptime(MONTH,'%b').tm_mon, strptime(DAY,'%d').tm_mday)
#	print "CMP_DATE_OBJ = " + str(CMP_DATE_OBJ)

	RUN_DELTA = RUN_DATE_OBJ - CMP_DATE_OBJ
#	print "RUN_DELTA    = " + str(RUN_DELTA.days)

	return RUN_DELTA.days


##############################################################################
# Main Program Execution
##############################################################################

fileOpen = "boot.txt"
section = "/last -xF"
content = {}
SIX_MONTHS = 120
THREE_MONTHS = 90
BOOT_TYPE_NORMAL = 0
BOOT_TYPE_BAD = 0
PROCESS_BOOT_STATE = 0
CURRENT_BOOT = -1 # -1 Not set, 0 Clean, 1 Unclean
CURRENT_DATE = ''
DATE_LAST_CLEAN = ''
DATE_LAST_UNCLEAN = ''

if Core.getSection(fileOpen, section, content):
	for line in content:
		if( PROCESS_BOOT_STATE ):
			if content[line].startswith("runlevel"):
				if "lvl 0" in content[line]:
					DATE_LAST_CLEAN = getRunLevelLineDate(DATE_LAST_CLEAN, content[line], " using init 0")
					if( CURRENT_BOOT < 0 ):
						CURRENT_DATE = DATE_LAST_CLEAN
						CURRENT_BOOT = 0
					BOOT_TYPE_NORMAL += 1
				elif "lvl 6" in content[line]:
					DATE_LAST_CLEAN = getRunLevelLineDate(DATE_LAST_CLEAN, content[line], " using init 6")
					if( CURRENT_BOOT < 0 ):
						CURRENT_DATE = DATE_LAST_CLEAN
						CURRENT_BOOT = 0
					BOOT_TYPE_NORMAL += 1
				else:
					DATE_LAST_UNCLEAN = getRunLevelLineDate(DATE_LAST_UNCLEAN, content[line], "")
					if( CURRENT_BOOT < 0 ):
						CURRENT_DATE = DATE_LAST_UNCLEAN
						CURRENT_BOOT = 1
					BOOT_TYPE_BAD += 1
				PROCESS_BOOT_STATE = 0
			elif "system boot" in content[line]:
				DATE_LAST_UNCLEAN = getRebootLineDate(DATE_LAST_UNCLEAN, content[line])
				if( CURRENT_BOOT < 0 ):
					CURRENT_DATE = DATE_LAST_UNCLEAN
					CURRENT_BOOT = 1
				BOOT_TYPE_BAD += 1
		elif "system boot" in content[line]:
			PROCESS_BOOT_STATE = 1

#print "CURRENT_BOOT       = " + str(CURRENT_BOOT)
#print "CURRENT_DATE       = " + CURRENT_DATE
#print "DATE_LAST_CLEAN    = " + DATE_LAST_CLEAN
#print "DATE_LAST_UNCLEAN  = " + DATE_LAST_UNCLEAN
if( CURRENT_BOOT > 0 ):
	DATE_RUN_SC = getSupportconfigRunDate()
	DAYS_PASSED_CURRENT_DATE = daysPassed(DATE_RUN_SC, CURRENT_DATE)
#	print "DAYS_PASSED_CURRENT_DATE = " + str(DAYS_PASSED_CURRENT_DATE)
	if( BOOT_TYPE_BAD > 1 ):
		ADDITIONAL = BOOT_TYPE_BAD - 1
		if( DAYS_PASSED_CURRENT_DATE > THREE_MONTHS ):
			Core.updateStatus(Core.WARN, "Last system down was not clean on " + CURRENT_DATE + " and " + str(ADDITIONAL) + " additional failure(s)")
		else:
			Core.updateStatus(Core.CRIT, "Last system down was not clean on " + CURRENT_DATE + " and " + str(ADDITIONAL) + " additional failure(s)")
	else:
		if( DAYS_PASSED_CURRENT_DATE > THREE_MONTHS ):
			Core.updateStatus(Core.WARN, "Last system down was not clean on " + CURRENT_DATE)
		else:
			Core.updateStatus(Core.CRIT, "Last system down was not clean on " + CURRENT_DATE)
elif( CURRENT_BOOT == 0 ):
	DATE_RUN_SC = getSupportconfigRunDate()
	DAYS_PASSED_CURRENT_DATE = daysPassed(DATE_RUN_SC, CURRENT_DATE)
	if( len(DATE_LAST_UNCLEAN) > 0 ):
		DAYS_PASSED_UNCLEAN_DATE = daysPassed(DATE_RUN_SC, DATE_LAST_UNCLEAN)
#		print "DAYS_PASSED_UNCLEAN_DATE = " + str(DAYS_PASSED_UNCLEAN_DATE)
		if( BOOT_TYPE_BAD > 1 ):
			ADDITIONAL = BOOT_TYPE_BAD - 1
			if( DAYS_PASSED_UNCLEAN_DATE > SIX_MONTHS ):
				Core.updateStatus(Core.SUCC, "Last system down was clean on " + CURRENT_DATE + ", but failed on " + DATE_LAST_UNCLEAN + " and " + str(ADDITIONAL) + " additional failure(s)")
			elif( DAYS_PASSED_UNCLEAN_DATE > THREE_MONTHS ):
				Core.updateStatus(Core.WARN, "Last system down was clean on " + CURRENT_DATE + ", but failed on " + DATE_LAST_UNCLEAN + " and " + str(ADDITIONAL) + " additional failure(s)")
			else:
				Core.updateStatus(Core.CRIT, "Last system down was clean on " + CURRENT_DATE + ", but failed on " + DATE_LAST_UNCLEAN + " and " + str(ADDITIONAL) + " additional failure(s)")
		else:
			if( DAYS_PASSED_UNCLEAN_DATE > SIX_MONTHS ):
				Core.updateStatus(Core.SUCC, "Last system down was clean on " + CURRENT_DATE + ", but failed on " + DATE_LAST_UNCLEAN)
			elif( DAYS_PASSED_UNCLEAN_DATE > THREE_MONTHS ):
				Core.updateStatus(Core.WARN, "Last system down was clean on " + CURRENT_DATE + ", but failed on " + DATE_LAST_UNCLEAN)
			else:
				Core.updateStatus(Core.CRIT, "Last system down was clean on " + CURRENT_DATE + ", but failed on " + DATE_LAST_UNCLEAN)
	else:
		Core.updateStatus(Core.SUCC, "Last system down was clean on " + CURRENT_DATE)
else:
	Core.updateStatus(Core.ERROR, "Unknown system down states")

Core.printPatternResults()

