#!/usr/bin/perl

# Title:       Missing or empty autofs map file
# Description: Checks for missing or empty autofs map files
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
	PROPERTY_NAME_CATEGORY."=AutoFS",
	PROPERTY_NAME_COMPONENT."=Map",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7008959"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub missingMapContent {
	SDP::Core::printDebug('> missingMapContent', 'BEGIN');
	my $RCODE = 0;
	my $ARRAY_REF = $_[0];
	my $FILE_OPEN = 'fs-autofs.txt';
	my @CONTENT = ();
	my @MAP_FILES = ();
	my %MAP_CHECKED = ();
	my @LC = ();
	my $MAP = '';
	my $EMPTY_MAP = 1;
	my $STATE = 0;
	my $AMSTATE = 0;
	my $CONTENT_FOUND = 0;
	if ( SDP::Core::loadFile($FILE_OPEN, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( $STATE ) {
				if ( /^#==\[/ ) {
					if ( $EMPTY_MAP ) {
						push(@$ARRAY_REF, $MAP);
					}
					$STATE = 0;
					$EMPTY_MAP = 1;
					SDP::Core::printDebug(" DONE", "Map State Off");
				} elsif ( /\S/ ) {
					$EMPTY_MAP = 0;
				}
			} elsif ( $AMSTATE ) {
				if ( /^#==\[/ ) {
					$AMSTATE = 0;
					SDP::Core::printDebug(" DONE", "Master State Off: @MAP_FILES");
				} else { # collect master map files
					next if ( m/^\s*#/ ); # skip commented lines
					SDP::Core::printDebug(" MAP", "$_");
					(undef, $MAP, undef) = split(/\s+/, $_);
					if ( defined $MAP ) {
						@LC = split(/:/, $MAP);
						$MAP = $LC[$#LC];
						$MAP = "/etc/$MAP" if ( $MAP !~ m/^\// );
						push(@MAP_FILES, $MAP);
						SDP::Core::printDebug(" MASTER MAP", "$MAP");
					}
				}
			} elsif ( /^# \/etc\/auto\.master/ ) { # Section, auto.master should always be first in the fs-autofs.txt file unless supportconfig is changed.
				$AMSTATE = 1;
				SDP::Core::printDebug("CHECK", "Section: $_");
			} else {
				foreach my $TMPMAP (@MAP_FILES) {
					if ( /^# ${TMPMAP}.*file not found/i && ! $MAP_CHECKED{$TMPMAP}) {
						push(@$ARRAY_REF, "$TMPMAP");
						$MAP_CHECKED{$TMPMAP} = 1;
						last;
					} elsif ( /^# ${TMPMAP}$/i && ! $MAP_CHECKED{$TMPMAP}) {
						$STATE = 1;
						$MAP_CHECKED{$TMPMAP} = 1;
						$MAP = $TMPMAP;
						SDP::Core::printDebug("CHECK", "Map: $MAP");
						last;
					}
				}
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: missingMapContent(): Cannot load file: $FILE_OPEN");
	}
	$RCODE = scalar @$ARRAY_REF;
	SDP::Core::printDebug("< missingMapContent", "Returns: $RCODE");
	return $RCODE;
}

sub activeAutofsFile {
	SDP::Core::printDebug('> activeAutofsFile', 'BEGIN');
	my $RCODE = 0;
	my $SERVICE_NAME = 'autofs';
	my %SERVICE_INFO = SDP::SUSE::getServiceInfo($SERVICE_NAME);
	if ( $SERVICE_INFO{'runlevelstatus'} > 0 ) {
		my $FILE_OPEN = 'fs-autofs.txt';
		my $SECTION = 'nsswitch.conf';
		my @CONTENT = ();
		if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
			foreach $_ (@CONTENT) {
				next if ( m/^\s*$/ ); # Skip blank lines
				if ( /^#--\[/ ) {
					last;
				} elsif ( /files/ ) {
					$RCODE++;
					SDP::Core::printDebug(" FOUND", $_);
					last;
				}
			}
		}
	}
	SDP::Core::printDebug("< activeAutofsFile", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( activeAutofsFile() ) {
		my @ME_MAP_FILES = ();
		if ( missingMapContent(\@ME_MAP_FILES) ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Missing or empty map files: @ME_MAP_FILES");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "All autofs map files found");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: AutoFS is inactive or does not use file types, skipping missing file test.");
	}
SDP::Core::printPatternResults();

exit;

