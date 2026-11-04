# attempt 10: pin_hdr gone.  The other way to (A): P(ECC) 28.7% or less.  The ECC test's predictors: PRED_CALL 71 plus whatever the comparison and a goto add.
# `<= 0` adds opcode-positive, a goto in the skipping arm counters it.  Good: finalizeImage about 57 and nothing else, or the head block >= 349 (iw10a.py <file>).
import os
PIN = '			__asm__("" :: "a"(xb.hdr));\n'
TEST = '''			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
'''
PE = 'pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16)'
CE = 'calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);\n'
F = {
 '': TEST,
 'le': f'			if ({PE} <= 0)\n				{CE}',
 'lt': f'			if ({PE} < 1)\n				{CE}',
 'gt': f'			if ({PE} > 0)\n				;\n			else\n				{CE}',
 'ge': f'			if ({PE} >= 1)\n				;\n			else\n				{CE}',
 'g0': f'			if ({PE})\n				goto copy;\n			{CE}		copy:\n',
 'g1': f'			if ({PE} > 0)\n				goto copy;\n			{CE}		copy:\n',
 'g2': f'			if ({PE} == 1)\n				goto copy;\n			{CE}		copy:\n',
 'g3': f'			if ({PE} != 0)\n				goto copy;\n			{CE}		copy:\n',
 'g4': f'			if ({PE} >= 1)\n				goto copy;\n			{CE}		copy:\n',
 'g5': f'			if (!{PE})\n				{CE}			goto copy;\n		copy:\n',
 'g6': f'			if ({PE} <= 0) {{\n				{CE}				goto copy;\n			}}\n		copy:\n',
 'ne': f'			if ({PE} != 1)\n				{CE}',
 'eq': f'			if ({PE} == 1)\n				;\n			else\n				{CE}',
}
AXES = [
 [('nopin', [(PIN, '')])],
 [(k, [(TEST, v)]) for k, v in F.items()],
]
BASE = os.environ.get('IWB', 'src/image_write.c')
FLAGS = []
FOCUS = ['_finalizeImage']
