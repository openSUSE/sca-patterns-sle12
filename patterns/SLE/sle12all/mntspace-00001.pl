#!/usr/bin/perl

# Title:       Mount Point May Conceal Used Disk Space
# Description: Checks for potential used disk space under a file system mount point
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
use constant THRESHOLD => 85;

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=SLE",
	PROPERTY_NAME_CATEGORY."=Disk",
	PROPERTY_NAME_COMPONENT."=Mount",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006091"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub getDFData {
	#SDP::Core::printDebug('> getDFData', 'BEGIN');
	my $RCODE = 0;
	my @LNDATA = ();
	my $FILE_OPEN = 'basic-health-check.txt';
	my $SECTION = '/bin/df -h';
	my $EXCEPTION_LIST = "admin|udev";
	my @CONTENT = ();
	my $LINE_WRAP = 0;
	my $LINE = '';
	my $ALLREF = $_[0];
	my $CHKREF = $_[1];
	my $CATLINE = '';

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^Filesystem/ ); # Skip header line
			next if ( m/^\s*$/ ); # Skip blank lines
			$_ =~ s/^\s*|%//g; # removes leading spaces and percents
			@LNDATA = split(/\s+/, $_);
			#SDP::Core::printDebug("LAST INDEX", "$#LNDATA: @LNDATA");
			if ( $LINE_WRAP ) {
				#SDP::Core::printDebug(" WRAPPED", "@LNDATA");
				$CATLINE = "$CATLINE @LNDATA";
				#SDP::Core::printDebug("PUSH", "@LNDATA");
				push(@$ALLREF, "$CATLINE");
				push(@$CHKREF, $LNDATA[4]) if ( $LNDATA[3] >= THRESHOLD );
				$LINE_WRAP = 0;
			} elsif ( $#LNDATA == 0 ) {
				#SDP::Core::printDebug(" WRAPPING", "@LNDATA");
				$CATLINE = "@LNDATA";
				$LINE_WRAP = 1;
			} elsif ( $#LNDATA == 5 ) {
				#SDP::Core::printDebug("PUSH", "@LNDATA");
				push(@$ALLREF, "@LNDATA");
				push(@$CHKREF, $LNDATA[5]) if ( $LNDATA[4] >= THRESHOLD );
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: getDFData(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	#SDP::Core::printDebug("< getDFData", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my @DFDATA = ();
	my @CHKDEVS = ();
	my @WARNDEVS = ();
	my @CHKDATA = ();
	my $DEVICE = '';
	my $DATA = '';

	getDFData(\@DFDATA, \@CHKDEVS);
	if ( @CHKDEVS ) {
		foreach $DEVICE (@CHKDEVS) {
			#SDP::Core::printDebug("CHKDEV", $DEVICE);
			foreach $DATA (@DFDATA) {
				@CHKDATA = split(/\s/, $DATA);
				#SDP::Core::printDebug(" Compare", "$DEVICE - $CHKDATA[5]");
				if ( "$DEVICE" eq "$CHKDATA[5]" ) {
					#SDP::Core::printDebug(" Skip", $DATA);
					next;
				} elsif ( $CHKDATA[5] =~ m/^$DEVICE/ ) { # the device matches the beginning of another device
					#SDP::Core::printDebug(" WARNING", $DATA);
					push(@WARNDEVS, $DEVICE);
					last;
				} else {
					#SDP::Core::printDebug(" Ingore", $DATA);
				}
			}
		}
		#SDP::Core::printDebug("CHKDEVS", "@CHKDEVS");
		#SDP::Core::printDebug("WARNDEVS", "@WARNDEVS");
		if ( @WARNDEVS ) {
			SDP::Core::updateStatus(STATUS_WARNING, "Check if mounted file system(s) may be hiding used disk space on: @WARNDEVS");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "No mounted file system(s) hiding disk space");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: No devices exceed " . THRESHOLD . "% used disk space threshold");
	}
SDP::Core::printPatternResults();

exit;

