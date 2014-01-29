#!/usr/bin/perl

# Title:       Check for Network Packet Issues
# Description: Errors, dropped network packets and collisions can cause unexpected application behavior
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
use constant PERCENT_CRIT => 5.00;
use constant PERCENT_WARN => 0.25;

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=SLE",
	PROPERTY_NAME_CATEGORY."=Network",
	PROPERTY_NAME_COMPONENT."=Packets",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006074"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub checkNetworkFailures {
	SDP::Core::printDebug('> checkNetworkFailures', 'BEGIN');
	my $RCODE = 0;
	my $STATE = 0;
	my $HEADER_LINES = 0;
	my @RESULTS = ();
	my %HIGH = (
		'EP' => 0,
		'DP' => 0,
		'COLLISIONS' => 0,
	);
	my $FILE_OPEN = 'network.txt';
	my $SECTION = 'ifconfig -a';
	my @CONTENT = ();
	my $NETDEV = '';
	my ($TOTAL, $ERRORS, $DROPPED, $COLLISIONS) = (0, 0, 0, 0);
	my ($EP, $DP) = (0, 0); # Percent of errors and dropped packets
	my ($LEP, $LDP, $LCP) = (0, 0, 0);

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			SDP::Core::printDebug(' check', "$_");
			if ( $STATE ) {
				if ( /packets\:(\d+) errors\:(\d+) dropped\:(\d+)/i ) {
					($TOTAL, $ERRORS, $DROPPED) = ($1, $2, $3);
					if ( $TOTAL > 0 ) {
						$EP = sprintf("%0.2f", $ERRORS * 100 / $TOTAL);
						$DP = sprintf("%0.2f", $DROPPED * 100 / $TOTAL);
					}
					$HIGH{'EP'} = $EP if ( $EP > $HIGH{'EP'} );
					$LEP = $EP if ( $EP > $LEP );
					$HIGH{'DP'} = $DP if ( $DP > $HIGH{'DP'} );
					$LDP = $DP if ( $DP > $LDP );
					SDP::Core::printDebug(' values', "T:$TOTAL E:$ERRORS,EP=$EP,LEP=$LEP D:$DROPPED,DP=$DP,LDP=$LDP C:$COLLISIONS,LCP=$LCP");
				} elsif ( /collisions\:(\d+)/i ) {
					$COLLISIONS = $1;
					$HIGH{'COLLISIONS'} = $COLLISIONS if ( $COLLISIONS > $HIGH{'COLLISIONS'} );
					$LCP = $COLLISIONS if ( $COLLISIONS > $LCP );
					SDP::Core::printDebug(' values', "T:$TOTAL E:$ERRORS,EP=$EP,LEP=$LEP D:$DROPPED,DP=$DP,LDP=$LDP C:$COLLISIONS,LCP=$LCP");
				} elsif ( /^$/ ) {
					if ( $LEP > 0 || $LDP > 0 || $LCP > 0 ) {
						push(@RESULTS, "($NETDEV: $LEP\% errors, $LDP\% dropped, $LCP collisions)");
						SDP::Core::printDebug(' PUSHED', "T:$TOTAL E:$ERRORS($LEP\%) D:$DROPPED($LDP\%) C:$LCP");
					} else {
						SDP::Core::printDebug(' PUNT', "T:$TOTAL E:$ERRORS($LEP\%) D:$DROPPED($LDP\%) C:$LCP");
					}
					$STATE = 0;
					($LEP, $LDP, $LCP) = (0, 0, 0);
				}
			} elsif ( /^(\S+)/ ) {
				$NETDEV = $1;
				($TOTAL, $ERRORS, $DROPPED, $COLLISIONS) = (0, 0, 0, 0);
				($EP, $DP) = (0, 0);
				$STATE = 1;
				SDP::Core::printDebug("INTERFACE $NETDEV", "T:$TOTAL E:$ERRORS($EP\%) D:$DROPPED($DP\%) C:$COLLISIONS");
			}
			my @TMP = values %HIGH;
			SDP::Core::printDebug(' highs', "@TMP");
		}
		if ( $HIGH{'EP'} >= PERCENT_CRIT || $HIGH{'DP'} >= PERCENT_CRIT ) { 
			SDP::Core::updateStatus(STATUS_CRITICAL, "Validate network stability for: @RESULTS");
		} elsif ( $HIGH{'EP'} >= PERCENT_WARN || $HIGH{'DP'} >= PERCENT_WARN || $HIGH{'COLLISIONS'} > 0 ) {
			SDP::Core::updateStatus(STATUS_WARNING, "Validate network stability for: @RESULTS");
		} elsif ( $HIGH{'EP'} > 0.00 || $HIGH{'DP'} > 0.00 ) {
			SDP::Core::updateStatus(STATUS_ERROR, "Minimal network errors for: @RESULTS");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "No network errors, dropped packets or collisions observed");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: checkNetworkFailures(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< checkNetworkFailures", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	checkNetworkFailures();
SDP::Core::printPatternResults();

exit;


