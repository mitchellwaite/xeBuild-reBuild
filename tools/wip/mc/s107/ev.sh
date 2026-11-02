#!/bin/sh
for f in "$@"; do echo $f; done | xargs -P 4 -I{} sh ../s104/run.sh {} > ev.out
python dist.py ev.out
