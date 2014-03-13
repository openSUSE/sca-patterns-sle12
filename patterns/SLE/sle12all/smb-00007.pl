#!/usr/bin/perl

# Title:       SLES 10 Samba Server Cannot Join Windows2008R2 Domains
# Description: Limitations in Samba 3.0.x disallow joining to a Windows2008 R2 domain.
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
#  along with this program; if not, see <http://www.gnu.org/licenses/>.

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
	PROPERTY_NAME_CATEGORY."=Samba",
	PROPERTY_NAME_COMPONENT."=Access",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006070"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub sambaActive {
	SDP::Core::printDebug('> sambaActive', 'BEGIN');
	my $RCODE = 0;
	my $SERVICE_NAME = 'smb';
	my %SERVICE_INFO = SDP::SUSE::getServiceInfo($SERVICE_NAME);
	if ( $SERVICE_INFO{'running'} > 0 ) {
		$RCODE++;
	} else {
		if ( $SERVICE_INFO{'runlevelstatus'} > 0 ) {
			$RCODE++;
		}
	}
	SDP::Core::printDebug("< sambaActive", "Returns: $RCODE");
	return $RCODE;
}


##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( sambaActive() ) {
		my $RPM_NAME = 'samba';
		my $VERSION_TO_COMPARE = '3.1';
		my $RPM_COMPARISON = SDP::SUSE::compareRpm($RPM_NAME, $VERSION_TO_COMPARE);
		if ( $RPM_COMPARISON == 2 ) {
			SDP::Core::updateStatus(STATUS_ERROR, "ERROR: RPM $RPM_NAME Not Installed");
		} elsif ( $RPM_COMPARISON > 2 ) {
			SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Multiple Versions of $RPM_NAME RPM are Installed");
		} else {
			if ( $RPM_COMPARISON < 0 ) {
				SDP::Core::updateStatus(STATUS_WARNING, "Joining Windows2008 R2 Domains is Unsupported");
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, "Joining Windows2008 R2 Domains is Supported");
			}			
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, 'ERROR: Samba not in use, skipping Windows2008 R2 test');
	}
SDP::Core::printPatternResults();

exit;

