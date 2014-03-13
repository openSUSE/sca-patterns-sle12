#!/usr/bin/perl -w

# Title:       Check for failed or skipped services
# Description: Checks to see if any system daemons failed or were skipped at boot time.
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
	PROPERTY_NAME_CATEGORY."=Boot",
	PROPERTY_NAME_COMPONENT."=Service",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7002802"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub check_services {
	SDP::Core::printDebug('>', 'check_services');
	my $HEADER_LINES             = 0;
	my $RCODE                    = 0;
	my $FILE_OPEN                = 'boot.txt';
	my $SECTION                  = 'boot.msg';
	my @CONTENT                  = ();
	my @LINE_CONTENT             = ();
	my $VALUE_FIELD              = 1;
	my $LINE                     = 0;
	my $SERVICE_STR              = "";

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( $LINE++ < $HEADER_LINES ); # Skip header lines
			next if ( /^\s*$/ );                    # Skip blank lines
			$SERVICE_STR = $_;
			if ( /Failed services in runlevel/i ) {
				SDP::Core::printDebug("LINE $LINE", $_);
				@LINE_CONTENT = split(/:/, $_);
				$LINE_CONTENT[$VALUE_FIELD] =~ s/^\s+|\s+$//g;
				SDP::Core::printDebug(" RESULT", $LINE_CONTENT[$VALUE_FIELD]);
				$LINE_CONTENT[$VALUE_FIELD] =~ s/microcode\.ctl//g if ( SDP::SUSE::xenDomU() );
				if ( $LINE_CONTENT[$VALUE_FIELD] ) {
					SDP::Core::updateStatus(STATUS_CRITICAL, "$SERVICE_STR");
					$RCODE++;
				} else {
					SDP::Core::updateStatus(STATUS_ERROR, "Failed Services: None");
				}
			} elsif ( /Skipped services in runlevel/i ) {
				SDP::Core::printDebug("LINE $LINE", $_);
				@LINE_CONTENT = split(/:/, $_);
				$LINE_CONTENT[$VALUE_FIELD] =~ s/^\s+|\s+$//g;
				$LINE_CONTENT[$VALUE_FIELD] =~ s/microcode\.ctl//g if ( SDP::SUSE::xenDomU() );
				if ( $LINE_CONTENT[$VALUE_FIELD] ) {
					SDP::Core::updateStatus(STATUS_ERROR, "$SERVICE_STR");
					$RCODE++;
				} else {
					SDP::Core::updateStatus(STATUS_ERROR, "Skipped Services: None");
				}
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< Returns: $RCODE", 'check_services');
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( ! check_services() ) {
		SDP::Core::updateStatus(STATUS_ERROR, "No failed or skipped services observed");
	}
SDP::Core::printPatternResults();

exit;

