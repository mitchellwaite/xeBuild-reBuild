cd $(dirname $0)
sh run3.sh R1 'ork11: goto rkE;' 'ork11: __asm__ goto ("" :::: u2, hdd4, hdd5, p0, i0); goto rkE;'
sh run3.sh R2 'ork11: goto rkE;' 'ork11: __asm__ goto ("" :::: u2, hdd4, hdd5); goto rkE;'
sh run3.sh R3 'ork11: goto rkE;' 'ork11: __asm__ goto ("" :::: u2); goto rkE;'
sh run3.sh R4 'ork11: goto rkE; ork12: goto rkE; ork13: goto rkE;' 'ork11: __asm__ goto ("" :::: u2, hdd4); goto rkE; ork12: __asm__ goto ("" :::: hdd5); goto rkE; ork13: __asm__ goto ("" :::: p0, i0); goto rkE;'
sh run3.sh R5 'ork11: goto rkE;' 'ork11: __asm__ goto ("" :::: u2, hdd4, hdd5, p0, i0, rkE, rkE, rkE, rkE, rkE, rkE, rkE, rkE, rkE, rkE); goto rkE;'
sh run3.sh R6 'ork11: goto rkE;' 'ork11: __asm__ goto ("" :::: hdd4, hdd5); goto rkE;'
sh run3.sh R7 'ork11: goto rkE;' 'ork11: __asm__ goto ("" :::: p0, i0); goto rkE;'
sh run3.sh R8 'ork43: goto rkE;' 'ork43: __asm__ goto ("" :::: u2, hdd4, hdd5, p0, i0); goto rkE;'
