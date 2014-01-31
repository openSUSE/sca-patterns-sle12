#!/usr/bin/perl

# Title:       DSfW recommended in OES environments for Samba PDC
# Description: Domain Services for Windows is recommended in OES environments.
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
use SDP::OESLinux;

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=SLE",
	PROPERTY_NAME_CATEGORY."=Samba",
	PROPERTY_NAME_COMPONENT."=PDC",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_MISC=http://www.novell.com/documentation/oes2/acc_dsfw_lx/?page=/documentation/oes2/acc_dsfw_lx/data/bookinfo.html#bookinfo"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub oesInstalled {
	SDP::Core::printDebug('> oesInstalled', 'BEGIN');
	my $RCODE = 0;
	my %HOST_INFO = SDP::SUSE::getHostInfo();
	$RCODE++ if ( $HOST_INFO{'oes'} );
	SDP::Core::printDebug("< oesInstalled", "Returns: $RCODE");
	return $RCODE;
}

sub isPDC {
	SDP::Core::printDebug('> isPDC', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'samba.txt';
	my $SECTION = 'smb.conf';
	my @CONTENT = ();
	my $GLOBAL = 0;
	my $PDC = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( $GLOBAL ) {
				if ( /domain master.*yes|preferred master.*yes|local master.*yes/i ) {
					SDP::Core::printDebug("PROCESSING", $_);
					$PDC++;
					$GLOBAL = 0;
					last;
				}
			} elsif ( /[global]/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$GLOBAL = 1;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: isPDC(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}

	my $SMB_DOWN = SDP::SUSE::serviceStatus($FILE_OPEN, 'smb');

	$RCODE++ if ( ! $SMB_DOWN && $PDC );
	SDP::Core::printDebug("< isPDC", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( SDP::OESLinux::dsfwCapable() ) {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: DSfW capable, abort PDC test for DSfW recommendation");
	} else {
		if ( oesInstalled() ) {
			if ( isPDC() ) {
				SDP::Core::updateStatus(STATUS_RECOMMEND, "Consider Domain Services for Windows on OES instead of a Samba PDC");
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, "Samba PDC not observed on OES for DSfW Recommendation");
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "Skipping Samba PDC Check, OES not installed");
		}
	}
SDP::Core::printPatternResults();

exit;

