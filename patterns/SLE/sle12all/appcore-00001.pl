#!/usr/bin/perl

# Title:       Check for Application Core Files
# Description: Checks if any application core files exist and from which applications.
# Modified:    2013 Jun 27

# Write a TID on how to gather core information.

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
	PROPERTY_NAME_CATEGORY."=Crash",
	PROPERTY_NAME_COMPONENT."=Apps",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7004526",
	"META_LINK_MISC=http://www.novell.com/support/php/search.do?cmd=displayKC&docType=kc&externalId=3054866&sliceId=2&docTypeID=DT_TID_1_1&dialogID=87992056&stateId=0%200%2087988873"
);

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my @APP_CORE_INFO = ();
	my $CRITICAL_AGE = 7;
	my ($SC_DAYS, $SC_YEAR, undef, undef) = split(/\t/, SDP::SUSE::getSupportconfigRunDate());
	my $RECENT = 0;
	my (%HCRIT,%HWARN) = ();
	my (@ACRIT,@AWARN) = ();
	my $APP_NAMES = 0;

	if ( SDP::SUSE::appCores(\@APP_CORE_INFO) ) {
		for ( my $I=0; $I<=$#APP_CORE_INFO; $I++) {
			my $CORE_AGE = $SC_DAYS - $APP_CORE_INFO[$I]->{'days'};
			SDP::Core::printDebug("CORE", "SC_DAYS $SC_DAYS, CORE_DAYS $APP_CORE_INFO[$I]->{'days'}, AGE $CORE_AGE, CORE $APP_CORE_INFO[$I]->{'filename'}, APP $APP_CORE_INFO[$I]->{'application'}");
			$APP_NAMES = 1 if ( $APP_CORE_INFO[$I]->{'filename'} ne $APP_CORE_INFO[$I]->{'application'} );
			if ( $CORE_AGE <= $CRITICAL_AGE ) {
				$HCRIT{$APP_CORE_INFO[$I]->{'application'}}++; # Increment the number of times this app has core dumped, the hash key is the application name that core dumped
			} else {
				$HWARN{$APP_CORE_INFO[$I]->{'application'}}++; # Increment the number of times this app has core dumped, the hash key is the application name that core dumped
			}
		}
		@ACRIT = keys %HCRIT;
		@AWARN = keys %HWARN;
		if ( $APP_NAMES ) {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Application core files found within $CRITICAL_AGE days for: @ACRIT") if ( @ACRIT );
			SDP::Core::updateStatus(STATUS_WARNING, "Application core files found for: @AWARN") if ( @AWARN );
		} else {
			SDP::Core::updateStatus(STATUS_CRITICAL, "Application core files found within $CRITICAL_AGE days: " . ($#ACRIT+1)) if ( @ACRIT );
			SDP::Core::updateStatus(STATUS_WARNING, "Application core files found: " . ($#AWARN + 1)) if ( @AWARN );
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "No application core files found");
	}
SDP::Core::printPatternResults();

exit;

