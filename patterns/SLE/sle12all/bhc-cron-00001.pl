#!/usr/bin/perl

# Title:       Cron Basic Service Pattern
# Description: Checks to see if the service is installed, valid and running
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
#
#  Authors/Contributors:
#     Jason Record (jrecord@suse.com)
#
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
	PROPERTY_NAME_COMPONENT."=Cron",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7001417"
);

my $CHECK_PACKAGE = "cron";
my $CHECK_SERVICE = "cron";
my $FILE_SERVICE = "cron.txt";

##############################################################################
# Program execution functions
##############################################################################

SDP::Core::processOptions();
	if ( packageInstalled($CHECK_PACKAGE) ) {
		SDP::SUSE::serviceHealth($FILE_SERVICE, $CHECK_PACKAGE, $CHECK_SERVICE);
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; Package Not Installed: $CHECK_PACKAGE");
	}
SDP::Core::printPatternResults();

exit;

