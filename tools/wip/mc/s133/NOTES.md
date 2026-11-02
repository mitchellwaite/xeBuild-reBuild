# s133 (attempt 114): NO MATCH. Plain-compile best stays s132/best34.c (f2 34); floor stays s117/best.c (18).

Tools: m.sh NAME SEDEXPR... (sed on $BASE, default best34.c, + f2), hk.py/hm.sh (best34 + selected best18 hunks,
c0-relative; `python hk.py list`), res.txt = all ~95 measured variants. All variants: k = __builtin_constant_p of
a runtime value (folds to 0), empty asm goto / labels / expect only -> equivalent to src.

## Mixed lever families (direction 1)
- best34 + b18 define hunks 0-3 (AT/JUMP active): 34 (inert). + single b18 hunks: 4,6,8,22,27 = 34; 9 38; 7 60;
  28 68; 14 80; 31 82; others need label partners (9999).
- Label-closed groups: {5,8} 38; {12-16} 66; {10-16} 88; {4-16} 96; {17-34} 125; {4,17-34} 86.
- All b18 hunks + EK/K7 k-levers = 18 (k inert there). b18 + 18A (`&& !k` on -bp usage4 test) 70; + c7 k 18;
  + k on -w usage test 34; dropping EK 18.
## u2 (direction 2): stays 4/0
- reboot test forms `|k`, `^k`, `!=k`, `>k`, `k||`, `k?0:`, `&& reboot+k`: 34-38; expect(reboot,0/1) 75;
  loop cond `&&!k`/`||k` 42; NO_MODE_ARG `||k` 134-180; else-branch k-forwarders to rok/fail/netDisconnect 98-120.
- -noenter asm-goto/`if(k) goto` feed to u2 with plain/hot/cold label: 150-187.
## Dispatch / labels (directions 3-4)
- k-levers on netConnect x2, hwFlags x2, c12/c7 dummy tests, final E(reboot): 34 (inside expect / `k||E`) or 56-106.
- cold labels on usage(0/1/3/4/5) calls: inert (34); hot/cold on u2 label inert; rok hot/no-cold 90; cold label on
  -reboot log 270.
## Conclusion
The two lever families don't compose: b18's dispatch/arg-loop hunks dominate and k-levers become inert, while
partial b18 hunks on best34 only hurt. u2 frequency is not movable by any local predicate/label form tried.
