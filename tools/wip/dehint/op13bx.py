"""Attempt 13: the hand-written parseButton.part.0 replaced by gcc's own splits of both
parseButton and parseButtonX (full chains), hoping ipa-icf merges the two identical parts.

python tools/wip/dehint/op13bx.py [names..]   (OUT=file writes the last one, -S prints the
function list of the asm)"""
import os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SRC = optlib.read_src(optlib.SRC)
i = SRC.index('/* parseButton after its first four names')
j = SRC.index('int baseFileExists(const char *name)')
k = SRC.rindex('\n}\n', 0, j) + 3
NOPART = SRC[:i] + SRC[k:]

TAIL = '''	else if (!strnicmp(s, "wirelessx", 9))
		b = 0x55;
	else if (!strnicmp(s, "wiredx", 6)) {
		if (!strnicmp(s, "wiredxb1", 8))
			b = 0x59;
		else if (!strnicmp(s, "wiredxb2", 8))
			b = 0x58;
		else if (!strnicmp(s, "wiredxb3", 8))
			b = 0x5a;
		else if (!strnicmp(s, "wiredxf1", 8))
			b = 0x56;
		else if (!strnicmp(s, "wiredxf2", 8))
			b = 0x57;
		else
			b = 0x5a;
	} else if (!strnicmp(s, "eject", 5))
		b = 0x12;
	else if (!strnicmp(s, "kiosk", 5))
		b = 0x41;
'''

PB_OLD = '''	else if (__builtin_expect(!strnicmp(s, "winbutton", 9), 1))
		b = 0x24;
	else
		b = parseButtonPart(s);
	return b;
}
'''
BX_OLD = '''		else if (!strnicmp(s, "winbutton", 9))
			b = 0x24;
		else
			b = parseButtonPart(s);
	}
	return b;
}
'''
BX_TAIL = ''.join('\t' + l + '\n' if l else '\n' for l in TAIL.rstrip('\n').split('\n'))


def variant(pbexp, bxform):
    t = NOPART
    w = '__builtin_expect(!strnicmp(s, "winbutton", 9), 1)' if pbexp else '!strnicmp(s, "winbutton", 9)'
    t = t.replace(PB_OLD, '\telse if (%s)\n\t\tb = 0x24;\n' % w + TAIL + '\treturn b;\n}\n')
    if bxform == 'full':
        t = t.replace(BX_OLD, '''		else if (!strnicmp(s, "winbutton", 9))
			b = 0x24;
''' + BX_TAIL + '''	}
	return b;
}
''')
    elif bxform == 'call':
        # parseButtonX's tail calls parseButton (re-tests power etc.: other code, probe only)
        t = t.replace(BX_OLD, '''		else if (!strnicmp(s, "winbutton", 9))
			b = 0x24;
		else
			b = parseButton(s);
	}
	return b;
}
''')
    return t


V = {}
for pe in (0, 1):
    for bx in ('full', 'call'):
        V['pe%d_%s' % (pe, bx)] = (pe, bx)


def fnlist(text):
    ok, o, d = optlib.compile_src(text, asm=True)
    if not ok:
        return o
    s = open(o).read()
    optlib.cleanup(d)
    return ' '.join(re.findall(r'^(_\w+(?:\.\w+\.\d+)?):', s, re.M))


def run(n):
    t = variant(*V[n])
    return n, optlib.score_text(t), t


if __name__ == '__main__':
    a = sys.argv[1:]
    S = '-S' in a
    a = [x for x in a if x != '-S']
    names = a or list(V)
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, names))
    for n, r, t in res:
        print('%-10s %s' % (n, optlib.fmt(r)))
        if S:
            print('   ', fnlist(t))
    if os.environ.get('OUT'):
        open(os.environ['OUT'], 'w', newline='\n').write(res[-1][2])
