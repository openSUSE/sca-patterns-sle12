#!/usr/bin/perl

# Title:       Checks for overlapping LVM packages installed
# Description: Only LVM version 1 or LVM version 2 should be installed. 
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
#
#  Authors/Contributors:
#     Jason Record (jrecord@suse.com)
#
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
	PROPERTY_NAME_CATEGORY."=Disk",
	PROPERTY_NAME_COMPONENT."=LVM",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7002759"
);

##############################################################################
# Program execution functions
##############################################################################

SDP::Core::processOptions();

	my @LVM1  = SDP::SUSE::getRpmInfo('lvm');
	my @LVM2  = SDP::SUSE::getRpmInfo('lvm2');

	if ( $#LVM1 >= 0 && $#LVM2 >= 0 ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "Both LVM1 and LVM2 are installed");
	} elsif ( $#LVM1 >= 0 ) {
		SDP::Core::updateStatus(STATUS_WARNING, "LVM1 is installed, update to LVM2");
	} elsif ( $#LVM2 >= 0 ) {
		SDP::Core::updateStatus(STATUS_ERROR, "LVM2 is installed");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "No LVM packages installed");
	}
SDP::Core::printPatternResults();

exit;

