#!/usr/bin/perl

# Title:       Machine Check Exception (MCE) Detection
# Description: Check for hardware issues when a MCE occurs.
# Modified:    2013 Jun 27

##############################################################################
#  Copyright (C) 2013,2012-2013 SUSE LLC
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

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=SLE",
	PROPERTY_NAME_CATEGORY."=Kernel",
	PROPERTY_NAME_COMPONENT."=MCE",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7003695"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub checkMceLog {
	# Run checkMceTaint after checkMceLog for proper STATUS_ERROR if /var/log/mcelog is missing
	SDP::Core::printDebug('> checkMceLog', 'BEGIN');
	my $RCODE                    = 0;
	my $FILE_OPEN                = 'boot.txt';
	my $SECTION                  = '/var/log/mcelog';
	my @CONTENT                  = ();
	my @LINE_CONTENT             = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ );                  # Skip blank lines
			if ( /^MCE|^CPU/ ) {
				SDP::Core::printDebug("LINE", $_);
				@LINE_CONTENT = split(/\s+/, $_);
				$RCODE++;
				last;
			}
		}
		if ( $RCODE ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Check for hardware failures, MCEs logged in /var/log/mcelog");
		} else {
			SDP::Core::updateStatus(STATUS_SUCCESS, "No machine check exceptions logged in /var/log/mcelog");
		}
	} else {
		SDP::Core::updateStatus(STATUS_PARTIAL, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< checkMceLog", "Returns: $RCODE");
	return $RCODE;
}

sub checkMceTaint {
	SDP::Core::printDebug('> checkMceTaint', 'BEGIN');
	my $RCODE                    = 0;
	my $FILE_OPEN                = 'basic-health-check.txt';
	my $SECTION                  = '/proc/sys/kernel/tainted';
	my @CONTENT                  = ();
	my @LINE_CONTENT             = ();
	my $LINE                     = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			next if ( /^\s*$/ );                  # Skip blank lines
			if ( /machine check event|exception/i ) {
				SDP::Core::printDebug("LINE $LINE", $_);
				@LINE_CONTENT = split(/\s+/, $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	if ( $RCODE ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "Check for hardware failures, TAINT: (M) Machine check exception");
	} else {
		SDP::Core::updateStatus(STATUS_SUCCESS, "Machine check exception taint flag not set");
	}
	SDP::Core::printDebug("< checkMceTaint", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( ! checkMceLog() ) {
		checkMceTaint();
	}
	if ( $GSTATUS == 0 ) {
		SDP::Core::updateStatus(STATUS_ERROR, "No machine check exceptions found");
	}
SDP::Core::printPatternResults();

exit;

