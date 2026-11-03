"""strip.py: named textual removals of src/mode_update.c's tricks.  python strip.py OUT.c NAME...
apply(names, txt) is used by the sweeps.  Names:
  wcp      dead cp(r+1..4) goto werr in updateNand (label werr stays out too)
  wok      hot label wok
  expect   __builtin_expect(!noReboot, 1)
  ipcp     cp(i+101) goto iperr
  dn       the asm goto / if(0) dummy block in the -noava arm
  noreeb   memset(argv,0,cp(i+106)) in the -noreeb arm
All are source-only; flags are separate."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
SRC = os.path.join(HERE, 'base.c')

R = {
    'wcp': [("""				if (cp(r + 1) && cp(r + 2) && cp(r + 3) && cp(r + 4))
					goto werr;
""", ''), ("""				werr:
""", '')],
    'wok': [("""			wok: __attribute__((hot, unused));
""", '')],
    'expect': [('if (__builtin_expect(!noReboot, 1)) {', 'if (!noReboot) {')],
    'ipcp': [("""			if (cp(i + 101))
				goto iperr;
""", ''), ("""			iperr:
""", '')],
    'dn': [("""
			__asm__ goto ("" :::: dn);
			if (0) {
			dn:
				__asm__ volatile ("" :: "r"(i));
				if (cp(argc + 103))
					continue;
				__builtin_unreachable();
			}
""", '')],
    'noreeb': [("""			__builtin_memset(argv, 0, cp(i + 106));
""", '')],
}
ALL = list(R)


def load():
    return open(SRC, newline='').read()


def apply(names, txt=None):
    t = load() if txt is None else txt
    for n in names:
        for a, b in R[n]:
            if a not in t:
                raise SystemExit('no text for ' + n + ': ' + a[:40])
            t = t.replace(a, b)
    return t


if __name__ == '__main__':
    out = sys.argv[1]
    t = apply(sys.argv[2:])
    with open(out, 'w', newline='\n') as f:
        f.write(t)
