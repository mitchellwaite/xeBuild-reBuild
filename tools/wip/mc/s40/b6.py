"""b6.py: base B6 = jT125 design + k67l label + -ip arm 'pp' bcp goto k67l. text(extra_fn) -> source."""
import os, json; os.environ['DUP'] = '1'
import voc, k67
def text(): return k67.inj(k67.lab(voc.make(json.load(open('jT125.json')))), 'ip', 'pp')
if __name__ == '__main__':
    import ev
    t = text(); open('B6.c', 'w', newline='\n').write(t)
    r = ev.ev(t, 'B6', True); print(r['score'], r['fncmp'], ' '.join(map(str, r['o'])))
