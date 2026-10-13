# bigdigits/spDivide.s -- 64/32 digit division
#
# original placement:
#   .eh_frame      0046de40-0046deb0
#   .rdata$zzz     0046424c-00464278
#   .text          00446830-00446a40

.intel_syntax noprefix
.globl FUN_446830

.text
.p2align 4
FUN_446830:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,20
          mov EAX,DWORD PTR [ESP+52]
          test EAX,EAX
          js L_446862
          mov EAX,DWORD PTR [ESP+44]
          mov EBX,4294967295
          mov DWORD PTR [EAX],0
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [EAX],0
          add ESP,20
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_446862:
          movzx EAX,WORD PTR [ESP+52]
          xor EDX,EDX
          mov ESI,EAX
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+52]
          shr EAX,16
          mov EBX,EAX
          mov DWORD PTR [ESP],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov ECX,DWORD PTR [EAX]
          movzx EAX,CX
          shr ECX,16
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+16],ECX
          mov ECX,DWORD PTR [EAX+4]
          mov EBP,ECX
          shr EBP,16
          mov EAX,EBP
          div EBX
          test EAX,EAX
          mov EBX,EAX
          je L_4468b7
          shl EDX,16
          movzx EAX,CX
          or EDX,EAX
          cmp ESI,EDX
          jbe L_4469e2
L_4468b5:
          xor EBX,EBX
L_4468b7:
          xor EDX,EDX
          mov EAX,ECX
          div DWORD PTR [ESP]
          cmp EAX,65536
          mov ESI,EAX
          je L_4468e1
          mov EDI,DWORD PTR [ESP+4]
          imul EDI,EAX
          mov DWORD PTR [ESP+8],EDI
          mov EDI,EDX
          shl EDI,16
          or EDI,DWORD PTR [ESP+16]
          cmp EDI,DWORD PTR [ESP+8]
          jae L_4468fe
L_4468e1:
          mov EDI,DWORD PTR [ESP+4]
          lea ESI,DWORD PTR [EAX-1]
          add EDX,DWORD PTR [ESP]
          imul EDI,ESI
          cmp EDX,65535
          mov DWORD PTR [ESP+8],EDI
          jbe L_446a10
L_4468fe:
          mov EAX,DWORD PTR [ESP]
          shl ECX,16
          mov EDI,DWORD PTR [ESP+8]
          or ECX,DWORD PTR [ESP+16]
          imul EAX,ESI
          mov EDX,EAX
          shl EDX,16
          add EDI,EDX
          sub ECX,EDI
          not EDI
          cmp EDI,ECX
          sbb EBP,0
          shr EAX,16
          sub EBP,EAX
          mov EAX,EBP
          shr EAX,16
          test EAX,EAX
          je L_446934
          add ECX,DWORD PTR [ESP+52]
          sub ESI,1
L_446934:
          xor EDX,EDX
          mov EAX,ECX
          shl ESI,16
          div DWORD PTR [ESP]
          mov DWORD PTR [ESP+8],ESI
          cmp EAX,65536
          mov ESI,EAX
          je L_44695f
          mov EDI,DWORD PTR [ESP+4]
          mov EBP,EDX
          shl EBP,16
          or EBP,DWORD PTR [ESP+12]
          imul EDI,EAX
          cmp EBP,EDI
          jae L_446990
L_44695f:
          add EDX,DWORD PTR [ESP]
          lea ESI,DWORD PTR [EAX-1]
          cmp EDX,65535
          ja L_446a02
          mov EBP,DWORD PTR [ESP+4]
          shl EDX,16
          or EDX,DWORD PTR [ESP+12]
          mov EDI,EBP
          imul EDI,ESI
          cmp EDX,EDI
          jae L_446990
          lea ESI,DWORD PTR [EAX-2]
          sub EDI,EBP
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_446990:
          mov EBP,DWORD PTR [ESP]
          mov EAX,ECX
          shl ECX,16
          or ECX,DWORD PTR [ESP+12]
          shr EAX,16
          imul EBP,ESI
          mov EDX,EBP
          shl EDX,16
          add EDI,EDX
          sub ECX,EDI
          not EDI
          cmp EDI,ECX
          sbb EAX,0
          shr EBP,16
          sub EAX,EBP
          shr EAX,16
          test EAX,EAX
          je L_4469c5
          add ECX,DWORD PTR [ESP+52]
          sub ESI,1
L_4469c5:
          movzx ESI,SI
          or ESI,DWORD PTR [ESP+8]
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [EAX],ESI
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [EAX],ECX
          add ESP,20
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4469e2:
          mov EAX,ECX
          mov EDX,DWORD PTR [ESP+52]
          sub EAX,DWORD PTR [ESP+52]
          not EDX
          cmp EAX,EDX
          ja L_4468b5
          mov EBP,EAX
          mov ECX,EAX
          shr EBP,16
          jmp L_4468b7
L_446a02:
          mov EDI,DWORD PTR [ESP+4]
          imul EDI,ESI
          jmp L_446990
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_446a10:
          shl EDX,16
          or EDX,DWORD PTR [ESP+16]
          cmp EDX,EDI
          jae L_4468fe
          mov EDX,DWORD PTR [ESP+4]
          lea ESI,DWORD PTR [EAX-2]
          mov EAX,EDI
          sub EAX,EDX
          mov DWORD PTR [ESP+8],EAX
          jmp L_4468fe
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_446830 - .
          .byte 0x3
          .byte 0x2
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
          .byte 0x28
          .byte 0x64
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x43
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
          .byte 0x3
          .byte 0x79
          .byte 0x1
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x43
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
          .byte 0x0
