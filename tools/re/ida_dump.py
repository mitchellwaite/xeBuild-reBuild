"""Dump everything the asm generator needs from an IDA analysis of xeBuild.exe.

Usage (needs IDA 9.x idalib):  python tools/re/ida_dump.py <path/to/xeBuild.exe> <out.json>

The exe is analysed in place (IDA writes its .i64 next to it), so point this at
a scratch copy, not the reference binary in the repo root.
"""
import idapro, sys, json

idapro.open_database(sys.argv[1], True)

import idaapi, idautils, idc, ida_bytes, ida_funcs, ida_nalt, ida_name, ida_segment, ida_ua, ida_xref

idaapi.auto_wait()

IMG_LO, IMG_HI = 0x400000, 0x513000


def in_image(v):
    return IMG_LO <= v < IMG_HI


out = {"insns": [], "data_offsets": [], "imports": {}, "names": {}, "funcs": [], "segments": []}

for s in idautils.Segments():
    seg = ida_segment.getseg(s)
    out["segments"].append([ida_segment.get_segm_name(seg), seg.start_ea, seg.end_ea])

for ea in idautils.Functions():
    f = ida_funcs.get_func(ea)
    out["funcs"].append([ea, f.end_ea, ida_name.get_name(ea)])

for ea, name in idautils.Names():
    out["names"][ea] = name


def imp_cb(ea, name, ordinal):
    out["imports"][ea] = [cur_mod, name, ordinal]
    return True


for i in range(ida_nalt.get_import_module_qty()):
    cur_mod = ida_nalt.get_import_module_name(i)
    ida_nalt.enum_import_names(i, imp_cb)

# Instructions in all code segments: record every field that holds an address.
text = ida_segment.get_segm_by_name(".text")
ea = text.start_ea
while ea < text.end_ea:
    flags = ida_bytes.get_flags(ea)
    if not ida_bytes.is_code(flags):
        ea = ida_bytes.next_head(ea, text.end_ea)
        continue
    insn = ida_ua.insn_t()
    n = ida_ua.decode_insn(insn, ea)
    if n <= 0:
        ea += 1
        continue
    fields = []
    for i, op in enumerate(insn.ops):
        if op.type == ida_ua.o_void:
            break
        if op.type == ida_ua.o_near:
            # relative branch: field runs from offb to end of insn
            fields.append(["rel", op.offb, n - op.offb, op.addr])
        elif op.type == ida_ua.o_mem:
            fields.append(["abs", op.offb, 4, op.addr, True])
        elif op.type == ida_ua.o_displ and op.offb and n - op.offb >= 4:
            # only 32-bit displacements can be addresses; size check done by generator
            fields.append(["disp", op.offb, 4, op.addr & 0xffffffff, bool(ida_bytes.is_off(flags, i))])
        elif op.type == ida_ua.o_imm:
            v = op.value & 0xffffffff
            if in_image(v) or ida_bytes.is_off(flags, i):
                fields.append(["imm", op.offb, 4, v, bool(ida_bytes.is_off(flags, i))])
        elif op.type == ida_ua.o_far:
            fields.append(["far", op.offb, 4, op.addr])
    out["insns"].append([ea, n, fields, idc.GetDisasm(ea)])
    ea += n

# Pointers stored in data: IDA-marked offsets and any dword that looks like an image address.
for segname in (".data", ".rdata", ".CRT", ".tls", ".text"):
    seg = ida_segment.get_segm_by_name(segname)
    if not seg:
        continue
    a = seg.start_ea
    while a + 4 <= seg.end_ea:
        fl = ida_bytes.get_flags(a)
        if segname == ".text" and ida_bytes.is_code(fl):
            a += 1
            continue
        v = ida_bytes.get_dword(a)
        marked = ida_bytes.is_off0(fl) and ida_bytes.is_head(fl)
        if marked or (in_image(v) and a % 4 == 0):
            out["data_offsets"].append([a, v, bool(marked)])
        a += 1

json.dump(out, open(sys.argv[2], "w"))
print("insns", len(out["insns"]), "data_offsets", len(out["data_offsets"]), "imports", len(out["imports"]))
idapro.close_database(True)
