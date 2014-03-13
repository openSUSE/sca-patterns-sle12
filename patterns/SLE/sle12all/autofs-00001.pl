#!/usr/bin/perl

# Title:       Automounter Basic Service Pattern
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
	PROPERTY_NAME_COMPONENT."=AutoFS",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7001417"
);

my $CHECK_SERVICE = "autofs";
my $FILE_SERVICE = "fs-autofs.txt";

##############################################################################
# Program execution functions
##############################################################################

SDP::Core::processOptions();
	if ( packageInstalled('autofs') ) {
		SDP::SUSE::serviceHealth($FILE_SERVICE, 'autofs', $CHECK_SERVICE);
	} elsif ( packageInstalled('autofs5') ) {
		SDP::SUSE::serviceHealth($FILE_SERVICE, 'autofs5', $CHECK_SERVICE);
	} elsif ( packageInstalled('autofs4') ) {
		SDP::SUSE::serviceHealth($FILE_SERVICE, 'autofs4', $CHECK_SERVICE);
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Basic Service Health; Packages Not Installed: autofs, autofs4, autofs5");
	}
SDP::Core::printPatternResults();

exit;

