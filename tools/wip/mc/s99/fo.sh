#!/bin/sh
# fo.sh LIST OUT : fncmp-only for every name in LIST
for n in $(cat $1); do echo "$n $(sh f.sh $n.c)"; done > $2
