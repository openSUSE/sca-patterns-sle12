#!/usr/bin/perl -w

# Title:       Detect split kernel scenario
# Description: A split kernel scenario is when the running kernel does not match the installed kernel
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
	PROPERTY_NAME_CATEGORY."=Update",
	PROPERTY_NAME_COMPONENT."=Kernel",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7001056"
);
# Edit and convert to new TID with update causes 1) updated kernel, but didn't reboot, 2) updated when /boot was not mounted. Get symptoms when rebooting in split kernel scenario.

##############################################################################
# Local Function Definitions
##############################################################################

sub check_split_kernel {
	SDP::Core::printDebug('>', 'check_split_kernel');
	use constant HEADER_LINES => 3;
	my $FILE_OPEN              = 'boot.txt';
	my $SECTION                = 'ls -lR /boot';
	my @CONTENT                = ();
	my $LINE                   = 0;
	my @LINE_DATA              = ();
	my %HOST_INFO              = SDP::SUSE::getHostInfo();
	my $MATCHES                = 0;
	my $INSTALLED              = "";
	my $KERNEL_TYPE            = 'vmlinuz';
	my $KERNEL_STR             = '';

	$KERNEL_TYPE = 'vmlinux' if ( $HOST_INFO{'architecture'} =~ /ppc|s390/i );
	SDP::Core::printDebug('KERNEL TYPE', $KERNEL_TYPE);
	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			next if ( $LINE < HEADER_LINES );
			if ( /\s$KERNEL_TYPE-\d/ ) {
				SDP::Core::printDebug("CHECKING", $_);
				@LINE_DATA = split(/\s+/, $_);
				$KERNEL_STR = pop(@LINE_DATA);
				next if ( $KERNEL_STR eq $KERNEL_TYPE );
				SDP::Core::printDebug(" LINE $LINE", $_);
				$KERNEL_STR =~ s/$KERNEL_TYPE-//g;
				$MATCHES++ if ( SDP::Core::compareVersions($HOST_INFO{'kernel'}, $KERNEL_STR) == 0 );
				$INSTALLED = $INSTALLED . " " . $KERNEL_STR;
			}
		}
		SDP::Core::printDebug("MATCHES FOUND", $MATCHES);
		if ( $MATCHES ) {
			SDP::Core::updateStatus(STATUS_ERROR, "Running and installed kernels match: $HOST_INFO{'kernel'}");
		} elsif ( ! $INSTALLED ) {
			SDP::Core::updateStatus(STATUS_WARNING, "Update Warning: Potential for split kernel, no $KERNEL_TYPE in /boot");
		} else {
			$INSTALLED =~ s/^\s+|\s+$//g;
			SDP::Core::updateStatus(STATUS_CRITICAL, "Split kernel detected, Running: $HOST_INFO{'kernel'}, Installed: $INSTALLED");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug('<', 'check_split_kernel');
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	check_split_kernel();
SDP::Core::printPatternResults();

exit;

