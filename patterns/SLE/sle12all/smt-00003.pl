#!/usr/bin/perl

# Title:       SMT sync fails using HTTP Proxy
# Description: smt-ncc-sync may give error Exiting subroutine via last line 1313
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
	PROPERTY_NAME_CATEGORY."=SMT",
	PROPERTY_NAME_COMPONENT."=System",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006741"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub checkSmtProxy {
	SDP::Core::printDebug('> checkSmtProxy', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'smt.txt';
	my $SECTION = 'smt.conf';
	my @CONTENT = ();
	my @BAD_PROXY = ();
	my @PROXIES = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /^HTTPProxy\s+=\s+(\S*)/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				my $VALUE = $1;
				if ( length($VALUE) > 0 ) {
					push(@PROXIES, "HTTPProxy=$VALUE");
					if ( $VALUE !~ m/http:\/\/|https:\/\//i ) {
						push(@BAD_PROXY, "HTTPProxy=$VALUE");
					}
				}
			}
			if ( /^HTTPSProxy\s+=\s+(\S*)/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				my $VALUE = $1;
				if ( length($VALUE) > 0 ) {
					push(@PROXIES, "HTTPSProxy=$VALUE");
					if ( $VALUE !~ m/http:\/\/|https:\/\//i ) {
						push(@BAD_PROXY, "HTTPSProxy=$VALUE");
					}
				}
			}
		}
		SDP::Core::printDebug("RESULTS", "PROXIES: @PROXIES; BAD_PROXY: @BAD_PROXY");
		if ( $#BAD_PROXY >= 0 ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "SMT proxy configuration error in smt.conf for: @BAD_PROXY");
		} elsif ( $#PROXIES >= 0 ) {
			SDP::Core::updateStatus(STATUS_ERROR, "Validated SMT proxy configuration in smt.conf for: @PROXIES");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "No SMT proxies configured, skipping proxy test");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: checkSmtProxy(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	$RCODE = scalar @BAD_PROXY;
	SDP::Core::printDebug("< checkSmtProxy", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( SDP::SUSE::packageInstalled('smt') ) {
		checkSmtProxy();
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: SMT not installed, skipping SMT proxy test");
	}
SDP::Core::printPatternResults();

exit;

