#!/usr/bin/perl

# Title:       Confirms fstab entries are mounted
# Description: Mount points in fstab are intended to be mounted
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
	PROPERTY_NAME_CATEGORY."=Filesystem",
	PROPERTY_NAME_COMPONENT."=Mount",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006069",
	"META_LINK_MISC=http://wiki.opensuse.org/SDB:Basics_of_partitions,_filesystems,_mount_points"
);

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my @MOUNTS = SDP::SUSE::getFileSystems();
	my $TMP;
	my @NOT_MOUNTED = ();

	foreach $TMP (@MOUNTS) {
		SDP::Core::printDebug("ANALYZE", "$TMP->{'MPT'}, Mounted=$TMP->{'MOUNTED'}, Type=$TMP->{'TYPE'}, Options=$TMP->{'OPTIONS'}");
		if ( $TMP->{'MOUNTED'} == 0 ) { # File system not mounted
			if ( $TMP->{'TYPE'} !~ m/subfs/i && $TMP->{'OPTIONS'} !~ m/noauto/i ) { 
				SDP::Core::printDebug(" FAILED", "NOT MOUNTED");
				push(@NOT_MOUNTED, "$TMP->{'MPT'}($TMP->{'TYPE'})");
			} else {
				SDP::Core::printDebug(" IGNORED", "For noauto or subfs");
			}
		}
	}
	if ( $#NOT_MOUNTED >= 0 ) {
		SDP::Core::updateStatus(STATUS_WARNING, "File systems configured, but not mounted: @NOT_MOUNTED");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "All fstab file systems are mounted");
	}
SDP::Core::printPatternResults();

exit;

