#!/usr/bin/perl -w

# Title:       NTP Time Drift with VMware
# Description: Time drifting when running a Linux guest under VMware
# Modified:    2014 Jun 12

##############################################################################
#  Copyright (C) 2014 SUSE LLC
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

use constant RED_OFFSET => 128; # The ntpq Program Output (http://docs.hp.com/en/B2355-90774/ch04s02.html)
use constant YEL_OFFSET => 64;

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=SLE",
	PROPERTY_NAME_CATEGORY."=NTP",
	PROPERTY_NAME_COMPONENT."=Drift",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=3858673"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub ntp_time_offset {
	printDebug('> ntp_time_offset', 'BEGIN');
	use constant OFFSET_FIELD  => 8;
	use constant STRATUM_FIELD => 2;
	use constant REQUIRED_FIELDS => 9;
	my $NTP_OFFSET = -1;
	my $NOPREF_OFFSET = -1;
	my $CURR_OFFSET = 0;
	my $FILE_OPEN = 'ntp.txt';
	my $SECTION = 'ntpq -p';
	my @CONTENT = ();
	my @TIME_LINE = ();
	my $SYNC_LINE;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			chomp;
			s/^\s+//;
			@TIME_LINE = split(/\s+/, $_);
			next if ( $#TIME_LINE != REQUIRED_FIELDS );
			next if ( $TIME_LINE[STRATUM_FIELD] =~ m/\D/ );
			next if ( m/^LOCAL/ || m/^$/ ); # skips the local clock if defined
			if ( /^\*/ ) { # prefer time sources in use, marked by ntpq with an '*'
				printDebug("TAKE ACTION ON", $_);
				$NTP_OFFSET = $TIME_LINE[OFFSET_FIELD];
				if ( $NTP_OFFSET =~ m/(\d+)\./ ) { # parse out the digits before the . in the offset field
					$NTP_OFFSET = $1;
				}
				printDebug("NTP_OFFSET", $NTP_OFFSET);
				last;
			} else {
				printDebug("NOT PREFERRED", $_);
				$CURR_OFFSET = $TIME_LINE[OFFSET_FIELD];
				printDebug("TIME OFFSET FIELD", $CURR_OFFSET);
				if ( $CURR_OFFSET =~ m/(\d+)\./ ) { # parse out the digits before the . in the offset field
					$CURR_OFFSET = $1;
					if ( $CURR_OFFSET > $NOPREF_OFFSET ) {
						$NOPREF_OFFSET = $CURR_OFFSET;
					}
				}
				printDebug("NOPREF_OFFSET", $NOPREF_OFFSET);
			}
		}
		if ( $NTP_OFFSET < 0 ) {
			printDebug("USING NOPREF_OFFSET", $NOPREF_OFFSET);
			$NTP_OFFSET = $NOPREF_OFFSET;
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	printDebug('< ntp_time_offset', "Returns: $NTP_OFFSET");
	return $NTP_OFFSET;
}

sub isVmwareVM {
	printDebug('> isVmwareVM', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'basic-environment.txt';
	my $SECTION = 'Virtualization';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /^Hardware:\s+VMware\s/i ) {
				$RCODE = 1;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find '$SECTION' section in $FILE_OPEN");
	}
	printDebug('< isVmwareVM', "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();

	if ( isVmwareVM() ) {
		my $TIME_OFFSET = ntp_time_offset();
		if ( $TIME_OFFSET >= 0 ) {
			if ( $TIME_OFFSET >= RED_OFFSET ) {
				SDP::Core::updateStatus(STATUS_CRITICAL, "NTP synch issue; offset $TIME_OFFSET meets or exceeds ".RED_OFFSET);
			} elsif ( $TIME_OFFSET >= YEL_OFFSET ) {
				SDP::Core::updateStatus(STATUS_WARNING, "NTP synch warning; offset $TIME_OFFSET meets or exceeds ".YEL_OFFSET);
			} else {
				SDP::Core::updateStatus(STATUS_IGNORE, "NTP time offset observed: $TIME_OFFSET");
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "Cannot determine NTP time sync offset");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "VMware Virtual Machine Required");
	}

SDP::Core::printPatternResults();

exit;

