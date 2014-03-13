#!/usr/bin/perl

# Title:       Samba 3.3 Failed to issue the StartTLS
# Description: Check for ldap ssl default change error
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
	PROPERTY_NAME_COMPONENT."=TLS",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7008014"
);




##############################################################################
# Local Function Definitions
##############################################################################

sub tlsErrorFound {
	SDP::Core::printDebug('> tlsErrorFound', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'samba.txt';
	my $SECTION = 'log.smbd ';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /Failed to issue the StartTLS instruction.*Operations error/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: tlsErrorFound(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< tlsErrorFound", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my $RPM_NAME = 'samba';
	my $VERSION_TO_COMPARE = '3.3';
	my $RPM_COMPARISON = SDP::SUSE::compareRpm($RPM_NAME, $VERSION_TO_COMPARE);
	if ( $RPM_COMPARISON == 2 ) {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: RPM $RPM_NAME Not Installed");
	} elsif ( $RPM_COMPARISON > 2 ) {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Multiple Versions of $RPM_NAME RPM are Installed");
	} else {
		if ( $RPM_COMPARISON >= 0 ) {
				my $SERVICE_NAME = 'smb';
				my %SERVICE_INFO = SDP::SUSE::getServiceInfo($SERVICE_NAME);
				if ( $SERVICE_INFO{'runlevelstatus'} > 0 ) {
					if ( tlsErrorFound() ) {
						SDP::Core::updateStatus(STATUS_CRITICAL, "Detected Samba StartTLS error, Check ldap ssl settings");
					} else {
						SDP::Core::updateStatus(STATUS_ERROR, "No Samba StartTLS errors detected");
					}
				} else {
					SDP::Core::updateStatus(STATUS_ERROR, "ERROR: $SERVICE_NAME turned off, skipping StartTLS check");
				}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Samba 3.3 or higher required, skipping StartTLS check");
		}			
	}
SDP::Core::printPatternResults();

exit;

