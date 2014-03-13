#!/usr/bin/perl

# Title:       Only root can login and login incorrect
# Description: The /etc/nologin file can cause this behavior
# Modified:    2013 Jun 27

##############################################################################
#  Copyright (C) 2013,2012 SUSE LLC
##############################################################################
#
#  This program is free software; you can redistribute it and/or
#  modify
#  it under the terms of the GNU General Public License as published
#  by
#  the Free Software Foundation; version 2 of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.

#  Authors/Contributors:
#   Thomas Schlosser (thomas.schlosser@novell.com)

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
	PROPERTY_NAME_CATEGORY."=Auth",
	PROPERTY_NAME_COMPONENT."=Nologin",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006487"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub foundnologin {
    SDP::Core::printDebug('> foundnologin', 'BEGIN');
    my $RCODE = 0;
    my $LINE = 0;
    my $HEADER_LINES = 0;
    my @LINE_CONTENT = ();
    my $FILE_OPEN = 'pam.txt';
    my $SECTION = '/etc/nologin';
    my @FILE_SECTIONS = ();
    my $CHECK = "";
    my $MISSING = 1;

    if ( SDP::Core::listSections($FILE_OPEN, \@FILE_SECTIONS) ) {
        foreach $CHECK (@FILE_SECTIONS) {
            if ( $CHECK =~ m/^\/etc\/nologin$/ ) {
                $RCODE = 1;
                $MISSING = 0;
                last;
				} elsif ( $CHECK =~ m/^\/etc\/nologin/ ) {
                $MISSING = 0;
            } 
        }
    }
    SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Missing nologin data, skipping test") if ( $MISSING );
    SDP::Core::printDebug("< foundnologin", "Returns: $RCODE");
    return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
    if ( foundnologin() ) {
        SDP::Core::updateStatus(STATUS_WARNING, "The /etc/nologin could prevent user logins");
    } else {
        SDP::Core::updateStatus(STATUS_ERROR, "No /etc/nologin preventing user logins");
    }
SDP::Core::printPatternResults();

exit;

