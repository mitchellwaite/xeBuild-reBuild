"""Generate mode_client tail variants from the draft and score them with wip/mc/mcvar.py.
python tailvar.py [names...]      (variants are written next to this script as tv_<name>.c)"""
import os, re, sys
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(ROOT, 'wip', 'mc'))
import mcvar
SP = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(ROOT, 'wip', 'app', 'mode_client.c')).read()
head, tail = src.split('\tif (!(mode && arg)) {\n', 1)
# the "unable to connect" log statement, taken verbatim from the draft (avoids escape trouble)
UNABLE = [l for l in src.split('\n') if 'unable to connect' in l][0].strip()
SWITCH = tail[tail.index('\t\t\tswitch (mode) {'):tail.index('\t\t\t}\n\t\t} else\n\t\t\tgoto fail;') + 5]


def sw(indent):
    out = []
    for l in SWITCH.split('\n'):
        out.append(indent + l[3:] if l.startswith('\t\t\t') else l)
    return '\n'.join(out)


V = {}
V['draft'] = '\tif (!(mode && arg)) {\n' + tail
V['nohint'] = V['draft'].replace('\t\t\trok: __attribute__((cold));\n', '').replace(
    'fail: __attribute__((cold));', 'fail:').replace('if (E(reboot))', 'if (reboot)')
V['single'] = '''	if (!(mode && arg) && !reboot)
		client_usage(2, NULL);
	if (netConnect(ip)) {
		cinfo = netGetInfo();
		if (mode && arg) {
%s
		}
		if (reboot)
			netReboot(reboot);
		netDisconnect();
	} else
		%s
	return 0;
}
''' % (sw('\t\t\t'), UNABLE)
V['dup'] = '''	if (mode && arg) {
		if (netConnect(ip)) {
			cinfo = netGetInfo();
%s
			if (reboot)
				netReboot(reboot);
			netDisconnect();
		} else
			%s
	} else if (reboot) {
		if (netConnect(ip)) {
			cinfo = netGetInfo();
			netReboot(reboot);
			netDisconnect();
		} else
			%s
	} else
		client_usage(2, NULL);
	return 0;
}
''' % (sw('\t\t\t'), UNABLE, UNABLE)
V['gotofail'] = '''	if (mode && arg) {
		if (netConnect(ip)) {
			cinfo = netGetInfo();
%s
		} else
			goto fail;
	} else if (reboot) {
		if (netConnect(ip))
			cinfo = netGetInfo();
		else
			goto fail;
	} else
		client_usage(2, NULL);
	if (reboot)
		netReboot(reboot);
	netDisconnect();
	return 0;
fail:
	%s
	return 0;
}
''' % (sw('\t\t\t'), UNABLE)
V['dupret'] = '''	if (mode && arg) {
		if (!netConnect(ip)) {
			%s
			return 0;
		}
		cinfo = netGetInfo();
%s
	} else if (reboot) {
		if (!netConnect(ip)) {
			%s
			return 0;
		}
		cinfo = netGetInfo();
	} else
		client_usage(2, NULL);
	if (reboot)
		netReboot(reboot);
	netDisconnect();
	return 0;
}
''' % (UNABLE, sw('\t\t'), UNABLE)
# single connect, usage check first, no retest of arg (mode alone)
V['single2'] = '''	if (!(mode && arg) && !reboot)
		client_usage(2, NULL);
	if (!netConnect(ip)) {
		%s
		return 0;
	}
	cinfo = netGetInfo();
	if (mode && arg) {
%s
	}
	if (reboot)
		netReboot(reboot);
	netDisconnect();
	return 0;
}
''' % (UNABLE, sw('\t\t'))

for n in list(V):
    # the HDD test as an equality with the mask (EQ with a nonzero constant is predicted false)
    V[n + '_eq'] = V[n].replace('if (cinfo->hwFlags & 0x20)', 'if ((cinfo->hwFlags & 0x20) == 0x20)')

# head transforms: alternative spellings of functions inlined into mode_client
ERASE_OLD = head[head.index('void clientEraseBlock(const char *sblock)\n{'):]
ERASE_OLD = ERASE_OLD[:ERASE_OLD.index('\n}\n') + 3]
ERASE_LINES = [l.strip() for l in ERASE_OLD.split('\n') if 'log_printf' in l]   # erasing, Success, Failed, Block, Invalid
ERASE_ER = '''void clientEraseBlock(const char *sblock)
{
	u32 block = myatoh32(sblock, -1);

	if (block == -1) {
		%s
		return;
	}
	if (block >= cinfo->nandSize / cinfo->blockSize) {
		%s
		return;
	}
	%s
	if (netEraseBlock(block, 1))
		%s
	else
		%s
}
''' % (ERASE_LINES[4], ERASE_LINES[3], ERASE_LINES[0], ERASE_LINES[1], ERASE_LINES[2])
HEADS = {'': head, '_er': head.replace(ERASE_OLD, ERASE_ER)}
assert HEADS['_er'] != head

if __name__ == '__main__':
    names = sys.argv[1:] or list(V)
    flags = os.environ.get('FLAGS', '-O3 --param builtin-expect-probability=50').split()
    for n in names:
        tv, _, hk = n.partition('+')          # <tail variant>[+<head key>], e.g. draft+er
        p = os.path.join(SP, 'var', 'tv_%s.c' % n.replace('+', '_')); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', newline='\n').write(HEADS['_' + hk if hk else ''] + V[tv])
        res, err = mcvar.run(p, flags, fncmp=True)
        if res is None:
            print(n, 'ERROR', err[-400:])
            continue
        print('%-10s inv=%2d pre=%2d fncmp=%3d missing=%s  dir=%s' % (n, res['inv'], res['pre'], res['fncmp'], res['missing'], os.path.basename(res['dir'])))
        print('   ', ' '.join(s.replace('strnicmp:', '').replace('log:', '')[:12] for s in res['order']))
