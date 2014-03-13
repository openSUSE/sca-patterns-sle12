#!/usr/bin/perl

# Title:       Proxy configured but not active
# Description: Checks for proxy environment variables
# Modified:    2013 Jun 24

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
	PROPERTY_NAME_CATEGORY."=Proxy",
	PROPERTY_NAME_COMPONENT."=Config",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7006745"
);

my %PROXY_ACTIVE = ();
my %PROXY_CONFIG = ();

##############################################################################
# Local Function Definitions
##############################################################################

sub getProxyActive {
	SDP::Core::printDebug('> getProxyActive', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'env.txt';
	my $SECTION = 'env';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$/ ); # Skip blank lines
			if ( /(\D+_proxy)=(.*)/ ) {
				SDP::Core::printDebug("PROCESSING", $_);
				$PROXY_ACTIVE{"$1"} = $2;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: getProxyActive(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	$RCODE = scalar keys %PROXY_ACTIVE;
	if ( $RCODE ) {
			if ( $OPT_LOGLEVEL >= LOGLEVEL_DEBUG ) {
				my $KEY;
				my $VALUE;
				print(' %PROXY_ACTIVE                  = ');
				while ( ($KEY, $VALUE) = each(%PROXY_ACTIVE) ) {
					print("$KEY => \"$VALUE\"  ");
				}
				print("\n");
			}
	}
	SDP::Core::printDebug("< getProxyActive", "Returns: $RCODE");
	return $RCODE;
}

sub getProxyConfigured {
	SDP::Core::printDebug('> getProxyConfigured', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'sysconfig.txt';
	my $SECTION = '/etc/sysconfig/proxy';
	my @CONTENT = ();

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			next if ( m/^\s*$|^#|^;/ ); # Skip blank lines
			if ( /PROXY_ENABLED.*NO/i ) {
				SDP::Core::printDebug("PUNT", $_);
				%PROXY_CONFIG = ();
				last;
			} elsif ( /(\D+_PROXY)=(.*)/ ) {
				my $KEY = lc($1);
				my $VALUE = $2;
				$VALUE =~ s/'|"//g;
				my $VALUE_LEN = length($VALUE);
				SDP::Core::printDebug("PROCESSED {$KEY}", "String: $VALUE, Length: $VALUE_LEN");
				if ( $VALUE_LEN > 0 ) {
					$PROXY_CONFIG{$KEY} = $VALUE;
				}
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: getProxyConfigured(): Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	$RCODE = scalar keys %PROXY_CONFIG;
	if ( $RCODE ) {
			if ( $OPT_LOGLEVEL >= LOGLEVEL_DEBUG ) {
				my $KEY;
				my $VALUE;
				print(' %PROXY_CONFIG                  = ');
				while ( ($KEY, $VALUE) = each(%PROXY_CONFIG) ) {
					print("$KEY => \"$VALUE\"  ");
				}
				print("\n");
			}
	}
	SDP::Core::printDebug("< getProxyConfigured", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( getProxyConfigured() ) {
		my @PROXY_FAILED = ();
		if ( getProxyActive() ) {
			my $KEY;
			while ( ($KEY) = each(%PROXY_CONFIG) ) {
				if ( ! defined $PROXY_ACTIVE{$KEY} ) {
					SDP::Core::printDebug(" PUSH  FAILED", "$KEY");
					push(@PROXY_FAILED, $KEY);
				}
			}
			if ( $#PROXY_FAILED >= 0 ) {
				SDP::Core::updateStatus(STATUS_CRITICAL, "Configured Proxies that are Inactive: @PROXY_FAILED");
			} else {
				my @PROXIES = keys (%PROXY_ACTIVE);
				SDP::Core::updateStatus(STATUS_ERROR, "All Configured Proxies are Active: @PROXIES");
			} 
		} else {	
			@PROXY_FAILED = keys (%PROXY_CONFIG);
			SDP::Core::updateStatus(STATUS_CRITICAL, "All Configured Proxies are Inactive: @PROXY_FAILED");
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: No Configured proxies to check");
	}
SDP::Core::printPatternResults();

exit;


