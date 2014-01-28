#!/usr/bin/perl

# Title:       DNS Basic Service Pattern
# Description: Checks to see if the service is installed, valid and running
# Modified:    2013 Jun 24

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
	PROPERTY_NAME_CLASS."=Basic Health",
	PROPERTY_NAME_CATEGORY."=SLE",
	PROPERTY_NAME_COMPONENT."=DNS",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7001417"
);

##############################################################################
# Program execution functions
##############################################################################

SDP::Core::processOptions();
	my @EXCLUDE = qw(/opt/novell/eDirectory/lib);
	if ( packageInstalled('novell-bind') ) {
		SDP::SUSE::serviceHealth('dns.txt', 'novell-bind', 'novell-named', \@EXCLUDE);
	} elsif ( packageInstalled('bind') ) {
		SDP::SUSE::serviceHealth('dns.txt', 'bind', 'named');
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; Packages Not Installed: novell-bind or bind");
	}
SDP::Core::printPatternResults();

exit;

