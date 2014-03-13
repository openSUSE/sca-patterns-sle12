#!/usr/bin/perl -w

# Title:       File system may go read-only in VMware
# Description: File system is switched to read-only in the event of busy I/O retry or path failover with SAN or iSCSI storage.
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
#    Jason Record (jrecord@suse.com)
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
	PROPERTY_NAME_CATEGORY."=Filesystem",
	PROPERTY_NAME_COMPONENT."=Read Only",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=3584352",
	"META_LINK_BUG=https://bugzilla.novell.com/show_bug.cgi?id=243958"
);
my $SLE8 = '2.4';
my $SLE9 = '2.6.5';
my $SLE9SP3 = '2.6.5-7.286';
my $SLE10SP1 = '2.6.16.46-0.12';

##############################################################################
# Local Function Definitions
##############################################################################

sub get_devlist_iscsi {
	printDebug('>', 'get_devlist_iscsi');
	my $RCODE       = 0;
	my $FILE_OPEN   = 'fs-iscsi.txt';
	my $SECTION     = 'iscsiadm \-m session';
	my @CONTENT     = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^$/ );
			$RCODE++;
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	printDebug("RETURN", $RCODE);
	printDebug('<', 'get_devlist_iscsi');
	return $RCODE;
}

# Right now it just checks if hba drivers are loaded. If they are, SAN use is
# assumed and the function returns true. 
#
# TO DO: return the if the drivers are loaded and the list of devices found on 
#        the server. This way a yellow flag can be set if the drivers are loaded
#        but no devices, and red can be set if there are devices.
sub get_devlist_san {
	printDebug('>', 'get_devlist_san');
	my $RCODE       = 0;
	my $FILE_OPEN   = 'modules.txt';
	my $SECTION     = 'lsmod';
	my @CONTENT     = ();
	my $SEARCHFOR   = 'lpfc|qla2|qla4';
	my $LINE        = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			if ( /^($SEARCHFOR)/ ) {
				printDebug("LINE $LINE", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	printDebug("RETURN", $RCODE);
	printDebug('<', 'get_devlist_san');
	return $RCODE;
}

sub running_under_vmware {
	printDebug('>', 'running_under_vmware');
	my $RCODE       = 0;
	my $FILE_OPEN   = 'hardware.txt';
	my $SECTION     = '/usr/sbin/hwinfo';
	my @CONTENT     = ();
	my $SEARCHFOR   = 'VMware Virtual Platform';
	my $LINE        = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			if ( /$SEARCHFOR/ ) {
				printDebug("LINE $LINE", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	printDebug("RETURN", $RCODE);
	printDebug('<', 'running_under_vmware');
	return $RCODE;
}
##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( running_under_vmware() ) {
		if ( SDP::SUSE::compareKernel($SLE9) > 0 && SDP::SUSE::compareKernel($SLE10SP1) < 0 ) {
			if ( get_devlist_iscsi() || get_devlist_san() ) {
				SDP::Core::updateStatus(STATUS_CRITICAL, 'File systems susceptible to going read-only');			
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, 'No SAN or iSCSI devices found');
			}
		} elsif ( SDP::SUSE::compareKernel($SLE8) > 0 && SDP::SUSE::compareKernel($SLE9SP3) < 0 ) {
			if ( get_devlist_iscsi() || get_devlist_san() ) {
				SDP::Core::updateStatus(STATUS_WARNING, 'File systems susceptible to going read-only');			
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, 'No SAN or iSCSI devices found');
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, 'Fixed in the running kernel');
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, 'Not running under VMware');
	}
SDP::Core::printPatternResults();

exit;

