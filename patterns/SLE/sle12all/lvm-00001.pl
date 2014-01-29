#!/usr/bin/perl

# Title:       LVM Basic Service Pattern
# Description: Checks to see if the service is installed, valid and running
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
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
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
	PROPERTY_NAME_COMPONENT."=LVM",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7002759"
);

my $CHECK_PACKAGE = "lvm2";
my @SRVBOOT_ON = qw(boot.device-mapper boot.lvm);
my @SRVBOOT_OFF = qw(boot.evms);
my $FILE_SERVICE = "lvm.txt";

##############################################################################
# Local Function Definitions
##############################################################################

sub devicesWithLVM {
	SDP::Core::printDebug('> devicesWithLVM', 'BEGIN');
	my $RCODE = 1; # Assume devices with LVM metadata are present
	my $FILE_OPEN = 'lvm.txt';
	my $SECTION = 'pvscan';
	my @CONTENT = ();
	my $LINE = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /No matching physical volumes found/i ) {
				SDP::Core::printDebug("LINE $LINE", $_);
				$RCODE = 0;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< devicesWithLVM", "Returns: $RCODE");
	return $RCODE;
}

sub evmsActive {
	SDP::Core::printDebug('> evmsActive', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'evms.txt';
	my @FILE_SECTIONS = ();
	my $CHECK = '';

	SDP::Core::listSections($FILE_OPEN, \@FILE_SECTIONS);
	foreach $_ (@FILE_SECTIONS) {
		if ( /\/bin\/ls.*\/dev\/evms/ ) {
			$RCODE++;;
			last;
		}
	}

	SDP::Core::printDebug("< evmsActive", "Returns: $RCODE");
	return $RCODE;
}
##############################################################################
# Program execution functions
##############################################################################

SDP::Core::processOptions();
	my $i;
	my $BOOTS_ON = -1;
	my $BOOTS_OFF = -1;
	my $VALIDATION_ALLOWED = 1;
	
	SDP::SUSE::updateStatus(STATUS_ERROR, "ERROR: EVMS active, ignoring LVM test") if evmsActive();

	if ( SDP::SUSE::packageInstalled($CHECK_PACKAGE) ) {
		my $LVM_DEVICES = devicesWithLVM();
		my $BOOT_LVM = serviceBootstate('boot.lvm');
		foreach $i (@SRVBOOT_ON) {
			if ( SDP::SUSE::serviceBootstate($i) ) {
				SDP::Core::updateStatus(STATUS_PARTIAL, "ON  - $i");
				$BOOTS_ON++;
			} else {
				SDP::Core::updateStatus(STATUS_PARTIAL, "OFF - $i");
			}
		}
		foreach $i (@SRVBOOT_OFF) {
			if ( SDP::SUSE::serviceBootstate($i) ) {
				SDP::Core::updateStatus(STATUS_PARTIAL, "ON  - $i");
			} else {
				SDP::Core::updateStatus(STATUS_PARTIAL, "OFF - $i");
				$BOOTS_OFF++;
			}
		}
		if ( $BOOTS_ON < 0 ) {
			SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; Not in use: @SRVBOOT_ON");
			$VALIDATION_ALLOWED = 0;
		} elsif ( ! $BOOT_LVM && ! $LVM_DEVICES ) {
			SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; Not in use: $CHECK_PACKAGE");
			$VALIDATION_ALLOWED = 0;
		} elsif ( $#SRVBOOT_ON == $BOOTS_ON && $#SRVBOOT_OFF == $BOOTS_OFF ) {
			SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; All Services Activated at Boot: @SRVBOOT_ON");
		} elsif ( $#SRVBOOT_ON == $BOOTS_ON && $#SRVBOOT_OFF != $BOOTS_OFF ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Basic Service Health; Conflicting Services Activated at Boot: @SRVBOOT_OFF");
		} elsif ( ! $BOOT_LVM && $LVM_DEVICES ) {
			SDP::Core::updateStatus(STATUS_WARNING, "Basic Service Health; boot.lvm is off at boot, but LVM devices are present");
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

