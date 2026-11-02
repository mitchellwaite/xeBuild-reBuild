import sys, ev, cm
for p in sys.argv[1:]:
    r = ev.ev(open(p).read(), 'ver_'+p.replace('/','_').replace('.','_'))
    print(p, 'score', r['score'], 'inv', r['tinv'], 'miss', r['tmiss'], 'fncmp', r.get('fncmp'), 'cm', cm.cm(p)); print('  ', ' '.join(map(str, r['o'])), flush=True)
