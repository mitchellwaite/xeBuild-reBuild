# runtime/libmingw32/gccmain.s -- byte match
#
# original placement:
#   .bss           00479ac8-00479ae0
#   .data          0044b6a4-0044b6cc
#   .eh_frame      0046df74-0046dfdc
#   .rdata$zzz     004642fc-00464328
#   .text          00446c10-00446cb0

.intel_syntax noprefix
.globl FUN_446c90
.globl L_44b6b0
.globl L_44b6b8
.globl L_44b6bc
.globl L_479acc

.text
.p2align 4
L_446c10:
          mov EAX,DWORD PTR [L_44b6a4]
          mov EAX,DWORD PTR [EAX]
          test EAX,EAX
          je L_446c3a
          sub ESP,12
          .byte 0x66   # nop
          nop
L_446c20:
          call EAX
          mov EAX,DWORD PTR [L_44b6a4]
          lea EDX,DWORD PTR [EAX+4]
          mov EAX,DWORD PTR [EAX+4]
          mov DWORD PTR [L_44b6a4],EDX
          test EAX,EAX
          jne L_446c20
          add ESP,12
L_446c3a:
          repz ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_446c40:
          push EBX
          sub ESP,24
          mov EBX,DWORD PTR [L_4497a0]
          cmp EBX,-1
          je L_446c70
L_446c4f:
          test EBX,EBX
          je L_446c5f
L_446c53:
          call DWORD PTR [EBX*4+L_4497a0]
          sub EBX,1
          jne L_446c53
L_446c5f:
          mov DWORD PTR [ESP],OFFSET L_446c10
          call FUN_446bf0
          add ESP,24
          pop EBX
          ret 
L_446c70:
          xor EBX,EBX
          jmp L_446c76
L_446c74:
          mov EBX,EAX
L_446c76:
          lea EAX,DWORD PTR [EBX+1]
          mov EDX,DWORD PTR [EAX*4+L_4497a0]
          test EDX,EDX
          jne L_446c74
          jmp L_446c4f
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_446c90:
          mov EAX,DWORD PTR [L_479ac8]
          test EAX,EAX
          je L_446ca0
          repz ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_446ca0:
          mov DWORD PTR [L_479ac8],1
          jmp L_446c40
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.data
.p2align 2
L_44b6a4:
          .long L_4497b0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
L_44b6b0:
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_44b6b8:
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_44b6bc:
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .long FUN_448820
          .long L_4492a0
          .long FUN_4492b0

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
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_446c10 - .
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4e
          .byte 0xe
          .byte 0x10
          .byte 0x5c
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_446c40 - .
          .byte 0x46
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x6a
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x58
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_446c90 - .
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0

.bss
.p2align 3
L_479ac8:
          .zero 4
L_479acc:
          .zero 20
