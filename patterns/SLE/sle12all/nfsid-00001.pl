#!/usr/bin/perl

# Title:       NFS mounting incorrect NFS export
# Description: Checks for duplicate fsid values
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
	PROPERTY_NAME_CATEGORY."=Filesystem",
	PROPERTY_NAME_COMPONENT."=NFS",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7010672"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub duplicateFSID {
	SDP::Core::printDebug('> duplicateFSID', 'BEGIN');
	my $RCODE = 0;
	my $LINE = 0;
	my $HEADER_LINES = 0;
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'nfs.txt';
	my $SECTION = '/etc/exports';
	my @CONTENT = ();
	my %KEYS = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /fsid=(\d*)/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				if ( exists $KEYS{ $1 } ) {
					$RCODE++;
				} else {
					$KEYS{ $1 } = 1;
				}
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: duplicateFSID(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< duplicateFSID", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( duplicateFSID() ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "Duplicate fsid value in /etc/exports");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "IGNORE: No duplicate fsid found");
	}
SDP::Core::printPatternResults();

exit;


