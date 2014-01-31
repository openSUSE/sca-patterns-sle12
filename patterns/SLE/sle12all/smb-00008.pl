#!/usr/bin/perl

# Title:       Samba Error: NT_STATUS_NO_SUCH_GROUP
# Description: While trying to connect to a Samba share, the user may encounter the following error: NT_STATUS_NO_SUCH_GROUP
# Modified:    2013 Jun 24

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
	PROPERTY_NAME_CATEGORY."=Samba",
	PROPERTY_NAME_COMPONENT."=Group",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006206",
	"META_LINK_BUG=https://bugzilla.novell.com/show_bug.cgi?id=611756"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub groupErrorFound {
	SDP::Core::printDebug('> groupErrorFound', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'samba.txt';
	my $SECTION = 'log.smbd ';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /NT_STATUS_NO_SUCH_GROUP/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: groupErrorFound(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< groupErrorFound", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( groupErrorFound() ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "Detected NT_STATUS_NO_SUCH_GROUP Error, Consider Force Group Option");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "No NT_STATUS_NO_SUCH_GROUP Errors");
	}
SDP::Core::printPatternResults();

exit;

