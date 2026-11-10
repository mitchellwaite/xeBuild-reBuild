#!/usr/bin/env python3
"""mode_client attempt 17: the fully natural file and whole-shape variants of it.

python tools/wip/dehint/mc17.py [-o out.c] [-v [fn]] [-l] [-d] variant ..
  a variant is `name` or `axis=value,axis=value,..` (see AXES below; unnamed axes take
  the first value).  `src` is today's src/mode_client.c, `old` commit e8c0b8d8's (the
  48-trick source the attempt started from).
  -l  print the layout diff against the reference, -v the per-function diff,
  -d  write dumps to build/mc/w17/d_<variant>, -o the source.

The file is commit e8c0b8d8's src/mode_client.c up to clientEraseBlock (the header comment
and the AT / JMP macros dropped), then the helpers and mode_client built from the axes: no
hint anywhere.  The landed source is
  conn=six,six=usage1,test=pos,ipa=onearg,bps=inpcbr,r=onec,w=onec,o2=jcr
with oneArgC named fileArg, and since the second part getArgs respelled (mc17ga.py's
f0-x-i-n-xn-a; the variants here keep the older getArgs, which compiles to the same code)."""
import os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc17lib as L

BASE_REV = 'e8c0b8d8'
SRC = subprocess.run(['git', 'show', BASE_REV + ':src/mode_client.c'], cwd=L.R,
                     capture_output=True).stdout.decode().replace('\r\n', '\n')
_h0 = SRC.index('/* mode_client is built with no profile')
_h1 = SRC.index('#include "xebuild.h"')
_e0 = SRC.index('static void clientEraseBlockI(')
_g0 = SRC.index('/* the option\'s argument(s); dies with usage')
_b0 = SRC.index('/* -bp <f> <o>: getArgs\' checks')
_m0 = SRC.index('int mode_client(int argc, char **argv)\n')
_t0 = SRC.index('/* 16 zero bytes end the original')
HEAD = SRC[:_h0] + SRC[_h1:_e0]
GETARGS = SRC[_g0:_b0]
TAILPAD = SRC[_t0:]

AXES = {}


def axis(name, *vals):
    AXES[name] = vals


# ---- helpers -------------------------------------------------------------------------
axis('bp', 'static', 'getargs', 'inline')      # -bp: bpArgs (no pin) / getArgs(.., &start, NULL) / written out
axis('wb', 'static', 'getargs', 'inline')
axis('eb', 'static', 'getargs', 'inline')

# ---- the option loop -----------------------------------------------------------------
axis('help', 'or', 'split')                    # one || test / one if per spelling
axis('rw', 'a', 'plain', 'getargs')            # -r / -w: `a = argv[i + 1]` temp / argv[i + 1] spelled out
# a second one-argument helper with getArgs' first test order (argc first), in a few spellings
ONEC = {
    'onec': '''static char *oneArgC(int argc, char **argv, int *pi, int mode)
{
	int i = *pi;
	char *a = argv[i + 1];

	if (i + 1 == argc || !a || *a == '-')
		client_usage(3, argv[i]);
	if (mode)
		client_usage(5, argv[i]);
	*pi = i + 1;
	return argv[i + 1];
}

''',
    'onec2': '''static char *oneArgC(int argc, char **argv, int *pi, int mode)
{
	int i = *pi;

	if (i + 1 == argc || !argv[i + 1] || *argv[i + 1] == '-')
		client_usage(3, argv[i]);
	if (mode)
		client_usage(5, argv[i]);
	*pi = i + 1;
	return argv[i + 1];
}

''',
    'onec3': '''static char *oneArgC(int argc, char **argv, int *pi, int mode)
{
	int i = *pi + 1;
	char *a = argv[i];

	if (i == argc || !a || *a == '-')
		client_usage(3, argv[i - 1]);
	if (mode)
		client_usage(5, argv[i - 1]);
	*pi = i;
	return argv[i];
}

''',
}
axis('onec', 'onec', 'onec2', 'onec3')         # which spelling of oneArgC
ONE = ('plain', 'plainc', 'a', 'an', 'getargs', 'onearg', 'onec', 'g', 'gn', 'ai', 'ain', 'pi', 'pin', 'j', 'jn', 'ja', 'jna')
axis('r', '', *ONE)                            # -r alone ('' = rw's value); w likewise (see arm1)
axis('w', '', *ONE)
axis('e', *ONE)                                # -e: tests written out / getArgs(.., 1, NULL, NULL) / oneArg
axis('c', *ONE)
axis('ipa', 'plain', 'getargs', 'onearg')      # -ip: tests written out / getArgs(.., 0, NULL, NULL) / oneArg(.., 0)


def arm1(k):
    """a one-argument option's argument: plain / plainc the tests written out (NULL or argc
    first), a / an the same through `a`, getargs / onearg a helper call"""
    if k == 'getargs':
        return '			arg = getArgs(argc, argv, &i, mode, 1, NULL, NULL);\n'
    if k == 'onearg':
        return '			arg = oneArg(argc, argv, &i, mode);\n'
    if k == 'onec':
        return '			arg = oneArgC(argc, argv, &i, mode);\n'
    if k in ('g', 'gn'):                        # arg itself holds the candidate
        c = "i + 1 == argc || !arg" if k == 'g' else "!arg || i + 1 == argc"
        return '''			arg = argv[i + 1];
			if (%s || *arg == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			i++;
''' % c
    if k in ('ai', 'ain'):                      # `a` temp, arg = a
        c = "i + 1 == argc || !a" if k == 'ai' else "!a || i + 1 == argc"
        return '''			a = argv[i + 1];
			if (%s || *a == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = a;
			i++;
''' % c
    if k in ('j', 'jn', 'ja', 'jna'):           # bpArgs' way: j = i + 1 (needs `int j` in mode_client)
        c = "j == argc || !a" if k in ('j', 'ja') else "!a || j == argc"
        return '''			j = i + 1;
			a = argv[j];
			if (%s || *a == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = %s;
			i = j;
''' % (c, 'a' if k in ('ja', 'jna') else 'argv[j]')
    if k in ('pi', 'pin'):                      # getArgs' way: step first
        c = "i == argc || !argv[i]" if k == 'pi' else "!argv[i] || i == argc"
        return '''			i++;
			if (%s || *argv[i] == '-')
				client_usage(3, argv[i - 1]);
			if (mode)
				client_usage(5, argv[i - 1]);
			arg = argv[i];
''' % c
    t = {'plain': "			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')\n",
         'plainc': "			if (i + 1 == argc || !argv[i + 1] || *argv[i + 1] == '-')\n",
         'a': "			a = argv[i + 1];\n			if (i + 1 == argc || !a || *a == '-')\n",
         'an': "			a = argv[i + 1];\n			if (!a || i + 1 == argc || *a == '-')\n"}[k]
    return t + '''				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[i + 1];
			i++;
'''
axis('s', 'eq2', 'ne2')                        # -s: if (reboot == 2) ignore else set / reversed

HELP = {
    'or': '''		if (!strnicmp(argv[i], "help", 2) || !strnicmp(argv[i], "-?", 2) || !strnicmp(argv[i], "/?", 2))
			client_usage(0, NULL);
''',
    'split': '''		if (!strnicmp(argv[i], "help", 2))
			client_usage(0, NULL);
		if (!strnicmp(argv[i], "-?", 2))
			client_usage(0, NULL);
		if (!strnicmp(argv[i], "/?", 2))
			client_usage(0, NULL);
''',
}

BP = {
    'static': '			arg = bpArgs(argc, argv, &i, mode, &start);\n',
    'getargs': '			arg = getArgs(argc, argv, &i, mode, 1, &start, NULL);\n',
    'inline': '''			a = argv[i + 1];
			if (!a || i + 1 == argc || *a == '-')
				client_usage(3, argv[i]);
			start = argv[i + 2];
			if (i + 2 == argc || !start || *start == '-')
				client_usage(4, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[i + 1];
			i += 2;
''',
}
WB = {
    'static': '			arg = wbArgs(argc, argv, &i, mode, &start);\n',
    'getargs': '			arg = getArgs(argc, argv, &i, mode, 1, &start, NULL);\n',
    'inline': '''			a = argv[i + 1];
			if (i + 1 == argc || !a || *a == '-')
				client_usage(3, argv[i]);
			start = argv[i + 2];
			if (!start || i + 2 == argc || *start == '-')
				client_usage(4, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[i + 1];
			i += 2;
''',
}
EB = {
    'static': '			arg = oneArg(argc, argv, &i, mode);\n',
    'getargs': '			arg = getArgs(argc, argv, &i, mode, 1, NULL, NULL);\n',
    'inline': '''			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[i + 1];
			i++;
''',
}
IPA = {
    'plain': '''			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			ip = argv[i + 1];
			i++;
''',
    'getargs': '			ip = getArgs(argc, argv, &i, mode, 0, NULL, NULL);\n',
    'onearg': '			ip = oneArg(argc, argv, &i, 0);\n',
}
SARM = {
    'eq2': '''			if (reboot == 2)
				log_printf(0, "reboot has already been set on command line, ignoring -s\\n");
			else {
				log_printf(0, "setting shutdown on completion\\n");
				reboot = 1;
			}
''',
    'ne2': '''			if (reboot != 2) {
				log_printf(0, "setting shutdown on completion\\n");
				reboot = 1;
			} else
				log_printf(0, "reboot has already been set on command line, ignoring -s\\n");
''',
}


def rw(o, flag, msg, mode):
    k = o[flag[1]] or {'plain': 'plainc'}.get(o['rw'], o['rw'])
    return '''		}} else if (!strnicmp(argv[i], "{flag}", 2)) {{
{body}			log_printf(0, "{msg}\\n", arg);
			mode = {mode};
'''.format(flag=flag, body=arm1(k), msg=msg, mode=mode)


def ec(o, flag, msg, mode):
    return '''		}} else if (!strnicmp(argv[i], "{flag}", 2)) {{
{body}			log_printf(0, "{msg}\\n", arg);
			mode = {mode};
'''.format(flag=flag, body=arm1(o[flag[1]]), msg=msg, mode=mode)


def ipq(o, flag, msg, mode):
    return '''		}} else if (!strnicmp(argv[i], "{flag}", 2)) {{
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				arg = dummy;
			else {{
				arg = argv[i + 1];
				i++;
				log_printf(0, "{msg}\\n", arg);
			}}
			mode = {mode};
'''.format(flag=flag, msg=msg, mode=mode)


def loop(o):
    t = '''	log_set_name("client");
	for (i = 0; i < argc; i++) {
''' + HELP[o['help']] + '''		if (!strnicmp(argv[i], "-noenter", 8)) {
			log_printf(0, "<enter> key on completion suppressed\\n");
			promptEnter = 0;
		} else if (!strnicmp(argv[i], "-reboot", 7)) {
			if (reboot == 1)
				log_printf(0, "shutdown superseded by reboot, ignoring -s in favor of -reboot\\n");
			log_printf(0, "setting reboot on completion\\n");
			reboot = 2;
		} else if (!strnicmp(argv[i], "-bp", 3)) {
''' + BP[o['bp']] + '''			log_printf(0, "setting binary patch file to %s, offset %s\\n", arg, start);
			mode = 11;
		} else if (!strnicmp(argv[i], "-rb", 3)) {
			arg = getArgs(argc, argv, &i, mode, 1, &start, &count);
			log_printf(0, "reading %s blocks to %s, starting block %s\\n", count, arg, start);
			mode = 8;
		} else if (!strnicmp(argv[i], "-wb", 3)) {
''' + WB[o['wb']] + '''			log_printf(0, "writing blocks from %s, starting at block %s\\n", arg, start);
			mode = 9;
		} else if (!strnicmp(argv[i], "-eb", 3)) {
''' + EB[o['eb']] + '''			log_printf(0, "erase block set to %s\\n", arg);
			mode = 10;
		} else if (!strnicmp(argv[i], "-s", 2)) {
''' + SARM[o['s']] + '''		} else if (!strnicmp(argv[i], "-keys", 5)) {
			mode = 3;
			arg = dummy;
		} else if (!strnicmp(argv[i], "-ip", 3)) {
''' + IPA[o['ipa']] + '''			log_printf(0, "setting forced IP to %s\\n", ip);
''' + rw(o, '-r', 'setting read filename to %s', 1) + rw(o, '-w', 'setting write filename to %s', 2) \
        + ec(o, '-e', 'setting avatar/kinect files base path to %s', 4) \
        + ec(o, '-c', 'setting xbox compatibility files base path to %s', 5) \
        + ipq(o, '-i', 'info dump path set to %s', 12) + ipq(o, '-p', 'patch file set to %s', 7) + '''		} else if (!strnicmp(argv[i], "-v", 2))
			log_verbose_flag(argv[i][2]);
		else
			client_usage(1, argv[i]);
	}
'''
    return t


# ---- after the loop ------------------------------------------------------------------
axis('test', 'inv', 'pos')                     # if (!(mode && arg)) reboot-only else switch / the reverse
axis('fail', 'goto', 'dup', 'ret0')            # connect failure: shared label / log + return in both
axis('end', 'plain', 'both')                   # if (reboot) netReboot; netDisconnect / disconnect in both arms
axis('erase', 'call', 'macro')                 # case 10: clientEraseBlock(arg)

CASES = '''			switch (mode) {
			case 1:
				netDumpNand(arg);
				break;
			case 2:
				clientWrite(arg);
				break;
			case 3:
				clientKeys();
				break;
			case 4:
				if (cinfo->hwFlags & 0x20)
					sendAvatarData(arg, cinfo->kernel);
				else
					log_printf(0, "\\n\\n***** ERROR: cannot send avatar data when a HDD does not exist!\\n");
				break;
			case 5:
				if (cinfo->hwFlags & 0x20)
					sendCompatData(arg);
				else
					log_printf(0, "\\n\\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\\n");
				break;
			case 6:
				break;
			case 7:
				if (arg == dummy)
					clientPatches(NULL);
				else
					clientPatches(arg);
				break;
			case 8:
				clientReadBlocks(arg, start, count);
				break;
			case 9:
				clientWriteBlocks(arg, start);
				break;
			case 10:
				clientEraseBlock(arg);
				break;
			case 11:
				clientBinPatch(arg, start);
				break;
			case 12:
				if (arg == dummy)
					clientInfo(NULL);
				else
					clientInfo(arg);
				break;
			default:
				log_printf(0, "\\n\\n***** ERROR: invalid mode specified, please inform author\\n");
				break;
			}
'''
FAILMSG = 'log_printf(0, "\\n\\n***** ERROR: unable to connect to xbox server\\n");'


axis('conn', 'two', 'one', 'gen', 'six')              # a connect per path / one connect, the switch guarded again / tail_gen
# conn=gen: two connects, every knob separate (wip/mc/gen2.py's, with the two paths' failure
# forms apart and nothing hinted)
axis('pre', '0', '1')                          # 1: `if (!(mode && arg) && !reboot) client_usage(2, NULL);` first
axis('tst', 'a', 'n', 'o', 'm')                # if (mode && arg) S else R / if (!(mode && arg)) R else S / if (!mode || !arg) R else S / nested ifs
axis('fs', 'g', 'G', 'r', 'R', 'e', 'E')       # switch path's failure (see connect())
axis('fr', 'g', 'G', 'r', 'R', 'e', 'E')       # reboot path's failure
axis('tl', 'c', 'd', 'D')                      # ending: common / in both arms / in both arms with return 0
axis('fl', 'end', 'ret')                       # fail label: after the common return / before it (falls into return)


def connect(kind, ok):
    """the connect and its failure: g `if (c) {ok} else goto fail`, G `if (!c) goto fail; ok`,
    r `if (!c) { log; return 0; } ok`, R `if (c) {ok} else { log; return 0; }`,
    e `if (c) {ok} else log` (the path's ending must be in ok), E `if (!c) log; else {ok}`"""
    c = 'netConnect(ip)'
    if kind == 'g':
        return 'if (%s) {\n%s} else\ngoto fail;\n' % (c, ok)
    if kind == 'G':
        return 'if (!%s)\ngoto fail;\n%s' % (c, ok)
    if kind == 'r':
        return 'if (!%s) {\n%s\nreturn 0;\n}\n%s' % (c, FAILMSG, ok)
    if kind == 'R':
        return 'if (%s) {\n%s} else {\n%s\nreturn 0;\n}\n' % (c, ok, FAILMSG)
    if kind == 'e':
        return 'if (%s) {\n%s} else\n%s\n' % (c, ok, FAILMSG)
    return 'if (!%s)\n%s\nelse {\n%s}\n' % (c, FAILMSG, ok)


def tail_gen(o):
    fs, fr, tl = o['fs'], o['fr'], o['tl']
    if tl == 'c' and (fs in 'eE' or fr in 'eE'):
        return None                             # `else log` needs the ending inside the arm
    s_ok = 'cinfo = netGetInfo();\n' + CASES
    r_ok = 'cinfo = netGetInfo();\n'
    if tl != 'c':
        s_ok += 'if (reboot)\nnetReboot(reboot);\nnetDisconnect();\n'
        r_ok += 'netReboot(reboot);\nnetDisconnect();\n'
        if tl == 'D':
            s_ok += 'return 0;\n'
            r_ok += 'return 0;\n'
    S = connect(fs, s_ok)
    R = connect(fr, r_ok)
    t = ''
    if o['pre'] == '1':
        t += 'if (!(mode && arg) && !reboot)\nclient_usage(2, NULL);\n'
        rfull = R
    else:
        rfull = 'if (reboot) {\n' + R + '} else\nclient_usage(2, NULL);\n'
    k = o['tst']
    if k == 'a':
        if o['pre'] == '0':
            t += 'if (mode && arg) {\n' + S + '} else ' + rfull
        else:
            t += 'if (mode && arg) {\n' + S + '} else {\n' + rfull + '}\n'
    elif k == 'n':
        t += 'if (!(mode && arg)) {\n' + rfull + '} else {\n' + S + '}\n'
    elif k == 'o':
        t += 'if (!mode || !arg) {\n' + rfull + '} else {\n' + S + '}\n'
    else:
        return None
    gl = 'g' in (fs + fr).lower()
    if gl and o['fl'] == 'ret':
        # the common code jumps over the fail block to the return
        if tl == 'c':
            t += 'if (reboot)\nnetReboot(reboot);\nnetDisconnect();\ngoto out;\n'
        elif tl == 'd':
            t += 'goto out;\n'
        t += 'fail:\n' + FAILMSG + '\nout:\nreturn 0;\n'
        return t
    if tl == 'c':
        t += 'if (reboot)\nnetReboot(reboot);\nnetDisconnect();\n'
    t += 'return 0;\n'
    if gl:
        t += 'fail:\n' + FAILMSG + '\nreturn 0;\n'
    return t
axis('guard', 'ifelse', 'early', 'earlyor')    # conn=one: if (run) {..} else usage / usage first
axis('inner', 'modearg', 'mode', 'arg', 'none')  # conn=one: the switch's guard after the connect
axis('cfail', 'else', 'not', 'notret')         # conn=one: if (ok) {..} else log / if (!ok) log else {..} / if (!ok) { log; return 0; }


def tail_one(o):
    g = {'modearg': 'if (mode && arg) {\n', 'mode': 'if (mode) {\n', 'arg': 'if (arg) {\n', 'none': '{\n'}[o['inner']]
    body = 'cinfo = netGetInfo();\n' + g + CASES + '}\n'
    if o['end'] == 'plain':
        body += 'if (reboot)\nnetReboot(reboot);\nnetDisconnect();\n'
    else:
        body += 'if (reboot) {\nnetReboot(reboot);\nnetDisconnect();\n} else\nnetDisconnect();\n'
    if o['cfail'] == 'else':
        c = 'if (netConnect(ip)) {\n' + body + '} else\n' + FAILMSG + '\n'
    elif o['cfail'] == 'not':
        c = 'if (!netConnect(ip))\n' + FAILMSG + '\nelse {\n' + body + '}\n'
    else:
        c = 'if (!netConnect(ip)) {\n' + FAILMSG + '\nreturn 0;\n}\n' + body
    if o['guard'] == 'ifelse':
        if o['test'] == 'inv':
            t = 'if (!((mode && arg) || reboot))\nclient_usage(2, NULL);\nelse {\n' + c + '}\n'
        else:
            t = 'if ((mode && arg) || reboot) {\n' + c + '} else\nclient_usage(2, NULL);\n'
    elif o['guard'] == 'early':
        t = 'if (!(mode && arg) && !reboot)\nclient_usage(2, NULL);\n' + c
    else:
        t = 'if ((!mode || !arg) && !reboot)\nclient_usage(2, NULL);\n' + c
    return t + 'return 0;\n'


axis('six', 'ifelse', 'usage1', 'pos', 'early', 'elseif')   # conn=six: how the reboot-only path gets mode 6


def tail_six(o):
    """one connect; with nothing to do but a reboot the mode is set to 6, the switch's
    empty case (`case 6: break;` is in the jump table and nothing else sets it)"""
    body = 'cinfo = netGetInfo();\n' + CASES
    if o['end'] == 'plain':
        body += 'if (reboot)\nnetReboot(reboot);\nnetDisconnect();\n'
    else:
        body += 'if (reboot) {\nnetReboot(reboot);\nnetDisconnect();\n} else\nnetDisconnect();\n'
    if o['cfail'] == 'else':
        c = 'if (netConnect(ip)) {\n' + body + '} else\n' + FAILMSG + '\n'
    elif o['cfail'] == 'not':
        c = 'if (!netConnect(ip))\n' + FAILMSG + '\nelse {\n' + body + '}\n'
    else:
        c = 'if (!netConnect(ip)) {\n' + FAILMSG + '\nreturn 0;\n}\n' + body
    cond = {'inv': '!(mode && arg)', 'pos': '!mode || !arg'}[o['test']]
    s = o['six']
    if s == 'ifelse':
        g = 'if (%s) {\nif (reboot)\nmode = 6;\nelse\nclient_usage(2, NULL);\n}\n' % cond
    elif s == 'usage1':
        g = 'if (%s) {\nif (!reboot)\nclient_usage(2, NULL);\nmode = 6;\n}\n' % cond
    elif s == 'pos':
        g = 'if (mode && arg) {\n} else if (reboot)\nmode = 6;\nelse\nclient_usage(2, NULL);\n'
    elif s == 'early':
        g = 'if (%s) {\nif (!reboot)\nclient_usage(2, NULL);\n}\nif (%s)\nmode = 6;\n' % (cond, cond)
    else:
        g = 'if (!mode || !arg) {\nif (!reboot)\nclient_usage(2, NULL);\nelse\nmode = 6;\n}\n'
    return g + c + 'return 0;\n'


def tail(o):
    if o['conn'] == 'one':
        return tail_one(o)
    if o['conn'] == 'six':
        return tail_six(o)
    if o['conn'] == 'gen':
        return tail_gen(o)
    f = o['fail']
    if f == 'goto':
        fl = '\t\t\tgoto fail;\n'
    else:
        fl = '\t\t\t' + FAILMSG + '\n\t\t\treturn 0;\n\t\t}\n'
    sw = '		if (netConnect(ip)) {\n			cinfo = netGetInfo();\n' + CASES
    sw += ('		} else\n' + fl) if f == 'goto' else ('		} else {\n' + fl)
    rb = '		if (netConnect(ip))\n			cinfo = netGetInfo();\n'
    rb += ('		else\n' + fl) if f == 'goto' else ('		else {\n' + fl)
    if o['test'] == 'inv':
        t = '	if (!(mode && arg)) {\n		if (reboot) {\n' + rb.replace('\n\t', '\n\t\t').replace('\t\tif', '\t\t\tif', 1) \
            + '		} else\n			client_usage(2, NULL);\n	} else {\n' + sw + '	}\n'
    else:
        t = '	if (mode && arg) {\n' + sw + '	} else if (reboot) {\n' + rb + '	} else\n		client_usage(2, NULL);\n'
    if o['end'] == 'plain':
        t += '	if (reboot)\n		netReboot(reboot);\n	netDisconnect();\n	return 0;\n'
    else:
        t += '	if (reboot) {\n		netReboot(reboot);\n		netDisconnect();\n	} else\n		netDisconnect();\n	return 0;\n'
    if f == 'goto':
        t += 'fail:\n	' + FAILMSG + '\n	return 0;\n'
    return t


# ---- helper spellings ----------------------------------------------------------------
# a two-argument helper as six letters: style i (i, j = i + 1) / f (getArgs': first, i);
# first test n (`!a || j == argc`) / c (`j == argc || !a`); advance p (`j++; b = argv[j];`) /
# b (`b = argv[i + 2]; j = i + 2;`) / j (`j = i + 2; b = argv[j];`); second test n / c;
# `*arg2 = b` b before / a after the mode test; return r `argv[i + 1]` / a `a`
def two_specs():
    out = []
    for st in 'ifxy':
        for t1 in 'nc':
            for adv in ('pbj' if st == 'i' else 'p'):
                for t2 in 'nc':
                    for s in 'ba':
                        for r in ('ra' if st in 'ix' else 'r'):
                            out.append(st + t1 + adv + t2 + s + r)
    return out


def two_helper(name, spec):
    st, t1, adv, t2, s, r = spec
    if st in 'xy':
        # no j: x through `a` / `b` (ifcombine merges the two simple tests, and the order
        # they come out in follows the SSA names it is handed), y everything spelled out
        A, B = ('a', 'b') if st == 'x' else ('argv[i + 1]', 'argv[i + 2]')
        T1 = {'n': "!%s || i + 1 == argc || *%s == '-'" % (A, A), 'c': "i + 1 == argc || !%s || *%s == '-'" % (A, A)}[t1]
        T2 = {'n': "!%s || i + 2 == argc || *%s == '-'" % (B, B), 'c': "i + 2 == argc || !%s || *%s == '-'" % (B, B)}[t2]
        t = 'static char *%s(int argc, char **argv, int *pi, int mode, char **arg2)\n{\n	int i = *pi;\n' % name
        if st == 'x':
            t += '	char *a = argv[i + 1], *b;\n'
        t += '\n	if (%s)\n		client_usage(3, argv[i]);\n' % T1
        if st == 'x':
            t += '	b = argv[i + 2];\n'
        t += '	if (%s)\n		client_usage(4, argv[i]);\n' % T2
        if s == 'b':
            t += '	*arg2 = %s;\n' % B
        t += '	if (mode)\n		client_usage(5, argv[i]);\n'
        if s == 'a':
            t += '	*arg2 = %s;\n' % B
        t += '	*pi = i + 2;\n	return %s;\n}\n\n' % {'r': 'argv[i + 1]', 'a': 'a'}[r]
        return t
    if st == 'i':
        T1 = {'n': "!a || j == argc || *a == '-'", 'c': "j == argc || !a || *a == '-'"}[t1]
        ADV = {'p': '	j++;\n	b = argv[j];\n', 'b': '	b = argv[i + 2];\n	j = i + 2;\n', 'j': '	j = i + 2;\n	b = argv[j];\n'}[adv]
        T2 = {'n': "!b || j == argc || *b == '-'", 'c': "j == argc || !b || *b == '-'"}[t2]
        t = '''static char *%s(int argc, char **argv, int *pi, int mode, char **arg2)
{
	int i = *pi;
	int j = i + 1;
	char *a = argv[j], *b;

	if (%s)
		client_usage(3, argv[i]);
%s	if (%s)
		client_usage(4, argv[i]);
''' % (name, T1, ADV, T2)
        if s == 'b':
            t += '	*arg2 = b;\n'
        t += '	if (mode)\n		client_usage(5, argv[i]);\n'
        if s == 'a':
            t += '	*arg2 = b;\n'
        t += '	*pi = j;\n	return %s;\n}\n\n' % {'r': 'argv[i + 1]', 'a': 'a'}[r]
        return t
    T1 = {'n': "!a || i == argc || *a == '-'", 'c': "i == argc || !a || *a == '-'"}[t1]
    T2 = {'n': "!a || i == argc || *a == '-'", 'c': "i == argc || !a || *a == '-'"}[t2]
    t = '''static char *%s(int argc, char **argv, int *pi, int mode, char **arg2)
{
	int first = *pi + 1;
	int i = first;
	char *a = argv[i];

	if (%s)
		client_usage(3, argv[first - 1]);
	i++;
	a = argv[i];
	if (%s)
		client_usage(4, argv[first - 1]);
''' % (name, T1, T2)
    if s == 'b':
        t += '	*arg2 = a;\n'
    t += '	if (mode)\n		client_usage(5, argv[first - 1]);\n'
    if s == 'a':
        t += '	*arg2 = a;\n'
    t += '	*pi = i;\n	return argv[first];\n}\n\n'
    return t


# a one-argument helper as three letters: style i (argv[i + 1] spelled out) / a (`a` temp) /
# f (getArgs': first); test n / c; return r `argv[i + 1]` / a `a`
def one_specs():
    return [st + t + r for st in 'iafj' for t in 'nc' for r in ('ra' if st in 'aj' else 'r')]


def one_helper(name, spec):
    st, t1, r = spec
    if st == 'j':                               # bpArgs' / wbArgs' way: j = i + 1, a = argv[j]
        T = {'n': "!a || j == argc || *a == '-'", 'c': "j == argc || !a || *a == '-'"}[t1]
        return '''static char *%s(int argc, char **argv, int *pi, int mode)
{
	int i = *pi;
	int j = i + 1;
	char *a = argv[j];

	if (%s)
		client_usage(3, argv[i]);
	if (mode)
		client_usage(5, argv[i]);
	*pi = j;
	return %s;
}

''' % (name, T, {'r': 'argv[i + 1]', 'a': 'a'}[r])
    if st == 'f':
        T = {'n': "!a || i == argc || *a == '-'", 'c': "i == argc || !a || *a == '-'"}[t1]
        return '''static char *%s(int argc, char **argv, int *pi, int mode)
{
	int i = *pi + 1;
	char *a = argv[i];

	if (%s)
		client_usage(3, argv[i - 1]);
	if (mode)
		client_usage(5, argv[i - 1]);
	*pi = i;
	return argv[i];
}

''' % (name, T)
    if st == 'a':
        T = {'n': "!a || i + 1 == argc || *a == '-'", 'c': "i + 1 == argc || !a || *a == '-'"}[t1]
        d = '	int i = *pi;\n	char *a = argv[i + 1];\n'
    else:
        T = {'n': "!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-'", 'c': "i + 1 == argc || !argv[i + 1] || *argv[i + 1] == '-'"}[t1]
        d = '	int i = *pi;\n'
    return '''static char *%s(int argc, char **argv, int *pi, int mode)
{
%s
	if (%s)
		client_usage(3, argv[i]);
	if (mode)
		client_usage(5, argv[i]);
	*pi = i + 1;
	return %s;
}

''' % (name, d, T, {'r': 'argv[i + 1]', 'a': 'a'}[r])


axis('bps', 'inbcbr', *[x for x in two_specs() if x != 'inbcbr'])   # bpArgs' spelling (first = today's)
axis('wbs', 'icpnbr', *[x for x in two_specs() if x != 'icpnbr'])   # wbArgs'
axis('two', 'sep', 'shared', 'sharedw')        # bpArgs and wbArgs / both arms call bpArgs (bps) / wbArgs (wbs)
axis('o1', 'inr', *[x for x in one_specs() if x != 'inr'])          # oneArg's spelling
axis('o2', '', *one_specs())                   # oneArgC's ('' = the onec axis' text)
axis('ho', 'bwo', 'bow', 'wbo', 'wob', 'obw', 'owb')   # order of the helpers' definitions (b, w, one-arg)


def build(o):
    o = dict({k: v[0] for k, v in AXES.items()}, **o)
    tl = tail(o)
    if tl is None:
        return None
    t = HEAD + GETARGS
    lp = loop(o)
    if o['two'] == 'shared':
        lp = lp.replace('wbArgs(', 'bpArgs(')
    elif o['two'] == 'sharedw':
        lp = lp.replace('bpArgs(', 'wbArgs(')
    hb = hw = ho = ''
    if 'bpArgs(' in lp:
        hb = '/* -bp <f> <o> */\n' + two_helper('bpArgs', o['bps'])
    if 'wbArgs(' in lp:
        hw = '/* -wb <f> <b> */\n' + two_helper('wbArgs', o['wbs'])
    if 'oneArg(' in lp:
        ho += '/* -eb <b> */\n' + one_helper('oneArg', o['o1'])
    if 'oneArgC(' in lp:
        ho += one_helper('oneArgC', o['o2']) if o['o2'] else ONEC[o['onec']]
    t += ''.join({'b': hb, 'w': hw, 'o': ho}[k] for k in o['ho'])
    t += '''int mode_client(int argc, char **argv)
{
	char dummy[] = "dummy";
	char *start = NULL, *count = NULL;
	int i = 0;
	int reboot = 0;
	char *ip = NULL;
	char *arg = NULL;
	int mode = 0;
''' + ('	char *a;\n' if ('a = argv' in lp) else '') + ('	int j;\n' if ('j = i + 1' in lp) else '') + '\n' + lp + tl + '}\n\n' + TAILPAD
    return t


def parse(v):
    if v == 'src':
        return None
    o = {}
    if v not in ('nat', ''):
        for kv in v.split(','):
            k, x = kv.split('=')
            assert k in AXES and x in AXES[k], kv
            o[k] = x
    return o


def text_of(v):
    if v == 'old':
        return SRC
    o = parse(v)
    return L.read_src(L.SRC) if o is None else build(o)


if __name__ == '__main__':
    a = sys.argv[1:]
    out = None
    if '-o' in a:
        k = a.index('-o'); out = a[k + 1]; del a[k:k + 2]
    lay = '-l' in a
    if lay:
        a.remove('-l')
    dmp = '-d' in a
    if dmp:
        a.remove('-d')
    vfn = None
    if '-v' in a:
        k = a.index('-v')
        vfn = a[k + 1] if k + 1 < len(a) and a[k + 1].startswith('_') else ''
        del a[k:k + (2 if vfn else 1)]
    if out or lay or dmp or vfn is not None:
        for v in a:
            t = text_of(v)
            if out:
                open(out, 'w', newline='\n').write(t)
            if dmp:
                print(L.dump(t, re.sub(r'[^\w]+', '_', v)))
            if vfn is not None:
                L.vdiff(t, vfn or None)
            if lay:
                ok, ob, d = L.compile_src(t)
                if not ok:
                    print('COMPILE ERROR', ob)
                else:
                    idn, tot, per, notes = L.report(ob)
                    m = L.laydiff(ob)
                    print(L.fmt({'identical': idn, 'total': tot, 'per': per, 'notes': notes}), 'moved=%d' % m)
                L.cleanup(d)
        sys.exit()
    with ThreadPoolExecutor(6) as ex:
        for v, s in zip(a, ex.map(lambda v: L.fmt(L.score_text(text_of(v), lay=True)), a)):
            print('%-50s %s' % (v, s), flush=True)
