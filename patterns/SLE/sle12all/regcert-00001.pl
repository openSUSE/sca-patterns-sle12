#!/usr/bin/perl

# Title:       Registration errors with suse_register
# Description: SUSE Registration Fails with Certificate and Permission Errors
# Modified:    2013 Jun 25

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
	PROPERTY_NAME_CATEGORY."=Update",
	PROPERTY_NAME_COMPONENT."=Registration",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7008662"
);

my @HOST_ENTRIES = ();

##############################################################################
# Local Function Definitions
##############################################################################

sub registrationHosts {
	SDP::Core::printDebug('> registrationHosts', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'network.txt';
	my $SECTION = '/etc/hosts';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /secure-www\.novell\.com/ ) {
				push(@HOST_ENTRIES, 'secure-www.novell.com');
			} elsif ( /nu\.novell\.com/ ) {
				push(@HOST_ENTRIES, 'nu.novell.com');
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: registrationHosts(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	$RCODE = scalar @HOST_ENTRIES;
	SDP::Core::printDebug("< registrationHosts", "Returns: $RCODE");
	return $RCODE;
}

sub regErrors {
	SDP::Core::printDebug('> regErrors', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'updates.txt';
	my @CONTENT = ();
	my ($CURL_SECTION,$ZYP_SECTION) = (0,0);

	if ( SDP::Core::loadFile($FILE_OPEN, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			if ( $CURL_SECTION ) {
				if ( /^#==\[/ ) {
					$CURL_SECTION = 0;
				} elsif ( /curl.*SSL.*certificate subject name.*does not match target host name/ ) {
					$RCODE++;
					last;
				}
			} elsif ( $ZYP_SECTION ) {
				if ( /^#==\[/ ) {
					$ZYP_SECTION = 0;
				} elsif ( /Exception\.cc.*Error message.*SSL.*certificate subject name.*does not match target host name/ ) {
					$RCODE++;
					last;
				}
			} elsif ( /^# .*curl --verbose/ ) {
				$CURL_SECTION = 1;
			} elsif ( /^# .*zypper\.log/ ) {
				$ZYP_SECTION = 1;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: regErrors(): Cannot load file $FILE_OPEN");
	}
	SDP::Core::printDebug("< regErrors", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( registrationHosts() ) {
		if ( regErrors() ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Host file entries causing server registration failures: @HOST_ENTRIES");
		} else {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Host file entries will cause server registration failures: @HOST_ENTRIES");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "No registration host entries, skipping suse_register cert error");
	}
SDP::Core::printPatternResults();

exit;

