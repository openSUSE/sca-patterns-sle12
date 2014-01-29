#!/usr/bin/perl

# Title:       TCP keepalive time for hosts using LDAP Authentication
# Description: Hosts that use LDAP for authentication can have problems with nscd if communication with the ldap server is interrupted and the default tcp keepalive is used.  nscd can use up all of its connections and applications get SIGPIPE errors using the nscd socket.  The result is that commands such as id, ls, tar etc. do not print anything to STDERR or STDOUT - they appear to simply not run.
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
#
#  Authors/Contributors:
#     Tregaron Bayly (tbayly@novell.com)
#
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
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7003590"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub check_for_ldap_authentication {
  my $file = "ldap.txt";
  my $section = "nsswitch.conf";
  my @output = ();

  if (SDP::Core::getSection($file, $section, \@output)) {
    foreach $_ (@output) {
      if (/passwd_compat/) {
        if ($_ =~ "ldap") { return 1; }
      }
    }
    return 0;
  }
  else {
    SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$section\" section in $file");
  }
}

sub get_tcp_keepalive {
  my $file = "env.txt";
  my @output = ();
  my $section = "sysctl -a";

  if (SDP::Core::getSection($file, $section, \@output)) {
    foreach $_ (@output) {
      if (/net.ipv4.tcp_keepalive_time/) {
        my (undef, undef, $keepalive_time) = split (/\s+/, $_);
        return $keepalive_time;
      }
    }
  }
  else {
    SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$section\" section in $file");
  }
}

##############################################################################
# Program execution functions
##############################################################################

SDP::Core::processOptions();
  my $target_keepalive = 300;
  
  if (check_for_ldap_authentication()) {
    my $keepalive_setting = get_tcp_keepalive();
    if ($keepalive_setting > $target_keepalive) {
      SDP::Core::updateStatus(STATUS_RECOMMEND, "Current tcp_keepalive_time is $keepalive_setting.  Consider adjusting to a lower value to avoid possible nscd problems");
    } else {
      SDP::Core::updateStatus(STATUS_ERROR, "Current tcp_keepalive_time is tuned properly for ldap-authenticated hosts");
    }
  } else {
    SDP::Core::updateStatus(STATUS_ERROR, "This host does not use ldap authentication");    
  }

SDP::Core::printPatternResults();
exit;
