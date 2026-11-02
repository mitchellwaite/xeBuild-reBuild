#!/bin/sh
sh ours.sh $1 o_$(basename $1 .c).txt && python sig.py origs.txt o_$(basename $1 .c).txt | sed -n '/-reboot/,/-c$/p' | tr '\n' '|'; echo
