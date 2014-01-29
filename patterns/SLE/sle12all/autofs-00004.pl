#!/usr/bin/perl

# Title:       Invalid autofs map file location
# Description: Map file location missing a leading colon
# Modified:    2013 Jun 27

##############################################################################
#  Copyright (C) 2013,2012 SUSE
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

sub getInvalidMaps {
	SDP::Core::printDebug('> getInvalidMaps', 'BEGIN');
	my $RCODE = 0;
	my $ARRAY_REF = $_[0];
	my $FILE_OPEN = 'fs-autofs.txt';
	my @CONTENT = ();
	my @MAP_FILES = ();
	my %MAP_CHECKED = ();
	my @LC = ();
	my $MAP = '';
	my $STATE = 0;
	my $AMSTATE = 0;
	my $CONTENT_FOUND = 0;
	if ( SDP::Core::loadFile($FILE_OPEN, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( $STATE ) {
				if ( /^#==\[/ ) {
					$STATE = 0;
					SDP::Core::printDebug(" DONE", "Map State Off");
				} else {
					@LC = split(/\s+/, $_);
					if ( $#LC == 2 ) {
						$CONTENT_FOUND = 1;
						if ( $LC[$#LC] =~ m/^\// ) {
							SDP::Core::printDebug(" PUSH", "$MAP($LC[$#LC])");
							push(@$ARRAY_REF, "$MAP($LC[$#LC])");
						}
					} else {
						SDP::Core::printDebug(" FILE", "Not a file map, LC: $#LC");
						$STATE = 0;
					}
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
					if ( /^# ${TMPMAP}$/i && ! $MAP_CHECKED{$TMPMAP}) {
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
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: getInvalidMaps(): Cannot load file: $FILE_OPEN");
	}
	if ( $CONTENT_FOUND ) {
		$RCODE = scalar @$ARRAY_REF;
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: getInvalidMaps(): No file map types found, skipping location test");
	}
	SDP::Core::printDebug("< getInvalidMaps", "Returns: $RCODE");
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
		my @INVALID_MAPS = ();
		if ( getInvalidMaps(\@INVALID_MAPS) ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Invalid autofs local map location(s): @INVALID_MAPS");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "All local autofs map locations are valid");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Autofs not running or file types not in use, skipping location test");
	}

SDP::Core::printPatternResults();

exit;

