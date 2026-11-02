#!/bin/sh
# run.sh DIR LIST OUT : 4-way run.sh over DIR/v_<name>.c
d=$1; tr -d '\r' < $2 | sed "s#^#$d/v_#; s#\$#.c#" | xargs -P 4 -I{} sh ../s104/run.sh {} 2>/dev/null > $3
