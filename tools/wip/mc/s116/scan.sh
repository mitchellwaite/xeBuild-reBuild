#!/bin/sh
# scan.sh files.mine : flags (141ok 139ok 145ok) per variant
for f in "$@"; do b=${f%.mine}; d=$(diff --minimal $b.ref $f); a=0;c=0;e=0; echo "$d" | grep -q "^> mov eax,dword ptr \[60+esp\]" || a=1; echo "$d" | grep -q "call _log_printf" || c=1; echo "$d" | grep -B1 "^[<>] call l" | grep -q "dword ptr \[esp\],0" || e=1; [ $((a+c+e)) -gt 0 ] && echo "$a$c$e $(echo "$d"|grep -c '^[<>]') $b"; done
