# crypto/rc4_skey.s -- RC4 key setup; RC4_options() "rc4(idx,int)"
#
# original placement:
#   .eh_frame      0046d8c0-0046d92c
#   .rdata         00462960-00462980
#   .rdata$zzz     00464118-00464144
#   .text          004429c0-00442b00

.intel_syntax noprefix
.globl FUN_4429d0

.text
.p2align 4
L_4429c0:
          mov EAX,OFFSET L_462960
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_4429d0:
          push EBP
          push EDI
          xor EAX,EAX
          push ESI
          push EBX
          sub ESP,8
          mov EDX,DWORD PTR [ESP+28]
          lea EBP,DWORD PTR [EDX+8]
L_4429e0:
          mov DWORD PTR [EBP+EAX*4],EAX
          add EAX,1
          cmp EAX,256
          jne L_4429e0
          lea EAX,DWORD PTR [EDX+1032]
          xor EBX,EBX
          mov DWORD PTR [EDX],0
          mov DWORD PTR [EDX+4],0
          mov ESI,EBP
          mov EDX,EBX
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EBP
          xor EAX,EAX
L_442a10:
          mov EBP,DWORD PTR [ESI]
          mov ECX,DWORD PTR [ESP+36]
          lea EBX,DWORD PTR [EDX+1]
          lea EDI,DWORD PTR [EDX+2]
          add EAX,EBP
          add AL,BYTE PTR [ECX+EDX*1]
          cmp EBX,DWORD PTR [ESP+32]
          mov EDX,1
          cmove EDI,EDX
          mov EDX,DWORD PTR [ESP]
          movzx EAX,AL
          cmp DWORD PTR [ESP+32],EDI
          lea EDX,DWORD PTR [EDX+EAX*4]
          mov ECX,DWORD PTR [EDX]
          mov DWORD PTR [ESI],ECX
          mov DWORD PTR [EDX],EBP
          lea EBP,DWORD PTR [EDI+1]
          mov ECX,1
          mov EDX,DWORD PTR [ESI+4]
          cmove EBP,ECX
          cmp EBX,DWORD PTR [ESP+32]
          mov ECX,0
          cmove EBX,ECX
          mov ECX,DWORD PTR [ESP+36]
          movzx EBX,BYTE PTR [ECX+EBX*1]
          add EBX,EDX
          add EAX,EBX
          mov EBX,DWORD PTR [ESP]
          cmp DWORD PTR [ESP+32],EBP
          movzx EAX,AL
          lea EBX,DWORD PTR [EBX+EAX*4]
          mov ECX,DWORD PTR [EBX]
          mov DWORD PTR [ESI+4],ECX
          mov DWORD PTR [EBX],EDX
          lea EDX,DWORD PTR [EBP+1]
          mov ECX,1
          mov EBX,DWORD PTR [ESI+8]
          cmove EDX,ECX
          cmp DWORD PTR [ESP+32],EDI
          mov ECX,0
          cmovne ECX,EDI
          mov EDI,DWORD PTR [ESP+36]
          movzx ECX,BYTE PTR [EDI+ECX*1]
          add ECX,EBX
          add EAX,ECX
          mov ECX,DWORD PTR [ESP]
          cmp DWORD PTR [ESP+32],EBP
          movzx EAX,AL
          lea ECX,DWORD PTR [ECX+EAX*4]
          mov EDI,DWORD PTR [ECX]
          mov DWORD PTR [ESI+8],EDI
          mov EDI,0
          mov DWORD PTR [ECX],EBX
          cmove EBP,EDI
          mov EDI,DWORD PTR [ESP+36]
          mov ECX,DWORD PTR [ESI+12]
          movzx EBX,BYTE PTR [EDI+EBP*1]
          mov EDI,0
          add EBX,ECX
          add EAX,EBX
          mov EBX,DWORD PTR [ESP]
          cmp DWORD PTR [ESP+32],EDX
          movzx EAX,AL
          lea EBX,DWORD PTR [EBX+EAX*4]
          cmove EDX,EDI
          add ESI,16
          mov EBP,DWORD PTR [EBX]
          mov DWORD PTR [ESI-4],EBP
          cmp DWORD PTR [ESP+4],ESI
          mov DWORD PTR [EBX],ECX
          jne L_442a10
          add ESP,8
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.section .rdata,"dr"
.p2align 5
L_462960:
          .string "rc4(idx,int)"
          .zero 19

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
          .long L_4429c0 - .
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4429d0 - .
          .byte 0x2c
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
          .byte 0x43
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
          .byte 0x1c
          .byte 0x3
          .byte 0x1e
          .byte 0x1
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
