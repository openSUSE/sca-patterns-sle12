#!/usr/bin/perl

# Title:       Supportconfig Plugin for SLEPOS Recommendation
# Description: Recommends SLEPOS plugin as needed
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
	PROPERTY_NAME_CATEGORY."=Supportconfig",
	PROPERTY_NAME_COMPONENT."=Plugin",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_Downloads",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_Downloads=https://build.opensuse.org/package/show?package=supportutils-plugin-slepos&project=Novell%3ANTS",
	"META_LINK_Patch=http://download.opensuse.org/repositories/Novell:/NTS/SLE_10/noarch/supportutils-plugin-slepos-1.0-3.1.noarch.rpm"
);

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my $CURRENT_VERSION = '1.0-3.1';
	if ( SDP::SUSE::packageInstalled('slepos-release') || SDP::SUSE::packageInstalled('sle-pos-release') ) {
		my $RPM_NAME = 'supportutils-plugin-slepos';
		my @RPM_INFO = SDP::SUSE::getRpmInfo($RPM_NAME);
		if ( $#RPM_INFO < 0 ) {
			SDP::Core::updateStatus(STATUS_RECOMMEND, "Install the Supportconfig Plugin for SLEPOS for better troubleshooting");
		} elsif ( $#RPM_INFO > 0 ) {
			SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Multiple $RPM_NAME RPMs Installed");
		} else {
			if ( SDP::Core::compareVersions($CURRENT_VERSION, $RPM_INFO[0]{'version'}) >= 0 ) {
				SDP::Core::updateStatus(STATUS_WARNING, "Update for Supportconfig Plugin for SLEPOS v$RPM_INFO[0]{'version'} needed");
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, "Supportconfig Plugin for SLEPOS installed and current");
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: SLEPOS not installed, ignore plugin recommendation");
	}
SDP::Core::printPatternResults();

exit;

