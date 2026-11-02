#!/bin/sh
# ev.sh names... : run.sh on v_<name>.c (4-way), then f2 + srch.dist (block numbers as in best; approximate when numbering shifts)
for n in "$@"; do echo v_$(echo $n | tr -d '\r').c; done | xargs -P 4 -I{} sh ../s104/run.sh {} 2>/dev/null > ev.out
python dist.py ev.out | sort -t= -k2 -n | cut -c1-170
