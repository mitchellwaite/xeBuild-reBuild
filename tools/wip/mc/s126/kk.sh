#!/bin/sh
# kk.sh NAME : keys of 49 and blocks around
cd $(dirname $0); grep "Changing key for bb \(49\|133\|134\|136\|148\|130\) \|start of next round: \(49\|5\|46\) " dd/$1/mc.bbro | sed 's/Changing key for bb //;s/Possible start of next round: //' | tr '\n' ';'; echo
