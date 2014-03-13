#!/usr/bin/perl

# Title:       Kernel Modules with Unknown Parameters Failing to Load
# Description: Modules failing to load due to an invalid parameter
# Modified:    2013 Jun 27

##############################################################################
#  Copyright (C) 2013,2012 SUSE LLC
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
	PROPERTY_NAME_CATEGORY."=Kernel",
	PROPERTY_NAME_COMPONENT."=Driver",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7005765"
);

# driver => unknown_parameter pair
my %UMOD = ();

##############################################################################
# Local Function Definitions
##############################################################################

sub unknownParameters {
	SDP::Core::printDebug('> unknownParameters', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'boot.txt';
	my $SECTION = 'dmesg';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /(.*): Unknown parameter `(.*)'/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$UMOD{$1} = $2;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: unknownParameters(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	$RCODE = keys(%UMOD);
	SDP::Core::printDebug("< unknownParameters", "Returns: $RCODE");
	return $RCODE;
}

sub confirmParameters {
	SDP::Core::printDebug('> confirmParameters', 'BEGIN');
	my $FILE_OPEN = 'boot.txt';
	my $SECTION = 'dmesg';
	my @CONTENT = ();
	my $DRIVER_NAME = '';
	my %DRIVER_INFO = (); 
	foreach $DRIVER_NAME ( keys %UMOD ) {
		%DRIVER_INFO = SDP::SUSE::getDriverInfo($DRIVER_NAME);
		if ( $DRIVER_INFO{'loaded'} ) {
			SDP::Core::updateStatus(STATUS_ERROR, "Inserted $DRIVER_NAME: Despite previous unknown parameter '$UMOD{$DRIVER_NAME}'");
		} else {
			my $FOUND = SDP::Core::inSection('modules.txt', "options.*$DRIVER_NAME.*$UMOD{$DRIVER_NAME}");
			if ( $FOUND ) {
				SDP::Core::updateStatus(STATUS_CRITICAL, "Failed inserting $DRIVER_NAME: Unknown parameter '$UMOD{$DRIVER_NAME}' in $FOUND");
			} else {
				SDP::Core::updateStatus(STATUS_WARNING, "Unloaded module $DRIVER_NAME: Unknown parameter '$UMOD{$DRIVER_NAME}' was not found, try reloading $DRIVER_NAME");
			}
		}
	}
	SDP::Core::printDebug("< confirmParameters", "END");
	return 1;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( unknownParameters() ) {
		confirmParameters();
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "No modules with unknown parameters observed");
	}
SDP::Core::printPatternResults();

exit;


