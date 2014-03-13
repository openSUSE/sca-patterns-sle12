#!/usr/bin/perl

# Title:       Setting up SLES Samba Server Domain Trusts
# Description: Brief instructions with basic information on setting up domain trusts between Windows and SLES servers running Samba.
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
	PROPERTY_NAME_CATEGORY."=Samba",
	PROPERTY_NAME_COMPONENT."=Domain",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7005575"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub sambaPDC {
	SDP::Core::printDebug('> sambaPDC', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'samba.txt';
	my $SECTION = 'smb.conf';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /domain\s+master\s+=\s+yes/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< sambaPDC", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( sambaPDC() ) {
		SDP::Core::updateStatus(STATUS_RECOMMEND, "How To Setup Samba Server Domain Trusts");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Not a Samba PDC, Trusted Servers Contraindicated");
	}
SDP::Core::printPatternResults();

exit;

