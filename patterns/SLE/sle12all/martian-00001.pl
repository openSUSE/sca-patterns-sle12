#!/usr/bin/perl

# Title:       Martian Source
# Description: Check for multiple nics on same network
# Modified:    2013 Sep 24

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
	PROPERTY_NAME_CATEGORY."=Network",
	PROPERTY_NAME_COMPONENT."=NIC",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=3923798",
	"META_LINK_TID2=http://www.suse.com/support/kb/doc.php?id=3815448"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub detectNicsOnSameNetwork {
	SDP::Core::printDebug('> detectNicsOnSameNetwork', 'BEGIN');
	my $RCODE = 0;
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'network.txt';
	my $SECTION = 'ifconfig';
	my @CONTENT = ();
	my @DUP_NICS = ();
	my $NIC = '';
	my $BCAST = '';
	my $IN = 0;
	my $SEC = 1;
	my %NIC_ARRAYS = (); # Hast with bcast key to the array of NIC names associated with that bcast address

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			if ( $IN ) {
				if ( /^\s*inet.*Bcast:(.*)\s/i ) { # Found the Bcast address of an interface
					$BCAST = $1;
					$BCAST =~ s/\s*//g;
				} elsif ( /^\s*RX/ ) { # Receive packets only present on physical interfaces
					$SEC = 0;
				} elsif ( /^\s*$/ ) { # blank line means I've reached the end of the interface section in ifconfig
					if ( $BCAST ) {
						SDP::Core::printDebug(" $NIC", "Secondary=$SEC, $BCAST");
						push(@{ $NIC_ARRAYS{$BCAST} }, $NIC) if ( ! $SEC );
					} else {
						SDP::Core::printDebug(" $NIC", "Secondary=$SEC");
					}
					$IN = 0;
					$BCAST = '';
					$NIC = '';
				}
			} elsif ( /^(\S*)\s/ ) { # The line starts with non-white space and therefore is the name of an interface to start processing
				$NIC = $1;
				$IN = 1;
				$SEC = 1;
			}
		}
		my @DUP_NICS = ();
		foreach my $KEY ( keys %NIC_ARRAYS ) {
			SDP::Core::printDebug("BCAST", $KEY);
			if ( $#{ $NIC_ARRAYS{$KEY} } > 0 ) { # More than one physical NIC on the same network
				push(@DUP_NICS, "[$KEY:@{$NIC_ARRAYS{$KEY}}]");
			}
			foreach my $i ( 0 .. $#{ $NIC_ARRAYS{$KEY} } ) {
				SDP::Core::printDebug(" NIC", $NIC_ARRAYS{$KEY}[$i]);
			}
		}
		if ( $#DUP_NICS >= 0 ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Detected multiple NICs on the same subnet: @DUP_NICS");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "No multiple NICs on the same subnet found");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: detectNicsOnSameNetwork(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	$RCODE = scalar @DUP_NICS;
	SDP::Core::printDebug("< detectNicsOnSameNetwork", "Returns: $RCODE");
	return @DUP_NICS;
}

sub martianSourceMissing {
	SDP::Core::printDebug('> martianSourceMissing', 'BEGIN');
	my $RCODE = 1;
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'messages.txt';
	my $SECTION = '/var/log/warn';
	my @CONTENT = ();
	my %MATCHED = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /martian source .* from (.*), on dev/i ) {
				$MATCHED{$1} = 1;
				$RCODE = 0;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, 'ERROR', "ERROR: martianSourceMissing(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	if ( $RCODE == 0 ) {
		my @DUP_NICS = keys %MATCHED;
		SDP::Core::updateStatus(STATUS_CRITICAL, "Detected martian source errors indicating multiple NICs on the same subnet: @DUP_NICS");
	}
	SDP::Core::printDebug("< martianSourceMissing", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( martianSourceMissing() ) {
		detectNicsOnSameNetwork();
	}
SDP::Core::printPatternResults();

exit;


