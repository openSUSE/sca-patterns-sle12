#!/usr/bin/perl

# Title:       IRQ Shielding Recommendation for SLERTE
# Description: Consider shielding hardware interrupts with SLERTE.
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
	PROPERTY_NAME_CATEGORY."=Kernel",
	PROPERTY_NAME_COMPONENT."=IRG",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7007602"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub defaultIRQaffinity {
	SDP::Core::printDebug('> defaultIRQaffinity', 'BEGIN');
	my $RCODE = 0; # assume non-default
	my $FILE_OPEN = 'slert.txt';
	my @FILE_SECTIONS = ();
	my $SECTION = '';
	my $CNT_TOTAL = 0;
	my $CNT_DEF = 0;
	use constant DEF_THRESHOLD => 90;

	if ( SDP::Core::listSections($FILE_OPEN, \@FILE_SECTIONS) ) {
		foreach $SECTION (@FILE_SECTIONS) {
			if ( $SECTION =~ m/\/proc\/irq\/.*affinity/ ) {
				SDP::Core::printDebug("PROCESSING", $SECTION);
				$CNT_TOTAL++;
				my @CONTENT = ();
				if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
					foreach $_ (@CONTENT) {
						next if ( m/^\s*$/ ); # Skip blank lines
						if ( /^ff/i ) {
							$CNT_DEF++;
						}
					}
				}
			}
		}
		my $DEF_PERCENT = 0;
		if ( $CNT_TOTAL > 0 ) {
			$DEF_PERCENT = $CNT_DEF * 100 / $CNT_TOTAL;
		}
		SDP::Core::printDebug("COUNT", "Default: $CNT_DEF, TOTAL: $CNT_TOTAL, $DEF_PERCENT\%");
		if ( $DEF_PERCENT > DEF_THRESHOLD ) { # if 90% of the smp_affinity values are default (ff), then assume deafult
			$RCODE++;
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: No sections found in $FILE_OPEN");
	}
	SDP::Core::printDebug("< defaultIRQaffinity", "Returns: $RCODE");
	return $RCODE;
}

sub irqPersistentShields {
	SDP::Core::printDebug('> irqPersistentShields', 'BEGIN');
	my $RCODE = 0;
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'slert.txt';
	my $SECTION = '/etc/init.d/cset';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /smp_affinity/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: irqPersistentShields(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< irqPersistentShields", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( defaultIRQaffinity() ) {
		SDP::Core::updateStatus(STATUS_RECOMMEND, "Consider shielding hardware interrupts");
	} else {
		if ( irqPersistentShields() ) {
			SDP::Core::updateStatus(STATUS_ERROR, "Persistent shielding of hardware interrupts configured");
		} else {
			SDP::Core::updateStatus(STATUS_WARNING, "IRQs shielded but not persistent");
		}
	}
SDP::Core::printPatternResults();

exit;

