#!/usr/bin/perl

# Title:       Modules failing to load at boot time
# Description: Checks for /etc/sysconfig/kernel modules that should be loaded
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
	PROPERTY_NAME_CATEGORY."=Kernel",
	PROPERTY_NAME_COMPONENT."=Driver",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7005784"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub getBootModules {
	SDP::Core::printDebug('> getBootModules', 'BEGIN');
	my $RCODE = 0;
	my @MODULES = ();
	my $FILE_OPEN = 'sysconfig.txt';
	my $SECTION = '/etc/sysconfig/kernel';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( /^\s*$/ ); # Skip blank lines
			if ( /^INITRD_MODULES/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				s/^INITRD_MODULES//g;
				s/=|"//g;
				push(@MODULES, split(/\s+/, SDP::Core::trimWhite($_)));
			} elsif ( /^DOMU_INITRD_MODULES/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				if ( SDP::SUSE::xenDom0running() ) {
					s/^DOMU_INITRD_MODULES//g;
					s/=|"//g;
					push(@MODULES, split(/\s+/, SDP::Core::trimWhite($_)));
					SDP::Core::printDebug(" XEN", "Running, Modules Pushed");
				} else {
					SDP::Core::printDebug(" XEN", "Skipped, Not Running");
				}
			} elsif ( /^MODULES_LOADED_ON_BOOT/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				s/^MODULES_LOADED_ON_BOOT//g;
				s/=|"//g;
				push(@MODULES, split(/\s+/, SDP::Core::trimWhite($_)));
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: getBootModules(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	$RCODE = scalar(@MODULES);

	SDP::Core::printDebug("< getBootModules", "Returns: $RCODE");
	return @MODULES;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	my @BOOT_MODULES = getBootModules();
	if ( @BOOT_MODULES ) {
		my @IN = ();
		my %FOUND = ();
		my @MISSING_MODULES = ();
		my $FILE_OPEN = 'modules.txt';
		my $SECTION = 'lsmod';
		my @CONTENT = ();
		my $MODULE;
		my $LINE;

		if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
			foreach $MODULE (@BOOT_MODULES) {
				my $MISSING = 1; # assume the module is missing
				foreach $LINE (@CONTENT) {
					next if ( $LINE =~ m/^$/ ); # Skip blank lines
					if ( $LINE =~ m/^$MODULE\s/ ) {
						$MISSING = 0;
						last;
					}
				}
				push(@IN, $MODULE) if ( $MISSING );
			}
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "ERROR: main(): Cannot find \"$SECTION\" section in $FILE_OPEN");
		}
		@FOUND{@IN} = ();
		@MISSING_MODULES = sort keys %FOUND;
		if ( @MISSING_MODULES ) {
			SDP::Core::updateStatus(STATUS_WARNING, "Modules requested in /etc/sysconfig/kernel not running: @MISSING_MODULES");
		} else {
			SDP::Core::updateStatus(STATUS_ERROR, "All /etc/sysconfig/kernel modules loaded");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: main(): Not modules to load at boot");
	}
SDP::Core::printPatternResults();

exit;

