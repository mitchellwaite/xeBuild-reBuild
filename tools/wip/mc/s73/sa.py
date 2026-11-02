"""s73 sa.py: s71 SA + -wb operand-order lever (`!b || k == argc`, k = i+2 in a block), fixed on."""
import sys,os,runpy,importlib.util as U
D=os.path.dirname(os.path.abspath(__file__))
sp=U.spec_from_file_location('sa71',os.path.join(D,'..','s71','sa.py')); M=U.module_from_spec(sp); sp.loader.exec_module(M)
OLD="""			b = argv[i + 2];
			if (i + 2 == argc || !b || *b == '-')
				client_usage(4, argv[i]);
			start = b;
			if (mode)
				client_usage(5, argv[i]);
			i += 2;"""
NEW="""			{ int k = i + 2; b = argv[k];
			if (!b || k == argc || *b == '-')
				client_usage(4, argv[i]); }
			start = b;
			if (mode)
				client_usage(5, argv[i]);
			i += 2;"""
_t=M.text
def text(st):
    s=_t(st); assert OLD in s; return s.replace(OLD,NEW)
M.text=text
if __name__=='__main__':
    sys.argv[0]=os.path.join(D,'sa.py')
    M.D=D
    src=open(os.path.join(D,'..','s71','sa.py')).read(); main=src[src.index("if __name__=='__main__':"):]
    exec(main.replace("if __name__=='__main__':","if True:"),M.__dict__)
