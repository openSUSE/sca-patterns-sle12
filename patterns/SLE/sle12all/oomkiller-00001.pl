#!/usr/bin/perl

# Title:       Out of Memory Killer Terminating Processes
# Description: When server memory is low, the OOM killer will kill processes using the most memory to free up memory for other calling applications.
# Modified:    2013 Aug 30

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
	PROPERTY_NAME_COMPONENT."=Memory",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7002775"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub searchOOMKiller {
	SDP::Core::printDebug('> searchOOMKiller', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'messages.txt';
	my $SECTION = '/var/log/messages';
	my @CONTENT = ();
	my @KILLED_PROCS = ();
	my %KILLED = ();
	my $LINE = 0;
	my $I = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /\s(\S+)\sinvoked oom-killer:/ ) {
				SDP::Core::printDebug("LINE $LINE", $_);
				$KILLED{$1} = 1;
				$RCODE = 1;
			}
		}
		@KILLED_PROCS = keys %KILLED;
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	if ( $RCODE ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "The out of memory killer has terminated processes: @KILLED_PROCS");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "No out of memory killer threads observed");
	}
	SDP::Core::printDebug("< searchOOMKiller", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
searchOOMKiller();
SDP::Core::printPatternResults();

exit;

