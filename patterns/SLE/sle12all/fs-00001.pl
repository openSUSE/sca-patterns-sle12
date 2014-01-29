#!/usr/bin/perl -w

# Title:       Ext3 File system Going Read-Only
# Description: An ext3 file system may be remounted read-only by the kernel.
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
	PROPERTY_NAME_CATEGORY."=Filesystem",
	PROPERTY_NAME_COMPONENT."=Read Only",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=3605538",
	"META_LINK_BUG=https://bugzilla.novell.com/show_bug.cgi?id=354451"
);

##############################################################################
# Program execution functions
##############################################################################

sub filesystem_exists {
	SDP::Core::printDebug(">", "filesystem_exists");
	use constant FSTYPE  => 4;
	my $RCODE            = 0;
	my $FS_TO_CHECK      = $_[0];
	my $FILE_OPEN        = "fs-diskio.txt";
	my $SECTION          = '/bin/mount';
	my @CONTENT          = ();
	my @MOUNTED          = ();
	my $LINE             = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			chomp;
			$LINE++;
			@MOUNTED = split(/\s/, $_);
			if ( $#MOUNTED > 0 ) {
				if ( $MOUNTED[FSTYPE] =~ m/$FS_TO_CHECK/i ) {
					printDebug("LINE $LINE", $_);
					$RCODE++;
					last;
				}
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Mount section NOT FOUND in $FILE_OPEN");
	}
	SDP::Core::printDebug("RETURN CODE", $RCODE);
	SDP::Core::printDebug("<", "filesystem_exists\n");
	return $RCODE;
}

SDP::Core::processOptions();
	if ( filesystem_exists('EXT3') ) {
		if ( SDP::SUSE::compareKernel('2.6.16.54-0.2.8') < 0 ) {
			SDP::Core::updateStatus(STATUS_WARNING, "Ext3 file systems susceptible to going read only");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "Ext3 file systems not susceptible to going read only");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "No ext3 filesystems");
	}
SDP::Core::printPatternResults();

exit;

