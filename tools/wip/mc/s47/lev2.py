import sys, os
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s42')
import m
G = '__asm__ goto("" :::: w5x);'
for src in sys.argv[1:]:
    base = open(src).read()
    W0 = 'k61l: if (!strnicmp(argv[i], "-w", 2)) {'
    i0 = base.index(W0); i1 = base.index('client_usage(5, argv[i]);', i0) + len('client_usage(5, argv[i]);')
    W = base[i0:i1]
    for k, w in {'c2': W.replace('|| !a ||', '|| ({' + G + ' 0;}) || !a ||', 1),
                 'c3': W.replace("*a == '-'", "({" + G + " 0;}) || *a == '-'", 1),
                 'c4': W.replace("if (mode)", "if (({" + G + " 0;}) || mode)", 1)}.items():
        w = w.replace('if (mode)\n\t\t\t\tclient_usage(5', 'if (mode) { w5x: client_usage(5').replace('if (({' + G + ' 0;}) || mode)\n\t\t\t\tclient_usage(5', 'if (({' + G + ' 0;}) || mode) { w5x: client_usage(5') + ' }'
        r = m.meas(base.replace(W, w), 's47' + k + str(os.getpid()), fncmp=True)
        print(os.path.basename(src), k, r.get('inv'), r.get('fncmp'), r.get('order', r.get('err', ''))[-60:], flush=True)
