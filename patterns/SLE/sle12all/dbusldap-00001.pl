#!/usr/bin/perl

# Title:       D-Bus hang with LDAP authentication
# Description: Boot hangs on Starting D-Bus daemon when ldap authentication enabled
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
	PROPERTY_NAME_CATEGORY."=LDAP",
	PROPERTY_NAME_COMPONENT."=Auth",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7007555",
	"META_LINK_BUG=https://bugzilla.novell.com/show_bug.cgi?id=602540"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub ldapAuthenticated {
	SDP::Core::printDebug('> ldapAuthenticated', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'pam.txt';
	my $SECTION = '/etc/nsswitch.conf';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /^passwd.*\sldap/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			} elsif ( /^group.*\sldap/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: ldapAuthenticated(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< ldapAuthenticated", "Returns: $RCODE");
	return $RCODE;
}

sub hardBindPolicy {
	SDP::Core::printDebug('> hardBindPolicy', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'ldap.txt';
	my $SECTION = '/etc/ldap.conf';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /bind_policy.*hard/ ) {
				$RCODE++;
				last;
			}
		}
		$RCODE > 0 ? SDP::Core::printDebug("BIND_POLICY", "HARD") : SDP::Core::printDebug("BIND_POLICY", "SOFT");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: hardBindPolicy(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< hardBindPolicy", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( ldapAuthenticated() ) {
		if ( hardBindPolicy() ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Change to soft LDAP bind_policy to avoid potential server hang at boot");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "D-Bus is fine with soft LDAP bind_policy");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Server does not use ldap bindings");
	}
SDP::Core::printPatternResults();

exit;

