#!/usr/bin/perl

# Title:       Master Troubleshooting TID: Samba
# Description: Recommended TID that helps troubleshoot configuration issues when Samba is installed on OES
# Modified:    2013 Jun 24

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
	PROPERTY_NAME_CATEGORY."=Master TID",
	PROPERTY_NAME_COMPONENT."=Samba",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_Master",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_Master=http://www.suse.com/support/kb/doc.php?id=7001492"
);

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my %HOST_INFO = SDP::SUSE::getHostInfo();
	if ( $HOST_INFO{'oes'} ) {
		my $SERVICE_NAME = 'smb';
		my %SERVICE_INFO = SDP::SUSE::getServiceInfo($SERVICE_NAME);
		if ( $SERVICE_INFO{'runlevelstatus'} ) { # samba is at least turned on for the current runlevel
			SDP::Core::updateStatus(STATUS_RECOMMEND, "Master Troubleshooting TID: Samba");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Samba running on OES Required");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Samba on OES Required");
	}
SDP::Core::printPatternResults();

exit;

