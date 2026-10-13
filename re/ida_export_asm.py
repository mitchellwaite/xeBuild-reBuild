"""Export IDA's own assembly listing of a database (MASM-style, reference only).

Usage (needs IDA 9.x idalib):  python re/ida_export_asm.py <xeBuild.exe.i64> <out.asm>

IDA has no GNU-as output for x86, so this is for reading alongside the
decompiler, not for rebuilding.
"""
import idapro, sys

idapro.open_database(sys.argv[1], False)

import ida_loader, ida_fpro, ida_ida

fp = ida_fpro.qfile_t()
fp.open(sys.argv[2], "wt")
r = ida_loader.gen_file(ida_loader.OFILE_ASM, fp.get_fp(), ida_ida.inf_get_min_ea(), ida_ida.inf_get_max_ea(), 0)
fp.close()
print("gen_file ->", r)
idapro.close_database(False)
