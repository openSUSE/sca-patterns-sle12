#!/usr/bin/perl

# Title:       Check for Duplicate LVM Volume Groups
# Description: Duplicate volume groups are usually a configuration issue
# Modified:    2021 May 18

##############################################################################
#  Copyright (C) 2012-2021 SUSE LLC
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
#

#  Authors/Contributors:
#   Jason Record <jason.record@suse.com>

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
	PROPERTY_NAME_CATEGORY."=Disk",
	PROPERTY_NAME_COMPONENT."=LVM",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000017046"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub check_dupvg {
	SDP::Core::printDebug('> check_dupvg', 'BEGIN');
	my $RCODE                    = 0;
	my $FILE_OPEN                = 'lvm.txt';
	my $SECTION                  = 'pvscan';
	my @CONTENT                  = ();
	my @LINE_CONTENT             = ();
	my $LINE                     = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ );                    # Skip blank lines
			if ( /duplicate vg name/i ) {
				SDP::Core::printDebug("LINE $LINE", $_);
				@LINE_CONTENT = split(/:\s+/, $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	if ( $RCODE ) {
		if ( $LINE_CONTENT[1] =~ /duplicate vg name/i ) {
			SDP::Core::updateStatus(STATUS_WARNING, "$LINE_CONTENT[1]");
		} else {
			SDP::Core::updateStatus(STATUS_WARNING, 'Duplicate LVM Volume Group(s) Found');
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "No Duplicate LVM Volume Groups Found");
	}
	SDP::Core::printDebug("< check_dupvg", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	check_dupvg();
SDP::Core::printPatternResults();

exit;


