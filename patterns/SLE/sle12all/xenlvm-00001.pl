#!/usr/bin/perl

# Title:       Xen performance with multiple LVM layers
# Description: Xen does not perform well when both the Dom0 and DomU are using LVM.
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
	PROPERTY_NAME_COMPONENT."=LVM",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=3559698",
	"META_LINK_MISC=http://www.novell.com/support/php/search.do?cmd=displayKC&docType=kc&externalId=7001362&sliceId=&docTypeID=DT_TID_1_1"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub checkLVM {
	my $XEN_STR = $_[0];
	SDP::Core::printDebug('> checkLVM', "Checking: $XEN_STR");
	my $RCODE = 0;
	my $HEADER_LINES = 0;
	my $FILE_OPEN = 'lvm.txt';
	my $SECTION = '/lvs';
	my @CONTENT = ();
	my @LINE_CONTENT = ();
	my $LINE = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		SDP::Core::printDebug('CONTENT', "'$CONTENT[0]'");
		if ( $CONTENT[0] =~ /LV\s+VG/ ) {
			if ( $XEN_STR =~ /Dom0/ ) {
				SDP::Core::updateStatus(STATUS_WARNING, "$XEN_STR is using LVM, don't use LVM in any VM");
			} else {
				SDP::Core::updateStatus(STATUS_WARNING, "$XEN_STR is using LVM, don't use LVM in Dom0");
			}
			$RCODE = 1;
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "$XEN_STR is not using LVM");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< checkLVM", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( SDP::SUSE::xenDom0installed() ) {
		checkLVM('Xen Dom0');
	} elsif ( SDP::SUSE::xenDomU() ) {
		checkLVM('Xen DomU');
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Not running Xen with LVM");
	}
SDP::Core::printPatternResults();

exit;

