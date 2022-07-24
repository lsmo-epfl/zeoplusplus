#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

function check_changes
{
    #diff=`git diff-index --quiet HEAD --`
    diff=`git diff --no-index $1 $2`
    rm $1
    if [ -n "$diff" ]; then
        echo "### Changes detected:"
        echo "$diff"
        exit 1
    fi
}

network -xyz ZIF-67_opt.cif
check_changes ZIF-67_opt.xyz ZIF-67_opt_ref.xyz

network -ha -res -allowAdjustCoordsAndCell EDI.cssr
check_changes EDI.res EDI_ref.res
network -ha -chan 1.5 EDI.cssr
check_changes EDI.chan EDI_ref.chan
network -ha -sa 1.2 1.2 2000 EDI.cssr
check_changes EDI.sa EDI_ref.sa
network -ha -vol 1.2 1.2 50000 EDI.cssr
check_changes EDI.vol EDI_ref.vol
network -ha -psd 1.2 1.2 50000 EDI.cssr
check_changes EDI.psd_histo EDI_ref.psd_histo

#The tests below take too long to be run on CI
#network -ha -res history_1000.cssr
#check_changes
#network -ha -sa 1.5 1.5 2000 history_1000.cssr
#check_changes
#network -ha -vol 1.5 1.5 200000 history_1000.cssr
#check_changes
