#!/usr/bin/perl

# Title:       Detect Conflict with irqbalance and IRQ Shielding
# Description: The irqbalance daemon comflicts with shielding hardware interrupts
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
	if ( irqPersistentShields() ) {
		my %CSET = SDP::SUSE::getServiceInfo('cset');
		my %IRQB = SDP::SUSE::getServiceInfo('irq_balancer');
		if ( $CSET{'runlevelstatus'} > 0 ) {
			if ( $IRQB{'runlevelstatus'} > 0 ) {
				SDP::Core::updateStatus(STATUS_CRITICAL, "$CSET{'name'} service conflicts with $IRQB{'name'}, disable $IRQB{'name'}");
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, "No Service conflict detected between $CSET{'name'} and $IRQB{'name'}");
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Service $CSET{'name'} is not on at boot");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: No cset persistent shields, skipping conflict check");
	}
SDP::Core::printPatternResults();

exit;

