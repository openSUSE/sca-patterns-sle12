#!/usr/bin/perl

# Title:       Checks for SAN internal target failure
# Description: SCSI errors that indicate SAN errors
# Modified:    2013 Jun 27

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
	PROPERTY_NAME_CATEGORY."=Disk",
	PROPERTY_NAME_COMPONENT."=SCSI",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006510"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub checkScsiSanError {
	SDP::Core::printDebug('> checkScsiSanError', 'BEGIN');
	my $RCODE = 0;
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'messages.txt';
	my $SECTION = '/var/log/messages';
	my @CONTENT = ();
	my %CODES = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /kernel: sd (.*): SCSI error: return code = 0x(.*)/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				my $SDEV = $1; # Device that errored
				my $SERR = $2; # SCSI error code
				if ( $SERR eq "08000002" || $SERR eq "08070002" ) {
					if ( $CODES{$SDEV} ) {
						if ( $CODES{$SDEV} ne $SERR ) { # The error code is differnet this time
							SDP::Core::updateStatus(STATUS_CRITICAL, "Further hardware diagnostics recommended for SCSI device: $SDEV");
						}
					} else {
						$CODES{$SDEV} = $SERR;
						SDP::Core::updateStatus(STATUS_WARNING, "Consider further hardware diagnostics for SCSI device: $SDEV");
					}
				} else {
					SDP::Core::printDebug("OTHER", "Error $SERR on SCSI Device: $SDEV");
				}
			}
		}
		my ($KEY, $VALUE);
		if ( $OPT_LOGLEVEL >= LOGLEVEL_DEBUG ) {
			print(' %CODES                         = ');
			while ( ($KEY, $VALUE) = each(%CODES) ) {
				print("$KEY => \"$VALUE\"  ");
			}
			print("\n");
		}
		$RCODE = scalar keys(%CODES);
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: checkScsiSanError(): No errors found, skipping hardware test") if ( ! $RCODE );
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: checkScsiSanError(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< checkScsiSanError", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	checkScsiSanError(); 
SDP::Core::printPatternResults();

exit;

