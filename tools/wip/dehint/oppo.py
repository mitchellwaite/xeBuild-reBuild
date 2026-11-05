"""parseOption with an int return: local types that keep uncprop from returning a
variable known to be 0.  python oppo.py [extra trick names, comma-separated]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks

DECL = '	int i, len, vlen;\n'
V = {
    'base': DECL,
    'vlen_sz': '	int i, len;\n	size_t vlen;\n',
    'vlen_u32': '	int i, len;\n	uint32_t vlen;\n',
    'len_vlen_sz': '	int i;\n	size_t len, vlen;\n',
    'all_u32': '	uint32_t i, len, vlen;\n',
    'i_len_sz': '	size_t i, len, vlen;\n',
}


def main():
    extra = sys.argv[1].split(',') if len(sys.argv) > 1 else []
    b, got = optricks.apply(optricks.base(), ['m_O', 'po_int'] + extra)
    print('applied', got)
    i = b.find('int parseOption(char *opt)\n{')
    for n, d in V.items():
        j = b.find(DECL, i)
        t = b[:j] + d + b[j + len(DECL):]
        print('%-12s %s' % (n, optlib.fmt(optlib.score_text(t, optricks.flags_for(got)))[:200]), flush=True)


main()
