"""scanD.py JOBS OUT: jobs = [tag, design]; design as in search2."""
import sys, json
from multiprocessing import Pool
import search2 as S
def job(a):
    tag,d=a
    _,sc,info=S.job((tag,d))
    return tag,d,sc,info
if __name__=='__main__':
    jobs=json.load(open(sys.argv[1])); out=open(sys.argv[2],'a')
    with Pool(int(sys.argv[3]) if len(sys.argv)>3 else 3) as p:
        for x in p.imap_unordered(job,jobs): out.write(json.dumps(x)+'\n'); out.flush()
