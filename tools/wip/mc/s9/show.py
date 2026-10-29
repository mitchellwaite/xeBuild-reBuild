"""python show.py '<json params>' : run one design (slot show), print fncmp, keys, diff calls"""
import sys, json, subprocess
sys.argv = [sys.argv[0], '0'] + sys.argv[1:]
exec(open(r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s9\search.py').read().replace('\nmain()\n', '\n'))
x = json.loads(sys.argv[2]) if len(sys.argv) > 2 else json.load(open(LOG + '.best'))
print('fncmp', run('show', x))
print(subprocess.run([sys.executable, ROOT + r'\tools\wip\mc\s9\k.py', ROOT + r'\build\mcsp\slotshow'], capture_output=True, text=True).stdout.replace('log:', '').replace('strnicmp:', ''))
