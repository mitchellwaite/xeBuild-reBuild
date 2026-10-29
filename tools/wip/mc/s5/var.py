"""5th session: apply a source change to the mode_client draft and fncmp it.
usage: python tools/wip/mc/s5/var.py NAME [extra gcc flags]
Prints the number of +/- lines of fncmp (72 = the draft), or MATCH."""
import subprocess, sys

SRC = 'tools/wip/mode_client.c'
src = open(SRC).read()
MA = r'log_printf(0, "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n");'
MC = r'log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n");'
T = '\t\t\t'
A4 = (T + 'case 4:\n' + T + '\tif (cinfo->hwFlags & 0x20)\n' + T + '\t\tsendAvatarData(arg, cinfo->kernel);\n'
      + T + '\telse\n' + T + '\t\t' + MA + '\n' + T + '\tbreak;\n'
      + T + 'case 5:\n' + T + '\tif (cinfo->hwFlags & 0x20)\n' + T + '\t\tsendCompatData(arg);\n'
      + T + '\telse\n' + T + '\t\t' + MC + '\n' + T + '\tbreak;\n')
assert A4 in src
C6 = T + 'case 6:\n' + T + '\tbreak;\n'
assert C6 in src

VARS = {**{n: A4 for n in sys.argv[1].split('+') if ':' in n}, 'dowhile': A4, 'while': A4, 'u2goto': A4, 'argfirst': A4, 'u2ret': A4,
    # both HDD cases share one hwFlags test (error blocks: one pred block)
    'shared': (T + 'case 4:\n' + T + 'case 5:\n'
               'if (!(cinfo->hwFlags & 0x20)) { if (mode == 4) ' + MA + ' else ' + MC + ' }'
               ' else if (mode == 4) sendAvatarData(arg, cinfo->kernel); else sendCompatData(arg);\nbreak;\n'),
    'inv': (T + 'case 4:\nif (!(cinfo->hwFlags & 0x20)) ' + MA + ' else sendAvatarData(arg, cinfo->kernel);\nbreak;\n'
            'case 5:\nif (!(cinfo->hwFlags & 0x20)) ' + MC + ' else sendCompatData(arg);\nbreak;\n'),
    # HDD check before the switch: the error blocks hang off a 2-way test
    'pre': ('case 4: sendAvatarData(arg, cinfo->kernel); break;\ncase 5: sendCompatData(arg); break;\n'),
    'nohdd6': A4,
    # a goto-shared error path (second predecessor)
    'gotoerr': (T + 'case 4:\nif (cinfo->hwFlags & 0x20) sendAvatarData(arg, cinfo->kernel); else goto noA;\nbreak;\n'
                'case 5:\nif (cinfo->hwFlags & 0x20) sendCompatData(arg); else goto noC;\nbreak;\n'),
}
name = sys.argv[1]; names = name.split('+')
body = src
for n in names: body = body.replace(A4, VARS[n])
if 'nohdd6' in names:
    body = body.replace(C6, '')
if 'pre' in names:
    body = body.replace('\t\t\tcinfo = netGetInfo();\n\t\t\tswitch (mode) {',
        '\t\t\tcinfo = netGetInfo();\n\t\t\tif ((mode == 4 || mode == 5) && !(cinfo->hwFlags & 0x20)) {'
        ' if (mode == 4) ' + MA + ' else ' + MC + ' } else\n\t\t\tswitch (mode) {')
if 'gotoerr' in names:
    body = body.replace('\t\t\t\tlog_printf(0, "\\n\\n***** ERROR: invalid mode',
        '\t\t\t\tif (0) { noA: ' + MA + ' break; noC: ' + MC + ' break; }\n\t\t\t\tlog_printf(0, "\\n\\n***** ERROR: invalid mode')
LOOP = '\tfor (i = 0; i < argc; i++) {\n'
LEND = '\t\t\tclient_usage(1, argv[i]);\n\t}\n'
assert LOOP in src and LEND in src
if 'dowhile' in names:      # guarded do-while: the entry test is a separate block
    body = body.replace(LOOP, '\tif (argc > 0) do {\n').replace(LEND, '\t\t\tclient_usage(1, argv[i]);\n\t} while (++i < argc);\n')
for n in names:            # dw:<guard>: do-while under an arbitrary guard
    if n.startswith('dw:'):
        body = body.replace(LOOP, '\tif (%s) do {\n' % n[3:]).replace(LEND, '\t\t\tclient_usage(1, argv[i]);\n\t} while (++i < argc);\n')
    if n.startswith('dwe:'):   # the same, guard written as an expect
        body = body.replace(LOOP, '\tif (__builtin_expect(%s, %s)) do {\n' % tuple(n[4:].split('@'))).replace(LEND, '\t\t\tclient_usage(1, argv[i]);\n\t} while (++i < argc);\n')
if 'while' in names:
    body = body.replace(LOOP, '\twhile (i < argc) {\n').replace(LEND, '\t\t\tclient_usage(1, argv[i]);\n\t\ti++;\n\t}\n')
if 'u2goto' in names:       # usage(2) reached by goto from a second place
    body = body.replace('\t\t} else\n\t\t\tclient_usage(2, NULL);\n', '\t\t} else\n\t\t\tgoto u2;\n')
    body = body.replace('\tif (E(reboot))\n', '\tif (0) {\nu2:\n\t\tclient_usage(2, NULL);\n\t}\n\tif (E(reboot))\n')
if 'argfirst' in names:     # test arg before mode
    body = body.replace('if (!(mode && arg))', 'if (!(arg && mode))')
if 'u2ret' in names:        # usage(2) then return (non-noreturn path shape)
    body = body.replace('\t\t\tclient_usage(2, NULL);\n\t} else {', '\t\t{ client_usage(2, NULL); return 0; }\n\t} else {')
out = 'tools/wip/mc/s5/v_%s.c' % name
open(out, 'w', newline='\n').write(body)
r = subprocess.run([sys.executable, 'tools/re/fncmp.py', out, 'mode_client', '-O3',
                    '--param', 'builtin-expect-probability=50'] + sys.argv[2:], capture_output=True, text=True)
d = [l for l in r.stdout.splitlines() if l[:1] in '+-']
print(name, 'MATCH' if 'MATCH' in r.stdout[:40] else len(d), r.stderr.strip()[:300])
