"""Attempt 29: compile parseButtonX bodies inside src/options.c and compare with the reference.

CF=0|1 python tools/wip/dehint/op29run.py tools/wip/dehint/op29gen.py [name-substr] [-v name] [-o name out.c]
The variants file defines V = {name: body of parseButtonX}; each is scored at plain -O3."""
import os, re, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
sys.path.insert(0, os.path.join(R, 'tools', 'wip', 'dehint'))
import optlib
from concurrent.futures import ThreadPoolExecutor

src = optlib.read_src(optlib.SRC)
a = src.index('static int parseButtonX(const char *s)\n{')
b = src.index('\n}\n', a)
HEAD = 'static int parseButtonX(const char *s)\n{\n'


def make(body):
    return src[:a] + HEAD + body.strip('\n') + src[b:]


def main():
    args = sys.argv[1:]
    ns = {}
    exec(open(args[0]).read(), ns)
    V = ns['V']
    if '-o' in args:
        i = args.index('-o')
        open(args[i + 2], 'w', newline='\n').write(make(V[args[i + 1]]))
        return
    if '-v' in args:
        optlib.vdiff(make(V[args[args.index('-v') + 1]]), [])
        return
    sel = [n for n in V if len(args) < 2 or args[1] in n]

    def one(n):
        return n, optlib.fmt(optlib.score_text(make(V[n]), []))
    with ThreadPoolExecutor(6) as ex:
        for n, r in ex.map(one, sel):
            print('%-28s %s' % (n, r[:150]))


if __name__ == '__main__':
    main()
