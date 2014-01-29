#!/usr/bin/perl

# Title:       SLES for VMware Support
# Description: Initial SLES for VMware support offered by VMware
# Modified:    2013 Dec 10
#
##############################################################################
# Copyright (C) 2013 SUSE LLC
##############################################################################
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#  Authors/Contributors:
#   Jason Record (jrecord@suse.com)
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
"META_CLASS=SLE",
"META_CATEGORY=Support",
"META_COMPONENT=VMware",
"PATTERN_ID=$PATTERN_ID",
"PRIMARY_LINK=META_LINK_Support",
"OVERALL=$GSTATUS",
"OVERALL_INFO=NOT SET",
"META_LINK_Support=https://www.vmware.com/support/services/basic.html",
"META_LINK_Info=http://www.vmware.com/products/sles-for-vmware/",
);

##############################################################################
# Local Function Definitions
##############################################################################

sub slesVMware {
	SDP::Core::printDebug('> slesVMware', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'basic-environment.txt';
	my $SECTION = 'Product';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /\svmware/i ) {
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: slesVMware(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< slesVMware", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( slesVMware() ) {
		SDP::Core::updateStatus(STATUS_WARNING, "Technical Support offered by VMware");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Error: No SLE for VMware, skipping");
	}
SDP::Core::printPatternResults();

exit;


