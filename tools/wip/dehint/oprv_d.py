# oprv.py variants: macid's last five bytes in place, the bound from a fresh length local
# (unknown trip count at profile_estimate, as macidRest's n is), against 98a0eba6's source.
import os

exec(open(os.path.join(os.path.dirname(__file__), 'oprv_a.py')).read())

HEAD_OLD = '''			if (strlen(val) == 12) {
				if (validateString(val)) {'''
HEAD_NEW = '''			n = strlen(val);
			if (n == 12) {
				if (validateString(val)) {'''
DECL = [('\tint i, len, vlen, ok;\n', '\tint i, len, vlen, ok, n;\n')]
DECLU = [('\tint i, len, vlen, ok;\n', '\tint i, len, vlen, ok;\n\tsize_t n;\n')]


def loop(body):
    return [(HEAD_OLD, HEAD_NEW), (MAC_OLD, '''					xb.macid[0] = myatox8(val);
					val += 2;
					log_printf(1, "%02x", xb.macid[0]);
''' + body)]


L1 = '''					for (i = 1; i < n / 2; i++) {
						log_printf(1, ":");
						xb.macid[i] = myatox8(val);
						val += 2;
						log_printf(1, "%02x", xb.macid[i]);
					}
'''
L2 = '''					for (i = 2; i < n; i += 2) {
						log_printf(1, ":");
						xb.macid[i / 2] = myatox8(val);
						val += 2;
						log_printf(1, "%02x", xb.macid[i / 2]);
					}
'''
L3 = '''					for (i = 1; i < n / 2; i++) {
						log_printf(1, ":");
						xb.macid[i] = myatox8(val + (i - 1) * 2);
						log_printf(1, "%02x", xb.macid[i]);
					}
'''
V = [('n1', DECL + loop(L1)), ('n2', DECL + loop(L2)), ('n3', DECL + loop(L3)),
     ('u1', DECLU + loop(L1)), ('u2', DECLU + loop(L2)), ('u3', DECLU + loop(L3))]
