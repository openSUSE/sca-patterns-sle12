#!/usr/bin/perl -w

# Title:       Basic Health Check - Free Memory and Disk Swapping
# Description: Check the available memory and disk swapping activity
# Modified:    2014 Mar 4

##############################################################################
#  Copyright (C) 2013,2014 SUSE LLC
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
#
#  Authors/Contributors:
#     Jason Record (jrecord@suse.com)
#
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
# Constants
##############################################################################

use constant LIMIT_OPT_MEMRED   => 90;           # Megabytes of free RAM; red
use constant LIMIT_OPT_MEMYEL   => 85;           # Megabytes of free RAM; yellow

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=Basic Health",
	PROPERTY_NAME_CATEGORY."=SLE",
	PROPERTY_NAME_COMPONENT."=Memory",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7000120"
);

##############################################################################
# Feature Subroutines
##############################################################################

# Check Free Memory and Disk Swapping
sub checkMemUsed() {
	SDP::Core::printDebug('> checkMemUsed');
	use constant MEM_USED_FIELD   => 2;
	use constant MEM_TOTAL_FIELD  => 1;
	use constant SWAP_FIELD       => 2;
	use constant FIELDS_REQUIRED  => 15;
	my $FILE_OPEN     = 'basic-health-check.txt';
	my @CONTENT       = ();
	my @LINE_ARRAY    = ();
	my $SWAPPING      = "Unknown";

	SDP::Core::printDebug("  checkMemUsed GET", "Swap Information");
	my $LINE          = 0;
	my $SECTION       = 'vmstat 1 4';
	my $HEADER_LINES  = 4;
	my $SWAP_VALUE    = 0;
	# get swapping information
	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		my $SWAP_CHANGES = 0;
		foreach $_ (@CONTENT) {
			$LINE++;
			next if ( $LINE < $HEADER_LINES );
			next if ( m/^$/ );
			$_ =~ s/^\s+//; # remove leading white space
			SDP::Core::printDebug("  checkMemUsed LINE $LINE", $_);
			@LINE_ARRAY = split(/\s+/, $_);
			if ( $#LINE_ARRAY > FIELDS_REQUIRED ) {
				if ( $LINE_ARRAY[SWAP_FIELD] != $SWAP_VALUE ) {
					$SWAP_VALUE = $LINE_ARRAY[SWAP_FIELD];
					$SWAP_CHANGES++;
				}
			} else {
				$SWAP_VALUE = -1;
			}
			SDP::Core::printDebug("  checkMemUsed SWAPPING/CHANGES/VALUE", "$SWAPPING/$SWAP_CHANGES/$SWAP_VALUE");
		}
		if ( $SWAP_CHANGES > 1 ) {
			$SWAPPING="Yes";
		} else {
			$SWAPPING="No";
		}
		SDP::Core::printDebug("  checkMemUsed SWAPPING/CHANGES/VALUE", "$SWAPPING/$SWAP_CHANGES/$SWAP_VALUE");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}

	SDP::Core::printDebug("  checkMemUsed GET", "Memory Information");
	$LINE             = 0;
	$SECTION          = 'free -k';
	$HEADER_LINES     = 2;
	@CONTENT          = ();
	my $MEM_USED_PCT  = 0;
	my $MEM_USED      = 0;
	my $MEM_TOTAL     = -1;
	# get memory information
	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			next if ( $LINE < $HEADER_LINES );
			next if ( m/^$/ );
			$_ =~ s/^\s+//; # remove leading white space
			@LINE_ARRAY = split(/\s+/, $_);
			if      ( $LINE_ARRAY[0] =~ m/^Mem/ ) {
				$MEM_TOTAL = $LINE_ARRAY[MEM_TOTAL_FIELD];
			} elsif ( $LINE_ARRAY[0] =~ m/^-/ ) {
				$MEM_USED  = $LINE_ARRAY[MEM_USED_FIELD];
			}
			$MEM_USED_PCT = sprintf("%u", ($MEM_USED/$MEM_TOTAL*100));
			SDP::Core::printDebug("  checkMemUsed LINE $LINE", "[$MEM_USED/$MEM_TOTAL/$MEM_USED_PCT\%] $_");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}

	SDP::Core::printDebug('  checkMemUsed STATUS', "Memory Used $MEM_USED_PCT%, Swapping: $SWAPPING");
	if ( $MEM_TOTAL == -1 ) {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Invalid total memory count");
	} elsif ( $SWAP_VALUE == -1 ) {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Invalid swap value");
	} elsif ( $MEM_USED_PCT >= LIMIT_OPT_MEMRED ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "Memory used $MEM_USED_PCT"."\% exceeds ".LIMIT_OPT_MEMRED."\% - Swapping: $SWAPPING");
	} elsif ( $MEM_USED_PCT >= LIMIT_OPT_MEMYEL ) {
		if ( $SWAPPING eq "Yes" ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Memory used $MEM_USED_PCT"."\% - Swapping: $SWAPPING");
		} else {
			SDP::Core::updateStatus(STATUS_WARNING, "Memory used $MEM_USED_PCT"."\% - Swapping: $SWAPPING");
		}
	} else {
		if ( $SWAPPING eq "Yes" ) {
			SDP::Core::updateStatus(STATUS_WARNING, "Memory used $MEM_USED_PCT"."\% - Swapping: $SWAPPING");
		} else {
			SDP::Core::updateStatus(STATUS_SUCCESS, "Memory used $MEM_USED_PCT"."\% - Swapping: $SWAPPING");
		}
	}
	SDP::Core::printDebug('< checkMemUsed');
}

##############################################################################
# Main
##############################################################################

SDP::Core::processOptions();
checkMemUsed();
SDP::Core::printPatternResults();
exit;

