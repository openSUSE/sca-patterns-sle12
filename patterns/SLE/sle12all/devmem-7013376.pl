#!/usr/bin/perl

# Title:       Memory access with /dev/mem
# Description: Checks for invalid memory access messages
# Modified:    2013 Sep 27
#
##############################################################################
# Copyright (C) 2013 SUSE LLC
##############################################################################
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#  Authors/Contributors:
#   Jason Record (jrecord@suse.com)
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
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
"META_CLASS=SLE",
"META_CATEGORY=Memory",
"META_COMPONENT=Access",
"PATTERN_ID=$PATTERN_ID",
"PRIMARY_LINK=META_LINK_TID",
"OVERALL=$GSTATUS",
"OVERALL_INFO=NOT SET",
"META_LINK_TID=https://www.suse.com/support/kb/doc.php?id=7013376",
"META_LINK_BUG=https://bugzilla.novell.com/show_bug.cgi?id=750815",
"META_LINK_BUG2=https://bugzilla.novell.com/show_bug.cgi?id=751047",
);

##############################################################################
# Local Function Definitions
##############################################################################

sub getInvalidMemoryMessages {
	SDP::Core::printDebug('> getInvalidMemoryMessages', 'BEGIN');
	my @BAD_APPS = ();
	my $FILE_OPEN = 'messages.txt';
	my $SECTION = '/var/log/messages';
	my %APPS = ();
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /Program (\S*) tried to access \/dev\/mem between /i ) {
#				SDP::Core::printDebug("MATCHED", $_);
				$APPS{$1} = 1;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: getInvalidMemoryMessages(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	@BAD_APPS = keys %APPS;
	SDP::Core::printDebug("< getInvalidMemoryMessages", "Returns: $#BAD_APPS");
	return @BAD_APPS;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
my @INVALID_MEM_APPS = getInvalidMemoryMessages();
my $RCODE = scalar @INVALID_MEM_APPS;
if ( $RCODE > 0 ) {
	SDP::Core::updateStatus(STATUS_CRITICAL, "Detected applications accessing memory incorrectly: @INVALID_MEM_APPS");
} else {
	SDP::Core::updateStatus(STATUS_ERROR, "No /dev/mem errors detected");
}
SDP::Core::printPatternResults();
exit;


