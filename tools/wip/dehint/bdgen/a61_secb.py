"""Attempt 61: the SE block holds its own checkBl call (a call in the SE block gives the 'E' test's SE edge
PRED_CALL as well as nonequal: 13.7% instead of 28%, so the SE block is 6 at profile_estimate, not 7),
crossed with exp_pr's spellings.
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a61_secb.py [-p 99|0|90] -o -"""
OLD = '''					xb.seReplacesCf = 1;
				}
				r = checkBl(e->data, e->size, type, e->crc);
'''
def se(arg, form):
    if form == 'else':
        return '''					xb.seReplacesCf = 1;
					r = checkBl(e->data, e->size, %s, e->crc);
				} else
					r = checkBl(e->data, e->size, type, e->crc);
''' % arg
    if form == 'else2':
        return '''					xb.seReplacesCf = 1;
					r = checkBl(e->data, e->size, %s, e->crc);
				} else {
					r = checkBl(e->data, e->size, type, e->crc);
				}
''' % arg
EXP = 'if (__builtin_expect(r != 0, 0))\n\t\t\t\t\t\tgoto fail;'
TAILS = {'x': None, 'ne': 'if (r != 0)\n\t\t\t\t\t\tgoto fail;', 'r': 'if (r)\n\t\t\t\t\t\tgoto fail;',
         'neg': 'if ((int)r < 0)\n\t\t\t\t\t\tgoto fail;'}
V = {}
for an, arg in (('t', 'type'), ('14', '14')):
    for f in ('else',):
        for tn, tl in TAILS.items():
            ed = [(OLD, se(arg, f))]
            if tl:
                ed.append((EXP, tl))
            V['%s_%s_%s' % (f, an, tn)] = ed
