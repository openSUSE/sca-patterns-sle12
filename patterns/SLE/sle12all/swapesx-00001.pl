#!/usr/bin/perl

# Title:       ESX overbooking may cause swapping and performance issues
# Description: Checks for possible ESX server overbooking
# Modified:    2013 Jun 28

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
	PROPERTY_NAME_CATEGORY."=Virtualization",
	PROPERTY_NAME_COMPONENT."=Performance",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006084"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub vmwarePlatform {
	SDP::Core::printDebug('> vmwarePlatform', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'hardware.txt';
	my $SECTION = 'hwinfo';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /VMware Virtual Platform/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: vmwarePlatform(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< vmwarePlatform", "Returns: $RCODE");
	return $RCODE;
}

sub swapActive {
	SDP::Core::printDebug('> swapActive', 'BEGIN');
	my $RCODE = 0;
	my $LINE = 0;
	my $HEADER_LINES = 4; # skips the two header lines and the first summary vmstat output line
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'basic-health-check.txt';
	my $SECTION = 'vmstat';
	my @CONTENT = ();
	my $SWAP_COUNT = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			next if ( $LINE < $HEADER_LINES ); # Skip header lines
			next if ( /^\s*$/ ); # Skip blank lines
			s/^\s+//g; # remove leading space
			SDP::Core::printDebug("PROCESSING", $_);
			@LINE_CONTENT = split(/\s+/, $_);
			$SWAP_COUNT++ if ( $LINE_CONTENT[6] > 0 || $LINE_CONTENT[7] > 0 );
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: swapActive(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	$RCODE = 1 if ( $SWAP_COUNT > 1 ); # swap read or written at least twice in the past few seconds
	SDP::Core::printDebug("< swapActive", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( vmwarePlatform() ) {
		if ( swapActive() ) {
			SDP::Core::updateStatus(STATUS_WARNING, "ESX VMs Only: VMware ESX server may be overbooking resources");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "ESX VMs Only: VMware ESX server does not appear to be overbooking resources");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Requires VMware, skipping ESX overbooking check");
	}
SDP::Core::printPatternResults();

exit;

