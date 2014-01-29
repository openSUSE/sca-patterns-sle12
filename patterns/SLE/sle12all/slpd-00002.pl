#!/usr/bin/perl

# Title:       openSLP causes CPU utilization spikes
# Description: openSLP causes spikes of 80% utilization every 15 seconds
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

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=SLE",
	PROPERTY_NAME_CATEGORY."=SLP",
	PROPERTY_NAME_COMPONENT."=Utilization",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7005907",
	"META_LINK_BUG=https://bugzilla.novell.com/show_bug.cgi?id=601002"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub checkSlpdUtilization {
	SDP::Core::printDebug('> checkSlpdUtilization', 'BEGIN');
	use constant UTIL_CRIT => 50;
	use constant UTIL_WARN => 15;
	my $FILE_OPEN = 'basic-health-check.txt';
	my $SECTION = '/bin/ps';
	my @CONTENT = ();
	my $SLPD_UTIL = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /sbin\/slpd/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				(undef, undef, undef, $SLPD_UTIL) = split(/\s+/, $_);
				$SLPD_UTIL =~ s/\..*//g; # truncate decimal
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: checkSlpdUtilization(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("SLPD UTIL", "$SLPD_UTIL%");
	if ( $SLPD_UTIL >= UTIL_CRIT ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "High daemon utilization for slpd: $SLPD_UTIL%");
	} elsif ( $SLPD_UTIL >= UTIL_WARN ) {
		SDP::Core::updateStatus(STATUS_WARNING, "Moderate daemon utilization for slpd: $SLPD_UTIL%");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Normal daemon utilization for slpd: $SLPD_UTIL%");
	}
	SDP::Core::printDebug("< checkSlpdUtilization", "Returns: $SLPD_UTIL");
	return $SLPD_UTIL;
}

sub patchApplied {
	SDP::Core::printDebug("> patchApplied", "BEGIN");
	my $RCODE = 0;
	SDP::Core::printDebug("PLACE HOLDER", "PENDING PATCH RELEASE");
	SDP::Core::printDebug("< patchApplied", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my $SERVICE_NAME = 'slpd';
	my %SERVICE_INFO = SDP::SUSE::getServiceInfo($SERVICE_NAME);
	if ( $SERVICE_INFO{'running'} > 0 ) {
		if ( patchApplied() ) {
			SDP::Core::updateStatus(STATUS_ERROR, "Patch for high openSLP Daemon utilization applied");
		} else {
			checkSlpdUtilization();
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "slpd Daemon not running, skipping high utilization test");
	}

SDP::Core::printPatternResults();

exit;

