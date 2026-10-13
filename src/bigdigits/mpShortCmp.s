# bigdigits/mpShortCmp.s -- compare with one digit
#
# original placement:
#   .eh_frame      0046deb0-0046dedc
#   .rdata$zzz     00464278-004642a4
#   .text          00446a40-00446a90

.intel_syntax noprefix
.globl FUN_446a40

.text
.p2align 4
FUN_446a40:
          mov EDX,DWORD PTR [ESP+12]
          xor EAX,EAX
          mov ECX,DWORD PTR [ESP+4]
          test EDX,EDX
          je L_446a87
          cmp EDX,1
          jbe L_446a6d
          cmp DWORD PTR [ECX+4],0
          mov EAX,1
          je L_446a66
          jmp L_446a89
L_446a60:
          cmp DWORD PTR [ECX+EAX*4],0
          jne L_446a82
L_446a66:
          add EAX,1
          cmp EDX,EAX
          jne L_446a60
L_446a6d:
          mov EAX,DWORD PTR [ESP+8]
          cmp DWORD PTR [ECX],EAX
          mov EDX,4294967295
          seta AL
          movzx EAX,AL
          cmovb EAX,EDX
          ret 
L_446a82:
          mov EAX,1
L_446a87:
          repz ret 
L_446a89:
          repz ret 
          .byte 0x90
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
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_446a40 - .
          .byte 0x4b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
