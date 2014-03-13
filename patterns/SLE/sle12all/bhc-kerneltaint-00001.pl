#!/usr/bin/perl

# Title:       Basic Health Check - Tainted Kernel
# Description: Checks if the kernel is tainted or not
# Modified:    2013 Jun 20

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
#
#  Authors/Contributors:
#     Jason Record (jrecord@suse.com)
#
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
	PROPERTY_NAME_CLASS."=Basic Health",
	PROPERTY_NAME_CATEGORY."=SLE",
	PROPERTY_NAME_COMPONENT."=Kernel",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=3582750"
);

##############################################################################
# Feature Subroutines
##############################################################################

sub checkKernelTaint() {
	SDP::Core::printDebug('> checkKernelTaint');
	my $RCODE = 0;
	my $FILE_OPEN = 'basic-health-check.txt';
	my $SECTION = '/proc/sys/kernel/tainted';
	my @CONTENT = ();
	my @LINE_CONTENT = ();
	my $LINE = 0;
	my $TAINT = 0;
	my $TAINT_STR = '';

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		$TAINT = $CONTENT[0];
		$RCODE = 1 if ( $TAINT != 0 );
		for $_ (@CONTENT) {
			if ( /Kernel Status.*Tainted/i ) {
				s/\s+/ /g; # change to single space
				s/\s+$//; # remove trailing whitespace
				$TAINT_STR = $_;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	if ( $RCODE ) {
		my $XTAINT = $TAINT_STR;
		$XTAINT =~ s/\s*//g; # remove all white space
		(undef, $XTAINT) = split(/:/, $XTAINT);
		SDP::Core::printDebug('  checkKernelTaint XTAINT', $XTAINT);
		if ( $XTAINT !~ m/X/i ) {
			my %HOST_INFO = SDP::SUSE::getHostInfo();
			if ( $HOST_INFO{'oes'} ) {
				SDP::Core::updateStatus(STATUS_WARNING, "$TAINT_STR; Check non-OES drivers");
			} else {
				SDP::Core::updateStatus(STATUS_CRITICAL, "$TAINT_STR");
			}
		} else {
			SDP::Core::updateStatus(STATUS_SUCCESS, "$TAINT_STR, but modules are externally supported");
		}
	} else {
		SDP::Core::updateStatus(STATUS_SUCCESS, "The Kernel is not Tainted");
	}
	SDP::Core::printDebug("< checkKernelTaint", "Returns: $RCODE");
	return $RCODE;
}


##############################################################################
# Main
##############################################################################

SDP::Core::processOptions(); 
checkKernelTaint();
SDP::Core::printPatternResults();
exit;

