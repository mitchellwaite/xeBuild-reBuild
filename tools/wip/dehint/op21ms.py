#!/usr/bin/env python3
"""Attempt 21: instruction multiset difference of one function (ignores order, jump and call
targets), to tell layout-only diffs from code diffs.  Reads `op21.py -v FN variant` on stdin."""
import collections, re, sys
m = collections.Counter(); p = collections.Counter()
for l in sys.stdin:
    if l.startswith(('---', '+++')) or l[:1] not in '-+':
        continue
    s = re.sub(r'^(j\w+|call)\s+\w+', r'\1', l[1:].strip())
    if s.startswith(('nop', 'xchg   ax,ax', 'lea    esi,[esi', 'lea    edi,[edi', 'data16', 'cs nop')):
        continue
    (m if l[0] == '-' else p)[s] += 1
print('only ref', sum((m - p).values()), sorted((m - p).items())[:20])
print('only new', sum((p - m).values()), sorted((p - m).items())[:20])
