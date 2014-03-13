#!/usr/bin/perl -w

# Title:       Basic Health Check - Interrupts per second
# Description: Checks if the host's interrupts are within normal parameters.
# Modified:    2013 Jun 20

##############################################################################
#  Copyright (C) 2013,2013 SUSE LLC
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
use warnings;    # should be same as -w command option
use SDP::Core;
use SDP::SUSE;

##############################################################################
# Constants
##############################################################################

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=Basic Health",
	PROPERTY_NAME_CATEGORY."=SLE",
	PROPERTY_NAME_COMPONENT."=Kernel",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7002721"
);

##############################################################################
# Feature Subroutines
##############################################################################

# Check CPU Interrupts per second
sub checkCPUint() {
	printDebug('> checkCPUint');
	use constant HEADER_LINES  => 4;
	use constant INT_FIELD     => 10;
	my $RCODE = 0;
	my $FILE_OPEN = 'basic-health-check.txt';
	my $SECTION = 'vmstat 1 4';
	my @CONTENT = ();
	my $LINE = 0;
	my @VMDATA = ();
	my $IAVG = 0;
	my $LIMIT_CPURED = 10000;
	my $LIMIT_CPUYEL = 8000;

	if ( SDP::SUSE::compareKernel(SLE11GA) >= 0 ) {
		$LIMIT_CPURED = 60000;
		$LIMIT_CPUYEL = 30000;
	}

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			next if ( $LINE < HEADER_LINES );
			next if ( m/^$/ );
			$_ =~ s/^\s+//;
			printDebug("  checkCPUint LINE $LINE", $_);
			@VMDATA = split(/\s+/, $_);
			$IAVG += $VMDATA[INT_FIELD];
			printDebug("  checkCPUint INT/IAVG", $VMDATA[INT_FIELD] . "/" . $IAVG);
		}
		$IAVG = sprintf("%u", ($IAVG /= 3));
		if ( $IAVG >= $LIMIT_CPURED ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Interrupts per second: $IAVG meets or exceeds $LIMIT_CPURED");
		} elsif ( $IAVG >= $LIMIT_CPUYEL ) {
			SDP::Core::updateStatus(STATUS_WARNING, "Interrupts per second: $IAVG meets or exceeds $LIMIT_CPUYEL");
		} else {
			SDP::Core::updateStatus(STATUS_SUCCESS, "Interrupts per second observed: $IAVG");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	printDebug('< checkCPUint', "RETURN $RCODE");
	return $RCODE;
}

##############################################################################
# Main
##############################################################################

SDP::Core::processOptions();
checkCPUint();
SDP::Core::printPatternResults();
exit;

