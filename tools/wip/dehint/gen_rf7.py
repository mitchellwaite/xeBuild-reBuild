"""buf as a non-void pointer: the return PHI can't coalesce with it (gimple_can_coalesce_p),
so buf and the return value are two allocnos and a thread in IRA."""
import importlib.util, os

def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def variants():
    for g in ['gen_rf1', 'gen_rf4', 'gen_rf5']:
        for tag, s in load(g).variants():
            if 'BOOL' in tag:
                continue
            for t in ['unsigned char', 'char', 'unsigned int']:
                yield '%s|%s|%s' % (g, t, tag), s.replace('void *buf = NULL', '%s *buf = NULL' % t)
