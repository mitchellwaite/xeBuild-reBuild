"""Attempt 5: gen_ca67 W|z5 is a plain while loop with one exit and only the hoist left (F1). The hoist goes if the forwarders into the
manifest send don't tail-merge in pre, which needs a PHI at the send whose arguments differ then, and fold later. So a 0/1 flag that
carries through to the return with no `ret = 1`: PHI <1 (guard), ok (loop)>, ok != 0 on that edge. Axes: flag and result types x update x stop x tail."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))
s = util.spec_from_file_location('gen_ca64', os.path.join(here, 'gen_ca64.py'))
m64 = util.module_from_spec(s)
s.loader.exec_module(m64)
m = m64.m
g = m.g
MFF, ARMS_OK, MFCALL = m.MFF, m.ARMS_OK, m.MFCALL
OKLOG = r'''log_printf(0, "success! Avatar data is successfully sent to the console!\n");
netTimerEnd();
'''
FRAME = r'''long sendAvatarData(const char *dir, uint32_t ver)
{
	int i, n;
	@TO@ ok;
	@TR@ ret;
@D@
	netTimerStart();
	log_printf(0, "loading avatar data...\n");
	ver &= ~0xf;
	addTitleId(ver);
	if (loadManifest(dir, ver)) {
		log_printf(0, "success!\nFormatting HDD partition...\n");
		ok = 1;
		if (prepSysex()) {
			log_printf(0, "success!\nSending avatar files to HDD partition...\n");
			log_printf(1, "sending %d items to xbox\n", manifest.count);
@LOOP@
@TAIL@
		}
		netUnmount(SYSEX);
		freeManifest();
	} else {
		log_printf(0, "***** WARNING: avatar data skipped, unable to load data!\n");
		ok = 1;
	}
	return ok;
}
'''
UPD = {
    'okr': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret) {\n%(f)s\ni = n;\n}\n',
    'okk': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ok) {\n%(f)s\ni = n;\n}\n',
    'okb': 'ok = ret != 0;\nn = manifest.count;\ni += ret != 0;\nif (!ret) {\n%(f)s\ni = n;\n}\n',
    'n0': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret) {\n%(f)s\nn = 0;\n}\n',
    'Nok': 'n = manifest.count;\nok = ret != 0;\ni += ok;\nif (!ret) {\n%(f)s\ni = n;\n}\n',
    'ifel': 'ok = ret != 0;\nn = manifest.count;\nif (ret)\ni++;\nelse {\n%(f)s\ni = n;\n}\n',
    'ifelk': 'ok = ret != 0;\nn = manifest.count;\nif (ok)\ni++;\nelse {\n%(f)s\ni = n;\n}\n',
}
TAILS = {
    'send': 'if (ok) {\n' + g.MFS + '\nif (!' + MFCALL + ') {\nok = 0;\n' + MFF + '} else {\n' + OKLOG + '}\n}\n',
    'send1': 'if (ok) {\n' + g.MFS + '\nif (' + MFCALL + ') {\n' + OKLOG + '} else {\nok = 0;\n' + MFF + '}\n}\n',
    'sret': 'if (ok) {\n' + g.MFS + '\nret = ' + MFCALL + ';\nif (!ret) {\nok = 0;\n' + MFF + '} else {\n' + OKLOG + '}\n}\n',
    'ok1': 'if (ok) {\n' + g.MFS + '\nif (!' + MFCALL + ') {\nok = 0;\n' + MFF + '} else {\n' + OKLOG + 'ok = 1;\n}\n}\n',
    'okset': 'if (ok) {\n' + g.MFS + '\nok = ' + MFCALL + ' != 0;\nif (!ok)\n' + MFF + 'else {\n' + OKLOG + '}\n}\n',
}
ITEMS = {k: m.ITEMS[k] for k in ('cast', 'k')}


def variants():
    for it, u, t, to, tr in itertools.product(ITEMS, UPD, TAILS, ('long', 'int'), ('long', 'int')):
        v, decl, d = ITEMS[it]
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + UPD[u] % {'f': g.FAIL % v}
        loop = 'i = 0;\nn = manifest.count;\nwhile (i < n) {\n' + body + '}\n'
        src = g.PREP + FRAME.replace('@TO@', to).replace('@TR@', tr).replace('@D@', d).replace('@LOOP@', loop).replace('@TAIL@', TAILS[t])
        yield '|'.join((it, u, t, to, tr)), src
