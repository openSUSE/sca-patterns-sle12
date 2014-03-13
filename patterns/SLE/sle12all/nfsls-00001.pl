#!/usr/bin/perl

# Title:       Listing files delayed on a large NFS mounted directory
# Description: Long delay when listing files on a large NFS mounted directory
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
	PROPERTY_NAME_CATEGORY."=Filesystem",
	PROPERTY_NAME_COMPONENT."=NFS",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7005969"
);

my @NFS_MOUNTS = ();

##############################################################################
# Local Function Definitions
##############################################################################

sub activeNFSMounts {
	SDP::Core::printDebug('> activeNFSMounts', 'BEGIN');
	my $RCODE = 0;
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'fs-diskio.txt';
	my $SECTION = '/bin/mount';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /type nfs \(/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				@LINE_CONTENT = split(/\s+/, $_);
				push(@NFS_MOUNTS, $LINE_CONTENT[2]);
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: activeNFSMounts(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	$RCODE = scalar @NFS_MOUNTS;
	SDP::Core::printDebug("< activeNFSMounts", "Returns: $RCODE");
	return $RCODE;
}

sub fixApplied {
	SDP::Core::printDebug('> fixApplied', 'BEGIN');
	my $RCODE = 1; # Assume the fix is applied
	my $FILE_OPEN = 'env.txt';
	my $SECTION = '/usr/bin/env';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /^LS_OPTIONS.*--color=tty/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE = 0; # found root cause
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: fixApplied(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< fixApplied", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( activeNFSMounts() ) {
		if ( fixApplied() ) {
			SDP::Core::updateStatus(STATUS_ERROR, "LS_OPTIONS does not delay NFS mount file listings");
		} else {
			SDP::Core::updateStatus(STATUS_WARNING, "LS_OPTIONS may delay NFS mount file listings on: @NFS_MOUNTS");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Requires Active NFS Mounts, skipping ls delay test");
	}
SDP::Core::printPatternResults();

exit;

