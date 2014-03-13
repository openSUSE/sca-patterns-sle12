#!/usr/bin/perl

# Title:       Check for Unsupported Package Distributions
# Description: Packages from other Linux distributions like Red Hat, Debian and Ubuntu are not supported
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
	PROPERTY_NAME_CATEGORY."=Support",
	PROPERTY_NAME_COMPONENT."=Packages",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7005936"
);

my $DISTRO_3RD = "Red Hat|Debian|Ubuntu|openSUSE|Mandriva|Fedora";

##############################################################################
# Local Function Definitions
##############################################################################

sub unsupportedDistros {
	SDP::Core::printDebug('> unsupportedDistros', 'BEGIN');
	my $RCODE = 0;
	my $SUSE = 0;
	my $FILE_OPEN = 'rpm.txt';
	my $SECTION = 'rpm.*uniq';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /SUSE Linux/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$SUSE++;
			} elsif ( /$DISTRO_3RD/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$RCODE++;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: unsupportedDistros(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::updateStatus(STATUS_ERROR, "SUSE Distribution Required, Skipping Test") if ( ! $SUSE );

	SDP::Core::printDebug("< unsupportedDistros", "Returns: $RCODE");
	return $RCODE;
}

sub checkCriticalPackages {
	SDP::Core::printDebug('> checkCriticalPackages', 'BEGIN');
	my $RCODE = 0;
	my @LINE_CONTENT = ();
	my $FILE_OPEN = 'rpm.txt';
	my $SECTION = 'rpm.*VERSION';
	my @CONTENT = ();
	my %UNPKG_CRIT = ();
	my %UNPKG_WARN = ();
	my %CRITICAL_PACKAGES = (
		'aaa_base' => 1,
		'bash' => 1,
		'coreutils' => 1,
		'rpm' => 1,
		'glib' => 1,
		'glib2' => 1,
		'glibc' => 1,
		'glibc-32bit' => 1,
		'glibc-locale' => 1,
		'glibc-info' => 1,
		'compat-libstdc++' => 1,
		'libgnome' => 1,
		'xorg-x11' => 1,
	);

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /$DISTRO_3RD/i ) {
				SDP::Core::printDebug("PROCESSING", $_);
				@LINE_CONTENT = split(/\s+/, $_);
				if ( $CRITICAL_PACKAGES{$LINE_CONTENT[0]} ) {
					$UNPKG_CRIT{$LINE_CONTENT[0]} = 1;
				} else {
					$UNPKG_WARN{$LINE_CONTENT[0]} = 1;
				}
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: checkCriticalPackages(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	my @CKEYS = keys %UNPKG_CRIT;
	if ( $#CKEYS >= 0 ) {
		SDP::Core::updateStatus(STATUS_CRITICAL, "Critical unsupported 3rd party packages: @CKEYS");
	} 
	my @WKEYS = keys %UNPKG_WARN;
	if ( $#WKEYS >= 0 ) {
		SDP::Core::updateStatus(STATUS_WARNING, "Unsupported 3rd party packages: @WKEYS");
	} else {
		SDP::Core::updateStatus(STATUS_WARNING, "Confirm any unsupported 3rd party packages");
	}

	$RCODE = scalar @CKEYS + scalar @WKEYS;

	SDP::Core::printDebug("< checkCriticalPackages", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( unsupportedDistros() ) {
		checkCriticalPackages();
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Passed common distribution check");
	}
SDP::Core::printPatternResults();

exit;

