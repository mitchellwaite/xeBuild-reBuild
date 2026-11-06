"""mode_client attempt 6: the bbro keys of the switch's case heads.

python tools/wip/dehint/mc6keys.py TAG [TAG ...]   (dumps from mc4dump.py in build/mc4/TAG)
For mode_client's bbro dump: maps bbs to the first called function inside them (from the
RTL in the dump), finds the jump-table block's successors (case heads) and prints, for each
case head, every key it was given ("Possible start" / "Changing key") and the trace it went
into, in trace order."""
import os, re, sys

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def load(tag):
    p = os.path.join(R, 'build', 'mc4', tag, 'mode_client.c.274r.bbro')
    t = open(p).read()
    t = t[t.index(';; Function mode_client'):]
    nxt = t.find(';; Function', 10)
    return t if nxt < 0 else t[:nxt]


def main():
    for tag in sys.argv[1:]:
        t = load(tag)
        # bb -> calls (in the final RTL listing)
        calls = {}
        cur = None
        for line in t.split('\n'):
            m = re.match(r';; basic block (\d+),', line) or re.match(r'\(note \d+ \d+ \d+ (\d+) \[bb \d+\] NOTE_INSN_BASIC_BLOCK', line)
            m2 = re.search(r'\[bb (\d+)\] NOTE_INSN_BASIC_BLOCK', line)
            if m2:
                cur = int(m2.group(1))
            m3 = re.search(r'symbol_ref:SI \("(\w+)"\)', line)
            if m3 and cur is not None and 'call' in line or (m3 and cur is not None and m3.group(1) not in ('log_printf',) and False):
                calls.setdefault(cur, [])
                if m3.group(1) not in calls[cur]:
                    calls[cur].append(m3.group(1))
        # succs of bbs from ";; bb N ... succs" lines
        succ = {}
        for m in re.finditer(r';; bb (\d+) artificial_defs.*?\n;;  succs\s*(?:\{[^}]*\})?\s*([^\n]*)', t):
            pass
        for m in re.finditer(r';;\s+succ:\s*([^\n]*)', t):
            pass
        keys = {}
        for m in re.finditer(r'Possible start of (?:this|next) round: (\d+) \(key: (-?\d+)\)', t):
            keys.setdefault(int(m.group(1)), []).append(int(m.group(2)))
        for m in re.finditer(r'Changing key for bb (\d+) from (-?\d+) to (-?\d+)', t):
            keys.setdefault(int(m.group(1)), []).append(int(m.group(3)))
        trace = {}
        for m in re.finditer(r'Basic block (\d+) was visited in trace (\d+)', t):
            trace.setdefault(int(m.group(1)), int(m.group(2)))
        want = {'netDumpNand': 1, 'clientWrite': 2, 'clientKeys': 3, 'sendAvatarData': 4,
                'sendCompatData': 5, 'clientPatches': 7, 'clientReadBlocks': 8,
                'clientWriteBlocks': 9, 'myatoh32': 10, 'clientBinPatch': 11, 'clientInfo': 12}
        print('==', tag)
        rows = []
        for bb, cs in calls.items():
            for c in cs:
                if c in want:
                    rows.append((trace.get(bb, -1), bb, want[c], c, keys.get(bb, [])))
        for r in sorted(rows):
            print('  trace %3d bb %3d case %2d %-18s keys %s' % r)


if __name__ == '__main__':
    main()
