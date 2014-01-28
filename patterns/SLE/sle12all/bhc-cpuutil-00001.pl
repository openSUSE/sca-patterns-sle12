#!/usr/bin/perl -w

# Title:       Basic Health Check - CPU Utilization
# Description: Checks to see if the host's CPU utilization is within normal parameters.
# Modified:    2013 Jun 20

##############################################################################
#  WARNING    WARNING    WARNING    WARNING    WARNING    WARNING    WARNING 
#    This pattern uses deprecated functions. Do not use as an example.
##############################################################################

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

use constant LIMIT_OPT_CPUURED  => 90;          # % CPU utilization; red
use constant LIMIT_OPT_CPUUYEL  => 80;          # % CPU utilization; yellow
use constant OPEN_FILE_ERROR    => "ERROR: Couldn't open file: ";
use constant SECTION_PROCS      => "vmstat";
use constant PATTERN_GREP       => "^ [0-9]";
use constant COLUMN_SPLIT       => " +";
use constant PROPERTY_NAME_CPUU => 'CPUU';

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=Basic Health",
	PROPERTY_NAME_CATEGORY."=SLE",
	PROPERTY_NAME_COMPONENT."=CPU",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7002713"
);
$ARCH_FILE = "basic-health-check.txt";
##############################################################################
# Feature Subroutines
##############################################################################

# Check CPU Utilization
sub checkCPUutil() {
	SDP::Core::printDebug('> checkCPUutil USING', "$SRC_FILE1");
	
	my @ALL_IDLE_LINES = SDP::Core::grepSectionLines(SECTION_PROCS, PATTERN_GREP, COLUMN_SPLIT);
	my @ONE_IDLE = ();
	my $IAVG = 0;
	SDP::Core::printDebug('  checkCPUutil vmstat LINES', $#ALL_IDLE_LINES);
	foreach my $i (1 .. $#ALL_IDLE_LINES) {
		@ONE_IDLE = @{$ALL_IDLE_LINES[$i]};
		print("$i is $ONE_IDLE[15]\n") if $OPT_LOGLEVEL >= LOGLEVEL_DEBUG;
		print("$i is @ONE_IDLE\n") if $OPT_LOGLEVEL >= LOGLEVEL_DEBUG;
		$IAVG+= $ONE_IDLE[15];
	}
	
	$IAVG = sprintf("%3.2f", ($IAVG/= 3));
	my $UAVG = sprintf("%3.2f", (100 - $IAVG));
	if ( $UAVG >= LIMIT_OPT_CPUURED ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "Utilization: ${UAVG}% meets or exceeds ".LIMIT_OPT_CPUURED."%");
	} elsif ( $UAVG >= LIMIT_OPT_CPUUYEL ) {
		SDP::Core::updateStatus(STATUS_WARNING, "Utilization: ${UAVG}% meets or exceeds ".LIMIT_OPT_CPUUYEL."%");
	}else {
		SDP::Core::updateStatus(STATUS_SUCCESS, "Utilization: ${UAVG}%, Idle: ${IAVG}%");
	}
	SDP::Core::printDebug('< checkCPUutil ');
}


##############################################################################
# Main
##############################################################################

SDP::Core::processOptions();
$SRC_FILE1 = $ARCH_PATH . $ARCH_FILE;

SDP::Core::initFileSections();    # core init
# pattern specific logic - pattern order important
checkCPUutil();

SDP::Core::printPatternResults();
exit;

