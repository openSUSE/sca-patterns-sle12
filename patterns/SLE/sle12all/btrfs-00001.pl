#!/usr/bin/perl

# Title:       Hourly btrfs snapshots fail
# Description: B-tree file system (btrfs) Missing from Snapper Config List
# Modified:    2013 Jun 27

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
	PROPERTY_NAME_COMPONENT."=btrfs",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7012008"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub getSnapperConfigs {
	SDP::Core::printDebug('> getSnapperConfigs', 'BEGIN');
	my $RCODE = 0;
	my %SCT = ();
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'fs-btrfs.txt';
	my $SECTION = '/etc/sysconfig/snapper';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /SNAPPER_CONFIGS/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				my (undef, $TMP) = split(/=/, $_);
				$TMP =~ s/"|'//g;
				SDP::Core::printDebug("TMP", "'$TMP'");
				@LINE_CONTENT = split(/\s+/, $TMP);
				foreach my $CFG (@LINE_CONTENT) {
					$SCT{$CFG}=1;
				}
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: getSnapperConfigs(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< getSnapperConfigs", "RETURN");
	return %SCT;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my %SNAPPER_CONFIGS = getSnapperConfigs();
	my $FILE_OPEN = 'fs-btrfs.txt';
	my @FILE_SECTIONS = ();
	my $SECTION = '';
	my @MISSING_CONFIGS = ();

	if ( SDP::Core::listSections($FILE_OPEN, \@FILE_SECTIONS) ) {
		foreach $SECTION (@FILE_SECTIONS) {
			if ( $SECTION =~ m/\/etc\/snapper\/configs\/(.*)/ ) {
				my $CFG = $1;
				if ( $SNAPPER_CONFIGS{$CFG} ) {
					SDP::Core::printDebug("FOUND", $CFG);
				} else {
					SDP::Core::printDebug("MISSING", $CFG);
					push(@MISSING_CONFIGS, $CFG);
				}
			}
		}
		SDP::Core::printDebug("MISSING CONFIGS", "@MISSING_CONFIGS");
		my $MISSING_COUNT = scalar @MISSING_CONFIGS;
		if ( $MISSING_COUNT ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Config names missing from /etc/sysconfig/snapper: @MISSING_CONFIGS");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "No missing configs in /etc/sysconfig/snapper");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: No sections found in $FILE_OPEN");
	}
SDP::Core::printPatternResults();

exit;


