#!/usr/bin/perl

# Title:       Chkbin log evaluation
# Description: Chkbin logs show the health of a particular application
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
	PROPERTY_NAME_CATEGORY."=Basic Health",
	PROPERTY_NAME_COMPONENT."=Application",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006753"
);

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my $FILE_OPEN = 'crash.txt';
	my @FILE_SECTIONS = ();
	my @LINE_CONTENT = ();
	my $SECTION = '';
	my @CHKBIN_CRIT = ();
	my @CHKBIN_WARN = ();
	my @CHKBINS = ();

	if ( SDP::Core::listSections($FILE_OPEN, \@FILE_SECTIONS) ) {
		foreach $SECTION (@FILE_SECTIONS) {
			if ( $SECTION =~ /nts_chkbin/ ) {
				SDP::Core::printDebug("SECTION", "Evaluating: $SECTION");
				@LINE_CONTENT = split(/_/, $SECTION);
				push(@CHKBINS, $LINE_CONTENT[2]);
				my @CONTENT = ();
				if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
					foreach $_ (@CONTENT) {
						next if ( m/^\s*$/ ); # Skip blank lines
						my $STATUS = '';
						if ( m/^STATUS:\s*(.*)/ ) {
							SDP::Core::printDebug("PROCESSING", $_);
							$STATUS = $1;
							if ( $STATUS =~ m/error|warning/i ) {
								push(@CHKBIN_CRIT, $LINE_CONTENT[2]);
								SDP::Core::printDebug(" PUSH", "CHKBIN_CRIT: $LINE_CONTENT[2]");
							} elsif ( $STATUS =~ m/differences/i ) {
								push(@CHKBIN_WARN, $LINE_CONTENT[2]);
								SDP::Core::printDebug(" PUSH", "CHKBIN_WARN: $LINE_CONTENT[2]");
							}
							last;
						}
					}
				}
			}
		}
		SDP::Core::printDebug("CHKBIN LOGS", "Applications: @CHKBINS");
		if ( $#CHKBINS >= 0 ) {
			if ( $#CHKBIN_CRIT >= 0 ) {
				SDP::Core::updateStatus(STATUS_CRITICAL, "Review chkbin logs in crash.txt, warnings or errors for: @CHKBIN_CRIT");
			} elsif ($#CHKBIN_WARN >= 0 ) {
				SDP::Core::updateStatus(STATUS_WARNING, "Review chkbin logs in crash.txt, differences for: @CHKBIN_WARN");
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, "Applications appear healthy in chkbin logs for: @CHKBINS");
			}	
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "ERROR: No chkbin logs to evaluate");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: main(): No sections found in $FILE_OPEN");
	}
SDP::Core::printPatternResults();

exit;

