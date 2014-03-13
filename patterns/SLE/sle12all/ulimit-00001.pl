#!/usr/bin/perl

# Title:       Ulimit settings fail on system boot
# Description: Using ulimit with /etc/sysconfig/ulimit fails at boot time
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
	PROPERTY_NAME_CATEGORY."=Boot",
	PROPERTY_NAME_COMPONENT."=Ulimit",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7005716",
	"META_LINK_BUG=https://bugzilla.novell.com/show_bug.cgi?id=562168"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub errorFound {
	SDP::Core::printDebug('> errorFound', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'boot.txt';
	my $SECTION = 'boot.msg';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /initscript.*ulimit.*open files.*cannot modify limit.*Invalid argument/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: errorFound(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< errorFound", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my $SCOPE = 1; # valid kernel scope
	my $RPM_NAME = 'ulimit';
	my $VERSION_TO_COMPARE = '';
	if ( SDP::SUSE::compareKernel(SLE11GA) >= 0 ) {
		$VERSION_TO_COMPARE = '1.2-1.22.1';
	} elsif ( SDP::SUSE::compareKernel(SLE10GA) >= 0 ) {
		$VERSION_TO_COMPARE = '1.2-2.4.14';
	} else {
		$SCOPE = 0; # invalid kernel scope
	}

	if ( $SCOPE ) {
		my $RPM_COMPARISON = SDP::SUSE::compareRpm($RPM_NAME, $VERSION_TO_COMPARE);
		if ( $RPM_COMPARISON == 2 ) {
			SDP::Core::updateStatus(STATUS_ERROR, "ERROR: RPM $RPM_NAME Not Installed");
		} elsif ( $RPM_COMPARISON > 2 ) {
			SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Multiple Versions of $RPM_NAME RPM are Installed");
		} else {
			if ( $RPM_COMPARISON <= 0 ) {
				if ( errorFound() ) {
					SDP::Core::updateStatus(STATUS_CRITICAL, "Settings in /etc/sysconfig/ulimit failed to apply");
				} else {
					SDP::Core::updateStatus(STATUS_WARNING, "Changing /etc/sysconfig/ulimit will fail to apply at boot");
				}
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, "Updated ulimit observed");
			}			
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Skipping ulimit test, outside kernel scope");
	}
SDP::Core::printPatternResults();

exit;

