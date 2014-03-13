#!/usr/bin/perl

# Title:       YaST2 Modules Fail to Load
# Description: YaST2 works, but after update modules do not.
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
	PROPERTY_NAME_CATEGORY."=YaST",
	PROPERTY_NAME_COMPONENT."=Base",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7008908",
	"META_LINK_BUG=https://bugzilla.novell.com/show_bug.cgi?id=702423"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub xauthError {
	SDP::Core::printDebug('> xauthError', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'messages.txt';
	my $SECTION = '/var/log/messages';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /gnomesu-pam-backend.*pam_xauth.*root not listed in \/root\/\.xauth\/export/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: xauthError(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< xauthError", "Returns: $RCODE");
	return $RCODE;
}

sub rootMissingXauth {
	SDP::Core::printDebug('> rootMissingXauth', 'BEGIN');
	my $RCODE = 1;
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'env.txt';
	my $SECTION = '/root/.xauth/export';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /^root\s*$/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE = 0;
				last;
			}
		}
	} else {
		$RCODE = -1;
		SDP::Core::printDebug("rootMissingXauth()", "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< rootMissingXauth", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my $RPM_NAME = 'libgnomesu';
	my $VERSION_TO_COMPARE = '1.0.0-307.8.1';
	my $RPM_COMPARISON = SDP::SUSE::compareRpm($RPM_NAME, $VERSION_TO_COMPARE);
	if ( $RPM_COMPARISON == 2 ) {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: RPM $RPM_NAME Not Installed");
	} elsif ( $RPM_COMPARISON > 2 ) {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Multiple Versions of $RPM_NAME RPM are Installed");
	} else {
		if ( $RPM_COMPARISON == 0 ) {
			my $MISSING = rootMissingXauth();
			if ( $MISSING < 0 ) { # no export file to check
				if ( xauthError() ) {
					SDP::Core::updateStatus(STATUS_CRITICAL, "Detected Xauth Error, Yast2 Modules Will Fail to Load; Modify Xauth Exports");
				} else {
					SDP::Core::updateStatus(STATUS_WARNING, "If yast2 modules do not load, check Xauth exports");
				}
			} elsif ( $MISSING > 0 ) { # export file found and root is missing
				SDP::Core::updateStatus(STATUS_CRITICAL, "Yast2 Modules May Fail to Load, Modify Xauth Exports");
			} else { # export file found and contains root
				SDP::Core::updateStatus(STATUS_ERROR, "Yast2 Modules Will Load, no Xauth Export restriction");
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "Invalid $RPM_NAME version, skipping Xauth Export test");
		}			
	}
SDP::Core::printPatternResults();

exit;

