# crypto/rc4_enc.s -- RC4 stream (OpenSSL RC4())
#
# original placement:
#   .eh_frame      0046d868-0046d8c0
#   .rdata$zzz     004640ec-00464118
#   .text          00442630-004429c0

.intel_syntax noprefix
.globl FUN_442630

.text
.p2align 4
FUN_442630:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov ESI,DWORD PTR [ESP+40]
          mov ECX,DWORD PTR [ESP+36]
          mov EAX,DWORD PTR [ESP+36]
          shr ESI,3
          add ECX,8
          test ESI,ESI
          mov EDX,DWORD PTR [EAX]
          mov DWORD PTR [ESP+12],ESI
          mov EAX,DWORD PTR [EAX+4]
          je L_442815
          mov DWORD PTR [ESP+8],ESI
          mov ESI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],ESI
          mov ESI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],ESI
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_442670:
          add EDX,1
          movzx EDX,DL
          lea EDI,DWORD PTR [ECX+EDX*4]
          add EDX,1
          movzx EDX,DL
          mov EBX,DWORD PTR [EDI]
          add EAX,EBX
          movzx EAX,AL
          lea EBP,DWORD PTR [ECX+EAX*4]
          mov ESI,DWORD PTR [EBP]
          mov DWORD PTR [EDI],ESI
          mov DWORD PTR [EBP],EBX
          add EBX,ESI
          mov ESI,DWORD PTR [ESP]
          movzx EBX,BL
          mov EDI,DWORD PTR [ESP+4]
          mov EBX,DWORD PTR [ECX+EBX*4]
          xor BL,BYTE PTR [ESI]
          mov BYTE PTR [EDI],BL
          lea EDI,DWORD PTR [ECX+EDX*4]
          add EDX,1
          movzx EDX,DL
          mov EBX,DWORD PTR [EDI]
          add EAX,EBX
          movzx EAX,AL
          lea EBP,DWORD PTR [ECX+EAX*4]
          mov ESI,DWORD PTR [EBP]
          mov DWORD PTR [EDI],ESI
          mov DWORD PTR [EBP],EBX
          add EBX,ESI
          mov ESI,DWORD PTR [ESP]
          movzx EBX,BL
          mov EDI,DWORD PTR [ESP+4]
          mov EBX,DWORD PTR [ECX+EBX*4]
          xor BL,BYTE PTR [ESI+1]
          mov BYTE PTR [EDI+1],BL
          lea EDI,DWORD PTR [ECX+EDX*4]
          add EDX,1
          movzx EDX,DL
          mov EBX,DWORD PTR [EDI]
          add EAX,EBX
          movzx EAX,AL
          lea EBP,DWORD PTR [ECX+EAX*4]
          mov ESI,DWORD PTR [EBP]
          mov DWORD PTR [EDI],ESI
          mov DWORD PTR [EBP],EBX
          add EBX,ESI
          mov ESI,DWORD PTR [ESP]
          movzx EBX,BL
          mov EDI,DWORD PTR [ESP+4]
          mov EBX,DWORD PTR [ECX+EBX*4]
          xor BL,BYTE PTR [ESI+2]
          mov BYTE PTR [EDI+2],BL
          lea EDI,DWORD PTR [ECX+EDX*4]
          add EDX,1
          movzx EDX,DL
          mov EBX,DWORD PTR [EDI]
          add EAX,EBX
          movzx EAX,AL
          lea EBP,DWORD PTR [ECX+EAX*4]
          mov ESI,DWORD PTR [EBP]
          mov DWORD PTR [EDI],ESI
          mov DWORD PTR [EBP],EBX
          add EBX,ESI
          movzx EBX,BL
          mov EBX,DWORD PTR [ECX+EBX*4]
          mov ESI,DWORD PTR [ESP]
          mov EDI,DWORD PTR [ESP+4]
          xor BL,BYTE PTR [ESI+3]
          mov BYTE PTR [EDI+3],BL
          lea EDI,DWORD PTR [ECX+EDX*4]
          add EDX,1
          movzx EDX,DL
          mov EBX,DWORD PTR [EDI]
          add EAX,EBX
          movzx EAX,AL
          lea EBP,DWORD PTR [ECX+EAX*4]
          mov ESI,DWORD PTR [EBP]
          mov DWORD PTR [EDI],ESI
          mov DWORD PTR [EBP],EBX
          add EBX,ESI
          mov ESI,DWORD PTR [ESP]
          movzx EBX,BL
          mov EDI,DWORD PTR [ESP+4]
          mov EBX,DWORD PTR [ECX+EBX*4]
          xor BL,BYTE PTR [ESI+4]
          mov BYTE PTR [EDI+4],BL
          lea EDI,DWORD PTR [ECX+EDX*4]
          add EDX,1
          movzx EDX,DL
          mov EBX,DWORD PTR [EDI]
          add EAX,EBX
          movzx EAX,AL
          lea EBP,DWORD PTR [ECX+EAX*4]
          mov ESI,DWORD PTR [EBP]
          mov DWORD PTR [EDI],ESI
          mov DWORD PTR [EBP],EBX
          add EBX,ESI
          mov ESI,DWORD PTR [ESP]
          movzx EBX,BL
          mov EDI,DWORD PTR [ESP+4]
          mov EBX,DWORD PTR [ECX+EBX*4]
          xor BL,BYTE PTR [ESI+5]
          mov BYTE PTR [EDI+5],BL
          lea EDI,DWORD PTR [ECX+EDX*4]
          add EDX,1
          movzx EDX,DL
          mov EBX,DWORD PTR [EDI]
          add EAX,EBX
          movzx EAX,AL
          lea EBP,DWORD PTR [ECX+EAX*4]
          mov ESI,DWORD PTR [EBP]
          mov DWORD PTR [EDI],ESI
          mov DWORD PTR [EBP],EBX
          add EBX,ESI
          mov ESI,DWORD PTR [ESP]
          movzx EBX,BL
          mov EDI,DWORD PTR [ESP+4]
          mov EBX,DWORD PTR [ECX+EBX*4]
          xor BL,BYTE PTR [ESI+6]
          mov BYTE PTR [EDI+6],BL
          lea EDI,DWORD PTR [ECX+EDX*4]
          mov EBX,DWORD PTR [EDI]
          add EAX,EBX
          movzx EAX,AL
          lea EBP,DWORD PTR [ECX+EAX*4]
          mov ESI,DWORD PTR [EBP]
          mov DWORD PTR [EDI],ESI
          mov DWORD PTR [EBP],EBX
          add EBX,ESI
          mov ESI,DWORD PTR [ESP]
          movzx EBX,BL
          mov EDI,DWORD PTR [ESP+4]
          mov EBX,DWORD PTR [ECX+EBX*4]
          xor BL,BYTE PTR [ESI+7]
          add ESI,8
          add EDI,8
          mov DWORD PTR [ESP],ESI
          mov BYTE PTR [EDI-1],BL
          sub DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EDI
          jne L_442670
          mov EBX,DWORD PTR [ESP+12]
          shl EBX,3
          add DWORD PTR [ESP+44],EBX
          add DWORD PTR [ESP+48],EBX
L_442815:
          mov ESI,DWORD PTR [ESP+40]
          and ESI,7
          mov DWORD PTR [ESP],ESI
          je L_4429ae
          add EDX,1
          movzx EDX,DL
          lea EBP,DWORD PTR [ECX+EDX*4]
          mov EBX,DWORD PTR [EBP]
          add EAX,EBX
          movzx EAX,AL
          lea EDI,DWORD PTR [ECX+EAX*4]
          mov ESI,DWORD PTR [EDI]
          mov DWORD PTR [EBP],ESI
          mov DWORD PTR [EDI],EBX
          add EBX,ESI
          mov EDI,DWORD PTR [ESP+44]
          movzx EBX,BL
          mov EBX,DWORD PTR [ECX+EBX*4]
          xor BL,BYTE PTR [EDI]
          cmp DWORD PTR [ESP],1
          mov EDI,DWORD PTR [ESP+48]
          mov BYTE PTR [EDI],BL
          je L_4429ae
          add EDX,1
          movzx EDX,DL
          lea EBP,DWORD PTR [ECX+EDX*4]
          mov EBX,DWORD PTR [EBP]
          add EAX,EBX
          movzx EAX,AL
          lea EDI,DWORD PTR [ECX+EAX*4]
          mov ESI,DWORD PTR [EDI]
          mov DWORD PTR [EBP],ESI
          mov DWORD PTR [EDI],EBX
          add EBX,ESI
          mov EDI,DWORD PTR [ESP+44]
          movzx EBX,BL
          mov EBX,DWORD PTR [ECX+EBX*4]
          xor BL,BYTE PTR [EDI+1]
          cmp DWORD PTR [ESP],2
          mov EDI,DWORD PTR [ESP+48]
          mov BYTE PTR [EDI+1],BL
          je L_4429ae
          add EDX,1
          movzx EDX,DL
          lea EBP,DWORD PTR [ECX+EDX*4]
          mov EBX,DWORD PTR [EBP]
          add EAX,EBX
          movzx EAX,AL
          lea EDI,DWORD PTR [ECX+EAX*4]
          mov ESI,DWORD PTR [EDI]
          mov DWORD PTR [EBP],ESI
          mov DWORD PTR [EDI],EBX
          add EBX,ESI
          mov EDI,DWORD PTR [ESP+44]
          movzx EBX,BL
          mov EBX,DWORD PTR [ECX+EBX*4]
          xor BL,BYTE PTR [EDI+2]
          cmp DWORD PTR [ESP],3
          mov EDI,DWORD PTR [ESP+48]
          mov BYTE PTR [EDI+2],BL
          je L_4429ae
          add EDX,1
          movzx EDX,DL
          lea EBP,DWORD PTR [ECX+EDX*4]
          mov EBX,DWORD PTR [EBP]
          add EAX,EBX
          movzx EAX,AL
          lea EDI,DWORD PTR [ECX+EAX*4]
          mov ESI,DWORD PTR [EDI]
          mov DWORD PTR [EBP],ESI
          mov DWORD PTR [EDI],EBX
          add EBX,ESI
          mov EDI,DWORD PTR [ESP+44]
          movzx EBX,BL
          mov EBX,DWORD PTR [ECX+EBX*4]
          xor BL,BYTE PTR [EDI+3]
          cmp DWORD PTR [ESP],4
          mov EDI,DWORD PTR [ESP+48]
          mov BYTE PTR [EDI+3],BL
          je L_4429ae
          add EDX,1
          movzx EDX,DL
          lea EBP,DWORD PTR [ECX+EDX*4]
          mov EBX,DWORD PTR [EBP]
          add EAX,EBX
          movzx EAX,AL
          lea EDI,DWORD PTR [ECX+EAX*4]
          mov ESI,DWORD PTR [EDI]
          mov DWORD PTR [EBP],ESI
          mov DWORD PTR [EDI],EBX
          add EBX,ESI
          mov EDI,DWORD PTR [ESP+44]
          movzx EBX,BL
          mov EBX,DWORD PTR [ECX+EBX*4]
          xor BL,BYTE PTR [EDI+4]
          cmp DWORD PTR [ESP],5
          mov EDI,DWORD PTR [ESP+48]
          mov BYTE PTR [EDI+4],BL
          je L_4429ae
          add EDX,1
          movzx EDX,DL
          lea EBP,DWORD PTR [ECX+EDX*4]
          mov EBX,DWORD PTR [EBP]
          add EAX,EBX
          movzx EAX,AL
          lea EDI,DWORD PTR [ECX+EAX*4]
          mov ESI,DWORD PTR [EDI]
          mov DWORD PTR [EBP],ESI
          mov DWORD PTR [EDI],EBX
          add EBX,ESI
          mov EDI,DWORD PTR [ESP+44]
          movzx EBX,BL
          mov EBX,DWORD PTR [ECX+EBX*4]
          xor BL,BYTE PTR [EDI+5]
          cmp DWORD PTR [ESP],6
          mov EDI,DWORD PTR [ESP+48]
          mov BYTE PTR [EDI+5],BL
          je L_4429ae
          add EDX,1
          movzx EDX,DL
          lea EBP,DWORD PTR [ECX+EDX*4]
          mov EBX,DWORD PTR [EBP]
          add EAX,EBX
          movzx EAX,AL
          lea EDI,DWORD PTR [ECX+EAX*4]
          mov ESI,DWORD PTR [EDI]
          mov DWORD PTR [EBP],ESI
          mov DWORD PTR [EDI],EBX
          add EBX,ESI
          mov ESI,DWORD PTR [ESP+44]
          movzx EBX,BL
          mov ECX,DWORD PTR [ECX+EBX*4]
          xor CL,BYTE PTR [ESI+6]
          mov ESI,DWORD PTR [ESP+48]
          mov BYTE PTR [ESI+6],CL
L_4429ae:
          mov ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [ECX],EDX
          mov DWORD PTR [ECX+4],EAX
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
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
          .long FUN_442630 - .
          .byte 0x8f
          .byte 0x3
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
          .byte 0x24
          .byte 0x3
          .byte 0x83
          .byte 0x3
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
