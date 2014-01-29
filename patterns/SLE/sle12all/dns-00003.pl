#!/usr/bin/perl

# Title:       DNS name resolution fails, novell-named errors
# Description: DNS name resolution fails along with novell-named errors
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
	PROPERTY_NAME_CATEGORY."=DNS",
	PROPERTY_NAME_COMPONENT."=Daemon",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006871"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub dnsErrors {
	SDP::Core::printDebug('> dnsErrors', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'messages.txt';
	my $SECTION = '/var/log/messages';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /couldn't add command channel.*#953.*address in use/i ) {
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: dnsErrors(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< dnsErrors", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my $SRVCOUNT = 0;
	my %SERVICE_INFO = SDP::SUSE::getServiceInfo('named');
	if ( $SERVICE_INFO{'running'} > 0 ) {
		$SRVCOUNT++;
	}
	%SERVICE_INFO = SDP::SUSE::getServiceInfo('novell-named');
	if ( $SERVICE_INFO{'running'} > 0 ) {
		$SRVCOUNT++;
	}

	if ( $SRVCOUNT > 1 ) {
		if ( dnsErrors() ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "DNS Service conflict with lookup errors: Use named or novell-named, but not both");
		} else {
			SDP::Core::updateStatus(STATUS_WARNING, "DNS Service conflict: Use named or novell-named, but not both");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: No DNS Service conflict to analyze");
	}
SDP::Core::printPatternResults();

exit;

