#!/usr/bin/perl

# Title:       Dom0 has network connectivity, but DomU does not
# Description: The most common cause of this is that the routing table does not contain a default route.
# Modified:    2013 Jun 28

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
	PROPERTY_NAME_CATEGORY."=Virtualization",
	PROPERTY_NAME_COMPONENT."=Network",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7001989",
	"META_LINK_MISC=http://www.novell.com/support/php/search.do?cmd=displayKC&docType=kc&externalId=7001362&sliceId=1&docTypeID=DT_TID_1_1&dialogID=84812161&stateId=0%200%2084810291"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub defaultRoute {
	SDP::Core::printDebug('> defaultRoute', 'BEGIN');
	my $RCODE = 0; # assume the default route is missing
	my $LINE = 0;
	my $ROUTE = '';
	my $role = '';
	my $i = '';
	my @NETWORK_ROUTES = ();

	if ( SDP::SUSE::netRouteTable(\@NETWORK_ROUTES) ) {
		for $i ( 0 .. $#NETWORK_ROUTES ) {
			SDP::Core::printDebug('FLAGS', "$i of $#NETWORK_ROUTES: $NETWORK_ROUTES[$i]{'gateway'} - $NETWORK_ROUTES[$i]{'flags'}");
			if ( $NETWORK_ROUTES[$i]{'flags'} =~ /UG|GU/i ) {
				SDP::Core::printDebug(' DEF ROUTE', "Found: $NETWORK_ROUTES[$i]{'gateway'} - $NETWORK_ROUTES[$i]{'flags'}");
				$RCODE = 1;
			}
		}
	}
	SDP::Core::printDebug("< defaultRoute", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( SDP::SUSE::xenDomU() ) {
		if ( defaultRoute() ) {
			SDP::Core::updateStatus(STATUS_ERROR, "Default network route found");
		} else {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Missing default network route");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ABORT: Not a Xen DomU");
	}
SDP::Core::printPatternResults();

exit;

