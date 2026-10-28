"""s10 runner: python wip/mc/s10/run.py SLOT design.json  -> fncmp, inv, pre, order sigs."""
import json, os, subprocess, sys
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
FIX = ['mode_client:112>133=0']
FAKE = ['clientEraseBlock:%d>1=100' % i for i in (5, 6, 7, 8)]
NAMES = {'M': 'mode_client:105>107', 'A': 'mode_client:106>107', 'H1': 'mode_client:116>118', 'H2': 'mode_client:119>121',
         'd1': 'mode_client:122>123', 'd2': 'mode_client:129>130', 'e2': 'clientEraseBlock:2>8', 'e3': 'clientEraseBlock:3>7',
         'e4': 'clientEraseBlock:4>6', 'ip': 'mode_client:49>50', 'r': 'mode_client:50>56', 'w': 'mode_client:56>64', 'e': 'mode_client:64>72'}
def run(slot, x):
    ov = ['%s=%.4f' % (NAMES.get(k, k), v) for k, v in x.items()] + FIX + FAKE + ['--consistent', '--entry=clientEraseBlock:mode_client:127']
    env = dict(os.environ, EXTRA='--param builtin-expect-probability=50', MCFDO_DIR=ROOT + r'\build\mcsp')
    r = subprocess.run([sys.executable, ROOT + r'\wip\mc\s9\fdorun9.py', slot, '--over'] + ov, cwd=ROOT, env=env, capture_output=True, text=True)
    f = inv = pre = 999
    for l in r.stdout.splitlines():
        if l.startswith('fncmp'): f = int(l.split()[1])
        if l.startswith('round4'):
            inv = int(l.split()[1].split('=')[1]); pre = int(l.split()[2].split('=')[1])
    return f, inv, pre, r.stdout + r.stderr
if __name__ == '__main__':
    f, inv, pre, o = run(sys.argv[1], json.load(open(sys.argv[2])))
    print(o)
