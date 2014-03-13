#!/usr/bin/perl

# Title:       Check for Empty CSET Service
# Description: The default cset service is empty and needs to be configured.
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
	PROPERTY_NAME_CATEGORY."=Kernel",
	PROPERTY_NAME_COMPONENT."=CSet",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7007601",
	"META_LINK_MISC=http://www.novell.com/documentation/slerte_11/"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub emptyCsetScript {
# Requires
#  Service script name
# Returns
# -1 Script not found
#  0 Script is configured
#  1 Script is empty

	my $SECTION = "/etc/init.d/$_[0]\$";
	SDP::Core::printDebug('> emptyCsetScript', "$SECTION");
	my $RCODE = 1;
	my $FILE_OPEN = 'slert.txt';
	my @CONTENT = ();
	my $BIN_REQ = 0;
	my $START = 0;
	my $STOP = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /^CSET_BIN=/ ) {
				SDP::Core::printDebug("CSET_BIN", "Defined");
				$BIN_REQ++;
			} elsif ( $START ) {
				if ( /\$CSET_BIN/ ) {
					SDP::Core::printDebug("CSET_BIN", "Start");
					$BIN_REQ++;
					$START = 0;
				} elsif ( /rc_status/ ) {
					$START = 0;
				}
			} elsif ( $STOP ) {
				if ( /\$CSET_BIN/ ) {
					SDP::Core::printDebug("CSET_BIN", "Stop");
					$BIN_REQ++;
					$STOP = 0;
				} elsif ( /rc_status/ ) {
					$STOP = 0;
				}
			} elsif ( /start\)/ ) {
				$START = 1;
			} elsif ( /stop\)/ ) {
				$STOP = 1;
			}
		}
		SDP::Core::printDebug("REQUIRED BIN", "$BIN_REQ");
		$RCODE = 0 if ( $BIN_REQ > 2 );
	} else {
		SDP::Core::printDebug("SECTION", "NOT FOUND: $SECTION");
		$RCODE = -1; # not found
	}
	SDP::Core::printDebug("< emptyCsetScript", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my @CSET_SERVICES = qw(cset cset.init.d);
	my $NOT_FOUND = 1; # assume the scripts are not found by default
	foreach my $SERVICE_NAME (@CSET_SERVICES) { # checks each possibility
		my $SCRIPT = emptyCsetScript($SERVICE_NAME);
		if ( $SCRIPT >= 0 ) { # the script was found
			$NOT_FOUND = 0;
			if ( $SCRIPT > 0 ) { # script was empty
				my %SERVICE_INFO = SDP::SUSE::getServiceInfo($SERVICE_NAME);
				if ( $SERVICE_INFO{'runlevelstatus'} > 0 ) { # turned on for run level
					SDP::Core::updateStatus(STATUS_CRITICAL, "Manually configure the cset service: /etc/init.d/$SERVICE_NAME");
				} else { # turned off for runlevel
					SDP::Core::updateStatus(STATUS_WARNING, "Manually configure the cset service before enabling it: /etc/init.d/$SERVICE_NAME");
				}
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, "The cset service script appears to be configured");
			}
			last;
		}
	}
	if ( $NOT_FOUND ) {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: No cset service script found.");
	}
SDP::Core::printPatternResults();

exit;

