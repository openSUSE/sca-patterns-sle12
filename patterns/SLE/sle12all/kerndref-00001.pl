#!/usr/bin/perl

# Title:       Kernel null pointer dereference
# Description: Null pointer dereference when using hugepages with the 2.6.16.60-0.101.1 kernel
# Modified:    2013 Jun 27

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
	PROPERTY_NAME_CATEGORY."=Kernel",
	PROPERTY_NAME_COMPONENT."=Memory",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7012445",
	"META_LINK_BUG=https://bugzilla.novell.com/show_bug.cgi?id=819403"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub hugePageActive {
	SDP::Core::printDebug('> hugePageActive', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'env.txt';
	my $SECTION = 'sysctl -a';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /^vm.nr_hugepages\s*=\s*(.*)/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE = $1;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: hugePageActive(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< hugePageActive", "Returns: $RCODE");
	return $RCODE;
}

sub hugePageDumped {
	SDP::Core::printDebug('> hugePageDumped', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'messages.txt';
	my $SECTION = '/var/log/messages';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /RIP:.*hugetlbfs_set_page_dirty/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: hugePageDumped(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< hugePageDumped", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( SDP::SUSE::compareKernel('2.6.16.60-0.101.1') == 0 ) {
		if ( SDP::SUSE::compareKernel('2.6.16.60-0.101.1.5472') == 0 ) {
			SDP::Core::updateStatus(STATUS_ERROR, "Kernel PTF applied, skipping kernel deref test");
		} else {
			if ( hugePageActive() ) {
				if ( hugePageDumped() ) {
					SDP::Core::updateStatus(STATUS_CRITICAL, "Detected kernel null pointer dereference when using hugepages");
				} else {
					SDP::Core::updateStatus(STATUS_WARNING, "Kernel susceptible to null pointer dereferencing");
				}
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, "Huge pages turned off, skipping kernel deref test");
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Error: Outside kernel scope, skipping kernel deref test");
	}
SDP::Core::printPatternResults();

exit;


