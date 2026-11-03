"""Attempt 6: gen_ca85 G, `for (i = 0; i < manifest.count; i++)` with `i = manifest.count` on failure, is text 0 data 0 with no n, cast, flag or dead test. How much
plainer can what's around it get? Axes: stop x ret init x ret type x decl x prepSysex x tail."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g = load('gen_ca80')
g10 = load('gen_ca10')
M = 'log_printf(0, "ERROR: unable to mount sysex partition!\\n");'
F = 'log_printf(0, "ERROR: unable to format sysex partition!\\n");'
NF = 'netFormatSysex()'
NM = 'netMount(SYSEX, "\\\\SEP")'
C = 'createSysexDirs()'
PREPS = {
    'h9d': g10.HEADS['h9'] + g10.TAIL['d'],
    'h5d': g10.HEADS['h5'] + g10.TAIL['d'],
    'h1d': g10.HEADS['h1'] + g10.TAIL['d'],
    's1': f'if (!{NF}) {{ {F} return 0; }} if (!{NM}) {{ {M} return 0; }} return {C};',
    's2': f'if ({NF}) {{ if ({NM}) return {C}; {M} }} else {F} return 0;',
    's3': f'if (!{NF}) {F} else if (!{NM}) {M} else return {C}; return 0;',
    's4': f'if ({NF}) {{ if (!{NM}) {M} else return {C}; }} else {F} return 0;',
    's5': f'int r = 0; if (!{NF}) {F} else if (!{NM}) {M} else r = {C}; return r;',
    's6': f'int r = 0; if ({NF}) {{ if ({NM}) r = {C}; else {M} }} else {F} return r;',
}
STOPS = {
    'cnt': 'if (!ret) {\n@F@\ni = manifest.count;\n}\n',
    'brk': 'if (!ret) {\n@F@\nbreak;\n}\n',
    'el': 'if (ret == 0) {\n@F@\ni = manifest.count;\n}\n',
}
TAILS = {
    'a1': 'if (ret) {\n' + g.MFS + '\n' + g.ARMS + '}\n',
    'a2': 'if (ret) {\n' + g.MFS + '\nret = netSendFile(manifest.path, manifest.data, manifest.size);\nif (!ret)\nlog_printf(0, "aborting sending avatar data, failed to send %s\\n", manifest.path);\nelse {\nlog_printf(0, "success! Avatar data is successfully sent to the console!\\n");\nnetTimerEnd();\n}\n}\n',
}
RET = ('r0', 'r1')
TYPE = ('long', 'int')
DECL = ('il', 'li')


def variants():
    for st, r, ty, d, p, t in itertools.product(STOPS, RET, TYPE, DECL, PREPS, TAILS):
        loop = 'for (i = 0; i < manifest.count; i++) {\n' + g.LOG.replace('e->', 'manifest.e[i].') + '\n' + g.SEND.replace('e->', 'manifest.e[i].') + '\n' + STOPS[st].replace('@F@', g.FAIL.replace('e->', 'manifest.e[i].')) + '}\n'
        src = g.FRAME.replace('@LOOP@', loop).replace('@TAIL@', TAILS[t])
        init = ' = 1' if r == 'r1' else ''
        decl = ('\tint i;\n\t%s ret%s;\n' if d == 'il' else '\t%s ret%s;\n\tint i;\n') % (ty, init)
        src = src.replace('\tint i;\n\tlong ret;\n\tint n;\n', decl)
        if r == 'r1':
            src = src.replace('\t\tret = 1;\n', '')
        yield '|'.join((st, r, ty, d, p, t)), 'int prepSysex(void)\n{\n' + PREPS[p] + '\n}\n\n' + src
