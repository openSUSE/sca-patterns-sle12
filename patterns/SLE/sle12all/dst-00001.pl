#!/usr/bin/perl

# Title:       Master TID: Time Zones
# Description: DST Master TID for Time zone and Daylight Saving Changes for Novell Products
# Modified:    2013 Jun 27

##############################################################################
#  Copyright (C) 2013 SUSE LLC
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
	PROPERTY_NAME_CATEGORY."=Master TID",
	PROPERTY_NAME_COMPONENT."=Time",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_Master",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_Master=http://www.suse.com/support/kb/doc.php?id=3094409"
);

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my (undef, undef, $SC_MONTH, undef) = split(/\t/, SDP::SUSE::getSupportconfigRunDate());
	if ( $SC_MONTH =~ /Feb|Mar|Apr|Sep|Oct|Nov/i ) { 
		SDP::Core::updateStatus(STATUS_RECOMMEND, "Consider TID3094409 - (DST Master TID) Time zone and Daylight Saving Changes for Novell Products");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Time zone changes outside of the month scope");
	}
SDP::Core::printPatternResults();

exit;

