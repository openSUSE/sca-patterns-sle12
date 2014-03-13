#!/usr/bin/perl

# Title:       File system check needed
# Description: Error kernel: ReiserFS: warning: search_by_key: invalid format found in block.
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
use constant CRITICAL_THRESHOLD => 10;
use constant WARNING_THRESHOLD => 5;

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=SLE",
	PROPERTY_NAME_CATEGORY."=Filesystem",
	PROPERTY_NAME_COMPONENT."=Check",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=3930300"
);

my %FSCK_DRIVES = ();

##############################################################################
# Local Function Definitions
##############################################################################

sub reiserCheckNeeded {
	SDP::Core::printDebug('> reiserCheckNeeded', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'messages.txt';
	my $SECTION = '/var/log/messages';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (reverse(@CONTENT)) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /kernel: ReiserFS: (.*): warning:.*search_by_key: invalid format found in block.*/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$FSCK_DRIVES{$1} = 1;
				$RCODE++;
			} elsif ( /kernel: ReiserFS: (.*): warning:.*reiserfs_read_locked_inode: i\/o failure occurred trying to find stat data/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$FSCK_DRIVES{$1} = 1;
				$RCODE++;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: reiserCheckNeeded(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< reiserCheckNeeded", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my $ERRORS = reiserCheckNeeded();
	my @DRIVES = keys %FSCK_DRIVES;
	if ( $ERRORS > CRITICAL_THRESHOLD ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "Targeted reiser errors: $ERRORS, Consider a filesystem check on: @DRIVES");
	} elsif ( $ERRORS > WARNING_THRESHOLD ) {
		SDP::Core::updateStatus(STATUS_WARNING, "Targeted reiser errors: $ERRORS, Consider a filesystem check on: @DRIVES");
	} elsif ( $ERRORS > 0 ) {
		SDP::Core::updateStatus(STATUS_WARNING, "Targeted reiser errors: $ERRORS, You might consider a filesystem check on: @DRIVES");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: No search_by_key errors detected, aborting");
	}
SDP::Core::printPatternResults();

exit;

