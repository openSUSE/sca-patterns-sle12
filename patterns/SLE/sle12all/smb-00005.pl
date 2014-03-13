#!/usr/bin/perl

# Title:       Access Denied Error, Workstation Fails to Join
# Description: Error attempting to join domain: The user name could not be found, ACCESS_DENIED
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
	PROPERTY_NAME_CATEGORY."=Samba",
	PROPERTY_NAME_COMPONENT."=Access",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7005562"
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

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /smbldap_open.*cannot access LDAP when not root/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: errorFound(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< errorFound", "Returns: $RCODE");
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
			SDP::Core::updateStatus(STATUS_WARNING, "Workstation joins may fail, check Samba user configuration");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "Samba Users Appear Valid");
		}
	}
SDP::Core::printPatternResults();

exit;

