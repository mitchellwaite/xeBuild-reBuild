# runtime/libmingwex/ftello64.s -- byte match
#
# original placement:
#   .eh_frame      0046ec0c-0046ec40
#   .rdata$zzz     00464698-004646c4
#   .text          00448ff0-00449030

.intel_syntax noprefix
.globl _ftello64

.text
.p2align 4
_ftello64:
          sub ESP,44
          lea EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call FUN_449170
          test EAX,EAX
          jne L_449020
          mov EAX,DWORD PTR [ESP+24]
          mov EDX,DWORD PTR [ESP+28]
L_449013:
          add ESP,44
          ret 
L_449017:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_449020:
          mov EAX,4294967295
          mov EDX,4294967295
          jmp L_449013
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

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
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _ftello64 - .
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x63
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x4a
          .byte 0xb
          .byte 0x0
          .byte 0x0
