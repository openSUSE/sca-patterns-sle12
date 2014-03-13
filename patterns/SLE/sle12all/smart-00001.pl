#!/usr/bin/perl

# Title:       Check SMART data for hard disk errors
# Description: Using smartmontools to detect impending hard disk failure
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
#

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

use constant ERROR_THRESHOLD => 50000;

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=SLE",
	PROPERTY_NAME_CATEGORY."=Disk",
	PROPERTY_NAME_COMPONENT."=SMART",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7004508",
	"META_LINK_MISC=http://smartmontools.sourceforge.net/"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub checkSMART {
	SDP::Core::printDebug('> checkSMART', 'BEGIN');
	my $RCODE = 0;
	my $SMART = 0;
	my $FILE_OPEN = 'fs-smartmon.txt';
	my @CONTENT = ();
	my @LINE_CONTENT = ();
	my @FILE_SECTIONS = ();
	my ($CHECK,$DISKDEV) = '';
	my $READ_ERR_CORRECTED = 0;
	my $READ_ERR_UNCORRECTED = 0;
	my $WRITE_ERR_CORRECTED = 0;
	my $WRITE_ERR_UNCORRECTED = 0;
	my $MEDIUM_ERR = 0;

	if ( SDP::Core::listSections($FILE_OPEN, \@FILE_SECTIONS) ) {
		foreach $CHECK (@FILE_SECTIONS) {
			if ( $CHECK =~ /smartctl --all (\S+)/ ) {
				$DISKDEV = $1;
				$SMART = 0;
				if ( SDP::Core::getSection($FILE_OPEN, $CHECK, \@CONTENT) ) {
					foreach $_ (@CONTENT) {
						next if ( /^\s*$/ ); # Skip blank lines
						if ( /Device supports SMART and is Enabled|SMART support is.*Enabled/i ) {
							SDP::Core::printDebug('ENABLED', $_);
							$SMART = 1;
						} elsif ( /^read:/ ) {
							SDP::Core::printDebug('READ', $_);
							(undef, undef, undef, undef, $READ_ERR_CORRECTED, undef, undef, $READ_ERR_UNCORRECTED) = split(/\s+/, $_);
						} elsif ( /^write:/ ) {
							SDP::Core::printDebug('WRITE', $_);
							(undef, undef, undef, undef, $WRITE_ERR_CORRECTED, undef, undef, $WRITE_ERR_UNCORRECTED) = split(/\s+/, $_);
						} elsif ( /^Non-medium error count:/i ) {
							SDP::Core::printDebug('MEDIUM', $_);
							@LINE_CONTENT = split(/\s+/, $_);
							$MEDIUM_ERR = pop(@LINE_CONTENT);
						}
					}
				} else {
					SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Cannot find \"$CHECK\" section in $FILE_OPEN");
				}
				SDP::Core::printDebug("DEV $DISKDEV", "SMART:$SMART, Corrected r:$READ_ERR_CORRECTED, w:$WRITE_ERR_CORRECTED, Uncorrected r:$READ_ERR_UNCORRECTED, w:$WRITE_ERR_UNCORRECTED, Medium:$MEDIUM_ERR");
				if ( $SMART ) {
					$RCODE = 1;
					if ( $READ_ERR_UNCORRECTED ) {
						SDP::Core::updateStatus(STATUS_CRITICAL, "$DISKDEV SMART reports " . $READ_ERR_CORRECTED + $READ_ERR_UNCORRECTED . "read errors, $READ_ERR_UNCORRECTED uncorrectible.");
					} elsif ( $READ_ERR_CORRECTED ) {
						if ( $READ_ERR_CORRECTED > ERROR_THRESHOLD ) {
							SDP::Core::updateStatus(STATUS_CRITICAL, "$DISKDEV SMART reports $READ_ERR_CORRECTED read errors.");
						} else {
							SDP::Core::updateStatus(STATUS_WARNING, "$DISKDEV SMART reports $READ_ERR_CORRECTED read errors.");
						}
					} elsif ( $WRITE_ERR_UNCORRECTED ) {
						SDP::Core::updateStatus(STATUS_CRITICAL, "$DISKDEV SMART reports " . $WRITE_ERR_CORRECTED + $WRITE_ERR_UNCORRECTED . "write errors, $WRITE_ERR_UNCORRECTED uncorrectible.");
					} elsif ( $WRITE_ERR_CORRECTED ) {
						if ( $WRITE_ERR_CORRECTED > ERROR_THRESHOLD ) {
							SDP::Core::updateStatus(STATUS_CRITICAL, "$DISKDEV SMART reports $WRITE_ERR_CORRECTED write errors.");
						} else {
							SDP::Core::updateStatus(STATUS_WARNING, "$DISKDEV SMART reports $WRITE_ERR_CORRECTED write errors.");
						}
					} elsif ( $MEDIUM_ERR ) {
						SDP::Core::updateStatus(STATUS_WARNING, "$DISKDEV SMART reports $MEDIUM_ERR non-medium errors.");
					} else {
						SDP::Core::updateStatus(STATUS_PARTIAL, "$DISKDEV SMART reports no errors.");
					}
				} else {
					SDP::Core::updateStatus(STATUS_PARTIAL, "SMART data on $DISKDEV is unavailable.");
				}
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: No sections found in $FILE_OPEN");
	}
	SDP::Core::printDebug("< checkSMART", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( checkSMART() ) {
		SDP::Core::updateStatus(STATUS_ERROR, "No SMART errors reported on any disk");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Unable to check SMART data on any disk");
	}
SDP::Core::printPatternResults();

exit;

