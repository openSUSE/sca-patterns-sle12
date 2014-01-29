#!/usr/bin/perl

# Title:       Check for JBD error message
# Description: Check for disabling barrier messages on mounted file systems.
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
#   Tregaron Bayly (tbayly@novell.com)

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
	PROPERTY_NAME_CATEGORY."=Filesystem",
	PROPERTY_NAME_COMPONENT."=Base",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=3907838"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub barrier_disabled_messages {
  my $file = "boot.txt";
  my @output = ();
  my $section = "boot.msg";

  if (SDP::Core::getSection($file, $section, \@output)) {
    foreach $_ (@output) {
      if (/barrier-based sync failed/) { return 1; }
    }  
  }
  else {
    SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$section\" section in $file");
  }

}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();

  if (barrier_disabled_messages) {
    SDP::Core::updateStatus(STATUS_RECOMMEND, "JBD 'barrier-based sync failed' messages found.  Consider disabling barriers to supress this message");
  } else {
    SDP::Core::updateStatus(STATUS_ERROR, "No JBD 'barrier-based sync failed' messages found.");
  }

SDP::Core::printPatternResults();

exit;

