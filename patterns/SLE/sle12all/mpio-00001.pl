#!/usr/bin/perl

# Title:       Multipath I/O Basic Service Pattern
# Description: Checks to see if the service is installed, valid and running
# Modified:    2013 Jun 27

##############################################################################
#  Copyright (C) 2013,2011,2012 SUSE LLC
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
#     Jason Record (jrecord@suse.com)
#
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
	PROPERTY_NAME_CLASS."=Basic Health",
	PROPERTY_NAME_CATEGORY."=SLE",
	PROPERTY_NAME_COMPONENT."=MPIO",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7001417"
);

my $CHECK_PACKAGE = "multipath-tools";
my @SRVBOOT_ON = qw(boot.device-mapper boot.multipath multipathd);
my $CHECK_SERVICE = "multipathd";
my $FILE_SERVICE = "mpio.txt";

##############################################################################
# Local Function Definitions
##############################################################################

sub devicesWithMPIO {
	SDP::Core::printDebug('> devicesWithMPIO', 'BEGIN');
	my $RCODE = 0; # Assume no MPIO devices present
	my $FILE_OPEN = 'mpio.txt';
	my $SECTION = 'multipath -ll';
	my @CONTENT = ();
	my $LINE = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /^\\/ ) {
				SDP::Core::printDebug("LINE $LINE", $_);
				$RCODE = 1;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	if ( $RCODE > 0 ) {
		SDP::Core::updateStatus(STATUS_PARTIAL, "Devices Found");
	} else {
		SDP::Core::updateStatus(STATUS_PARTIAL, "Devices Not Found");
	}
	SDP::Core::printDebug("< devicesWithMPIO", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Program execution functions
##############################################################################

SDP::Core::processOptions();
	my $i;
	my $SRV_BOOT = -1;
	my $VALIDATION_ALLOWED = 1;
	my @SERVICES_OFF = ();
	my %SERVICE_ON = ();
	
	if ( SDP::SUSE::packageInstalled($CHECK_PACKAGE) ) {
		foreach $i (@SRVBOOT_ON) {
			if ( SDP::SUSE::serviceBootstate($i) ) {
				SDP::Core::updateStatus(STATUS_PARTIAL, "ON  - $i");
				$SRV_BOOT++;
				$SERVICE_ON{"$i"} = 1;
			} else {
				SDP::Core::updateStatus(STATUS_PARTIAL, "OFF - $i");
				push(@SERVICES_OFF, $i);
			}
		}
		my $SRV_STATUS = SDP::SUSE::serviceStatus($FILE_SERVICE, $CHECK_SERVICE);
		my $MPIO_DEVICES = devicesWithMPIO();

		if ( $SRV_STATUS > 0 ) {
			SDP::Core::updateStatus(STATUS_PARTIAL, "Not Running: $CHECK_SERVICE");
		} else {
			SDP::Core::updateStatus(STATUS_PARTIAL, "Running: $CHECK_SERVICE");
		}
		if ( $SRV_BOOT < 0 && $SRV_STATUS == 1 ) { # Off and unused
			SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; Not in use: @SRVBOOT_ON $CHECK_SERVICE");
			$VALIDATION_ALLOWED = 0;
		} elsif ( ! $SERVICE_ON{'boot.multipath'} && ! $SERVICE_ON{'multipathd'} && ! $MPIO_DEVICES ) { # Off and no MPIO devices
			SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; Not in use: MPIO");
			$VALIDATION_ALLOWED = 0;
		} elsif ( $SRV_BOOT != $#SRVBOOT_ON && $SRV_STATUS == 0 ) { # Off but running
			SDP::Core::updateStatus(STATUS_WARNING, "Basic Service Health; Turned off at boot: @SERVICES_OFF, but currently running: $CHECK_SERVICE");
		} elsif ( $SRV_BOOT == $#SRVBOOT_ON && $SRV_STATUS == 0 ) { # On and running
			SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; Turned on at boot: @SRVBOOT_ON, and currently running: $CHECK_SERVICE");
		} elsif ( $SRV_BOOT != $#SRVBOOT_ON && $MPIO_DEVICES) { # One or more services turned off, but MPIO devices found
			SDP::Core::updateStatus(STATUS_WARNING, "Basic Service Health; Turned off at boot: @SERVICES_OFF, but MPIO Devices Found");
		} elsif ( ! $SERVICE_ON{'boot.multipath'} || ! $SERVICE_ON{'multipathd'} ) { # One service is off
			SDP::Core::updateStatus(STATUS_WARNING, "Basic Service Health; Turned off at boot: @SERVICES_OFF");
		}

		if ( $VALIDATION_ALLOWED ) {
			my $SRV_RPMV = SDP::SUSE::packageVerify($FILE_SERVICE, $CHECK_PACKAGE);
			if ( $SRV_RPMV == 0 ) { # No differences found
				SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; Passed RPM Validation: $CHECK_PACKAGE");
			} elsif ( $SRV_RPMV == 1 ) { # minor changes
				SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; Minor Modifications in RPM Validation: $CHECK_PACKAGE");
			} elsif ( $SRV_RPMV == 2 ) { # consider changes
				SDP::Core::updateStatus(STATUS_WARNING, "Basic Service Health; Review Changes in RPM Validation: $CHECK_PACKAGE");
			} elsif ( $SRV_RPMV == 3 ) { # A bin or lib failed
				SDP::Core::updateStatus(STATUS_CRITICAL, "Basic Service Health; Binary/Library Failed RPM Validation: $CHECK_PACKAGE");
			} else {
				SDP::Core::updateStatus(STATUS_WARNING, "Basic Service Health; Review Changes in RPM Validation: $CHECK_PACKAGE");
			}
		} else {
			SDP::Core::printDebug("VALIDATION", "Skipped");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; Package Not Installed: $CHECK_PACKAGE");
	}
SDP::Core::printPatternResults();

exit;

