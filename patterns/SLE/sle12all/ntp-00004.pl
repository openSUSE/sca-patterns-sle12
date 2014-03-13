#!/usr/bin/perl

# Title:       ntpd reports frequency errors
# Description: ntpd reports frequency errors on IBM x3550 servers
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
	PROPERTY_NAME_CATEGORY."=NTP",
	PROPERTY_NAME_COMPONENT."=Frequency",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7005287"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub suspectHardware {
	SDP::Core::printDebug('> suspectHardware', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'hardware.txt';
	my $SECTION = 'Virtualization';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /^Hardware:.*x3550/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: suspectHardware(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< suspectHardware", "Returns: $RCODE");
	return $RCODE;
}

sub frequencyErrorFound {
	SDP::Core::printDebug('> frequencyErrorFound', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'ntp.txt';
	my $SECTION = '/var/log/ntp';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank linesfrequency
			if ( /ntpd.*frequency error.*PPM exceeds tolerance/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: frequencyErrorFound(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< frequencyErrorFound", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( suspectHardware() ) {
		if ( frequencyErrorFound() ) {
			SDP::Core::updateStatus(STATUS_WARNING, "Detected NTP frequency errors, consider system clocksource");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "Ignore: Not frequency errors found");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Error: IBM x3550 hardware needed");
	}
SDP::Core::printPatternResults();

exit;


