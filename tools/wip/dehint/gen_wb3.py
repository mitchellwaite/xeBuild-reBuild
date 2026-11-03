"""netWriteBlocks: gen_wb1's axes with `netSendStr(cmd) <= 0`, to see which of the scope/check/tail shapes it tolerates."""
import importlib.util, itertools, os

spec = importlib.util.spec_from_file_location('gen_wb1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_wb1.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
S = 'netSendData(buf, len, log_get_verbose() != 0)'
g.HEAD = {
    'seq': ('if (netSendStr(cmd) <= 0)\n\t\treturn 0;\n\tif (!%s)\n\t\treturn 0;\n' % S, ''),
    'or': ('if (netSendStr(cmd) <= 0 || !%s)\n\t\treturn 0;\n' % S, ''),
    'and': ('if (netSendStr(cmd) > 0 && %s) {\n' % S, '}\n\treturn 0;\n'),
    'nest': ('if (netSendStr(cmd) > 0) {\n\tif (%s) {\n' % S, '}\n\t}\n\treturn 0;\n'),
}
variants = g.variants
