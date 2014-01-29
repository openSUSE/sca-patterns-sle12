#!/usr/bin/perl

# Title:       Users Friendly Names on Multipath Root
# Description: Do not use use_friendly_names when root is multipathed.
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
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7001133",
	"META_LINK_BUG=https://bugzilla.novell.com/show_bug.cgi?id=414381"
);

my @WWIDS = ();

##############################################################################
# Local Function Definitions
##############################################################################

sub mpioUserFriendlyNames {
	SDP::Core::printDebug('> mpioUserFriendlyNames', 'BEGIN');
	my $RCODE = 0;
	my $MPIO_ACTIVE = 0;
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'mpio.txt';
	my $SECTION = 'multipath -ll';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /^\[/ ) {
				$MPIO_ACTIVE = 1;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: mpioUserFriendlyNames(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}

	if ( ! $MPIO_ACTIVE ) {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: mpioUserFriendlyNames(): MPIO not active, skipping user_friendly_names test");
	} else {
		$SECTION = 'multipath.conf';
		@CONTENT = ();
		if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
			foreach $_ (@CONTENT) {
				next if ( m/^\s*$/ ); # Skip blank lines
				if ( /user_friendly_names.*yes/i ) {
					$RCODE++;
					last;
				}
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "ERROR: mpioUserFriendlyNames(): Cannot find \"$SECTION\" section in $FILE_OPEN");
		}
	}
	SDP::Core::printDebug("< mpioUserFriendlyNames", "Returns: $RCODE");
	return $RCODE;
}

sub getMpioWWID {
	SDP::Core::printDebug('> getMpioWWID', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'mpio.txt';
	my $SECTION = 'multipath -v3 -d';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /^(.*)\s*\d:\d:\d:\d\s*sd.*\[.*\]\[.*\]\s*\S/ ) {
				SDP::Core::printDebug("EVAL", "$_");
				push(@WWIDS, SDP::Core::trimWhite($1));
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: getMpioWWID(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	$RCODE = scalar @WWIDS;
	SDP::Core::printDebug("< getMpioWWID", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( mpioUserFriendlyNames() ) {
		my @MOUNTS = SDP::SUSE::getFileSystems();
		my $TMP;
		my $ID;
		my $ROOTDEV;
		my $RCODE = 0;
		foreach $TMP (@MOUNTS) {
			if ( $TMP->{'MPT'} eq '/' ) {
				SDP::Core::printDebug('FS', "Found Root");
				my @ROOTDEVS = ( $TMP->{'DEV'}, $TMP->{'DEVF'}, $TMP->{'DEVM'} );
				getMpioWWID();
				foreach $ID (@WWIDS) {
					foreach $ROOTDEV (@ROOTDEVS) {
						SDP::Core::printDebug('ID in ROOTDEV', "$ID - $ROOTDEV");
						if ( $ROOTDEV =~ m/$ID/i ) {
							$RCODE++;
							last;
						}
					}
					last if $RCODE;
				}
				last;
			}
		}
		if ( $RCODE ) {
			SDP::Core::updateStatus(STATUS_WARNING, "Root MPIO device; user_friendly_names in multipath.conf NOT recommended");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "Root device is not under MPIO");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: MPIO active, but user_friendly_names required, skipping check");
	}
SDP::Core::printPatternResults();

exit;

