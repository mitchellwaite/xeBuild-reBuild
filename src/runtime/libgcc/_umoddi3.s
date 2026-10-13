# runtime/libgcc/_umoddi3.s -- byte match
#
# original placement:
#   .eh_frame      0046e73c-0046e7d8
#   .rdata$zzz     00464590-004645bc
#   .text          00448040-00448190

.intel_syntax noprefix
.globl FUN_448040

.text
.p2align 4
FUN_448040:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EAX,DWORD PTR [ESP+60]
          mov ECX,DWORD PTR [ESP+48]
          mov ESI,DWORD PTR [ESP+52]
          mov EDI,DWORD PTR [ESP+56]
          test EAX,EAX
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],ECX
          mov EDX,ESI
          jne L_448080
          cmp EDI,ESI
          jbe L_4480b0
          mov EAX,ECX
          div EDI
L_448074:
          mov EAX,EDX
          xor EDX,EDX
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_448080:
          cmp EAX,ESI
          mov EBX,ESI
          ja L_4480d0
          bsr EBP,EAX
          xor EBP,31
          jne L_4480e0
          cmp EAX,ESI
          jb L_448170
          cmp DWORD PTR [ESP],ECX
          jbe L_448170
L_44809f:
          mov EAX,DWORD PTR [ESP+4]
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4480b0:
          test EDI,EDI
          mov EBP,EDI
          jne L_4480c1
          mov EAX,1
          xor EDX,EDX
          div EDI
          mov EBP,EAX
L_4480c1:
          mov EAX,ESI
          xor EDX,EDX
          div EBP
          mov EAX,ECX
          div EBP
          jmp L_448074
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4480d0:
          mov EAX,ECX
          mov EDX,ESI
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4480e0:
          mov ESI,DWORD PTR [ESP]
          mov EDI,32
          mov ECX,EBP
          sub EDI,EBP
          shl EAX,CL
          mov ECX,EDI
          mov EDX,ESI
          shr EDX,CL
          mov ECX,EBP
          or EDX,EAX
          mov EAX,EBX
          mov DWORD PTR [ESP],EDX
          mov EDX,ESI
          shl EDX,CL
          mov ECX,EDI
          mov DWORD PTR [ESP+4],EDX
          mov EDX,DWORD PTR [ESP+8]
          shr EAX,CL
          mov ECX,EBP
          mov ESI,EAX
          shl EBX,CL
          mov ECX,EDI
          mov EAX,EDX
          shr EAX,CL
          mov ECX,EBP
          or EAX,EBX
          mov EBX,EDX
          mov EDX,ESI
          div DWORD PTR [ESP]
          mov ESI,EDX
          shl EBX,CL
          mul DWORD PTR [ESP+4]
          cmp ESI,EDX
          mov DWORD PTR [ESP+8],EBX
          mov ECX,EDX
          mov EBX,EAX
          jb L_448140
          jne L_44814b
          cmp DWORD PTR [ESP+8],EAX
          jae L_44814b
L_448140:
          sub EAX,DWORD PTR [ESP+4]
          sbb EDX,DWORD PTR [ESP]
          mov ECX,EDX
          mov EBX,EAX
L_44814b:
          mov EDX,DWORD PTR [ESP+8]
          sub EDX,EBX
          sbb ESI,ECX
          mov ECX,EDI
          mov EAX,ESI
          shl EAX,CL
          mov ECX,EBP
          shr EDX,CL
          mov ECX,EBP
          shr ESI,CL
          or EAX,EDX
          mov EDX,ESI
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_448170:
          mov EDX,ESI
          sub ECX,EDI
          sbb EDX,DWORD PTR [ESP+12]
          mov DWORD PTR [ESP+4],ECX
          jmp L_44809f
          .byte 0x90
          .byte 0x90
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop

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
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_448040 - .
          .byte 0x41
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x87
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x74
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x66
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x46
          .byte 0xb
          .byte 0x67
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x45
          .byte 0xb
          .byte 0x2
          .byte 0x88
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
