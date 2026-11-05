"""Attempt 17: gen_ir227's `a != lim`, `a < lim` nest needs P(sane) under about 23.5 (26.3 there: outer 90.8 x inner 29): predictor flags on the inner or outer test."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_ir227 import *
L = f'unsigned lim = {LIM};'
A = '(unsigned)addr'
SAN = 'loadSmc(addr, size); return;'
F = {
 # inner flag, sane falls through
 'in_out_gt': f'{{ {L} if ({A} != lim) {{ int out = {A} >= lim; if (out <= 0) {{ {SAN} }} }} }}\n {NOTSANE}',
 'in_out_gt2': f'{{ {L} int out; if ({A} != lim) {{ out = {A} >= lim; if (out > 0) goto ns; {SAN} }} ns: {NOTSANE} }}',
 'in_in_gt': f'{{ {L} if ({A} != lim) {{ int in = {A} < lim; if (in > 0) {{ {SAN} }} }} }}\n {NOTSANE}',
 'in_in_le': f'{{ {L} int in; if ({A} != lim) {{ in = {A} < lim; if (in <= 0) goto ns; {SAN} }} ns: {NOTSANE} }}',
 # outer flag
 'o_gt': f'{{ {L} int d = {A} != lim; if (d > 0) {{ if ({A} < lim) {{ {SAN} }} }} }}\n {NOTSANE}',
 'o_le': f'{{ {L} int d = {A} != lim; if (d <= 0) goto ns; if ({A} < lim) {{ {SAN} }} ns: {NOTSANE} }}',
 'o_eq': f'{{ {L} int d = {A} == lim; if (d > 0) goto ns; if ({A} < lim) {{ {SAN} }} ns: {NOTSANE} }}',
 'o_eq2': f'{{ {L} int d = {A} == lim; if (d <= 0) {{ if ({A} < lim) {{ {SAN} }} }} }}\n {NOTSANE}',
 # both tests go to the arm as a chain, sane written last
 'ch1': f'{{ {L} if ({A} == lim) goto ns; if ({A} >= lim) goto ns; {SAN} ns: {NOTSANE} }}',
 'ch2': f'{{ {L} if ({A} > lim) goto ns; if ({A} == lim) goto ns; {SAN} ns: {NOTSANE} }}',
 'ch3': f'{{ {L} int d = {A} > lim; if (d > 0) goto ns; if ({A} == lim) goto ns; {SAN} ns: {NOTSANE} }}',
 'ch4': f'{{ {L} int d = {A} > lim; if (d <= 0) {{ if ({A} != lim) {{ {SAN} }} }} }}\n {NOTSANE}',
 'ch5': f'{{ {L} int d = {A} == lim; if (d > 0) goto ns; d = {A} > lim; if (d > 0) goto ns; {SAN} ns: {NOTSANE} }}',
}
forms = {k: body(v, zset='') for k, v in F.items()}
if __name__ == '__main__':
    sweep(forms)
