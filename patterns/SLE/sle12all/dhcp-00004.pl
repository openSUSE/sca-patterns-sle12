#!/usr/bin/perl

# Title:       DHCP Server Fails To Start failover peer
# Description: DHCP Server Fails To Start: failover peer FailoverPeer-1: not found
# Modified:    2013 Jun 24

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
	PROPERTY_NAME_CATEGORY."=DHCP",
	PROPERTY_NAME_COMPONENT."=Peer",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7008808"
);




##############################################################################
# Local Function Definitions
##############################################################################

sub hostOnLoopBack {
	SDP::Core::printDebug('> hostOnLoopBack', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'network.txt';
	my $SECTION = '/etc/hosts';
	my @CONTENT = ();
	my %HOST_INFO = SDP::SUSE::getHostInfo();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /^127\.\d*\.\d*\.\d*\s*$HOST_INFO{'hostname'}/ ) {
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: hostOnLoopBack(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< hostOnLoopBack", "Returns: $RCODE");
	return $RCODE;
}

sub dhcpError {
	SDP::Core::printDebug('> dhcpError', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'dhcp.txt';
	my $SECTION = '/var/log/warn';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (reverse(@CONTENT)) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /failover peer .*: not found/ ) {
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: dhcpError(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< dhcpError", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my $SERVICE_NAME = 'dhcpd';
	my %SERVICE_INFO = SDP::SUSE::getServiceInfo($SERVICE_NAME);
	if ( $SERVICE_INFO{'runlevelstatus'} && ! $SERVICE_INFO{'running'} ) {
		if ( hostOnLoopBack() ) {
			if ( dhcpError() ) {
				SDP::Core::updateStatus(STATUS_CRITICAL, "DHCP Error, Host Defined on Loopback Address");
			} else {
				SDP::Core::updateStatus(STATUS_WARNING, "DHCP Warning, Host Defined on Loopback Address");
			}
		} else {
			SDP::Core::updateStatus(STATUS_PARTIAL, "Host not on loopback, skipping DHCP test");
		}
	} else {
		if ( ! $SERVICE_INFO{'running'} ) {
			if ( dhcpError() ) {
				if ( hostOnLoopBack() ) {
					SDP::Core::updateStatus(STATUS_CRITICAL, "DHCP Error, Host Defined on Loopback Address");
				} else {
					SDP::Core::updateStatus(STATUS_WARNING, "DHCP Peer Error Detected, but Host is Not Defined on Loopback Address; Restart DHCP Service");
				}
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, "DHCP Not Running, but No Peer Error Detected");
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "DHCP Running, skipping DHCP test");
		}
	}
SDP::Core::printPatternResults();

exit;

