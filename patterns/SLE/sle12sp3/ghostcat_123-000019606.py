#!/usr/bin/python3
#
# Title:       Pattern for TID000019606
# Description: Ghostcat - Apache Tomcat AJP File Read/Inclusion Vulnerability
# Source:      Package Version Pattern Template v0.3.8
# Options:     SLE,Security,Ghostcat,ghostcat_151,000019606,1164692,tomcat,9.0.31-4.22.1,0,0
# Distro:      SLES12 SP3
# Modified:    2021 Apr 22
#
##############################################################################
# Copyright (C) 2021, SUSE LLC
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

import os
import Core
import SUSE

META_CLASS = "SLE"
META_CATEGORY = "Security"
META_COMPONENT = "Ghostcat"
PATTERN_ID = os.path.basename(__file__)
PRIMARY_LINK = "META_LINK_TID"
OVERALL = Core.TEMP
OVERALL_INFO = "NOT SET"
OTHER_LINKS = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000019606|META_LINK_BUG=https://bugzilla.suse.com/show_bug.cgi?id=1164692"

Core.init(META_CLASS, META_CATEGORY, META_COMPONENT, PATTERN_ID, PRIMARY_LINK, OVERALL, OVERALL_INFO, OTHER_LINKS)

##############################################################################
# Main Program Execution
##############################################################################

RPM_TOMCAT = 'tomcat'
RPM_APACHE = 'apache2'
RPM_TOMCAT_FIXED = '8.0.53-29.22.1'
RPM_APACHE_FIXED = '2.4.23-29.54.1'

if( SUSE.packageInstalled(RPM_TOMCAT) ):
	if( SUSE.packageInstalled(RPM_APACHE) ):
		INSTALLED_VERSION_TOMCAT = SUSE.compareRPM(RPM_TOMCAT, RPM_TOMCAT_FIXED)
		INSTALLED_VERSION_APACHE = SUSE.compareRPM(RPM_APACHE, RPM_APACHE_FIXED)
		if( INSTALLED_VERSION_TOMCAT >= 0 and INSTALLED_VERSION_APACHE >= 0 ):
			Core.updateStatus(Core.IGNORE, "Bug fixes applied for " + RPM_TOMCAT + " and " + RPM_APACHE)
		else:
			Core.updateStatus(Core.WARN, "Possible Ghostcat - Apache Tomcat AJP File Read/Inclusion Vulnerability")
	else:
		Core.updateStatus(Core.ERROR, "ERROR: " + RPM_APACHE + " not installed")
else:
	Core.updateStatus(Core.ERROR, "ERROR: " + RPM_TOMCAT + " not installed")


Core.printPatternResults()

