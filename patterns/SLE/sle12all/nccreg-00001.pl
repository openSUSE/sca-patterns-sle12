#!/usr/bin/perl

# Title:       Invalid NCC URL host name
# Description: Novell Customer Center server connection errors when registering
# Modified:    2013 Jun 25

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
	PROPERTY_NAME_CATEGORY."=Update",
	PROPERTY_NAME_COMPONENT."=NCC",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7008797"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub getURL {
	SDP::Core::printDebug('> getURL', 'BEGIN');
	my $RCODE = '';
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'updates.txt';
	my $SECTION = 'suseRegister.conf';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /url\s*=\s*/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$_ =~ s/\"|\'|\s//g;
				@LINE_CONTENT = split(/=/, $_);
				$RCODE = $LINE_CONTENT[1];
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: getURL(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< getURL", "Returns: $RCODE");
	return $RCODE;
}

sub urlDown {
	my $REG_URL = $_[0];
	SDP::Core::printDebug('> urlDown', "$REG_URL");
	my $RCODE = 0;
	my $FILE_OPEN = 'updates.txt';
	my $SECTION = '.suse_register.log';
	my @CONTENT = ();
	my $FOUND = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( $FOUND ) {
				if ( /ERROR.*resolve host name/i ) {
					SDP::Core::printDebug(" ERROR", $_);
					$RCODE++;
					last;
				}
			} elsif ( /$REG_URL/ ) {
				$FOUND = 1;
				SDP::Core::printDebug("DATA URL", $REG_URL);
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: urlDown(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< urlDown", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my $URL = getURL();
	if ( urlDown($URL) ) {
		if ( $URL eq 'https://secure-www.novell.com/center/regsvc' || $URL eq 'https://secure-www.novell.com/center/regsvc/' ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Cannot Reach the Novell NCC Server: $URL");
		} else {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Cannot Resolve NCC Host Name: $URL");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Valid NCC Registration Host: $URL");
	}
SDP::Core::printPatternResults();

exit;

