# runtime/libgcc/_moddi3.s -- byte match
#
# original placement:
#   .eh_frame      0046e648-0046e6a0
#   .rdata$zzz     00464538-00464564
#   .text          00447d70-00447f20

.intel_syntax noprefix
.globl ___moddi3

.text
.p2align 4
___moddi3:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EDI,DWORD PTR [ESP+68]
          mov EBX,DWORD PTR [ESP+76]
          mov ESI,DWORD PTR [ESP+64]
          mov ECX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+8],0
          test EDI,EDI
          mov EAX,EBX
          js L_447e50
L_447d99:
          test EAX,EAX
          js L_447e43
L_447da1:
          test EBX,EBX
          mov EAX,ESI
          mov EDX,EDI
          mov DWORD PTR [ESP+16],EDI
          mov DWORD PTR [ESP+24],ECX
          mov DWORD PTR [ESP+20],ESI
          mov DWORD PTR [ESP+12],EDI
          jne L_447dd0
          cmp ECX,EDX
          jbe L_447e20
          div ECX
          mov DWORD PTR [ESP+12],EDX
L_447dc3:
          mov EAX,DWORD PTR [ESP+12]
          xor EDX,EDX
          jmp L_447ddc
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_447dd0:
          mov EBP,DWORD PTR [ESP+16]
          cmp EBX,EBP
          jbe L_447df3
          mov EAX,ESI
          mov EDX,EBP
L_447ddc:
          mov ECX,DWORD PTR [ESP+8]
          test ECX,ECX
          je L_447deb
          neg EAX
          adc EDX,0
          neg EDX
L_447deb:
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_447df3:
          bsr EDI,EBX
          xor EDI,31
          mov DWORD PTR [ESP+28],EDI
          jne L_447e64
          cmp EBX,DWORD PTR [ESP+16]
          jb L_447f03
          cmp ECX,DWORD PTR [ESP+20]
          jbe L_447f03
L_447e13:
          mov EAX,DWORD PTR [ESP+20]
          mov EDX,DWORD PTR [ESP+12]
          jmp L_447ddc
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_447e20:
          test ECX,ECX
          jne L_447e2f
          mov EAX,1
          xor EDX,EDX
          div ECX
          mov ECX,EAX
L_447e2f:
          mov EAX,DWORD PTR [ESP+16]
          xor EDX,EDX
          div ECX
          mov EAX,DWORD PTR [ESP+20]
          div ECX
          mov DWORD PTR [ESP+12],EDX
          jmp L_447dc3
L_447e43:
          neg ECX
          adc EBX,0
          neg EBX
          jmp L_447da1
          .byte 0x90
L_447e50:
          neg ESI
          mov DWORD PTR [ESP+8],4294967295
          adc EDI,0
          neg EDI
          jmp L_447d99
L_447e64:
          mov EDI,DWORD PTR [ESP+28]
          mov EBP,DWORD PTR [ESP+24]
          mov EDX,32
          sub EDX,EDI
          mov ECX,EDI
          mov ESI,EDX
          shl EBX,CL
          mov DWORD PTR [ESP+20],EDX
          mov ECX,ESI
          mov EDX,EBP
          shr EDX,CL
          mov ECX,EDX
          mov EDX,EBP
          mov EBP,DWORD PTR [ESP+16]
          or ECX,EBX
          mov DWORD PTR [ESP+12],ECX
          mov ECX,EDI
          shl EDX,CL
          mov EBX,EBP
          mov ECX,ESI
          shr EBX,CL
          movzx ECX,BYTE PTR [ESP+28]
          mov EDI,EDX
          mov EDX,ESI
          mov ESI,EBP
          mov EBP,EAX
          shl ESI,CL
          mov ECX,EDX
          mov EDX,EBX
          shr EBP,CL
          movzx ECX,BYTE PTR [ESP+28]
          or ESI,EBP
          shl EAX,CL
          mov EBP,EAX
          mov EAX,ESI
          div DWORD PTR [ESP+12]
          mov EBX,EDX
          mul EDI
          cmp EBX,EDX
          mov ESI,EAX
          mov ECX,EDX
          jb L_447ed3
          jne L_447edd
          cmp EBP,EAX
          jae L_447edd
L_447ed3:
          sub EAX,EDI
          sbb EDX,DWORD PTR [ESP+12]
          mov ECX,EDX
          mov ESI,EAX
L_447edd:
          mov EAX,EBP
          mov EDI,DWORD PTR [ESP+28]
          sub EAX,ESI
          sbb EBX,ECX
          movzx ECX,BYTE PTR [ESP+20]
          mov ESI,EBX
          shl ESI,CL
          mov ECX,EDI
          shr EAX,CL
          mov ECX,EDI
          or ESI,EAX
          shr EBX,CL
          mov EAX,ESI
          mov EDX,EBX
          jmp L_447ddc
L_447f03:
          mov EAX,DWORD PTR [ESP+20]
          mov EDX,DWORD PTR [ESP+16]
          sub EAX,ECX
          sbb EDX,EBX
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+20],EAX
          jmp L_447e13
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long ___moddi3 - .
          .byte 0xac
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
          .byte 0x40
          .byte 0x2
          .byte 0x77
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
