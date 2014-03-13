#!/usr/bin/perl

# Title:       Oracle and Asynchronous I/O Threads
# Description: A server with Oracle and insufficient Asynchronous I/O threads can cause swapping and poor server performance.
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
# Constants
##############################################################################

use constant FSAIO_RED  => 85;
use constant FSAIO_YEL  => 65;

##############################################################################
# Overriden (eventually or in part) from SDP::Core Module
##############################################################################

@PATTERN_RESULTS = (
	PROPERTY_NAME_CLASS."=SLE",
	PROPERTY_NAME_CATEGORY."=Filesystem",
	PROPERTY_NAME_COMPONENT."=AIO",
	PROPERTY_NAME_PATTERN_ID."=$PATTERN_ID",
	PROPERTY_NAME_PRIMARY_LINK."=META_LINK_TID",
	PROPERTY_NAME_OVERALL."=$GSTATUS",
	PROPERTY_NAME_OVERALL_INFO."=None",
	"META_LINK_TID=http://www.suse.com/support/kb/doc.php?id=3445451"
);

##############################################################################
# Local Function Definitions
##############################################################################

sub check_fsaio_limits {
	SDP::Core::printDebug('> check_fsaio_limits', 'BEGIN');
	my $RCODE        = 0;
	my $FILE_OPEN    = 'env.txt';
	my $SECTION      = 'sysctl -a';
	my @CONTENT      = ();
	my @LINE_CONTENT = ();
	my $LINE         = 0;
	my $MAXAIO       = 0;
	my $CURAIO       = 0;
	my $FSAIO_RATIO  = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			if ( /^fs\.aio\-max\-nr/ ) {
				SDP::Core::printDebug("LINE $LINE", $_);
				s/\s+//g;
				@LINE_CONTENT = split(/=/, $_);
				$MAXAIO = $LINE_CONTENT[1];
				$RCODE++;
			} elsif ( /^fs\.aio\-nr/ ) {
				SDP::Core::printDebug("LINE $LINE", $_);
				s/\s+//g;
				@LINE_CONTENT = split(/=/, $_);
				$CURAIO = $LINE_CONTENT[1];
				$RCODE++;
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	if ( $RCODE > 1) {
		if ( $CURAIO == 0 ) {
			if ( $MAXAIO <= 65536 ) {
				SDP::Core::updateStatus(STATUS_WARNING, "If Oracle uses asynchronous I/O threads, the default ($MAXAIO) will be insufficient");
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, "Oracle with no asynchronous I/O threads in use");
			}
		} else {
			if ( $MAXAIO <= 65536 ) {
				SDP::Core::updateStatus(STATUS_CRITICAL, "Oracle with default asynchronous I/O threads ($MAXAIO) is insufficient");
			}
			$FSAIO_RATIO = sprintf("%0.0i", ($CURAIO * 100 / $MAXAIO) );
			if ( $FSAIO_RATIO >= FSAIO_RED ) {
				SDP::Core::updateStatus(STATUS_CRITICAL, "Oracle with Asynchronous I/O threads used: ${FSAIO_RATIO}%. Exceeds limit of " . FSAIO_RED . "% ($CURAIO/$MAXAIO)");
			} elsif ( $FSAIO_RATIO >= FSAIO_YEL ) {
				SDP::Core::updateStatus(STATUS_WARNING, "Oracle with Asynchronous I/O threads used: ${FSAIO_RATIO}%. Exceeds limit of " . FSAIO_YEL . "% ($CURAIO/$MAXAIO)");
			} else {
				SDP::Core::updateStatus(STATUS_ERROR, "Oracle with Asynchronous I/O threads used: ${FSAIO_RATIO}% ($CURAIO/$MAXAIO)");
			}
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "Cannot find fs.aio-max-nr and/or fs.aio-nr values.");
	}
	SDP::Core::printDebug('< check_fsaio_limits', "Returns: $RCODE");
	return $RCODE;
}

sub oracleRunning {
	SDP::Core::printDebug('> oracleRunning', 'BEGIN');
	my $RCODE = 0;
	my $FILE_OPEN = 'basic-health-check.txt';
	my $SECTION = 'ps axwwo';
	my @CONTENT = ();
	my @ORACLE_PROCS = qw(ora_pmon_ ora_diag_ ora_psp0_ ora_lmon_ ora_lmd0_ ora_lms0_);
	my $i;
	my @LINE_CONTENT = ();
	my $LINE = 0;

	if ( SDP::Core::getSection($FILE_OPEN, $SECTION, \@CONTENT) ) {
		foreach $_ (@CONTENT) {
			$LINE++;
			next if ( /^\s*$/ ); # Skip blank lines
			@LINE_CONTENT = split(/\s+/, $_);
			foreach $i (@ORACLE_PROCS) {
				if ( $LINE_CONTENT[9] =~ /$i/ ) {
					SDP::Core::printDebug("ORACLE $LINE", $_);
					$RCODE++;
					last;
				}
			}
			last if ( $RCODE );
		}
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Cannot find \"$SECTION\" section in $FILE_OPEN");
	}
	SDP::Core::printDebug("< oracleRunning", "Returns: $RCODE");
	return $RCODE;
}

##############################################################################
# Main Program Execution
##############################################################################

SDP::Core::processOptions();
	if ( oracleRunning() ) {
		check_fsaio_limits();
	} else {
		SDP::Core::updateStatus(STATUS_ERROR, "ERROR: Oracle is not running.");
	}

SDP::Core::printPatternResults();

exit;

