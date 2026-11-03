"""gen5base.py: BASE (mkcur.cur()), the reboot block OLD (with expect), W (the warning logs), HAT (where helpers go)."""
import mkcur

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
