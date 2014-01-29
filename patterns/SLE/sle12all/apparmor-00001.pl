#!/usr/bin/perl

# Title:       AppArmor Basic Serivce Pattern
# Description: Checks to see if the service is installed, valid and running
# Modified:    2013 Jun 26

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
	PROPERTY_NAME_CLASS."=Basic Health",
	PROPERTY_NAME_CATEGORY."=SLE",
	PROPERTY_NAME_COMPONENT."=AppArmor",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7001417"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub apparmorStatus {
	my $FILE_OPEN     = $_[0];
	my $SERVICE_NAME  = $_[1];
	SDP::Core::printDebug('> apparmorStatus', "$SERVICE_NAME");
	my $SECTION = "$SERVICE_NAME status";
	my @CONTENT = ();
	my $RCODE = 3;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			SDP::Core::printDebug("PROCESSING", $_);
			if ( /filesystem is not mounted/i ) {
				SDP::Core::printDebug('STATUS', "Down: $SERVICE_NAME");
				$RCODE = 2;
				last;
			} elsif ( /module is loaded/i ) {
				SDP::Core::printDebug('STATUS', "Running: $SERVICE_NAME");
				$RCODE = 0;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Cannot find \"$SECTION\" section in $FILE_OPEN");	
	}
	SDP::Core::printDebug("< apparmorStatus", "Returned: $RCODE, $SERVICE_NAME");
	return $RCODE;
}

sub apparmorHealth {
	my $FILE_OPEN = $_[0];
	my $CHECK_PACKAGE = $_[1];
	my $CHECK_SERVICE = $_[2];
	my $EXCLUDE = $_[3];
	SDP::Core::printDebug('> apparmorHealth', "File: $FILE_OPEN, Package: $CHECK_PACKAGE, Service: $CHECK_SERVICE");
	my $RCODE = 0; # Assume health state
	my $VALIDATE_RPM = 1; # Assume we need to validate
	my $SRV_BOOT = SDP::SUSE::serviceBootstate($CHECK_SERVICE);
	my $SRV_STATUS = apparmorStatus($FILE_OPEN, $CHECK_SERVICE);
	if ( $SRV_BOOT == 0 && $SRV_STATUS == 1 ) { # Off and unused
		SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; Not in use: $CHECK_SERVICE");
		$VALIDATE_RPM = 0; # Not in use, don't validate
	} elsif ( $SRV_BOOT == 0 && $SRV_STATUS > 1 ) { # Off but dead/down/unknown state
		SDP::Core::updateStatus(STATUS_PARTIAL, "Basic Service Health; Apparently unused: $CHECK_SERVICE");
	} elsif ( $SRV_BOOT > 0 && $SRV_STATUS > 0 ) { # On but not running
		SDP::Core::updateStatus(STATUS_CRITICAL, "Basic Service Health; Turned on at boot, but not running: $CHECK_SERVICE in $FILE_OPEN");
		$RCODE = 1;
	} elsif ( $SRV_BOOT == 0 && $SRV_STATUS == 0 ) { # Off but running
		SDP::Core::updateStatus(STATUS_WARNING, "Basic Service Health; Turned off at boot, but currently running: $CHECK_SERVICE in $FILE_OPEN");
		$RCODE = 1;
	} elsif ( $SRV_BOOT > 0 && $SRV_STATUS == 0 ) { # On and running
		SDP::Core::updateStatus(STATUS_PARTIAL, "Basic Service Health; Turned on at boot, and currently running: $CHECK_SERVICE");
	} else {
		SDP::Core::updateStatus(STATUS_PARTIAL, "Basic Service Health; Boot State: $SRV_BOOT, Run State: $SRV_STATUS, Service: $CHECK_SERVICE");
	}
	if ( $VALIDATE_RPM ) {
		my $SRV_RPMV = SDP::SUSE::packageVerify($FILE_OPEN, $CHECK_PACKAGE, $EXCLUDE);
		if ( $SRV_RPMV == 0 ) { # No differences found
			SDP::Core::updateStatus(STATUS_PARTIAL, "Basic Service Health; Passed RPM Validation: $CHECK_PACKAGE");
		} elsif ( $SRV_RPMV == 1 ) { # minor changes
			SDP::Core::updateStatus(STATUS_PARTIAL, "Basic Service Health; Minor Modifications in RPM Validation: $CHECK_PACKAGE in $FILE_OPEN");
		} elsif ( $SRV_RPMV == 2 ) { # consider changes
			SDP::Core::updateStatus(STATUS_WARNING, "Basic Service Health; Review Changes in RPM Validation: $CHECK_PACKAGE in $FILE_OPEN");
			$RCODE = 1;
		} elsif ( $SRV_RPMV == 3 ) { # A bin or lib failed
			SDP::Core::updateStatus(STATUS_CRITICAL, "Basic Service Health; Binary/Library Failed RPM Validation: $CHECK_PACKAGE in $FILE_OPEN");
		} else {
			SDP::Core::updateStatus(STATUS_WARNING, "Basic Service Health; Review Changes in RPM Validation: $CHECK_PACKAGE in $FILE_OPEN");
			$RCODE = 1;
		}
	}
	SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health: Confirmed") if ($GSTATUS < 1);
	SDP::Core::printDebug("< apparmorHealth", "Returned: $RCODE, $CHECK_SERVICE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my $FOPEN = "security-apparmor.txt";
	my $PACKAGE = "apparmor-parser";
	my $SERVICE = "boot.apparmor";
	my @EXCLUDES = ();

	if ( packageInstalled($PACKAGE) ) {
		apparmorHealth($FOPEN, $PACKAGE, $SERVICE, \@EXCLUDES);
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; Package Not Installed: $PACKAGE");
	}

SDP::Core::printPatternResults();

exit;

