#!/usr/bin/perl

# Title:       Veritas module mismatch
# Description: Various issues with Veritas cluster software on SLES
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
	PROPERTY_NAME_COMPONENT."=Vertias",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7005194"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub veritasFound {
	SDP::Core::printDebug('> veritasFound', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'modules.txt';
	my $SECTION = 'lsmod';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /^vxdmp|^vxio|^vxspec/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: veritasFound(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< veritasFound", "Returns: $RCODE");
	return $RCODE;
}

sub mismatchedModuleLoaded {
	SDP::Core::printDebug('> mismatchedModuleLoaded', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'boot.txt';
	my $SECTION = 'boot\.msg';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /vxdmp|vxio|vxspec.*loading module compiled for kernel version.*into kernel version/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: mismatchedModuleLoaded(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< mismatchedModuleLoaded", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( veritasFound() ) {
		if ( mismatchedModuleLoaded() ) {
			SDP::Core::updateStatus(STATUS_WARNING, "Detected kernel mismatch for loaded Vertias modules");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "No kernel mismatched Veritas modules");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Error: Missing Vertias modules");
	}
SDP::Core::printPatternResults();

exit;


