#!/usr/bin/perl

# Title:       Xen performance and stability
# Description: Checks if Xen Dom0 is susceptible to being unresponsive when shutting down a DomU virtual machine
# Modified:    2013 Jun 28

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
	PROPERTY_NAME_COMPONENT."=Memory",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=3559698",
	"META_LINK_BUG=https://bugzilla.novell.com/show_bug.cgi?id=220421",
	"META_LINK_MISC=http://www.novell.com/support/php/search.do?cmd=displayKC&docType=kc&externalId=7001362&sliceId=&docTypeID=DT_TID_1_1"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub checkMemLock {
	SDP::Core::printDebug('> checkMemLock', "BEGIN");
	my @DOM0MEM = ();
	my $XENINST = 0;
	my $MEMDEF = 0;
	my $RCODE = 0;
	my $FILE_OPEN = 'boot.txt';
	my $SECTION = '/boot/grub/menu.lst';
	my @CONTENT = ();
	my @LINE_CONTENT = ();
	my $LINE = 0;
	my $i;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /^\s+kernel.*\/xen\.gz/ ) {
				$XENINST++; # Xen kernel installed
				SDP::Core::printDebug("LINE $LINE", $_);
				@LINE_CONTENT = split(/\s+/, $_);
				foreach $i (@LINE_CONTENT) {
					if ( $i =~ /dom0_mem=(\d+)/ ) {
						$MEMDEF++; # Memory reserved for this Xen kernel
						push(@DOM0MEM, $1);
					}
				}
			}
		}
		if ( $XENINST == 0 ) {
			SDP::Core::updateStatus(STATUS_ERROR, "Xen kernel not installed or used");
		} elsif ( $XENINST != $MEMDEF ) {
			if ( SDP::SUSE::xenDom0running() ) {
				SDP::Core::updateStatus(STATUS_CRITICAL, "Not all Xen kernels have dom0_mem set, check menu.lst");
			} else {
				SDP::Core::updateStatus(STATUS_WARNING, "Not all Xen kernels have dom0_mem set, check menu.lst before booting to Xen");
			}
		} else {
			SDP::Core::updateStatus(STATUS_PARTIAL, "All Xen kernels have dom0_mem set");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< checkMemLock", "Returns: @DOM0MEM");
	return @DOM0MEM;
}

sub checkBallooning {
	SDP::Core::printDebug('> checkBallooning', "BEGIN");
	my $RCODE = 0;
	my $FILE_OPEN = 'xen.txt';
	my $SECTION = 'xend-config.sxp';
	my @CONTENT = ();
	my $LINE = 0;
	my $i;
	if  ( SDP::SUSE::compareKernel(SLE11GA) >= 0 && SDP::SUSE::compareKernel(SLE12GA) < 0 ) {
		SDP::Core::printDebug('XEN', 'SLE11 Ballooning');
		if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
			foreach $_ (@CONTENT) {
				$LINE++;
				next if ( /^\s*$/ ); # Skip blank lines
				if ( /^\(enable-dom0-ballooning\s+(\S+)/ ) {
					SDP::Core::printDebug("LINE $LINE", "$_");
					if ( $1 =~ /yes/i ) {
						$RCODE++;
						last;
					}
				}
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
		}
	} elsif  ( SDP::SUSE::compareKernel(SLE10GA) >= 0 && SDP::SUSE::compareKernel(SLE11GA) < 0 ) {
		SDP::Core::printDebug('XEN', 'SLE10 Ballooning');
		my $BALLOONS = $_[0]; # Array reference

		if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
			foreach $_ (@CONTENT) {
				$LINE++;
				next if ( /^\s*$/ ); # Skip blank lines
				if ( /^\(dom0-min-mem\s+(\d+)/ ) {
					SDP::Core::printDebug("LINE $LINE", "$_ Must match each: @$BALLOONS");
					foreach $i (@$BALLOONS) {
						if ( $i != $1 ) {
							$RCODE++;
						}
					}
				}
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Xen outside the kernel scope");
	}
	if ( $RCODE > 0 ) {
		if ( SDP::SUSE::xenDom0running() ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Xen memory ballooning is enabled");
		} else {
			SDP::Core::updateStatus(STATUS_WARNING, "Xen memory ballooning is enabled, disable before booting to Xen");
		}
	} else {
		SDP::Core::updateStatus(STATUS_PARTIAL, "Xen memory ballooning is disabled");
	}
	SDP::Core::printDebug("< checkBallooning", "Returns: $RCODE");
	return $RCODE;
}

sub checkVcpu {
	SDP::Core::printDebug('> checkVcpu', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'xen.txt';
	my $SECTION = 'xend-config.sxp';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /^\(dom0-cpus\s+(\d+)/ ) {
				if ( $1 == 1 ) {
					if ( SDP::SUSE::xenDom0running() ) {
						SDP::Core::updateStatus(STATUS_CRITICAL, "Dom0 restricted to one virtual CPU");
					} else {
						SDP::Core::updateStatus(STATUS_WARNING, "Dom0 restricted to one virtual CPU, increase before booting to Xen");
					}
					$RCODE++;
				} else {
					SDP::Core::updateStatus(STATUS_PARTIAL, "More than one virtual CPU configured");
				}
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< checkVcpu", "Returns: $RCODE");
	return $RCODE;
}
##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my @MEMCHECKS = checkMemLock();
	checkBallooning(\@MEMCHECKS);
	checkVcpu();
	SDP::Core::setStatus(STATUS_ERROR, "Xen performance and stability configuration confirmed") if ($GSTATUS < 1);
SDP::Core::printPatternResults();

exit;


