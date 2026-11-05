"""parseCmdOptions forms calling a uint32_t parseOption directly (po_int2 base)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks

OLD = '''				if (!parseOption(opt))
					return 0;
'''
V = {
    'int_r': ('int i, j, len;', 'int i, j, len, r;', '''				r = parseOption(opt);
				if (!r)
					return 0;
'''),
    'int_r_ret': ('int i, j, len;', 'int i, j, len, r;', '''				r = parseOption(opt);
				if (!r)
					return r;
'''),
    'u32_r': ('int i, j, len;', 'int i, j, len;\n\tuint32_t r;', '''				r = parseOption(opt);
				if (!r)
					return 0;
'''),
    'eq0': (None, None, '''				if (parseOption(opt) == 0)
					return 0;
'''),
    'cast': (None, None, '''				if (!(int)parseOption(opt))
					return 0;
'''),
    'ok_flag': ('int i, j, len;', 'int i, j, len;\n\tint ok = 1;', None),
}


def main():
    b, got = optricks.apply(optricks.base(), sys.argv[1].split(',') if len(sys.argv) > 1 else ['m_O', 'po_int2'])
    i = b.find('int parseCmdOptions(')
    j = b.find('\n}\n', i)
    for n, (d0, d1, body) in V.items():
        if body is None:
            continue
        f = b[i:j]
        if d0:
            f = f.replace(d0, d1, 1)
        f = f.replace(OLD, body)
        t = b[:i] + f + b[j:]
        print('%-10s %s' % (n, optlib.fmt(optlib.score_text(t))))


main()
