#!/usr/bin/perl

# Title:       NCC Invalid Registration URL
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

sub checkSuseRegister {
	SDP::Core::printDebug('> checkSuseRegister', 'BEGIN');
	my $RCODE = 0;
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'updates.txt';
	my $SECTION = '/etc/suseRegister.conf';
	my @CONTENT = ();
	my $VALUE = '';
	my $INDEX = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /url\s*=\s*/ ) {
				$_ =~ s/\"|\'|\s//g;
				SDP::Core::printDebug("PROCESSING", $_);
				@LINE_CONTENT = split(/\//, $_);
				$INDEX = $#LINE_CONTENT;
				if ( $LINE_CONTENT[$INDEX] ) {
					if ( $LINE_CONTENT[$INDEX] ne 'regsvc' || $LINE_CONTENT[--$INDEX] ne 'center' ) {
						$RCODE++;
					}
				} else {
					$INDEX--;
					if ( $LINE_CONTENT[$INDEX] ne 'regsvc' || $LINE_CONTENT[--$INDEX] ne 'center' ) {
						$RCODE++;
					}
				}
				last; # only checks the first occurance of url=, assuming there is only one defined in the conf file.
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: checkSuseRegister(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< checkSuseRegister", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( checkSuseRegister() ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "Invalid NCC Registration URL, Requires: /center/regsvc.");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Valid NCC Registration URL");
	}
SDP::Core::printPatternResults();

exit;

