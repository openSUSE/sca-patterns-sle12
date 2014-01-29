#!/usr/bin/perl

# Title:       Autofs mount point blocked
# Description: Files with mount point name block autofs
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

sub mapsBlocked {
	SDP::Core::printDebug('> mapsBlocked', 'BEGIN');
	my $RCODE = 0;
	my $ARRAY_REF = $_[0];
	my $FILE_OPEN = 'fs-autofs.txt';
	my $SECTION = '/var/log/messages';
	my @CONTENT = ();
	my %MAPS = ();
	my $CHECK_MAP = '';

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /automount.*failed to create iautofs directory (.*)/ ) {
				$CHECK_MAP = $1;
				SDP::Core::printDebug("PROCESSING", $_);
				$MAPS{$CHECK_MAP} = 1;
			} elsif ( /automount.*do_mount_autofs_indirect: failed to mount autofs path (.*) at/ ) {
				$CHECK_MAP = $1;
				SDP::Core::printDebug("PROCESSING", $_);
				$MAPS{$CHECK_MAP} = 1;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: mapsBlocked(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	@$ARRAY_REF = keys %MAPS;
	$RCODE = scalar keys %MAPS;
	SDP::Core::printDebug("< mapsBlocked", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( activeAutofsFile() ) {
		my @BLOCKED_MAPS = ();
		if ( mapsBlocked(\@BLOCKED_MAPS) ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Mount error detected, check mount points that may be blocked: @BLOCKED_MAPS");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "No file type mount points appear blocked");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: AutoFS is inactive or does not use file types, skipping missing file test.");
	}
SDP::Core::printPatternResults();

exit;


