"""Attempt 4: xellbutton site forms on the natural parseButton base (build/op/nat.c = optricks
part+m_bx+pb_exp with parseButtonX deleted, 335 lines).  For each form: the call block's
frequency at profile_estimate (target ~169..173, notes/options.md) and the optlib score.

python tools/wip/dehint/opxs4.py [base.c] [names..]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, opfq, bdlib

HEAD = '''		if (!xb.xellButton && (xb.bootFlags & 4)) {
			xb.xellButton = parseButton(getIniValue("xellbutton"));
			if (!xb.xellButton) {
				log_printf(1, "default console DVD eject button is being used to start xell\\n");
				xb.xellButton = 0x12;
			}
		}
'''
BODY = '''			xb.xellButton = parseButton(getIniValue("xellbutton"));
			if (!xb.xellButton) {
				log_printf(1, "default console DVD eject button is being used to start xell\\n");
				xb.xellButton = 0x12;
			}
'''
V = {
    'base': HEAD,
    'nest': '''		if (!xb.xellButton) {
			if (xb.bootFlags & 4) {
''' + BODY.replace('\n\t\t\t', '\n\t\t\t\t').replace('\t\t\txb.xellButton = parseButton', '\t\t\t\txb.xellButton = parseButton', 1) + '''			}
		}
''',
    'goto_or': '''		if (xb.xellButton || !(xb.bootFlags & 4))
			goto alt;
''' + BODY.replace('\t\t\t', '\t\t', ) + '''alt:
''',
    'goto_x': '''		if (xb.xellButton)
			goto alt;
		if (xb.bootFlags & 4) {
''' + BODY + '''		}
alt:
''',
    'goto_b': '''		if (!xb.xellButton) {
			if (!(xb.bootFlags & 4))
				goto alt;
''' + BODY + '''		}
alt:
''',
    'nest_b': '''		if (xb.bootFlags & 4 && !xb.xellButton) {
''' + BODY + '''		}
''',
    'ne0': '''		if (xb.xellButton == 0 && (xb.bootFlags & 4) != 0) {
''' + BODY + '''		}
''',
    'neg': '''		if (!(xb.xellButton || !(xb.bootFlags & 4))) {
''' + BODY + '''		}
''',
    'else': '''		if (xb.xellButton || !(xb.bootFlags & 4))
			;
		else {
''' + BODY + '''		}
''',
}


def make(base, name):
    if HEAD not in base:
        raise SystemExit('site not found')
    return base.replace(HEAD, V[name])


def one(base, name):
    t = make(base, name)
    dt, d = opfq.dump(t)
    fr = None
    if dt:
        body = opfq.fn(dt, 'applyIniOptions')
        for bb, f, p in opfq.blocks(body):
            if 'getIniValue ("xellbutton")' in p:
                fr = f
                break
    bdlib.cleanup(d)
    return name, fr, optlib.score_text(t)


def main():
    a = sys.argv[1:]
    bp = a.pop(0) if a and a[0].endswith('.c') else os.path.join(optlib.BUILD, 'nat.c')
    base = optlib.read_src(bp)
    names = a or list(V)
    with ThreadPoolExecutor(6) as p:
        for n, fr, r in p.map(lambda n: one(base, n), names):
            print('%-10s freq %-5s %s' % (n, fr, optlib.fmt(r)), flush=True)


if __name__ == '__main__':
    main()
