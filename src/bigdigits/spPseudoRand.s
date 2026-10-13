# bigdigits/spPseudoRand.s -- rand()-based random digit
#
# original placement:
#   .bss           00479ac4-00479ac8
#   .eh_frame      0046dedc-0046df18
#   .rdata         00463280-00463284
#   .rdata$zzz     004642a4-004642d0
#   .text          00446a90-00446b30

.intel_syntax noprefix
.globl FUN_446a90

.text
.p2align 4
FUN_446a90:
          push EBX
          sub ESP,56
          mov EAX,DWORD PTR [L_479ac4]
          test EAX,EAX
          je L_446af0
L_446a9d:
          call FUN_4490c0
          fnstcw WORD PTR [ESP+38]
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+68]
          xor EDX,EDX
          fild DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+20],EDX
          fdiv DWORD PTR [L_463280]
          mov DWORD PTR [ESP+16],EAX
          movzx EAX,WORD PTR [ESP+38]
          mov AH,12
          mov WORD PTR [ESP+36],AX
          fild QWORD PTR [ESP+16]
          fmulp ST(1)
          fldcw WORD PTR [ESP+36]
          fistp QWORD PTR [ESP+24]
          fldcw WORD PTR [ESP+38]
          mov EAX,DWORD PTR [ESP+24]
          add EAX,DWORD PTR [ESP+64]
          add ESP,56
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_446af0:
          mov DWORD PTR [ESP],0
          call FUN_449050
          mov DWORD PTR [ESP],EAX
          call FUN_449090
          call FUN_4490c0
          movzx EAX,AL
          test EAX,EAX
          lea EBX,DWORD PTR [EAX-1]
          je L_446b20
L_446b13:
          sub EBX,1
          call FUN_4490c0
          cmp EBX,-1
          jne L_446b13
L_446b20:
          mov DWORD PTR [L_479ac4],1
          jmp L_446a9d
          .byte 0x90

.section .rdata,"dr"
.p2align 2
L_463280:
          .byte 0x0
          .byte 0xfe
          .byte 0xff
          .byte 0x46

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
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_446a90 - .
          .byte 0x9f
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
          .byte 0x40
          .byte 0x2
          .byte 0x57
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb

.bss
.p2align 2
L_479ac4:
          .zero 4
