#!/usr/bin/perl

# Title:       Multiple Hypervisor Detection
# Description: Detects unsupported multiple virtualization hypervisors.
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
	PROPERTY_NAME_CATEGORY."=Virtualization",
	PROPERTY_NAME_COMPONENT."=Hypervisor",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7003403"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub check_multi_hypervisor {
	SDP::Core::printDebug('>', 'check_multi_hypervisor');
	my $RCODE                    = 0;
	my $FILE_OPEN                = 'basic-environment.txt';
	my $SECTION                  = 'Virtualization';
	my @CONTENT                  = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ );                   # Skip blank lines
			if ( /^Hypervisor:/ ) {
				SDP::Core::printDebug("LINE", $_);
				$RCODE++;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	if ( $RCODE > 1 ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "Multiple hypervisors detected");
	} elsif ( $RCODE > 0 ) {
		SDP::Core::updateStatus(STATUS_ERROR, "Only one hypervisor observed");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "No hypervisors installed");
	}
	SDP::Core::printDebug("< Returns: $RCODE", 'check_multi_hypervisor');
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	check_multi_hypervisor();
SDP::Core::printPatternResults();

exit;

