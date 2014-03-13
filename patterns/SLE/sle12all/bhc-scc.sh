#!/bin/bash

# Title:       Validate supportconfig
# Description: Confirms supportconfig is current
# Modified:    2013 Nov 19

CURRENT_VERSION='2.25-390'

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
#
#  Authors/Contributors:
#   Jason Record (jrecord@suse.com)
#
##############################################################################

##############################################################################
# Module Definition
##############################################################################

LIBS='Core.rc SUSE.rc'
for LIB in $LIBS; do [[ -s ${BASHLIB}/${LIB} ]] && . ${BASHLIB}/${LIB} || { echo "Error: Library not found - ${BASHLIB}/${LIB}"; exit 5; }; done

##############################################################################
# Overriden (eventually or in part) from Core.rc
##############################################################################

PATTERN_RESULTS=(\
"META_CLASS=Basic Health" \
"META_CATEGORY=SLE" \
"META_COMPONENT=Supportconfig" \
"PATTERN_ID=$(basename $0)" \
"PRIMARY_LINK=META_LINK_CoolSolution" \
"OVERALL=$GSTATUS" \
"OVERALL_INFO=None" \
"META_LINK_CoolSolution=http://www.novell.com/coolsolutions/tools/16106.html" \
"META_LINK_Patch=https://www.suse.com/communities/conversations/files/2013/03/supportutils-plugin-updater-1.0-25.1.noarch.rpm" \
                 
)

processOptions "$@"
packageInstalled 'ntsutils'
if (( $? ))
then
	updateStatus $STATUS_CRITICAL "Supportconfig from ntsutils package is deprecated, remove ntsutils and install the supportutils package"
else
	getSCInfo # populates SC_INFO_VERSION
	compareVersions "$SC_INFO_VERSION" "$CURRENT_VERSION"
	RESULTS=$?
	printDebug "main RESULTS" "$RESULTS"
	if (( $RESULTS < $COMPARED_EQUAL ))
	then
		packageInstalled 'supportutils-plugin-updater'
		if (( $? ))
		then
			updateStatus $STATUS_WARNING "Supportconfig version $SC_INFO_VERSION is outdated, run updateSupportutils to update"
		else
			updateStatus $STATUS_WARNING "Supportconfig version $SC_INFO_VERSION is outdated, update supportutils package for better results"
		fi
	else
		setStatus $STATUS_SUCCESS "Supportconfig version $SC_INFO_VERSION is sufficient"
	fi
fi
printPatternResults

