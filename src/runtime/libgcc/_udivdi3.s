# runtime/libgcc/_udivdi3.s -- byte match
#
# original placement:
#   .eh_frame      0046e6a0-0046e73c
#   .rdata$zzz     00464564-00464590
#   .text          00447f20-00448040

.intel_syntax noprefix
.globl ___udivdi3

.text
.p2align 4
___udivdi3:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov ESI,DWORD PTR [ESP+60]
          mov EBX,DWORD PTR [ESP+48]
          mov ECX,DWORD PTR [ESP+52]
          mov EDI,DWORD PTR [ESP+56]
          test ESI,ESI
          mov DWORD PTR [ESP+8],EBX
          mov EDX,ECX
          mov EAX,EDI
          jne L_447f80
          cmp EDI,ECX
          ja L_448002
          test EDI,EDI
          mov EBP,EDI
          jne L_447f5c
          mov EAX,1
          xor EDX,EDX
          div EDI
          mov EBP,EAX
L_447f5c:
          mov EAX,ECX
          xor EDX,EDX
          div EBP
          mov ECX,EAX
          mov EAX,EBX
          mov EDI,ECX
          div EBP
          mov EBX,EAX
L_447f6c:
          mov EAX,EBX
          mov EDX,EDI
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_447f80:
          cmp ESI,ECX
          ja L_447ff2
          bsr EDI,ESI
          xor EDI,31
          je L_448020
          mov EBX,32
          mov ECX,EDI
          mov EBP,EAX
          sub EBX,EDI
          shl ESI,CL
          mov ECX,EBX
          shr EBP,CL
          mov ECX,EDI
          shl EAX,CL
          or ESI,EBP
          mov ECX,EBX
          mov DWORD PTR [ESP+12],EAX
          mov EBP,EDX
          mov EAX,DWORD PTR [ESP+8]
          shr EBP,CL
          mov ECX,EDI
          shl EDX,CL
          mov ECX,EBX
          shr EAX,CL
          or EDX,EAX
          mov EAX,EDX
          mov EDX,EBP
          div ESI
          mov EBP,EDX
          mov EBX,EAX
          mul DWORD PTR [ESP+12]
          cmp EBP,EDX
          jb L_447fe1
          mov ESI,DWORD PTR [ESP+8]
          mov ECX,EDI
          shl ESI,CL
          cmp ESI,EAX
          jae L_447fe4
          cmp EBP,EDX
          jne L_447fe4
L_447fe1:
          sub EBX,1
L_447fe4:
          xor EDI,EDI
          mov EAX,EBX
          mov EDX,EDI
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_447ff2:
          xor EDI,EDI
          xor EBX,EBX
          mov EAX,EBX
          mov EDX,EDI
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_448002:
          mov EAX,EBX
          div EDI
          xor EDI,EDI
          mov EBX,EAX
          mov EAX,EBX
          mov EDX,EDI
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_448020:
          cmp ESI,ECX
          jb L_448030
          xor EBX,EBX
          cmp EAX,DWORD PTR [ESP+8]
          ja L_447f6c
L_448030:
          mov EBX,1
          jmp L_447f6c
          .byte 0x90
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
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long ___udivdi3 - .
          .byte 0x1a
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
          .byte 0x4c
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
          .byte 0x49
          .byte 0xb
          .byte 0x2
          .byte 0x6d
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
          .byte 0x4b
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
          .byte 0x4f
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
          .byte 0x4b
          .byte 0xb
          .byte 0x0
          .byte 0x0
