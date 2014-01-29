#!/usr/bin/perl

# Title:       Novell Client Mappings Fail on SLES11
# Description: Receiving initd message: novfs kernel loadable module is not installed correctly
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
	PROPERTY_NAME_CATEGORY."=Base",
	PROPERTY_NAME_COMPONENT."=Novell Client",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006171"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub novfsMessage {
	SDP::Core::printDebug('> novfsMessage', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'messages.txt';
	my $SECTION = '/var/log/messages';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /novfs kernel loadable module is not installed correctly/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: novfsMessage(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< novfsMessage", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my $PKG_NAME = 'novell-client';
	if ( SDP::SUSE::packageInstalled($PKG_NAME) ) {
		if ( SDP::SUSE::compareKernel(SLE11GA) >= 0 && SDP::SUSE::compareKernel(SLE11SP1) <= 0 ) {
			if ( novfsMessage() ) {
				SDP::Core::updateStatus(STATUS_WARNING, "Novell Client logins and mappings may fail to work properly");
			} else {
				SDP::Core::updateStatus(STATUS_RECOMMEND, "Novell Client logins and mappings may fail to work properly");
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "Outside Kernel Scope, skipping Novell Client test");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Package NOT Installed: $PKG_NAME, Skipping Novell Client test");
	}

SDP::Core::printPatternResults();

exit;

