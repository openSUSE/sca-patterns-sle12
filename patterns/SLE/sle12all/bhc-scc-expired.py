#!/usr/bin/python3

# Title:       Expired SCC Registrations
# Description: Identify if SCC registrations have expired
# Modified:    2021 Sep 13
#
##############################################################################
# Copyright (C) 2015,2021 SUSE LLC
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

##############################################################################
# Module Definition
##############################################################################

import os
import Core
import SUSE
import datetime

##############################################################################
# Overriden (eventually or in part) from Core.py Module
##############################################################################

META_CLASS = "Basic Health"
META_CATEGORY = "SLE"
META_COMPONENT = "Registration"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_SCC"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_SCC=https://scc.suse.com/dashboard|META_LINK_Renew=https://www.suse.com/renewals/|META_LINK_Video=https://youtu.be/um4XQFG_nCo"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

SCC_INFO = SUSE.getSCCInfo()
REG_EXPIRED = []
REG_EXPIRING = []
REG_VALID = []
WARNING_DAYS = 60
EXPIRE_DATE_FOUND = False
TODAY = datetime.datetime.today()
if( SCC_INFO ):
	for PRODUCT in SCC_INFO:
		#print "PRODUCT:    " + str(PRODUCT)
		EXPIRE_DATE = ''
		EXPIRE_STR = ''
		if 'expires_at' in PRODUCT:
			EXPIRE_DATE_FOUND = True
			TMP = PRODUCT['expires_at'].split()
			del TMP[-1]
			EXPIRE_DATE = TMP[0]
			EXPIRE_STR = ' '.join(TMP)
			EXPIRATION = datetime.datetime.strptime(EXPIRE_STR, "%Y-%m-%d %H:%M:%S")
			EXPIRATION_WARNING = EXPIRATION - datetime.timedelta(days=int(WARNING_DAYS))
		if( EXPIRE_STR ):
			if( TODAY > EXPIRATION ):
				REG_EXPIRED.append(str(PRODUCT['identifier']) + " " + str(PRODUCT['version']) + ": " + str(EXPIRE_DATE))
			elif( TODAY > EXPIRATION_WARNING ):
				REG_EXPIRING.append(str(PRODUCT['identifier']) + " " + str(PRODUCT['version']) + ": " + str(EXPIRE_DATE))
			else:
				REG_VALID.append(str(PRODUCT['identifier']) + " " + str(PRODUCT['version']) + ": " + str(EXPIRE_DATE))

	if( EXPIRE_DATE_FOUND ):
		if( REG_EXPIRED ):
			if( REG_EXPIRING ):
				Core.updateStatus(Core.CRIT, "Detected expired product registrations: " + ' '.join(REG_EXPIRED) + "; expiring within " + str(WARNING_DAYS) + " days: " + ' '.join(REG_EXPIRING))
			else:
				Core.updateStatus(Core.CRIT, "Detected expired product registrations: " + ' '.join(REG_EXPIRED))
		elif( REG_EXPIRING ):
				Core.updateStatus(Core.WARN, "Detected product registrations expiring within " + str(WARNING_DAYS) + " days: " + ' '.join(REG_EXPIRING))
		else:
			Core.updateStatus(Core.SUCC, "No product registrations have expired or will expire within " + str(WARNING_DAYS) + " days, " + ' '.join(REG_VALID))
	else:
		Core.updateStatus(Core.ERROR, "SCC Status: No expire dates found")
else:
	Core.updateStatus(Core.ERROR, "SCC Status: Not Found")

Core.printPatternResults()


