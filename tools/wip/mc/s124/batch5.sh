cd $(dirname $0)
O="if (i + 1 == argc || ({__asm__ goto(\"\" :::: r3x); 0;}) || !a || *a == '-')"
J='({__asm__ goto("" :::: r3x); 0;})'
timeout 400 sh run3.sh R6 'ork11: goto rkE;' 'ork11: __asm__ goto ("" :::: hdd4, hdd5); goto rkE;'
timeout 400 sh run3.sh R7 'ork11: goto rkE;' 'ork11: __asm__ goto ("" :::: p0, i0); goto rkE;'
timeout 400 sh run3.sh R8 'ork43: goto rkE;' 'ork43: __asm__ goto ("" :::: u2, hdd4, hdd5, p0, i0); goto rkE;'
timeout 400 sh run3.sh T1 "$O" "if (i + 1 == argc || !a || $J || *a == '-')" r9.c
timeout 400 sh run3.sh T2 "$O" "if ($J || i + 1 == argc || !a || *a == '-')" r9.c
timeout 400 sh run3.sh T3 "$O" "if (i + 1 == argc || !a || *a == '-' || $J)" r9.c
timeout 400 sh run3.sh T5 "$O" "if (i + 1 == argc || $J || $J || !a || *a == '-')" r9.c
timeout 400 sh run3.sh T6 "$O" "if (i + 1 == argc || $J || !a || $J || *a == '-')" r9.c
echo BATCH5DONE
