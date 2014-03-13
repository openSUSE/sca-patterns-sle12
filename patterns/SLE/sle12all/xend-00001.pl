#!/usr/bin/perl

# Title:       Xen Basic Service Pattern
# Description: Checks to see if the service is installed, valid and running
# Modified:    2013 Jun 28

##############################################################################
#  Copyright (C) 2013,2010 SUSE LLC
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
	PROPERTY_NAME_COMPONENT."=Xen",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7001417"
);

my $CHECK_PACKAGE = "xen-tools";
my $CHECK_SERVICE = "xend";
my $FILE_SERVICE = "xen.txt";

##############################################################################
# Program execution functions
##############################################################################

SDP::Core::processOptions();
	if ( packageInstalled($CHECK_PACKAGE) ) {
		if ( SDP::SUSE::xenDom0running() ) {
			SDP::SUSE::serviceHealth($FILE_SERVICE, $CHECK_PACKAGE, $CHECK_SERVICE);
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; No Xen Kernel Loaded");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; Package Not Installed: $CHECK_PACKAGE");
	}
SDP::Core::printPatternResults();

exit;

