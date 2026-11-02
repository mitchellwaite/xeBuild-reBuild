"""lev.py: asm-goto lever variants on H5b's -w/-r arms; measure with s42 m.py (fncmp)."""
import sys, os
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s42')
import m
base = open(r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s42\H5b.c').read()
W = '''		} else { k61l: if (!strnicmp(argv[i], "-w", 2)) {
			a = argv[i + 1];
			if (i + 1 == argc || !a || *a == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);'''
assert W in base
G = '__asm__ goto("" :::: w5x);'
V = {
 'w_top': W.replace('{\n\t\t\ta = argv', '{ ' + G + '\n\t\t\ta = argv').replace('if (mode)\n\t\t\t\tclient_usage(5', 'if (mode) { w5x: client_usage(5') + ' }',
 'w_mid': W.replace('a = argv[i + 1];', 'a = argv[i + 1]; ' + G).replace('if (mode)\n\t\t\t\tclient_usage(5', 'if (mode) { w5x: client_usage(5') + ' }',
 'w_c1': W.replace('if (i + 1 == argc', 'if (({' + G + ' 0;}) || i + 1 == argc').replace('if (mode)\n\t\t\t\tclient_usage(5', 'if (mode) { w5x: client_usage(5') + ' }',
 'w_c2': W.replace('|| !a ||', '|| ({' + G + ' 0;}) || !a ||').replace('if (mode)\n\t\t\t\tclient_usage(5', 'if (mode) { w5x: client_usage(5') + ' }',
}
for k, w in V.items():
    r = m.meas(base.replace(W, w), 's47' + k + str(os.getpid()), fncmp=True)
    print(k, r.get('inv'), r.get('fncmp'), r.get('order', r.get('err', ''))[-90:], flush=True)
