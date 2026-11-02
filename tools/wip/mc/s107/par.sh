#!/bin/sh
# par.sh files... -> res lines
for f in "$@"; do echo $f; done | xargs -P 4 -I{} sh -c 'echo "{} $(sh ../s101/f2.sh {})"'
