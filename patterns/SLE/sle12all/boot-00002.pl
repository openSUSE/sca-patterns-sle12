#!/usr/bin/perl

# Title:       Boot failure due to missing boot flag
# Description: Server will fail to boot if boot flag is missing
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
	PROPERTY_NAME_CATEGORY."=Boot",
	PROPERTY_NAME_COMPONENT."=Flag",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7008829"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub findBootDevices {
	SDP::Core::printDebug('> findBootDevices', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'fs-diskio.txt';
	my @CONTENT = ();
	my $DEV_CURRENT = '';
	my $STATE = 0;
	my %BOOT_DEVICES = ();
	my $DEV_FOUND = 0;
	my $BOOT_FOUND = 0;

	if ( SDP::Core::loadFile($FILE_OPEN, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( $STATE ) {
				if ( /^#==\[/ ) {
					$STATE = 0;
					SDP::Core::printDebug(" OFF", "Done");
				} elsif ( /^\s*\d* .*boot,/ ) { # find the boot partition
					SDP::Core::printDebug(" PUSH", "Boot Partion");
					$DEV_FOUND = 1;
					$BOOT_DEVICES{$DEV_CURRENT} = 1;
				}
			} elsif ( /parted -s (.*) print/ ) { # found device
				$DEV_CURRENT = $1;
				$STATE = 1;
				SDP::Core::printDebug("CHECK", "Device: $DEV_CURRENT");
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: findBootDevices(): Cannot load file: $FILE_OPEN");
	}
	if ( $DEV_FOUND ) {
		$RCODE = scalar keys %BOOT_DEVICES;
	}
	SDP::Core::printDebug("< findBootDevices", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( SDP::SUSE::xenDomU() ) {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Xen DomU exempt, skipping boot flag test");
	} else {
		my %HOST_INFO = SDP::SUSE::getHostInfo();
		if ( $HOST_INFO{'architecture'} =~ m/i386|i586|i686|x86_64|ppc/i ) {
			if ( findBootDevices() ) {
				SDP::Core::updateStatus(STATUS_ERROR, "Boot flag found");
			} else {
				SDP::Core::updateStatus(STATUS_CRITICAL, "Boot failure probable, no disks found with boot flag enabled.");
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Architecture not applicable, skipping boot flag test");
		}
	}
SDP::Core::printPatternResults();

exit;

