# attempt 20: `if (partial)` (P 50%, t 96, no pin needed: imgAdd clean). Forms of the test and of partial, on nopt + if (partial).
# `IWB=build/iw/a20/nopt.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw269.py -n 40 -t 4`
import os
BASE = os.environ.get('IWB', 'build/iw/a20/nopt.c')
H = '''		small = type != 0 && type != '0';
		partial = small && len < 0x4000;
		if (partial > 0) {
			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
		} else
			npages = 32;
'''
ARM = '''if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;'''
ARM2 = 'npages = len % 512 ? (len + 512) / 512 : len / 512;'
ARM3 = '''npages = len / 512;
			if (len % 512)
				npages = (len + 512) / 512;'''
ARM4 = '''npages = (len + 512) / 512;
			if (!(len % 512))
				npages = len / 512;'''
DEF = {
 'sm': "small = type != 0 && type != '0';\n\t\tpartial = small && len < 0x4000;\n",
 'si': "partial = type != 0 && type != '0' && len < 0x4000;\n",
 'ms': "partial = len < 0x4000 && type != 0 && type != '0';\n",
 'sl': "small = type != 0 && type != '0';\n\t\tpartial = small & (len < 0x4000);\n",
}
A = []
for dn, df in DEF.items():
  for an, arm in (('a1', ARM), ('a2', ARM2), ('a3', ARM3), ('a4', ARM4)):
    for form in ('ie', 'ne', 'pre', 'inl'):
      if form == 'ie': b = '\t\t' + df + '\t\tif (partial) {\n\t\t\t' + arm + '\n\t\t} else\n\t\t\tnpages = 32;\n'
      elif form == 'ne': b = '\t\t' + df + '\t\tif (!partial)\n\t\t\tnpages = 32;\n\t\telse {\n\t\t\t' + arm + '\n\t\t}\n'
      elif form == 'pre': b = '\t\t' + df + '\t\tnpages = 32;\n\t\tif (partial) {\n\t\t\t' + arm + '\n\t\t}\n'
      else: b = "\t\tif (type != 0 && type != '0' && len < 0x4000) {\n\t\t\t" + arm + '\n\t\t} else\n\t\t\tnpages = 32;\n'
      if form == 'inl' and dn != 'sm': continue
      A.append(('%s_%s_%s' % (dn, an, form), [(H, b)]))
T = [('int', []), ('bool', [('\tint partial;\n', '\t_Bool partial;\n')]), ('u8', [('\tint partial;\n', '\tuint8_t partial;\n')])]
AXES = [A, T]
