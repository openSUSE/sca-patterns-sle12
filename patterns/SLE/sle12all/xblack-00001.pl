#!/usr/bin/perl

# Title:       X display fails
# Description: After updating, GUI will not work, shows black screen
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
	PROPERTY_NAME_CATEGORY."=X",
	PROPERTY_NAME_COMPONENT."=Display",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7012065"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub xServerError {
	SDP::Core::printDebug('> xServerError', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'x.txt';
	my $SECTION = '/var/log/Xorg.0.log';
	my @CONTENT = ();
	my $FATAL = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( $FATAL ) {
				if ( /no screens found/i ) {
					$RCODE++;
				} elsif ( /Initializing.*extension/i ) {
					$RCODE = 0;
					$FATAL = 0;
				}
			} elsif ( /fatal server error/i ) {
				$FATAL = 1;
			}
		}
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: xServerError(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< xServerError", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( xServerError() ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "Fatal X server error detected, no screens found");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "No fatal X server errors");
	}
SDP::Core::printPatternResults();

exit;


