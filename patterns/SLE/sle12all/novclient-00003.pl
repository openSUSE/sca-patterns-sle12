#!/usr/bin/perl

# Title:       Novell Client induced kernel failures
# Description: Repeated connects/disconnects to a novell server using the Novell Client for Linux will cause kernel failures.
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
	PROPERTY_NAME_CATEGORY."=Novell",
	PROPERTY_NAME_COMPONENT."=Client",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006900"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub kernelErrorsFound {
	SDP::Core::printDebug('> kernelErrorsFound', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'messages.txt';
	my $SECTION = '/var/log/messages';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /kernel.*VFS.*Busy inodes after unmount of novfs.*Self-destruct/i ) {
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: kernelErrorsFound(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< kernelErrorsFound", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if  ( SDP::SUSE::compareKernel(SLE10SP3) >= 0 && SDP::SUSE::compareKernel(SLE11SP2) < 0 ) {
		if ( SDP::SUSE::packageInstalled('novell-client') ) {
			if ( SDP::SUSE::compareKernel('2.6.32.19') < 0 ) {
				if ( kernelErrorsFound() ) {
					SDP::Core::updateStatus(STATUS_CRITICAL, "Novell Client induced kernel errors observed");
				} else {
					SDP::Core::updateStatus(STATUS_WARNING, "Susceptible to Novell Client induced kernel errors");
				}
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, "Updated kernel stablizes workstation performance when using the Novell Client");
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Novell Client not Installed, Skipping performance test");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Outside Kernel Scope, Skipping Novell Client performance test");
	}
SDP::Core::printPatternResults();

exit;

