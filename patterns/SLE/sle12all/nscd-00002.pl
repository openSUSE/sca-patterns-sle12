#!/usr/bin/perl

# Title:       Running nscd as non-root user
# Description: Apparmor conflict when running nscd as user nobody
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
	PROPERTY_NAME_CATEGORY."=Service",
	PROPERTY_NAME_COMPONENT."=NSCD",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7011454"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub nonRootNscd {
	SDP::Core::printDebug('> nonRootNscd', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'network.txt';
	my $SECTION = '/etc/nscd.conf';
	my @CONTENT = ();
	my $NSCD_USER = '';

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			s/^\s*//g; # remove leading white space
			if ( /^server-user\s*nobody/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				(undef, $NSCD_USER) = split(/\s+/, $_);
				if ( $NSCD_USER !~ m/root/ ) {
					$RCODE++;
				}
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: nonRootNscd(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< nonRootNscd", "Returns: $RCODE");
	return $RCODE;
}

sub apparmorBlock {
	SDP::Core::printDebug('> apparmorBlock', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'security-apparmor.txt';
	my $SECTION = 'audit.log';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /apparmor.*DENIED.*profile="\/usr\/sbin\/nscd".*capname.*set[g,u]id/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: apparmorBlock(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< apparmorBlock", "Returns: $RCODE");
	return $RCODE;
}

sub apparmorOn {
	SDP::Core::printDebug('> apparmorOn', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'security-apparmor.txt';
	my $SECTION = 'AppArmor REJECT Messages';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /Module:.*Loaded/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
				last;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: apparmorOn(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< apparmorOn", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my $SERVICE_NAME = 'nscd';
	if ( nonRootNscd() ) {
		my %SERVICE_INFO = SDP::SUSE::getServiceInfo($SERVICE_NAME);
		if ( $SERVICE_INFO{'runlevelstatus'} ) { # turned on for the runlevel
			if ( $SERVICE_INFO{'running'} > 0 ) { # check if it's running
				SDP::Core::updateStatus(STATUS_ERROR, "Service $SERVICE_INFO{'name'} is running");
			} else {
				if ( apparmorBlock() ) {
					SDP::Core::updateStatus(STATUS_CRITICAL, "Service $SERVICE_INFO{'name'} blocked by AppArmor");
				} else {
					if ( apparmorOn() ) {
						SDP::Core::updateStatus(STATUS_WARNING, "Service $SERVICE_INFO{'name'} may be blocked by AppArmor");
					} else {
						SDP::Core::updateStatus(STATUS_ERROR, "Service AppArmor is not loaded, skipping block test");
					}
				}
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "Error: Service $SERVICE_INFO{'name'} turned off, skipping");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Error: Service $SERVICE_NAME running as root user, skipping");
	}
SDP::Core::printPatternResults();

exit;


