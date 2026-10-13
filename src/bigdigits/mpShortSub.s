# bigdigits/mpShortSub.s -- subtract one digit with borrow
#
# original placement:
#   .eh_frame      0046d1a0-0046d1e8
#   .rdata$zzz     00463eb0-00463edc
#   .text          00441780-004417d0

.intel_syntax noprefix
.globl FUN_441780

.text
.p2align 4
FUN_441780:
          push EDI
          push ESI
          push EBX
          mov ESI,DWORD PTR [ESP+20]
          mov EAX,DWORD PTR [ESP+24]
          mov EDI,DWORD PTR [ESP+28]
          mov EBX,DWORD PTR [ESP+16]
          mov EDX,DWORD PTR [ESI]
          sub EDX,EAX
          not EAX
          cmp EDX,EAX
          mov DWORD PTR [EBX],EDX
          seta AL
          cmp EDI,1
          movzx EAX,AL
          jbe L_4417c9
          mov EDX,1
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_4417b0:
          mov ECX,DWORD PTR [ESI+EDX*4]
          sub ECX,EAX
          not EAX
          cmp ECX,EAX
          mov DWORD PTR [EBX+EDX*4],ECX
          seta AL
          add EDX,1
          cmp EDI,EDX
          movzx EAX,AL
          jne L_4417b0
L_4417c9:
          pop EBX
          pop ESI
          pop EDI
          ret 
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
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_441780 - .
          .byte 0x4d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x87
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x86
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x2
          .byte 0x47
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
