#!/usr/bin/perl

# Title:       Error 17 with invalid root
# Description: Error 17 Cannot mount selected partition root hd0
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
	PROPERTY_NAME_CATEGORY."=GRUB",
	PROPERTY_NAME_COMPONENT."=Base",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7010670",
	"META_LINK_BUG=https://bugzilla.novell.com/show_bug.cgi?id=776915"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub invalidMenuRoot {
	SDP::Core::printDebug('> invalidMenuRoot', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'boot.txt';
	my $SECTION = 'menu.lst';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /root\s*\(hd\d*\)/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: invalidMenuRoot(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< invalidMenuRoot", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( invalidMenuRoot() ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "Boot failure imminent, bad menu.lst root setting");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "IGNORNED: Valid menu.lst root setting");
	}
SDP::Core::printPatternResults();

exit;

