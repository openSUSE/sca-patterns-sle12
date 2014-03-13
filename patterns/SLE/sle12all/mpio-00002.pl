#!/usr/bin/perl

# Title:       MPIO Ramdisk Configuration
# Description: Fibre cards require an HBA driver in the initrd for MPIO to function properly.
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
	PROPERTY_NAME_CATEGORY."=Disk",
	PROPERTY_NAME_COMPONENT."=MPIO",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=3594167",
	"META_LINK_MISC=http://support.novell.com/techcenter/sdb/en/2005/04/sles_multipathing.html"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub fibreCardInfo {
	# returns an array of supported fibre card names
	# Supported Fibre Cards: Emulex LightPulse, QLogic 2xxx
	SDP::Core::printDebug('> fibreCardInfo', 'BEGIN');
	my %HBA_USED = (); # used to mark when I've found a unique fibre card, so I don't add duplicates to @DRIVERS_CHECKED
	my $FILE_OPEN = 'mpio.txt';
	my $SECTION = 'lspci -b';
	my @CONTENT = ();
	my @LINE_CONTENT = ();
	my $LINE = 0;
	my $ARRAY_REF = $_[0];
	my $RCODE = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			next if ( /^\s*$/ );                  # Skip blank lines
			if ( /Fibre Channel/i ) {
				SDP::Core::printDebug("LINE $LINE", $_);
				if ( /qlogic/i ) {
					if ( $HBA_USED{'qla2'} ) {
						SDP::Core::printDebug(" PUSH", "Duplicate Driver: qla2xxx");
					} else {
						SDP::Core::printDebug(" PUSH", "Driver: qla2xxx");
						push(@$ARRAY_REF, 'qla2xxx');
						$HBA_USED{'qla2'} = 1;
						$RCODE++;
					}
				} elsif ( /lightpulse/i) {
					if ( $HBA_USED{'lpfc'} ) {
						SDP::Core::printDebug(" PUSH", "Duplicate Driver: lpfc");
					} else {
						SDP::Core::printDebug(" PUSH", "Driver: lpfc");
						push(@$ARRAY_REF, 'lpfc');
						$HBA_USED{'lpfc'} = 1;
						$RCODE++;
					}
				} else {
					SDP::Core::printDebug(" SKIP", "Unsupported HBA Card for Pattern");
				}
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::updateStatus(STATUS_PARTIAL, "Fibre Card Drivers: @$ARRAY_REF");
	SDP::Core::printDebug("FIBRE_CARDS", "@$ARRAY_REF");	
	SDP::Core::printDebug("< fibreCardInfo", "Returns: $RCODE");
	return $RCODE;
}

sub checkInitrd {
	SDP::Core::printDebug('> checkInitrd', "BEGIN");
	my $FILE_OPEN = 'mpio.txt';
	my $SECTION = '/etc/sysconfig/kernel';
	my @CONTENT = ();
	my @DRIVERS_DEFINED = ();
	my @DRIVERS_MISSING = ();
	my $LINE = 0;
	my $RCODE = 1;
	my $DRVD;
	my $DRVC;
	my %MATCHES = ();
	my $ARRAY_REF = $_[0];

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			next if ( /^\s*$/ );                  # Skip blank lines
			if ( /^INITRD_MODULES/ ) {
				SDP::Core::printDebug("KERNEL", $_);
				s/INITRD_MODULES\s*=\s*\"\s*|\"$//g;
				SDP::Core::updateStatus(STATUS_PARTIAL, "$_");
				@DRIVERS_DEFINED = split(/\s+/, $_);
				last;
			}
		}
		SDP::Core::printDebug("DRIVERS_CHECKED", "@$ARRAY_REF");
		# define the matches
		foreach $DRVC (@$ARRAY_REF) {
			foreach $DRVD (@DRIVERS_DEFINED) {
				if ( $DRVD eq $DRVC ) {
					SDP::Core::printDebug("MATCH CONFIRMED", "DRVD=$DRVD to DRVC=$DRVC");
					$MATCHES{$DRVC} = 1;
				} else {
					SDP::Core::printDebug("MATCH FAILED", "DRVD=$DRVD to DRVC=$DRVC");
				}
			}
		}
		# make sure all drivers matched
		foreach $DRVC (@$ARRAY_REF) {
			if ( $MATCHES{$DRVC} ) {
				SDP::Core::printDebug('MATCH', "PASS: $DRVC");
			} else {
				SDP::Core::printDebug('MATCH', "FAIL: $DRVC");
				push(@DRIVERS_MISSING, $DRVC);
				$RCODE = 0;
			}
		}
		if ( $RCODE ) {
			SDP::Core::updateStatus(STATUS_ERROR, "All HBA Drivers Found in INITRD_MODULES");
		} else {
			SDP::Core::updateStatus(STATUS_WARNING, "Drivers missing from INITRD_MODULES: @DRIVERS_MISSING");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< checkInitrd", "Results: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my @DRIVERS_CHECKED = ();

	if ( fibreCardInfo(\@DRIVERS_CHECKED) ) {
		checkInitrd(\@DRIVERS_CHECKED);
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Supported Fibre Card Required for Pattern Test");
	}
SDP::Core::printPatternResults();

exit;

