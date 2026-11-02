import sys,os
sys.path.insert(0,r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s42')
os.environ['BASE']=r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s42\H5b.c'
import lev
s,t,n=map(int,sys.argv[1:4])
open(sys.argv[4],'w',newline='\n').write(lev.make(s,t,n))
