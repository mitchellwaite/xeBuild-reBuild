#!/bin/sh
# status of every app/image_write function against wip/app/image_write.c
for f in $(grep "^########" build/decomp_13.txt | awk '{print $3}'); do
  r=$(python re/fncmp.py ${1:-wip/app/image_write.c} $f 2>/dev/null)
  n=$(echo "$r" | grep -c '^[-+][^-+]')
  printf '%-20s %s\n' $f "$( [ "$r" = MATCH ] && echo MATCH || echo "$n $(echo "$r" | head -1 | cut -c1-50)")"
done
