"""run.py: evaluate gen variants. ev(w,tag,...) -> es2 result dict."""
import sys,os,json
D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D); sys.path.insert(0,os.path.join(D,'..','s53'))
import rkgen as gen,es2
def ev(w,tag,fn=False,**k):
    r=es2.run(gen.mk(w,**k),tag,fn)
    return r
if __name__=='__main__':
    w=json.loads(sys.argv[1]) if len(sys.argv)>1 else {}
    print(ev(w,'s54t',True))
