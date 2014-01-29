#!/usr/bin/perl

# Title:       Loading weak kernel drivers
# Description: Modules loading that are compiled for a different kernel
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
	PROPERTY_NAME_CATEGORY."=Kernel",
	PROPERTY_NAME_COMPONENT."=Driver",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7008799"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub weakModules {
	SDP::Core::printDebug('> weakModules', 'BEGIN');
	my $RCODE = 0;
	my $ARRAY_REF = $_[0];
	my %MODULES = ();
	my $FILE_OPEN = 'boot.txt';
	my $SECTION = 'dmesg';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /^(.*): Loading module compiled for kernel version .* into kernel version/i ) {
				my $MOD = $1;
				SDP::Core::printDebug("MODULE", $MOD);
				$MODULES{$MOD} = 1;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: weakModules(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	$RCODE = scalar keys %MODULES;
	@$ARRAY_REF = keys %MODULES;
	SDP::Core::printDebug("< weakModules", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my @WEAK_MODULES = ();
	if ( weakModules(\@WEAK_MODULES) ) {
		SDP::Core::updateStatus(STATUS_SUCCESS, "Weak Modules Loaded: @WEAK_MODULES");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "No weak modules loaded");
	}
SDP::Core::printPatternResults();

exit;

