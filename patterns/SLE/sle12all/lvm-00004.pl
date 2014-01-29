#!/usr/bin/perl

# Title:       Check for LVM Metadata Check Sum Errors
# Description: LMV Check sum errors may indicate corrupted LVM metadata
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
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

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
	PROPERTY_NAME_CATEGORY."=Disk",
	PROPERTY_NAME_COMPONENT."=LVM",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_CoolSolution",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_CoolSolution=http://www.novell.com/communities/node/1502/recovering+lost+lvm+volume+disk#CorruptedLVMMetaData"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub check_lvm_errors {
	SDP::Core::printDebug('> check_lvm_errors', 'BEGIN');
	my $RCODE                    = 0;
	my $FILE_OPEN                = 'lvm.txt';
	my $SECTION                  = 'pvscan';
	my @CONTENT                  = ();
	my $LINE                     = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ );                    # Skip blank lines
			if ( /Checksum error/i ) {
				SDP::Core::printDebug("LINE $LINE", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	if ( $RCODE ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "pvscan: Detected LVM check sum errors, consider vgcfsrestore");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "pvscan: Reported no check sum errors");
	}
	SDP::Core::printDebug("< check_lvm_errors", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	check_lvm_errors();
SDP::Core::printPatternResults();

exit;

