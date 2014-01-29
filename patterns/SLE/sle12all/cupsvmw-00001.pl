#!/usr/bin/perl

# Title:       CUPS starts even when CUPS is disabled
# Description: CUPS starts even when CUPS is disabled when using VMware tools
# Modified:    2013 Jun 25

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
	PROPERTY_NAME_CATEGORY."=Print",
	PROPERTY_NAME_COMPONENT."=CUPS",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7007383"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub vmwareToolsOn {
	SDP::Core::printDebug('> vmwareToolsOn', 'BEGIN');
	my $RCODE = 0;
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'chkconfig.txt';
	my $SECTION = 'CommandToIdentifyFileSection';
	my @CONTENT = ();

	my $VMW_NAME = 'vmware-tools';
	my %VMW_INFO = SDP::SUSE::getServiceInfo($VMW_NAME);
	if ( $VMW_INFO{'runlevelstatus'} > 0 ) {
		$RCODE++;
	}

	SDP::Core::printDebug("< vmwareToolsOn", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( vmwareToolsOn() ) {
		my $SERVICE_NAME = 'cups';
		my %SERVICE_INFO = SDP::SUSE::getServiceInfo($SERVICE_NAME);
		if ( $SERVICE_INFO{'runlevelstatus'} == 0 ) { # CUPS turned off
			if ( $SERVICE_INFO{'running'} > 0 ) { # However, CUPS is running
				SDP::Core::updateStatus(STATUS_WARNING, "CUPS is running, VMware Tools may be interfering");
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, "CUPS is not running, VMware Tools is not interfering");
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "CUPS turned on at boot, disregard VMware");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "SKIPPED, VMware Tools is not on or not installed");
	}
SDP::Core::printPatternResults();

exit;

