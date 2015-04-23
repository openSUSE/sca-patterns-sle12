#!/usr/bin/python

# Title:       Expired SCC Registrations
# Description: Identify if SCC registration has expired
# Modified:    2015 Apr 17
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
import datetime

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Updates"
META_COMPONENT = "Registration"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_SCC"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_SCC=https://scc.suse.com/dashboard|META_LINK_Renew=https://www.suse.com/products/server/how-to-buy/"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

SCC_INFO = SUSE.getSCCInfo()
REG_EXPIRED = []
REG_EXPIRING = []
if( SCC_INFO ):
	for PRODUCT in SCC_INFO:
		#print "PRODUCT:    " + str(PRODUCT)
		ID = ''
		VER = ''
		EXPIRE_DATE = ''
		EXPIRE_STR = ''
		for ELEMENT in PRODUCT:
			#print " ELEMENT:   " + str(ELEMENT)
			if ELEMENT.lower().startswith("expires_at:"):
				TMP = ELEMENT.split(':', 1)[1].split()
				#print "  TMP:      ", TMP
				EXPIRE_DATE = TMP[0]
				#print "  EXP_DATE: ", EXPIRE_DATE
				del TMP[-1]
				EXPIRE_STR = ' '.join(TMP)
				#print "  STR:      ", EXPIRE_STR
				EXPIRATION = datetime.datetime.strptime(EXPIRE_STR, "%Y-%m-%d %H:%M:%S")
				#print "  EXP:      ", EXPIRATION
				EXPIRED = SUSE.compareDateTime('today', EXPIRATION)
				EXPIRING = SUSE.compareDateTime('today', EXPIRATION - datetime.timedelta(days=30))
				#print "   EXPIRED: ", EXPIRED
				#print "  EXPIRING: ", EXPIRING
			elif ELEMENT.lower().startswith("identifier:"):
				ID = str(ELEMENT.split(":")[1])
			elif ELEMENT.lower().startswith("version:"):
				VER = str(ELEMENT.split(":")[1])
		if( EXPIRE_STR ):
			if( EXPIRED >= 0 ):
				REG_EXPIRED.append(str(ID) + " " + str(VER) + ": " + str(EXPIRE_DATE))
			elif( EXPIRING >= 0 ):
				REG_EXPIRING.append(str(ID) + " " + str(VER) + ": " + str(EXPIRE_DATE))
	if( REG_EXPIRED ):
		if( REG_EXPIRING ):
			Core.updateStatus(Core.CRIT, "Detected expired product registrations: " + str(REG_EXPIRED) + ", about to expire: " + str(REG_EXPIRING))
		else:
			Core.updateStatus(Core.CRIT, "Detected expired product registrations: " + str(REG_EXPIRED))
	elif( REG_EXPIRING ):
			Core.updateStatus(Core.WARN, "Detected product registrations expiring soon: " + str(REG_EXPIRING))
	else:
		Core.updateStatus(Core.IGNORE, "No product registrations have expired or will expire within 30 days.")
else:
	Core.updateStatus(Core.ERROR, "SCC Status: Not Found")

Core.printPatternResults()


