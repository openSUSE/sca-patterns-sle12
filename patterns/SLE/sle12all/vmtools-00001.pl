#!/usr/bin/perl

# Title:       VMware tools may prevent booting
# Description: SLE and OES system on VMware Vsphere not able to boot, waiting for device to appear
# Modified:    2013 Jun 28

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
#   David Hamner (dhamner@suse.com)

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
	PROPERTY_NAME_CATEGORY."=Virtualization",
	PROPERTY_NAME_COMPONENT."=VMware Tools",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=7005233"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub checkForVmwareModule
{
    SDP::Core::printDebug('> checkSomething', 'BEGIN');
    my $RCODE = 0;
    my $FILE_OPEN = 'boot.txt';
    my $SECTION = '/etc/sysconfig/kernel';
    my @CONTENT = ();

    if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) 
    {
	foreach $_ (@CONTENT) 
	{
	    next if ( m/^\s*$/ ); # Skip blank lines
	    #if line has vmxnet and there is two or less modules
	    if ( /^INITRD_MODULES.*vmxnet.*/)
	    {
			if( $_ !~ /\S*\s\S*\s/) 
			{
			    SDP::Core::printDebug("PROCESSING", $_);
			    $RCODE = 1;
			}
			else
			{
			    $RCODE = 0;
			}
	    }
	    else
	    {
			if(/^INITRD_MODULES.*/)
			{
			    $RCODE = 0;
			}
	    }
	}
    } 
    else 
    {
	SDP::Core::updateStatus(STATUS_ERROR, "ERROR: checkForVmwareModule(): Cannot find \"$SECTION\" section in $FILE_OPEN");
    }
    SDP::Core::printDebug("< checkForVmwareModule", "Returns: $RCODE");
    return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
    if ( checkForVmwareModule() ) 
    {
	SDP::Core::updateStatus(STATUS_CRITICAL, "Upgrading server or recreating the ram-disk could cause down server");
    } 
    else 
    {
	SDP::Core::updateStatus(STATUS_ERROR, "No vmware modules or more than two modules found");
    }
SDP::Core::printPatternResults();

exit;

