#!/usr/bin/perl

# Title:       Unused disk space with four primary partitions
# Description: The partition table has four primary partitioned defined but the hard drive also has unpartitioned, unusable space.
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
use constant TRAPPED_CRIT => 15;
use constant TRAPPED_WARN => 5;

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=SLE",
	PROPERTY_NAME_CATEGORY."=Disk",
	PROPERTY_NAME_COMPONENT."=Partition",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7004417"
);

my @PRIMARIES = ();
my $TRAP_SIZE = 0;
my $TRAP_USED = 0;

##############################################################################
# Local Function Definitions
##############################################################################

sub convertSize {
	SDP::Core::printDebug('> convertSize', "Convert: $1");
	my $CONVERT = $1;
	my %MULTIPLIER = (
		NA => 1,
		kB => 1024,
		MB => 1024*1024,
		GB => 1024*1024*1024,
		TB => 1024*1024*1024*1024,
	);
	my $TYPE = 'NA';
	if ( $CONVERT =~ m/[a-z]|[A-Z]/ ) {
		$CONVERT =~ m/(\D+)$/;
		$TYPE = $1;
		$CONVERT =~ s/$TYPE//g; 
	}
	my $CONVERTED = $CONVERT * $MULTIPLIER{$TYPE};
	$CONVERTED =~ s/\..*//g;
	SDP::Core::printDebug("CONVERT INFO", "CONVERT=$CONVERT, TYPE=$TYPE");
	SDP::Core::printDebug("< convertSize", "Returns: $CONVERTED");
	return $CONVERTED;
}

sub trappedDiskSpace {
	SDP::Core::printDebug('> trappedDiskSpace', 'BEGIN');
	my $RCODE = 0;
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'fs-diskio.txt';
	my $SECTION = '';
	my @CONTENT = ();
	my @FILE_SECTIONS = ();
	my $PRI_CNT = 0;
	my $MSDOS = 0;
	my $DISK_DEV = '';
	my $DISK_SIZE = 0;
	my $DISK_USED = 0;
	my $DISK_PERCENT = 0;
	my $DISK_TRAP = 0;
	my $DISK = '';
	my $TRAPPED = 0;

	if ( SDP::Core::listSections($FILE_OPEN, \@FILE_SECTIONS) ) {
		foreach $SECTION (@FILE_SECTIONS) {
			if ( $SECTION =~ /\/parted -s (\S+) print/ ) {
				$DISK_DEV = $1;
				SDP::Core::printDebug("PROCESS DEVICE", "$DISK_DEV");
				@CONTENT = ();
				if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
					$PRI_CNT = 0;
					$MSDOS = 0;
					$DISK_SIZE = 0;
					$DISK_USED = 0;
					$DISK_PERCENT = 0;
					$TRAPPED = 0;
					foreach $DISK (@CONTENT) {
						next if ( $DISK =~ /^$/ ); # Skip blank lines
						SDP::Core::printDebug("PART TABLE", "$DISK_DEV => $DISK");
						$DISK =~ s/^\s+//; # remove leading white space
						if ( $DISK =~ /Disk geometry for \S+ \S+ - (\S+)/i ) {
							$DISK_SIZE = convertSize($1);
						} elsif ( $DISK =~ m/Disk \/.*:\s+(.*)/i ) {
							$DISK_SIZE = convertSize($1);
						} elsif ( $DISK =~ m/Disk geometry for \/\S+\s+\d+\.\d+-(\d+)\.\d+ megabytes/i ) { # sles9 format
							$DISK_SIZE = convertSize($1);
						} elsif ( $DISK =~ m/Disk label type.*msdos|Partition Table.*msdos/i ) {
							SDP::Core::printDebug("TYPE", "MSDOS");
							$MSDOS++;
						} elsif ( $MSDOS && $DISK =~ m/\d+\s+\S+\s+(\S+).*primary/ ) {
							SDP::Core::printDebug("PRIMARY", "FOUND");
							$DISK_USED = convertSize($1);
							$PRI_CNT++;
						}
					}
					if ( $PRI_CNT > 3 && $MSDOS ) {
						$DISK_TRAP = $DISK_SIZE-$DISK_USED;
						$TRAPPED = $DISK_TRAP*100/$DISK_SIZE;
						$TRAPPED =~ s/\..*//g;
						if ( $TRAPPED >= TRAPPED_CRIT ) {
							SDP::Core::printDebug("PUSH", $DISK_DEV);
							push(@PRIMARIES, $DISK_DEV);
							$TRAP_SIZE += $DISK_SIZE;
							$TRAP_USED += $DISK_USED;
							SDP::Core::updateStatus(STATUS_CRITICAL, "Four primary partitions are trapping $TRAPPED% disk space on: $DISK_DEV");
						} elsif ( $TRAPPED >= TRAPPED_WARN ) {
							SDP::Core::printDebug("PUSH", $DISK_DEV);
							push(@PRIMARIES, $DISK_DEV);
							$TRAP_SIZE += $DISK_SIZE;
							$TRAP_USED += $DISK_USED;
							SDP::Core::updateStatus(STATUS_WARNING, "Four primary partitions are trapping $TRAPPED% disk space on: $DISK_DEV");
						}
					}
					SDP::Core::printDebug("DISK INFO", "$DISK_DEV, MSDOS=$MSDOS, PRI_CNT=$PRI_CNT, DISK_SIZE=$DISK_SIZE, DISK_USED=$DISK_USED, DISK_TRAP=$DISK_TRAP, TRAPPED=$TRAPPED%");
				} else {
					SDP::Core::updateStatus(STATUS_ERROR, "ERROR: trappedDiskSpace(): Cannot find \"$SECTION\" section in $FILE_OPEN");
				}
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: trappedDiskSpace(): No sections found in $FILE_OPEN");
	}
	$RCODE = scalar(@PRIMARIES);
	SDP::Core::printDebug("< trappedDiskSpace", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( trappedDiskSpace() ) {
		my $TRAP_PERCENT = ($TRAP_SIZE-$TRAP_USED)*100/$TRAP_SIZE;
		$TRAP_PERCENT =~ s/\..*//g;
		SDP::Core::setStatus($GSTATUS, "Four primary partitions are trapping $TRAP_PERCENT% disk space on: @PRIMARIES");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "No trapped disk space observed on any disk");
	}
SDP::Core::printPatternResults();

exit;

