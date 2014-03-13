#!/usr/bin/perl

# Supported third party drivers
# vxdmp - Veritas Dynamic Multipathing
# emcp - EMC PowerPath
# mppVhba - Dell Multipath Protection (MPP)

# Title:       Conflicting MPIO Solutions
# Description: Detects multiple MPIO solutions running currently
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
	PROPERTY_NAME_CATEGORY."=Disk",
	PROPERTY_NAME_COMPONENT."=MPIO",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006317"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub getBootServiceInfo {
	my $SERVICE_NAME = $_[0];
	SDP::Core::printDebug('> getBootServiceInfo', "$SERVICE_NAME");
	my $RCODE = 0;
	my %SERVICE_INFO            = (
		name                     => $SERVICE_NAME,
		running                  => 0,
	);

	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'chkconfig.txt';
	my $SECTION = 'chkconfig --list';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			$_ =~ s/^\s*//g;
			if ( /^\s*boot.multipath:/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				@LINE_CONTENT = split(/\s+/, $_);
				$RCODE++;
				last;
			}
		}
		if ( $RCODE ) {
			$SERVICE_INFO{'running'} = 1 if ( $LINE_CONTENT[1] =~ m/on/i );
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: checkSomething(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	my ($key, $value);
	if ( $OPT_LOGLEVEL >= LOGLEVEL_DEBUG ) {
		print(' %SERVICE_INFO                  = ');
		while ( ($key, $value) = each(%SERVICE_INFO) ) {
			print("$key => \"$value\"  ");
		}
		print("\n");
	}

	SDP::Core::printDebug("< getBootServiceInfo", "$SERVICE_INFO{'name'}=$SERVICE_INFO{'running'}");
	return %SERVICE_INFO;
}

sub mpioEnabled {
	SDP::Core::printDebug('> mpioEnabled', 'BEGIN');
	my $RCODE = 0;
	my %SERVICE_INFO = SDP::SUSE::getServiceInfo('multipathd');
	$RCODE++ if ( $SERVICE_INFO{'running'} > 0 );
	%SERVICE_INFO = getBootServiceInfo('boot.multipath');
	$RCODE++ if ( $SERVICE_INFO{'running'} > 0 );
	SDP::Core::printDebug("< mpioEnabled", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my %DRIVER_INFO = ();
	my @mpioDriverList = qw(vxdmp emcp mppVhba);
	foreach my $DRIVER_NAME (@mpioDriverList) {
		%DRIVER_INFO = SDP::SUSE::getDriverInfo($DRIVER_NAME);
		last if ( $DRIVER_INFO{'loaded'} );
	}
	if ( $DRIVER_INFO{'loaded'} ) {
		if ( mpioEnabled() ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Multiple MPIO Solutions: multipathd and $DRIVER_INFO{'name'}");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "Single MPIO Solution: $DRIVER_INFO{'name'}");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: No active third party MPIO solutions");
	}
SDP::Core::printPatternResults();

exit;


