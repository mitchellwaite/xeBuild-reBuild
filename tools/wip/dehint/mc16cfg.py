"""mode_client attempt 16: pre-bbro CFG (rtl_dce dump with -blocks) of mode_client: for each
listed bb its freq, preds, succs and the first insns' summary (calls, labels).

python tools/wip/dehint/mc16cfg.py A.c BB[,BB...]"""
import os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, mc1lib, mc12keys

t = mc1lib.read_src(sys.argv[1])
want = [int(x) for x in sys.argv[2].split(',')]
d = tempfile.mkdtemp(dir=mc1lib.BUILD, prefix='k')
open(os.path.join(d, 'mode_client.c'), 'w', newline='\n').write('#line 1 "mode_client.c"\n' + t)
subprocess.run([bdlib.GCC, '-c', '-O3', '-fdump-rtl-rtl_dce-blocks', '-I' + os.path.join(bdlib.R, 'src'),
                'mode_client.c', '-o', 'o.o'], cwd=d, capture_output=True)
f = [x for x in os.listdir(d) if x.endswith('rtl_dce')][0]
dce = mc12keys.fn_part(open(os.path.join(d, f)).read())
mc1lib.cleanup(d)
blocks = re.split(r'\n(?=;; basic block \d+,)', dce)
for b in blocks:
    m = re.match(r';; basic block (\d+), loop depth \d+()', b)
    if not m or int(m.group(1)) not in want:
        continue
    pred = re.search(r';;  pred:(.*?)\n(?!;;  +\d)', b, re.S)
    succ = re.search(r';;  succ:(.*?)(\n\n|\Z)', b, re.S)
    calls = re.findall(r'symbol_ref:SI \("(\w+)"\)', b)
    labs = re.findall(r'\(code_label \d+ \d+ \d+ \d+ \d+ \("(\w+)"\)', b)
    asm = 'asm_operands' in b
    print('bb', m.group(1), 'freq', m.group(2), 'labels', labs, 'calls', calls, 'asm' if asm else '')
    print('   pred', ' '.join(pred.group(1).split()) if pred else '')
    print('   succ', ' '.join(succ.group(1).split())[:300] if succ else '')
