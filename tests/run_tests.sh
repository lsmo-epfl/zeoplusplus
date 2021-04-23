#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

function check_changes
{
    #diff=`git diff-index --quiet HEAD --`
    diff=`git diff .`

    if [ -n "$diff" ]; then
        echo "### Changes detected:"
        echo "$diff"
        exit 1
    fi
}

network -ha -res ZIF-67_opt.cif
check_changes

network -ha -res -allowAdjustCoordsAndCell EDI.cssr
check_changes
network -ha -chan 1.5 EDI.cssr
check_changes
network -ha -sa 1.2 1.2 2000 EDI.cssr
check_changes
network -ha -vol 1.2 1.2 50000 EDI.cssr
check_changes
network -ha -psd 1.2 1.2 50000 EDI.cssr
check_changes

#The tests below take too long to be run on CI
#network -ha -res history_1000.cssr
#check_changes
#network -ha -sa 1.5 1.5 2000 history_1000.cssr
#check_changes
#network -ha -vol 1.5 1.5 200000 history_1000.cssr
#check_changes
