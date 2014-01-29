#!/usr/bin/perl

# Title:       Upgrading to Subscription Management Tool 10 SP3
# Description: Recommends steps required to perform the upgrade if needed
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
	PROPERTY_NAME_CATEGORY."=SMT",
	PROPERTY_NAME_COMPONENT."=System",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7005364",
	"META_LINK_MISC=http://www.novell.com/support/php/search.do?cmd=displayKC&docType=kc&externalId=7005002"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub foundSMT10 {
	SDP::Core::printDebug("> foundSMT10", "BEGIN");
	my $RCODE = 0;
	my $RPM_NAME = 'smt';
	my $VERSION_TO_COMPARE = '1.0.14'; # SMT 1.0 SP3 version
	my $RPM_COMPARISON = SDP::SUSE::compareRpm($RPM_NAME, $VERSION_TO_COMPARE);
	if ( $RPM_COMPARISON == 2 ) {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: RPM $RPM_NAME Not Installed");
	} elsif ( $RPM_COMPARISON > 2 ) {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Multiple Versions of $RPM_NAME RPM are Installed");
	} else {
		if ( $RPM_COMPARISON < 0 ) {
			$RCODE=1;
		}                       
	}
	SDP::Core::printDebug("< foundSMT10", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( SDP::SUSE::compareKernel(SLE10SP3) >= 0 && SDP::SUSE::compareKernel(SLE10SP4) < 0 ) {
		foundSMT10() ? SDP::Core::updateStatus(STATUS_WARNING, 'UP', "Update Scenario 2 - SLES10 SP3 and SMT10 installed") : SDP::Core::updateStatus(STATUS_ERROR, "SLES10 SP3 with SMT10 SP3 Observed");
	} elsif ( SDP::SUSE::compareKernel(SLE10SP2) >= 0 && SDP::SUSE::compareKernel(SLE10SP3) < 0 ) {
		foundSMT10() ? SDP::Core::updateStatus(STATUS_WARNING, 'UP', "Update Scenario 1 - SLES10 SP2 and SMT10 installed") : SDP::Core::updateStatus(STATUS_CRITICAL, "SLES10 SP2 with SMT10 SP3, SLES10 SP3 Upgrade Required");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Outside kernel scope, skipping SMT upgrade test");
	}
SDP::Core::printPatternResults();

exit;

