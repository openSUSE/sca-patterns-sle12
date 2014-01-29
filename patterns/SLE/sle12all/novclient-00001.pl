#!/usr/bin/perl

# Title:       Workstation freeze saving OpenOffice Docs
# Description: Saving Open Office documents freezes the workstation on SLED 11.0 SP1
# Modified:    2013 Jun 27

##############################################################################
#  Copyright (C) 2013,2012 SUSE LLC
##############################################################################
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; version 2 of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

#  Authors/Contributors:
#   Jason Record (jrecord@suse.com)

##############################################################################

##############################################################################
# Module Definition
##############################################################################

use strict;
use warnings;
use SDP::Core;
use SDP::SUSE;

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=SLE",
	PROPERTY_NAME_CATEGORY."=Novell",
	PROPERTY_NAME_COMPONENT."=Client",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006898",
	"META_LINK_BUG=https://bugzilla.novell.com/show_bug.cgi?id=614061"
);

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if  ( SDP::SUSE::compareKernel(SLE11SP1) >= 0 && SDP::SUSE::compareKernel(SLE11SP2) < 0 ) {
		if ( SDP::SUSE::packageInstalled('novell-client') ) {
			if ( SDP::SUSE::packageInstalled('OpenOffice_org') ) {
				if ( SDP::SUSE::compareKernel('2.6.32.19') < 0 ) {
					SDP::Core::updateStatus(STATUS_WARNING, "Workstation may become unresponsive when saving to Novell Client directories");
				} else {
					SDP::Core::updateStatus(STATUS_ERROR, "Updated kernel stablizes workstation when saving to Novell Client directories");
				}
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, "ERROR: OpenOffice not Installed, Skipping Novell Client Write test");
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Novell Client not Installed, Skipping Write test");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Outside Kernel Scope, Skipping Novell Client Write test");
	}
SDP::Core::printPatternResults();

exit;

