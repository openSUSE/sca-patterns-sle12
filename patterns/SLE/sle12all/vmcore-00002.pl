#!/usr/bin/perl

# Title:       Kernel Core Analysis Needed
# Description: Detects the need for a kernel core analysis
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
	PROPERTY_NAME_CATEGORY."=Crash",
	PROPERTY_NAME_COMPONENT."=Base",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7010484"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub vmcoresFound {
	SDP::Core::printDebug('> vmcoresFound', 'BEGIN');
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'crash.txt';
	my $SECTION = 'bin/find /';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /\/vmcore$/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				push(@LINE_CONTENT, $_);
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: vmcoresFound(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< vmcoresFound", "Returns: @LINE_CONTENT");
	return @LINE_CONTENT;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my @VMCORES = vmcoresFound();
	my $CORE = '';
	my $FILE_OPEN = 'crash.txt';
	my @CONTENT = ();
	my $CORES = 0;
	my $CONTENT_FOUND = 0;
	if ( SDP::Core::loadFile($FILE_OPEN, \@CONTENT) ) {
		if ( scalar @VMCORES > 0 ) {
			cores: foreach $CORE (@VMCORES) {
				content: foreach $_ (@CONTENT) {
					next if ( m/^\s*$/ ); # Skip blank lines
					if ( /DUMPFILE:\s*$CORE$/ ) {
						$CORES++;
						last;
					}
				}
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "No kernel core files detected");
		}
		if ( scalar @VMCORES == $CORES ) {
			SDP::Core::updateStatus(STATUS_ERROR, "Kernel core with matching analysis file(s) detected");
		} else {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Missing kernel core analysis file(s), run analyzevmcore");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Cannot load file: $FILE_OPEN");
	}
SDP::Core::printPatternResults();

exit;


