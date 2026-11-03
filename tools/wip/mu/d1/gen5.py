"""gen5.py: shapes of the reboot block replacing __builtin_expect(!noReboot, 1).  No expect left -> plain -O3.
Keeps the other hints; a 0 means this shape alone reproduces what expect + param did."""
import mkcur
import sw

BASE = mkcur.cur()
W = """log_printf(0, "\\n***** WARNING: due to previous possible errors, console reboot is not being done\\n");
				log_printf(0, "               it is not recommended to use update mode on this console again\\n");
				log_printf(0, "               until you have determined it's got a good image on it\\n\\n");
"""
OLD = """			if (__builtin_expect(!noReboot, 1)) {
				if (!ret)
					netReboot(2);
				else {
					%s				}
			}
""" % W.replace('\n\t\t\t\tlog', '\n\t\t\t\t\tlog')
assert OLD in BASE, OLD
HAT = 'static void updateNand(char *dumpDir, int *pret)\n'


def inl(s):
    return BASE.replace(OLD, s)


def helper(body, ret='void', call='rebootConsole(ret);\n'):
    t = BASE.replace(OLD, '\t\t\t' + call)
    return t.replace(HAT, 'static %s rebootConsole(int ret)\n{\n%s}\n\n' % (ret, body) + HAT)


vs = [
    ('plain', inl("""			if (!noReboot) {
				if (!ret)
					netReboot(2);
				else {
					%s				}
			}
""" % W)),
    ('pol', inl("""			if (!noReboot) {
				if (ret) {
					%s				} else
					netReboot(2);
			}
""" % W)),
    ('and1', inl("""			if (!noReboot && !ret)
				netReboot(2);
			else if (!noReboot) {
				%s			}
""" % W)),
    ('and2', inl("""			if (!noReboot && ret) {
				%s			} else if (!noReboot)
				netReboot(2);
""" % W)),
    ('goto', inl("""			if (noReboot)
				goto noreb;
			if (ret) {
				%s				goto noreb;
			}
			netReboot(2);
		noreb:
""" % W)),
    ('flag', inl("""			{
				int reboot = !noReboot;

				if (reboot) {
					if (!ret)
						netReboot(2);
					else {
						%s					}
				}
			}
""" % W)),
    ('h_early', helper("""	if (noReboot)
		return;
	if (!ret)
		netReboot(2);
	else {
		%s	}
""" % W)),
    ('h_early_pol', helper("""	if (noReboot)
		return;
	if (ret) {
		%s	} else
		netReboot(2);
""" % W)),
    ('h_early2', helper("""	if (noReboot)
		return;
	if (ret) {
		%s		return;
	}
	netReboot(2);
""" % W)),
    ('h_early3', helper("""	if (noReboot)
		return;
	if (!ret) {
		netReboot(2);
		return;
	}
	%s
""" % W)),
    ('h_nest', helper("""	if (!noReboot) {
		if (!ret)
			netReboot(2);
		else {
			%s		}
	}
""" % W)),
    ('h_int', helper("""	if (noReboot)
		return 0;
	if (!ret)
		return netReboot(2);
	%s	return 0;
""" % W, 'int')),
]
sw.run(vs, '-O3', save='gen5')
