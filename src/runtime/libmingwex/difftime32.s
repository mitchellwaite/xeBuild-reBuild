# runtime/libmingwex/difftime32.s -- byte match
#
# original placement:
#   .eh_frame      0046e7d8-0046e810
#   .rdata$zzz     004645bc-004645e8
#   .text          00448190-004481c0

.intel_syntax noprefix
.globl FUN_448190

.text
.p2align 4
FUN_448190:
          sub ESP,12
          mov EDX,DWORD PTR [ESP+16]
          mov ECX,DWORD PTR [ESP+20]
          mov EAX,EDX
          sub EAX,ECX
          cmp EDX,EAX
          jl L_4481b0
          mov DWORD PTR [ESP+4],EAX
          fild DWORD PTR [ESP+4]
          add ESP,12
          ret 
          .byte 0x90
L_4481b0:
          sub ECX,EDX
          mov DWORD PTR [ESP+4],ECX
          fild DWORD PTR [ESP+4]
          add ESP,12
          fchs 
          ret 

.section .rdata$zzz,"dr"
.p2align 2
          .byte 0x47
          .byte 0x43
          .byte 0x43
          .byte 0x3a
          .byte 0x20
          .byte 0x28
          .byte 0x52
          .byte 0x65
          .byte 0x76
          .byte 0x32
          .byte 0x2c
          .byte 0x20
          .byte 0x42
          .byte 0x75
          .byte 0x69
          .byte 0x6c
          .byte 0x74
          .byte 0x20
          .byte 0x62
          .byte 0x79
          .byte 0x20
          .byte 0x4d
          .byte 0x53
          .byte 0x59
          .byte 0x53
          .byte 0x32
          .byte 0x20
          .byte 0x70
          .byte 0x72
          .byte 0x6f
          .byte 0x6a
          .byte 0x65
          .byte 0x63
          .byte 0x74
          .byte 0x29
          .byte 0x20
          .byte 0x36
          .byte 0x2e
          .byte 0x32
          .byte 0x2e
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0

.section .eh_frame,"dr"
.p2align 2
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1
          .byte 0x7a
          .byte 0x52
          .byte 0x0
          .byte 0x1
          .byte 0x7c
          .byte 0x8
          .byte 0x1
          .byte 0x1b
          .byte 0xc
          .byte 0x4
          .byte 0x4
          .byte 0x88
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_448190 - .
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x5b
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x42
          .byte 0xb
          .byte 0x4d
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
