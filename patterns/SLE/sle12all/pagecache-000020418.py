#!/usr/bin/python3
#
# Title:       System hang caused by vm.pagecache_limit_mb
# Description: Pattern for TID000020418
# Template:    SCA Tool Python Pattern Generator v3.0.0, Generation 1
# Modified:    2024 Mar 01
#
##############################################################################
# Copyright (C) 2024 SUSE LLC
##############################################################################
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
#  Authors/Contributors:
#   Brad Bendily
#
##############################################################################

import re
import os
import Core
import SUSE

meta_class = "SLE"
meta_category = "Memory"
meta_component = "Limit"
pattern_id = os.path.basename(__file__)
primary_link = "META_LINK_TID"
overall = Core.TEMP
overall_info = "NOT SET"
other_links = "META_LINK_TID=https://www.suse.com/support/kb/doc/?id=000020418"
Core.init(meta_class, meta_category, meta_component, pattern_id, primary_link, overall, overall_info, other_links)

##############################################################################
# Local Function Definitions
##############################################################################

def pagecache_limit_mb_is_zero():
    file_open = "env.txt"
    section = "sysctl -a"
    content = []
    confirmed = re.compile("pagecache_limit_mb", re.IGNORECASE)
    if Core.isFileActive(file_open):
        if Core.getRegExSection(file_open, section, content):
            for line in content:
                if confirmed.search(line):
                    if line.endswith("0"):
                        return True
    return False

#def condition2():
#    file_open = "boot.txt"
#    section = "dmesg -T"
#    content = []
#    confirmed = re.compile("shrink_page_cache", re.IGNORECASE)
#    if Core.isFileActive(file_open):
#        if Core.getRegExSection(file_open, section, content):
#            for line in content:
#                if confirmed.search(line):
#                    return True
#    return False

##############################################################################
# Main
##############################################################################

def main():
    '''main entry point'''

##############################################################################
#    if( condition1() ):
#        if( condition2() ):
#            Core.updateStatus(Core.CRIT, "Condition2 met")
#        else:
#            Core.updateStatus(Core.WARN, "Condition2 not found")
#    else:
#        Core.updateStatus(Core.ERROR, "Condition1 not found")
#
#    Core.printPatternResults()
##############################################################################
    if( pagecache_limit_mb_is_zero() ):
        Core.updateStatus(Core.IGNORE, "pagecache_limit_mb is 0")
    else:
        Core.updateStatus(Core.WARN, "pagecache_limit_mb found not 0")

    Core.printPatternResults()

if __name__ == "__main__":
    main()

