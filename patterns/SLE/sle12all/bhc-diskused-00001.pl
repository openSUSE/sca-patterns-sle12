#!/usr/bin/perl -w

# Title:       Basic Health Check - File System Used Space
# Description: Check the available of mounted disk space
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
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#  Authors/Contributors:
#     Jason Record (jrecord@suse.com) - original BASH script
#
##############################################################################

##############################################################################
# Module Definition
##############################################################################

use strict;
use warnings;    # should be same as -w command option
use SDP::Core;
use SDP::SUSE;


##############################################################################
# Constants
##############################################################################

use constant LIMIT_OPT_DISKRED  => 90;          # % Disk Space Used; red
use constant LIMIT_OPT_DISKYEL  => 80;          # % Disk Space Used; yellow

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=Basic Health",
	PROPERTY_NAME_CATEGORY."=SLE",
	PROPERTY_NAME_COMPONENT."=Disk",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7002723",
	"META_LINK_TID2=http://www.suse.com/support/kb/doc.php?id=3005720"
);

##############################################################################
# Feature Subroutines
##############################################################################

# Check Free Memory and Disk Swapping
sub checkDiskUsed() {
	SDP::Core::printDebug('> checkDiskUsed');
	use constant HEADER_LINES     => 2;
	use constant DISK_PCT_FIELD   => 4;
	use constant DISK_MOUNT_FIELD => 5;
	use constant DISK_DEV_FIELD   => 0;
	use constant FSTYPE_FIELD     => 4;
	my $FILE_OPEN                 = 'fs-diskio.txt';
	my $SECTION                   = 'mount';
	my @CONTENT                   = ();
	my @MOUNTCMD                  = ();
	my @MOUNT_CONTENT             = ();
	my $MOUNT_LINE                = "";
	my $LINE                      = 0;
	my $LINE_WRAPPED              = 0;
	my $i                         = 0;
	my @LINE_DATA                 = ();
	my @MOUNT_DEV                 = ();
	my @DFDATA                    = ();
	my $TMP_USED_PCT              = 0;
	my $HIGHEST_DISK_USED_PCT     = 0;
	my $HIGHEST_MOUNT             = "";
	my $EXCEPTION_LIST            = "sysfs|proc|debugfs|tmpfs|devpts|fusectl|securityfs|iso9660";
	my $PROPERTY_NAME_DISK        = "DISK";
	my $DISK_NUM                  = 1;

	if ( ! SDP::Core::getSection($FILE_OPEN, $SECTION, \@MOUNTCMD) ) {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}

	$FILE_OPEN                 = 'basic-health-check.txt';
	$SECTION                   = 'df -h';
	$LINE                      = 0;
	my $FS_CHECKED             = 0;
	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			next if ( $LINE < HEADER_LINES );
			next if ( m/^\s*$/ );
			$_ =~ s/^\s+//;
			@LINE_DATA = split(/\s+/, $_);
			SDP::Core::printDebug("  checkDiskUsed LINE", "$#LINE_DATA of ". DISK_MOUNT_FIELD ." :: @LINE_DATA");
			if ( $LINE_WRAPPED ) {
				for ( $i = 0; $i <= $#LINE_DATA; $i++ ) {
					push(@DFDATA, $LINE_DATA[$i]);
				}
				$LINE_WRAPPED=0;
			} else {
				@DFDATA = @LINE_DATA;
			}
			if ( $#DFDATA < DISK_MOUNT_FIELD ) {
				SDP::Core::printDebug("  checkDiskUsed STATUS", "INCOMPLETE");
				@DFDATA = @LINE_DATA;
				$LINE_WRAPPED=1;
			} else {
				foreach $MOUNT_LINE (@MOUNTCMD) {
					@MOUNT_CONTENT = split(/\s+/, $MOUNT_LINE);
					if ( $#MOUNT_CONTENT > 0 && $MOUNT_CONTENT[0] =~ m/$DFDATA[0]/ ) {
						if ( $MOUNT_CONTENT[FSTYPE_FIELD] !~ m/$EXCEPTION_LIST/ ) {
							$TMP_USED_PCT = $DFDATA[DISK_PCT_FIELD];
							SDP::Core::printDebug("  checkDiskUsed STATUS", "Complete - $TMP_USED_PCT :: $HIGHEST_DISK_USED_PCT\%");
							if($TMP_USED_PCT) {
		  						$TMP_USED_PCT =~ s/\%//;
								if ( $TMP_USED_PCT >= LIMIT_OPT_DISKRED ) {
									SDP::Core::updateStatus(STATUS_CRITICAL, "$TMP_USED_PCT% exceeds ".LIMIT_OPT_DISKRED."% mounted on " . $DFDATA[DISK_MOUNT_FIELD]);
								} elsif ( $TMP_USED_PCT >= LIMIT_OPT_DISKYEL ) {
									SDP::Core::updateStatus(STATUS_WARNING, "$TMP_USED_PCT% exceeds ".LIMIT_OPT_DISKYEL."% mounted on " . $DFDATA[DISK_MOUNT_FIELD]);
								}
								if ( $HIGHEST_DISK_USED_PCT < $TMP_USED_PCT ) {
									$HIGHEST_DISK_USED_PCT = $TMP_USED_PCT;
									$HIGHEST_MOUNT         = $DFDATA[DISK_MOUNT_FIELD]; 
								}
							}
						} else {
							SDP::Core::printDebug("  checkDiskUsed EXCEPTION", "Skipped file system: $DFDATA[DISK_DEV_FIELD] type $MOUNT_CONTENT[FSTYPE_FIELD]");
						}
					}
				}
			}
		}
		SDP::Core::printDebug("  checkDiskUsed HIGHEST", "$HIGHEST_MOUNT at $HIGHEST_DISK_USED_PCT\%");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}

	# check against thresholds for status and message
	if ( $HIGHEST_DISK_USED_PCT >= LIMIT_OPT_DISKRED ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "$HIGHEST_DISK_USED_PCT% exceeds ".LIMIT_OPT_DISKRED."% mounted on $HIGHEST_MOUNT");
	} elsif ( $HIGHEST_DISK_USED_PCT >= LIMIT_OPT_DISKYEL ) {
		SDP::Core::updateStatus(STATUS_WARNING, "$HIGHEST_DISK_USED_PCT% exceeds ".LIMIT_OPT_DISKYEL."% mounted on $HIGHEST_MOUNT");
	} else {
		SDP::Core::updateStatus(STATUS_SUCCESS, "Mount on $HIGHEST_MOUNT has highest used space: $HIGHEST_DISK_USED_PCT%");
	}
	SDP::Core::printDebug('< checkDiskUsed');
}


##############################################################################
# Main
##############################################################################

SDP::Core::processOptions();
checkDiskUsed();
SDP::Core::printPatternResults();
exit;

