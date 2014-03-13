#!/usr/bin/perl

# Title:       Yast GUI modules will not load
# Description: After running yast2 users the GUI opens but then suddenly closes with no on screen errors.
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
	PROPERTY_NAME_CATEGORY."=YaST",
	PROPERTY_NAME_COMPONENT."=Base",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7007717"
);

my $PERL_MOD = '';

##############################################################################
# Local Function Definitions
##############################################################################

sub perlErrorFound {
	SDP::Core::printDebug('> perlErrorFound', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'y2log.txt';
	my $SECTION = 'y2log';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (reverse(@CONTENT)) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /Perl.*: Can\'t locate (.*)\.pm in \@INC/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$PERL_MOD = $1;
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: perlErrorFound(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< perlErrorFound", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( perlErrorFound() ) {
		SDP::Core::updateStatus(STATUS_WARNING, "YaST2 GUI is missing a critical perl module: $PERL_MOD.pm, try yast ncurses.");
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "No perl module errors found in y2log.");
	}
SDP::Core::printPatternResults();

exit;

