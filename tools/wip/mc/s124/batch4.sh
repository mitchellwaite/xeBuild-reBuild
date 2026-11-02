cd $(dirname $0)
sh run3.sh T1 'if (i + 1 == argc || ({__asm__ goto("" :::: r3x); 0;}) || !a || *a == '-')' 'if (i + 1 == argc || !a || ({__asm__ goto("" :::: r3x); 0;}) || *a == '"'-'"')' r9.c
sh run3.sh T2 'if (i + 1 == argc || ({__asm__ goto("" :::: r3x); 0;}) || !a || *a == '-')' 'if (({__asm__ goto("" :::: r3x); 0;}) || i + 1 == argc || !a || *a == '"'-'"')' r9.c
sh run3.sh T3 'if (i + 1 == argc || ({__asm__ goto("" :::: r3x); 0;}) || !a || *a == '-')' 'if (i + 1 == argc || !a || *a == '"'-'"' || ({__asm__ goto("" :::: r3x); 0;}))' r9.c
sh run3.sh T4 'if (i + 1 == argc || ({__asm__ goto("" :::: r3x); 0;}) || !a || *a == '-')' 'if (i + 1 == argc || ({__asm__ goto("" :::: r3x, r3x); 0;}) || !a || *a == '"'-'"')' r9.c
sh run3.sh T5 'if (i + 1 == argc || ({__asm__ goto("" :::: r3x); 0;}) || !a || *a == '-')' 'if (i + 1 == argc || ({__asm__ goto("" :::: r3x); 0;}) || ({__asm__ goto("" :::: r3x); 0;}) || !a || *a == '"'-'"')' r9.c
sh run3.sh T6 'if (i + 1 == argc || ({__asm__ goto("" :::: r3x); 0;}) || !a || *a == '-')' 'if (i + 1 == argc || ({__asm__ goto("" :::: r3x); 0;}) || !a || ({__asm__ goto("" :::: r3x); 0;}) || *a == '"'-'"')' r9.c
