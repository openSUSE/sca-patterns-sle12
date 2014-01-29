#!/usr/bin/perl -w

# Title:       Xen with NetworkManager
# Description: Xen is incomputable with the NetworkManager.
# Modified:    2013 Jun 28

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
	PROPERTY_NAME_CLASS."=SLE",
	PROPERTY_NAME_CATEGORY."=Virtualization",
	PROPERTY_NAME_COMPONENT."=Xen",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=3588210"
);

##############################################################################
# Program execution functions
##############################################################################
sub xen_kernel_installed {
	printDebug('>', 'xen_kernel_installed');
	my $RCODE=0;
	my %HOSTINFO = SDP::SUSE::getHostInfo();
	printDebug("KERNEL", $HOSTINFO{'kernel'});
	if ( $HOSTINFO{'kernel'} =~ m/xen/i ) {
		printDebug('XEN', 'Kernel Found');
		$RCODE++;
	} else {
		printDebug('XEN', 'Kernel Not Found');
	}
	printDebug('RETURN', $RCODE);
	printDebug('<', 'xen_kernel_installed');
	return $RCODE;
}

sub using_network_manager {
	printDebug('>', 'using_network_manager');
	my $RCODE          = 0;
	my $FILE_OPEN      = 'network.txt';
	my $SECTION        = '/etc/sysconfig/network/config';
	my $SEARCH_STRING  = 'NETWORKMANAGER';
	my @CONTENT        = ();
	my @NM_SETTING     = ();
	my $LINE           = 0;
	my $FOUND          = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
#			printDebug("LINE $LINE", $_);
			if ( m/^$SEARCH_STRING/ ) {
				printDebug("LINE $LINE", $_);
				$FOUND++;
				@NM_SETTING = split(/=/, $_);
				$NM_SETTING[$#NM_SETTING] =~ s/\"|\'//;
				if ( $NM_SETTING[$#NM_SETTING] =~ m/yes/i ) {
					$RCODE++;
				}
				last;
			}
		}
		SDP::Core::updateStatus(STATUS_ERROR, "Network Manager setting not found") if ( ! $FOUND );
	} else {
	}
	printDebug('RETURN', $RCODE);
	printDebug('<', 'using_network_manager');
	return $RCODE;
}

SDP::Core::processOptions();
	if ( xen_kernel_installed() ) {
		if ( using_network_manager() ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Xen running with Network Manager enabled");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "Xen running with traditional networking");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Xen kernel not installed");
	}
SDP::Core::printPatternResults();

exit;

