"""Attempt 47: the tail test as `(int)r < 0` (0 loose / 7 strict: only the no-key log's
.p2align) with natural edits around it that move the SE copy's and the no-key log's frequencies.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a47_neg.py"""
import os, itertools
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src', 'build.c')
NEG = ('if (__builtin_expect(r != 0, 0))\n', 'if ((int)r < 0)\n')
SIG = open(BASE, newline='').read()
i = SIG.index('\t\t\t\tif (type == 5 || type == 17 || type == 11) {')
j = SIG.index('\t\t\t\t/* the expect leaves', i)
SIG = SIG[i:j]
SIG_NOT = '''				if (type == 5 || type == 17 || type == 11) {
					if (!xb.pub1bl)
						log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
					else if (!cbVerifySig(e->data, xb.pub1bl)) {
						log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
						r = -1;
					} else
						log_printf(1, "loaded %s, signature check passed!\\n", e->name);
				}
'''
SIG_OK = '''				if (type == 5 || type == 17 || type == 11) {
					if (xb.pub1bl) {
						if (cbVerifySig(e->data, xb.pub1bl))
							log_printf(1, "loaded %s, signature check passed!\\n", e->name);
						else {
							log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
							r = -1;
						}
					} else
						log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
				}
'''
SE = ('if (type == 9 && e->data[0] == \'S\' && e->data[1] == \'E\') {', 'if (type == 9 && e->data[0] == \'S\' && e->data[1] == \'E\') {')
SEm = ('if (type == 9 && e->data[0] == \'S\' && e->data[1] == \'E\') {', 'if (type == 9 && !memcmp(e->data, "SE", 2)) {')
ORD = {'5_17_11': None, '11_5_17': 'type == 11 || type == 5 || type == 17', '5_11_17': 'type == 5 || type == 11 || type == 17',
       '17_5_11': 'type == 17 || type == 5 || type == 11'}
V = {}
for (sk, sv), (ok, ov), (ek, ev) in itertools.product({'sig': None, 'not': SIG_NOT, 'ok': SIG_OK}.items(), ORD.items(),
                                                     {'se': None, 'sem': SEm}.items()):
    e = [NEG]
    if sv:
        e.append((SIG, sv))
    if ov:
        e.append(('type == 5 || type == 17 || type == 11', ov))
    if ev:
        e.append(ev)
    V['%s_%s_%s' % (sk, ok, ek)] = e
