#!/usr/bin/perl

# Title:       Erroneous MCE taint on Some CPU Processors
# Description: Checks for processors that may have invalid MCEs
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
	PROPERTY_NAME_CATEGORY."=Kernel",
	PROPERTY_NAME_COMPONENT."=MCE",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7008578",
	"META_LINK_BUG=https://bugzilla.novell.com/show_bug.cgi?id=692709"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub affectedCPU {
	SDP::Core::printDebug('> affectedCPU', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'hardware.txt';
	my $SECTION = '/proc/cpuinfo';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /model name.*AMD.*6180 SE/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			} elsif ( /model name.*Xeon.* E7-8800|E7-4800|E7-2800/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: affectedCPU(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< affectedCPU", "Returns: $RCODE");
	return $RCODE;
}

sub mceKernelTaint {
	SDP::Core::printDebug('> mceKernelTaint', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'basic-health-check.txt';
	my $SECTION = '/proc/sys/kernel/tainted';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /machine check event|exception/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
		if ( $RCODE == 0 ) { # skip if kernel is currently tainted
			$FILE_OPEN = 'boot.txt';
			$SECTION = '/var/log/mcelog';
			@CONTENT = ();
			if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
				foreach $_ (@CONTENT) {
					next if ( m/^\s*$/ ); # Skip blank lines
					if ( /^MCE|^CPU/i ) {
						SDP::Core::printDebug("PROCESSING", $_);
						$RCODE++;
						last;
					}
				}
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: mceKernelTaint(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< mceKernelTaint", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( affectedCPU() ) {
		if ( mceKernelTaint() ) {
			SDP::Core::updateStatus(STATUS_WARNING, "Kernel is tainted with an MCE, but it may NOT apply to this CPU(s)");
		} else {
			SDP::Core::updateStatus(STATUS_RECOMMEND, "Kernel MCE taints may not apply to this CPU(s)");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: CPU model exempt from MCE check");
	}
SDP::Core::printPatternResults();

exit;

