#!/usr/bin/perl

# Title:       Missing User Name Error, Workstation Fails to Join
# Description: Error attempting to join domain: The user name could not be found.
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

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=SLE",
	PROPERTY_NAME_CATEGORY."=Samba",
	PROPERTY_NAME_COMPONENT."=User",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7005642"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub errorFound {
	SDP::Core::printDebug('> errorFound', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'samba.txt';
	my $SECTION = '/var/log/samba/log.smbd';
	my @CONTENT = ();
	my $STATE = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( $STATE ) {
				if ( /_samr_create_user.*Running the command.*namuseradd.*gave 1/i ) {
					SDP::Core::printDebug(" CONFIRMED", $_);
					$RCODE++;
					last;
				} else {
					SDP::Core::printDebug(" DENIED", $_);
				}
				$STATE = 0;
			} elsif ( /\[.*\].*passdb\/pdb_interface\.c\:pdb_default_create_user\(329\)/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$STATE = 1;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: errorFound(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< errorFound", "Returns: $RCODE");
	return $RCODE;
}

sub invalidConfig {
	SDP::Core::printDebug('> invalidConfig', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'samba.txt';
	my $SECTION = 'smb.conf';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /enable privileges.*no/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: invalidConfig(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< invalidConfig", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my $SMB_DOWN = SDP::SUSE::serviceStatus('samba.txt', 'smb');
	if ( $SMB_DOWN ) {
		SDP::Core::updateStatus(STATUS_ERROR, "Skipping Join Test, Requires Samba SMB to be Up");
	} else {
		if ( errorFound() ) {
			if ( invalidConfig() ) {
				SDP::Core::updateStatus(STATUS_CRITICAL, "Workstation join failure, set enable privileges to yes");
			} else {
				SDP::Core::updateStatus(STATUS_WARNING, "Workstation joins may fail, check SeMachineAccountPrivilege");
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "SeMachineAccountPrivilege appears Valid");
		}
	}
SDP::Core::printPatternResults();

exit;

