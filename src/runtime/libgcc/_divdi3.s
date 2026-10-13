# runtime/libgcc/_divdi3.s -- byte match
#
# original placement:
#   .eh_frame      0046e5f0-0046e648
#   .rdata$zzz     0046450c-00464538
#   .text          00447c30-00447d70

.intel_syntax noprefix
.globl FUN_447c30

.text
.p2align 4
FUN_447c30:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EDX,DWORD PTR [ESP+52]
          mov EBX,DWORD PTR [ESP+60]
          mov EAX,DWORD PTR [ESP+48]
          mov ECX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+4],0
          test EDX,EDX
          mov ESI,EBX
          js L_447cf1
L_447c59:
          test ESI,ESI
          js L_447ce1
L_447c61:
          test EBX,EBX
          mov DWORD PTR [ESP+8],EAX
          mov ESI,EDX
          mov EDI,ECX
          mov EBP,EAX
          jne L_447c80
          cmp ECX,EDX
          jbe L_447cc0
          div ECX
          xor EBP,EBP
          mov ECX,EAX
          jmp L_447c88
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_447c80:
          cmp EBX,EDX
          jbe L_447ca3
          xor EBP,EBP
          xor ECX,ECX
L_447c88:
          mov EAX,ECX
          mov ECX,DWORD PTR [ESP+4]
          mov EDX,EBP
          test ECX,ECX
          je L_447c9b
          neg EAX
          adc EDX,0
          neg EDX
L_447c9b:
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_447ca3:
          bsr EBP,EBX
          xor EBP,31
          jne L_447d05
          cmp EBX,EDX
          jb L_447cb7
          xor ECX,ECX
          cmp EDI,DWORD PTR [ESP+8]
          ja L_447c88
L_447cb7:
          mov ECX,1
          jmp L_447c88
          .byte 0x66
          .byte 0x90
L_447cc0:
          test ECX,ECX
          jne L_447ccf
          mov EAX,1
          xor EDX,EDX
          div ECX
          mov ECX,EAX
L_447ccf:
          mov EAX,ESI
          xor EDX,EDX
          div ECX
          mov ESI,EAX
          mov EAX,EBP
          mov EBP,ESI
          div ECX
          mov ECX,EAX
          jmp L_447c88
L_447ce1:
          neg ECX
          not DWORD PTR [ESP+4]
          adc EBX,0
          neg EBX
          jmp L_447c61
L_447cf1:
          neg EAX
          mov DWORD PTR [ESP+4],4294967295
          adc EDX,0
          neg EDX
          jmp L_447c59
L_447d05:
          mov EAX,32
          mov ECX,EBP
          mov EDX,EDI
          sub EAX,EBP
          shl EBX,CL
          mov ECX,EAX
          shr EDX,CL
          mov ECX,EBP
          or EDX,EBX
          shl EDI,CL
          mov EBX,ESI
          mov ECX,EAX
          mov DWORD PTR [ESP+12],EDX
          mov EDX,DWORD PTR [ESP+8]
          shr EBX,CL
          mov ECX,EBP
          shl ESI,CL
          mov ECX,EAX
          shr EDX,CL
          or ESI,EDX
          mov EDX,EBX
          mov EAX,ESI
          div DWORD PTR [ESP+12]
          mov EBX,EDX
          mov ESI,EAX
          mul EDI
          cmp EBX,EDX
          jb L_447d60
          mov EDI,DWORD PTR [ESP+8]
          mov ECX,EBP
          shl EDI,CL
          cmp EDI,EAX
          jae L_447d56
          cmp EBX,EDX
          je L_447d60
L_447d56:
          mov ECX,ESI
          xor EBP,EBP
          jmp L_447c88
          nop
L_447d60:
          lea ECX,DWORD PTR [ESI-1]
          xor EBP,EBP
          jmp L_447c88
          .byte 0x90
          .byte 0x90
          .byte 0x90
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_447c30 - .
          .byte 0x3a
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
          .byte 0x2
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
          .byte 0x41
          .byte 0xb
          .byte 0x0
