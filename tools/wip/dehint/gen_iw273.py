# attempt 20: partial's if-forms x tests that have a heuristic, to look for an arm frequency on the 10-multiple grid other than 50% (mechanism: the expect probes pass at P 60, 70, 80).
# `IWB=build/iw/a20/nopt.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw273.py -n 30 -t 1`
import importlib.util, os
here = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location('g0', os.path.join(here, 'gen_iw270.py')); g0 = importlib.util.module_from_spec(sp); sp.loader.exec_module(g0)
BASE = os.environ.get('IWB', 'build/iw/a20/nopt.c')
ARM = '''			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
'''
H = g0.H + ARM + '		} else\n			npages = 32;\n'
TESTS = {
 'gt': lambda: '\t\tif (partial > 0) {\n' + ARM + '\t\t} else\n\t\t\tnpages = 32;\n',
 'le': lambda: '\t\tif (partial <= 0)\n\t\t\tnpages = 32;\n\t\telse {\n' + ARM + '\t\t}\n',
 'two': lambda: '\t\tif (partial > 0) {\n' + ARM + '\t\t}\n\t\tif (partial <= 0)\n\t\t\tnpages = 32;\n',
 'two2': lambda: '\t\tif (partial <= 0)\n\t\t\tnpages = 32;\n\t\tif (partial > 0) {\n' + ARM + '\t\t}\n',
 'twop': lambda: '\t\tif (partial) {\n' + ARM + '\t\t}\n\t\tif (!partial)\n\t\t\tnpages = 32;\n',
 'nz': lambda: '\t\tif (partial != 0) {\n' + ARM + '\t\t}\n\t\tif (partial <= 0)\n\t\t\tnpages = 32;\n',
 'pz': lambda: '\t\tif (partial > 0) {\n' + ARM + '\t\t}\n\t\tif (!partial)\n\t\t\tnpages = 32;\n',
}
A = []
F = dict(g0.F)
F['plain'] = "small = type != 0 && type != '0';\n\t\tpartial = small && len < 0x4000;\n"
for k, v in F.items():
    for tk, tf in TESTS.items():
        A.append((k + '_' + tk, [(H, '\t\t' + v + tf())]))
AXES = [A]
