/* Link script for the single-object rebuild of xeBuild.exe (ld -m i386pe).
   Same section order as the default i386pe script, but the inputs are
   ddisasm's whole sections rather than per-object .idata$N etc.  Addresses
   follow from SizeOfHeaders + 0x1000 section alignment. */
SECTIONS
{
  .text  __image_base__ + __section_alignment__ :
  {
    *(.text)
    *(SORT(.text$*))
  }
  .data   BLOCK(__section_alignment__) : { *(.data) *(SORT(.data$*)) }
  .rdata  BLOCK(__section_alignment__) : { *(.rdata) *(SORT(.rdata$*)) }
  .eh_frame BLOCK(__section_alignment__) : { KEEP(*(.eh_frame)) }
  .bss    BLOCK(__section_alignment__) : { *(.bss) *(COMMON) }
  .idata  BLOCK(__section_alignment__) : { KEEP(*(.idata)) }
  .CRT    BLOCK(__section_alignment__) : { KEEP(*(.CRT)) }
  .tls    BLOCK(__section_alignment__) : { KEEP(*(.tls)) }
  .rsrc   BLOCK(__section_alignment__) : { KEEP(*(.rsrc)) }
  /DISCARD/ : { *(.drectve) }
}
