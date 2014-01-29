#!/usr/bin/perl

# Title:       AppArmor Rejects Can Cause Unexpected Application Behavior
# Description: Make sure AppArmor is not rejecting application functionality
# Modified:    2013 Jun 26

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
	PROPERTY_NAME_CLASS."=Security",
	PROPERTY_NAME_CATEGORY."=SLE",
	PROPERTY_NAME_COMPONENT."=AppArmor",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006073",
	"META_LINK_Doc=http://www.novell.com/documentation/sles11/book_sle_security/data/part_aaa.html"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub appArmorRunning {
	SDP::Core::printDebug('> appArmorRunning', 'BEGIN');
	my $RCODE = 0;
	my @LINE_CONTENT = ();
	my %REJECTS = ();
	my $FILE_OPEN = 'security-apparmor.txt';
	my $SECTION = '/etc/init.d/boot.apparmor status';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /filesystem is not mounted/i ) {
				SDP::Core::printDebug("STATUS", "DOWN: $_");
				$RCODE = 0;
				last;
			} elsif ( /module is loaded/i ) {
				SDP::Core::printDebug("STATUS", "RUNNING: $_");
				$RCODE = 1;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: checkRejectMessages(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< appArmorRunning", "Returns: $RCODE");
	return $RCODE;
}

sub checkRejectMessages {
	SDP::Core::printDebug('> checkRejectMessages', 'BEGIN');
	my $RCODE = 0;
	my %REJECTS = ();
	my $FILE_OPEN = 'security-apparmor.txt';
	my $SECTION = '/var/log/audit/audit.log';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /type=APPARMOR.*REJECTING.*\((.*)\(/ ) {
				SDP::Core::printDebug("PROCESSING", "$1 in line => $_");
				$REJECTS{$1} = 1;
				$RCODE++;
			} elsif ( /apparmor="DENIED".*comm="(.*)"/ ) {
				SDP::Core::printDebug("PROCESSING", "$1 in line => $_");
				$REJECTS{$1} = 1;
				$RCODE++;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: checkRejectMessages(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	if ( $RCODE ) {
		my @PROCS = keys %REJECTS;
		SDP::Core::updateStatus(STATUS_WARNING, "Observed $RCODE AppArmor reject messages for application(s): @PROCS");		
	} else {
		SDP::Core::updateStatus(STATUS_SUCCESS, "There are no AppArmor reject messages");		
	}
	SDP::Core::printDebug("< checkRejectMessages", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my $PKG_NAME = 'apparmor-parser';
	if ( SDP::SUSE::packageInstalled($PKG_NAME) && appArmorRunning() ) {
		checkRejectMessages();
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "AppArmor Required, Skipping Reject Message Test");
	}
SDP::Core::printPatternResults();

exit;

