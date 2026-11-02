import sys,os,re,subprocess
D=os.path.dirname(os.path.abspath(__file__))
def kv(t):
    o=subprocess.run([sys.executable,os.path.join(D,'..','s61','rk.py'),t,'2'],capture_output=True,text=True).stdout
    for l in o.splitlines():
        if re.match(r'^110[58] ',l): return re.findall(r"'ins', '(\w+)', (\d+), (-\d+)",l)
print(' '.join('%s:%s'%(b,k) for _,b,k in kv(sys.argv[1])))
