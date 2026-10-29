"""Generate mode_client variants from the draft by textual toggles and score them.
python mcgen.py [toggle ...]   (no args: every single toggle; 'all' prints the toggle names;
'pairs': every pair).  Env FNCMP=1 also runs fncmp; BASE=<file> uses another base draft."""
import os, sys, re, itertools
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import mcvar
DRAFT = os.environ.get('BASE') or r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mode_client.c'
base = open(DRAFT).read()


def sub(t, old, new, count=1):
    assert old in t, old[:60]
    return t.replace(old, new, count)


TOG = {}


def toggle(name):
    def deco(f):
        TOG[name] = f
        return f
    return deco


@toggle('hdd')
def _(t):
    t = sub(t, """				if (cinfo->hwFlags & 0x20)
					sendAvatarData(arg, cinfo->kernel);
				else
					log_printf(0, "\\n\\n***** ERROR: cannot send avatar data when a HDD does not exist!\\n");""",
            """				if (!(cinfo->hwFlags & 0x20))
					log_printf(0, "\\n\\n***** ERROR: cannot send avatar data when a HDD does not exist!\\n");
				else
					sendAvatarData(arg, cinfo->kernel);""")
    t = sub(t, """				if (cinfo->hwFlags & 0x20)
					sendCompatData(arg);
				else
					log_printf(0, "\\n\\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\\n");""",
            """				if (!(cinfo->hwFlags & 0x20))
					log_printf(0, "\\n\\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\\n");
				else
					sendCompatData(arg);""")
    return t


@toggle('dummy')
def _(t):
    t = sub(t, """				if (arg == dummy)
					clientPatches(NULL);
				else
					clientPatches(arg);""", """				if (arg != dummy)
					clientPatches(arg);
				else
					clientPatches(NULL);""")
    t = sub(t, """				if (arg == dummy)
					clientInfo(NULL);
				else
					clientInfo(arg);""", """				if (arg != dummy)
					clientInfo(arg);
				else
					clientInfo(NULL);""")
    return t


@toggle('erase')
def _(t):
    return sub(t, """	if (block != -1) {
		if (block < cinfo->nandSize / cinfo->blockSize) {
			log_printf(0, "erasing block 0x%x...", block);
			if (netEraseBlock(block, 1))
				log_printf(0, "Success!\\n");
			else
				log_printf(0, "\\n\\n***** ERROR: Failed to erase block 0x%x!\\n", block);
		} else
			log_printf(0, "\\n\\n***** ERROR: Block 0x%x is outside system area!\\n", block);
	} else
		log_printf(0, "\\n\\n***** ERROR: Invalid arguments specified, please provide hex only for offset!\\n");""",
               """	if (block == -1)
		log_printf(0, "\\n\\n***** ERROR: Invalid arguments specified, please provide hex only for offset!\\n");
	else if (block >= cinfo->nandSize / cinfo->blockSize)
		log_printf(0, "\\n\\n***** ERROR: Block 0x%x is outside system area!\\n", block);
	else {
		log_printf(0, "erasing block 0x%x...", block);
		if (!netEraseBlock(block, 1))
			log_printf(0, "\\n\\n***** ERROR: Failed to erase block 0x%x!\\n", block);
		else
			log_printf(0, "Success!\\n");
	}""")


@toggle('erase2')
def _(t):
    return sub(t, """			if (netEraseBlock(block, 1))
				log_printf(0, "Success!\\n");
			else
				log_printf(0, "\\n\\n***** ERROR: Failed to erase block 0x%x!\\n", block);""",
               """			if (!netEraseBlock(block, 1))
				log_printf(0, "\\n\\n***** ERROR: Failed to erase block 0x%x!\\n", block);
			else
				log_printf(0, "Success!\\n");""")


@toggle('norok')
def _(t):
    return sub(t, "			rok: __attribute__((cold));\n", "")


@toggle('nofail')
def _(t):
    return sub(t, "fail: __attribute__((cold));", "fail:")


@toggle('noereboot')
def _(t):
    return sub(t, "	if (E(reboot))\n		netReboot(reboot);", "	if (reboot)\n		netReboot(reboot);")


@toggle('tail')
def _(t):
    s = t.index("	if (!(mode && arg)) {")
    e = t.index("	} else {\n		if (netConnect(ip)) {\n			cinfo = netGetInfo();\n			switch (mode) {")
    tailend = "		} else\n			goto fail;\n	}\n"
    e2 = t.index(tailend, e)
    sw = t[t.index("			switch (mode) {", e):e2]
    new = ("	if (mode && arg) {\n		if (netConnect(ip)) {\n			cinfo = netGetInfo();\n" + sw +
           "		} else\n			goto fail;\n	} else if (reboot) {\n		if (netConnect(ip))\n			cinfo = netGetInfo();\n		else\n			goto fail;\n	} else\n		client_usage(2, NULL);\n")
    return t[:s] + new + t[e2 + len(tailend):]


@toggle('ip')
def _(t):
    return sub(t, """			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			ip = argv[++i];
			log_printf(0, "setting forced IP to %s\\n", ip);""",
               """			if (argv[i + 1] && i + 1 != argc && *argv[i + 1] != '-') {
				ip = argv[++i];
				log_printf(0, "setting forced IP to %s\\n", ip);
			} else
				client_usage(3, argv[i]);""")


def nest(logline, modeno):
    def f(t):
        old = ("""			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, "%s", arg);
			mode = %d;""" % (logline, modeno))
        new = ("""			if (argv[i + 1] && i + 1 != argc && *argv[i + 1] != '-') {
				if (!mode) {
					arg = argv[++i];
					log_printf(0, "%s", arg);
					mode = %d;
				} else
					client_usage(5, argv[i]);
			} else
				client_usage(3, argv[i]);""" % (logline, modeno))
        return sub(t, old, new)
    return f


TOG['nest_eb'] = nest('erase block set to %s\\n', 10)
TOG['nest_e'] = nest('setting avatar/kinect files base path to %s\\n', 4)
TOG['nest_c'] = nest('setting xbox compatibility files base path to %s\\n', 5)


def nest2(logline, modeno):
    def f(t):
        old = ("""			a = argv[i + 1];
			if (i + 1 == argc || !a || *a == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, "%s", arg);
			mode = %d;""" % (logline, modeno))
        new = ("""			a = argv[i + 1];
			if (i + 1 != argc && a && *a != '-') {
				if (!mode) {
					arg = argv[++i];
					log_printf(0, "%s", arg);
					mode = %d;
				} else
					client_usage(5, argv[i]);
			} else
				client_usage(3, argv[i]);""" % (logline, modeno))
        return sub(t, old, new)
    return f


TOG['nest_r'] = nest2('setting read filename to %s\\n', 1)
TOG['nest_w'] = nest2('setting write filename to %s\\n', 2)


def ip_(logline, modeno):
    def f(t):
        old = ("""			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				arg = dummy;
			else {
				arg = argv[++i];
				log_printf(0, "%s", arg);
			}
			mode = %d;""" % (logline, modeno))
        new = ("""			if (argv[i + 1] && i + 1 != argc && *argv[i + 1] != '-') {
				arg = argv[++i];
				log_printf(0, "%s", arg);
			} else
				arg = dummy;
			mode = %d;""" % (logline, modeno))
        return sub(t, old, new)
    return f


TOG['ip_i'] = ip_('info dump path set to %s\\n', 12)
TOG['ip_p'] = ip_('patch file set to %s\\n', 7)


@toggle('mode_bp')
def _(t):
    return sub(t, """			start = b;
			if (mode)
				client_usage(5, argv[i]);
			i = j;""", """			start = b;
			if (!mode)
				i = j;
			else
				client_usage(5, argv[i]);""")


def make(toggles):
    t = base
    for n in toggles:
        t = TOG[n](t)
    return t


if __name__ == '__main__':
    args = sys.argv[1:]
    flags = ['-O3', '--param', 'builtin-expect-probability=50']
    if args == ['all']:
        print(' '.join(TOG))
        sys.exit()
    combos = [[n] for n in TOG] if not args else [args]
    if args and args[0] == 'pairs':
        combos = [list(c) for c in itertools.combinations(TOG, 2)]
    os.makedirs(os.path.join(S, 'gen'), exist_ok=True)
    for c in combos:
        try:
            t = make(c)
        except AssertionError as e:
            print(c, 'SKIP', e)
            continue
        p = os.path.join(S, 'gen', '_'.join(c) + '.c')
        open(p, 'w', newline='\n').write(t)
        res, err = mcvar.run(p, flags, fncmp=bool(os.environ.get('FNCMP')))
        if res is None:
            print(c, 'ERR', err[:200])
            continue
        print('%-28s inv=%2d pre=%2d%s' % ('+'.join(c), res['inv'], res['pre'],
                                           ' fncmp=%d' % res['fncmp'] if 'fncmp' in res else ''), ' '.join(res['order'][:8]))
