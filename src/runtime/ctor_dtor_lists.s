# runtime/ctor_dtor_lists.s -- __CTOR_LIST__/__DTOR_LIST__ from the link script
#
# original placement:
#   .ctors_dtors   004497a0-004497b4

.intel_syntax noprefix
.globl L_4497a0
.globl L_4497b0

.section .ctors_dtors,"dxr"
.p2align 2
L_4497a0:
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .long L_449790
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
L_4497b0:
          .zero 4
