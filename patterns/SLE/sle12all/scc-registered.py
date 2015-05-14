#!/usr/bin/python

# Title:       Detect unregistered products
# Description: Identify if SCC registrations are valid
# Modified:    2015 May 11
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
# Overriden (eventually or in part) from Core.py Module
##############################################################################

META_CLASS = "SLE"
META_CATEGORY = "Updates"
META_COMPONENT = "Registration"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7016501|META_LINK_SCC=https://scc.suse.com/dashboard|META_LINK_Register=https://www.suse.com/products/server/how-to-buy/"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

REPO_INFO = SUSE.getZypperRepoList()
PROD_INFO = SUSE.getZypperProductList()
UNREG_LIST = []
DISABLED_LIST = []
if( PROD_INFO ):
	for PRODUCT in PROD_INFO:
		#print "\n-PRODUCT: ", PRODUCT
		REGISTERED = False
		ENABLED = False
		REPO_KEY = (str(PRODUCT['InternalName']) + str(PRODUCT['Version'].split('-')[0]) + '-updates').lower()
		#print "     KEY: ", REPO_KEY
		for REPO in REPO_INFO:
			if REPO_KEY in REPO['Alias'].lower():
				REGISTERED = True
				if REPO['Enabled']:
					ENABLED = True
		if REGISTERED:
			if not ENABLED:
				DISABLED_LIST.append(PRODUCT['Name'])
		else:
			UNREG_LIST.append(PRODUCT['Name'])
	#print "Unregistered:", UNREG_LIST
	#print "    Disabled:", DISABLED_LIST, "\n"
	if( UNREG_LIST ):
		if( DISABLED_LIST ):
			Core.updateStatus(Core.CRIT, "Detected unregistred products: " + str(UNREG_LIST) + "; and products that are registered, but disabled: " + str(DISABLED_LIST))
		else:
			Core.updateStatus(Core.WARN, "Detected unregistred products: " + str(UNREG_LIST))
	elif( DISABLED_LIST ):
		Core.updateStatus(Core.CRIT, "Detected products that are registered, but disabled: " + str(DISABLED_LIST))
	else:
		Core.updateStatus(Core.IGNORE, "All products appear registered and enabled")
else:
	Core.updateStatus(Core.ERROR, "ERROR: Zypper product information is unavailable")

Core.printPatternResults()


