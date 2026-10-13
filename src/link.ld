/* Link script for the per-object rebuild of xeBuild.exe (ld -m i386pe).
   Mirrors the default i386pe script for the sections this image uses:
   .text.startup after all .text, then the ctor/dtor lists the default script
   writes (kept as data in runtime/ctor_dtor_lists.s), .jcr at the end of .data,
   the per-object `GCC:` idents (.rdata$zzz) after .rdata, COMMON after .bss.
   .idata/.CRT/.tls/.rsrc come whole from runtime/*.s. */
__ImageBase = __image_base__;
SECTIONS
{
  .text  __image_base__ + __section_alignment__ :
  {
    *(.text)
    *(.text.startup)
    KEEP(*(.ctors_dtors))
  }
  .data   BLOCK(__section_alignment__) : { *(.data) KEEP(*(.jcr)) }
  .rdata  BLOCK(__section_alignment__) : { *(.rdata) KEEP(*(SORT(.rdata$*))) }
  .eh_frame BLOCK(__section_alignment__) : { KEEP(*(.eh_frame)) }
  .bss    BLOCK(__section_alignment__) : { *(.bss) *(COMMON) }
  .idata  BLOCK(__section_alignment__) : { KEEP(*(.idata)) }
  .CRT    BLOCK(__section_alignment__) : { KEEP(*(.CRT)) }
  .tls    BLOCK(__section_alignment__) : { KEEP(*(.tls)) }
  .rsrc   BLOCK(__section_alignment__) : { KEEP(*(.rsrc)) }
  /DISCARD/ : { *(.drectve) }
}
