# app/bootloaders.s -- CB/CF/CD/CE decryption, pairing, FCRT, bootloader signature checks
#
# original placement:
#   .eh_frame      00465130-00465650
#   .rdata         0044c064-0044c6e8
#   .rdata$zzz     00463778-004637a4
#   .text          00401630-004030b0

.intel_syntax noprefix
.globl FUN_401630
.globl FUN_401730
.globl FUN_4017d0
.globl FUN_401a00
.globl FUN_401ce0
.globl FUN_401dc0
.globl FUN_401e60
.globl FUN_402020
.globl FUN_402210
.globl FUN_402410
.globl FUN_402720
.globl FUN_402a00

.text
.p2align 4
FUN_401630:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,92
          mov EDI,DWORD PTR [ESP+112]
          lea EBX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+32],EBX
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+16],0
          lea EBP,DWORD PTR [EDI+16]
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET _cpuKey
          mov BYTE PTR [ESP+62],7
          mov BYTE PTR [ESP+63],18
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [ESP+116]
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],16
          lea ESI,DWORD PTR [EAX-16]
          mov DWORD PTR [ESP+12],ESI
          call _XeCryptRc4
          lea EAX,DWORD PTR [ESP+62]
          mov DWORD PTR [ESP+32],EBX
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],2
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET _cpuKey
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],16
          call _memcmp
          test EAX,EAX
          sete AL
          add ESP,92
          pop EBX
          movzx EAX,AL
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_401730:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+28],2035184962
          mov EBP,EAX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+68]
          test EAX,EAX
          mov DWORD PTR [ESP+12],EAX
          je L_4017ac
          mov ESI,EBP
          mov EBX,66
          add EBP,EAX
          mov EDI,1
          mov EAX,117
          jmp L_401775
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_401770:
          movzx EBX,BYTE PTR [ESP+ECX*1+28]
L_401775:
          movzx EDX,BYTE PTR [ESI]
          and EDI,3
          add ESI,1
          mov ECX,EDX
          imul EDX,EDX,251
          xor ECX,EBX
          mov BYTE PTR [ESI-1],CL
          mov ECX,EDI
          add EAX,EDX
          sar EDX,8
          mov BYTE PTR [ESP+EDI*1+28],AL
          lea EDI,DWORD PTR [EDI+1]
          mov EAX,EDX
          mov EBX,EDI
          and EBX,3
          add AL,BYTE PTR [ESP+EBX*1+28]
          cmp ESI,EBP
          mov BYTE PTR [ESP+EBX*1+28],AL
          jne L_401770
L_4017ac:
          mov ESI,DWORD PTR [ESP+12]
          mov EAX,DWORD PTR [ESP+8]
          mov DWORD PTR [ESP+68],4
          lea EAX,DWORD PTR [EAX+ESI*1-4]
          mov DWORD PTR [ESP+64],EAX
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _checkZeros
FUN_4017d0:
          push EBP
          push EDI
          xor EBP,EBP
          push ESI
          push EBX
          sub ESP,92
          mov EBX,DWORD PTR [ESP+112]
          movzx EDX,BYTE PTR [EBX]
          and EDX,67
          cmp DL,67
          je L_4017f2
L_4017e8:
          add ESP,92
          mov EAX,EBP
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4017f2:
          cmp BYTE PTR [EBX+1],66
          jne L_4017e8
          lea EAX,DWORD PTR [EBX+12]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          lea ESI,DWORD PTR [EAX+15]
          and ESI,4294967280
          mov DWORD PTR [ESP],ESI
          call _malloc
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EBX
          mov EDI,EAX
          mov DWORD PTR [ESP],EAX
          add EBX,16
          sub ESI,32
          call _memcpy
          lea EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          lea EBX,DWORD PTR [EDI+32]
          mov DWORD PTR [ESP+32],EAX
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a10c
          mov DWORD PTR [ESP+60],EAX
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],EAX
          call _XeCryptRc4
          lea EAX,DWORD PTR [EDI+624]
          mov DWORD PTR [ESP+4],288
          mov DWORD PTR [ESP],EAX
          call _checkZeros
          test EAX,EAX
          jne L_4018e0
          mov DWORD PTR [ESP+4],OFFSET L_44c09c
          mov DWORD PTR [ESP],0
          call _log_printf
L_4018ca:
          mov DWORD PTR [ESP],EDI
          call _free
          jmp L_4017e8
L_4018d7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4018e0:
          mov DWORD PTR [ESP],EBX
          call _getBeU32
          xor AL,AL
          mov DWORD PTR [ESP+4],OFFSET L_44c064
          mov DWORD PTR [ESP],1
          mov EBP,EAX
          mov DWORD PTR [ESP+8],EBP
          call _log_printf
          jmp L_4018ca
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_401910:
          push EDI
          push ESI
          xor EAX,EAX
          push EBX
          sub ESP,64
          mov EBX,DWORD PTR [ESP+80]
          movzx EDX,BYTE PTR [EBX]
          and EDX,67
          cmp DL,67
          je L_401930
L_401927:
          add ESP,64
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x66
          .byte 0x90
L_401930:
          cmp BYTE PTR [EBX+1],70
          jne L_401927
          lea EAX,DWORD PTR [EBX+12]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          lea ESI,DWORD PTR [EAX+15]
          and ESI,4294967280
          cmp DWORD PTR [ESP+84],ESI
          jae L_401951
L_40194d:
          xor EAX,EAX
          jmp L_401927
L_401951:
          lea EAX,DWORD PTR [EBX+32]
          lea EDI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          sub ESI,48
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a10c
          call _XeCryptHmacSha
          lea EAX,DWORD PTR [EBX+48]
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptRc4
          lea EAX,DWORD PTR [EBX+496]
          mov DWORD PTR [ESP+4],32
          mov DWORD PTR [ESP],EAX
          call _checkZeros
          test EAX,EAX
          je L_40194d
          add EBX,540
          mov DWORD PTR [ESP],EBX
          call _getBeU32
          jmp L_401927
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_401a00:
          push EBP
          push EDI
          push ESI
          push EBX
          xor ESI,ESI
          sub ESP,92
          mov EBX,DWORD PTR [ESP+116]
          cmp EBX,131072
          jbe L_401a20
          add ESP,92
          mov EAX,ESI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_401a20:
          mov DWORD PTR [ESP],EBX
          call _malloc
          mov EDI,EAX
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          movzx EAX,BYTE PTR [EDI]
          and EAX,67
          cmp AL,67
          je L_401b73
L_401a4c:
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EDI
          add EAX,EBX
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          movzx EAX,BYTE PTR [EDI]
          and EAX,67
          cmp AL,67
          je L_401a80
L_401a6c:
          mov DWORD PTR [ESP],EDI
          xor ESI,ESI
          call _free
          add ESP,92
          mov EAX,ESI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_401a80:
          cmp BYTE PTR [EDI+1],70
          jne L_401a6c
          lea EBP,DWORD PTR [EDI+12]
          xor ESI,ESI
          mov BYTE PTR [ESP+60],0
L_401a90:
          mov DWORD PTR [ESP],EBP
          call _getBeU32
          lea EBP,DWORD PTR [EAX+15]
          and EBP,4294967280
          cmp EBX,EBP
          jb L_401bc4
          lea EAX,DWORD PTR [EDI+32]
          lea EBX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          sub EBP,48
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+32],EBX
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a10c
          call _XeCryptHmacSha
          lea EAX,DWORD PTR [EDI+48]
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptRc4
          lea EAX,DWORD PTR [EDI+496]
          mov DWORD PTR [ESP+4],32
          mov DWORD PTR [ESP],EAX
          call _checkZeros
          test EAX,EAX
          je L_401bc4
          lea EAX,DWORD PTR [EDI+540]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          test EAX,EAX
          mov EBX,EAX
          je L_401cce
          mov EBP,EAX
          shr EAX,8
          mov DWORD PTR [ESP+4],OFFSET L_44c110
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BL
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_401bc8
L_401b73:
          cmp BYTE PTR [EDI+1],70
          jne L_401a4c
          lea EBP,DWORD PTR [EDI+12]
          mov DWORD PTR [ESP],EBP
          call _getBeU32
          lea ESI,DWORD PTR [EAX+15]
          and ESI,4294967280
          cmp EBX,ESI
          jae L_401be3
L_401b92:
          xor ESI,ESI
          mov BYTE PTR [ESP+60],0
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_401ba0:
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EDI
          add EAX,EBX
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          movzx EAX,BYTE PTR [EDI]
          and EAX,67
          cmp AL,67
          je L_401cbf
L_401bc4:
          xor EBX,EBX
          xor EBP,EBP
L_401bc8:
          mov DWORD PTR [ESP],EDI
          call _free
          mov EAX,EBP
          cmp AL,BYTE PTR [ESP+60]
          cmovae ESI,EBX
          add ESP,92
          pop EBX
          mov EAX,ESI
          pop ESI
          pop EDI
          pop EBP
          ret 
L_401be3:
          lea EDX,DWORD PTR [ESP+64]
          lea EAX,DWORD PTR [EDI+32]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          sub ESI,48
          mov DWORD PTR [ESP+32],EDX
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a10c
          mov DWORD PTR [ESP+60],EDX
          call _XeCryptHmacSha
          mov EDX,DWORD PTR [ESP+60]
          lea EAX,DWORD PTR [EDI+48]
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],EDX
          call _XeCryptRc4
          lea EAX,DWORD PTR [EDI+496]
          mov DWORD PTR [ESP+4],32
          mov DWORD PTR [ESP],EAX
          call _checkZeros
          test EAX,EAX
          je L_401b92
          lea EAX,DWORD PTR [EDI+540]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          test EAX,EAX
          mov ESI,EAX
          je L_401a4c
          mov BYTE PTR [ESP+60],AL
          shr EAX,8
          mov DWORD PTR [ESP+4],OFFSET L_44c0dc
          mov DWORD PTR [ESP+12],EAX
          mov EAX,ESI
          mov DWORD PTR [ESP],1
          movzx EAX,AL
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_401ba0
L_401cbf:
          cmp BYTE PTR [EDI+1],70
          jne L_401bc4
          jmp L_401a90
L_401cce:
          xor EBP,EBP
          jmp L_401bc8
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_401ce0:
          push EDI
          push ESI
          push EBX
          sub ESP,64
          mov EBX,DWORD PTR [ESP+80]
          movzx EAX,BYTE PTR [EBX]
          and EAX,67
          cmp AL,67
          je L_401d00
L_401cf4:
          xor EAX,EAX
L_401cf6:
          add ESP,64
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_401d00:
          cmp BYTE PTR [EBX+1],70
          jne L_401cf4
          lea EAX,DWORD PTR [EBX+12]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          lea ESI,DWORD PTR [EAX+15]
          and ESI,4294967280
          cmp ESI,DWORD PTR [ESP+84]
          ja L_401cf4
          lea EAX,DWORD PTR [EBX+32]
          lea EDI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          sub ESI,48
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a10c
          call _XeCryptHmacSha
          lea EAX,DWORD PTR [EBX+48]
          mov DWORD PTR [ESP+12],ESI
          add EBX,496
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptRc4
          mov DWORD PTR [ESP+4],32
          mov DWORD PTR [ESP],EBX
          call _checkZeros
          mov EDX,1
          test EAX,EAX
          cmovne EAX,EDX
          jmp L_401cf6
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_401dc0:
          push ESI
          push EBX
          sub ESP,68
          mov EBX,DWORD PTR [ESP+80]
          lea ESI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+32],ESI
          mov DWORD PTR [ESP+20],0
          lea EAX,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          add EBX,32
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP],EAX
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],16
          sub EAX,32
          mov DWORD PTR [ESP+12],EAX
          call _XeCryptRc4
          mov DWORD PTR [ESP],EBX
          call _getBeU32
          cmp EAX,1179648
          sete AL
          add ESP,68
          movzx EAX,AL
          pop EBX
          pop ESI
          ret 
L_401e57:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_401e60:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,108
          mov ESI,DWORD PTR [ESP+128]
          lea EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          lea EDI,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+32],EAX
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+16],0
          lea EBP,DWORD PTR [ESI+16]
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET _cpuKey
          mov DWORD PTR [ESP+60],EAX
          mov DWORD PTR [ESP+80],0
          mov DWORD PTR [ESP+84],0
          mov DWORD PTR [ESP+88],0
          mov DWORD PTR [ESP+92],0
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [ESP+132]
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],16
          lea EBX,DWORD PTR [EAX-16]
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP],EAX
          call _XeCryptRc4
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET _cpuKey
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],16
          call _memcmp
          test EAX,EAX
          sete AL
          add ESP,108
          pop EBX
          movzx EAX,AL
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_401f80:
          mov EAX,DWORD PTR [L_47a144]
          test EAX,EAX
          je L_401fb0
          sub ESP,44
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          cmp EAX,1129466960
          je L_401fc0
          mov EAX,1
L_401fa4:
          add ESP,44
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_401fb0:
          mov EAX,1
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_401fc0:
          mov EAX,DWORD PTR [L_47a144]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+48]
          add EAX,32
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EAX
          call _XeKeysPkcs1Verify
          test EAX,EAX
          mov DWORD PTR [ESP+28],EAX
          jne L_402002
          mov DWORD PTR [ESP+4],OFFSET L_44c14e
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+28]
          jmp L_401fa4
L_402002:
          mov DWORD PTR [ESP+4],OFFSET L_44c143
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+28]
          jmp L_401fa4
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_402020:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,588
          mov EDX,DWORD PTR [ESP+616]
          mov EBX,DWORD PTR [ESP+608]
          mov EDI,DWORD PTR [ESP+612]
          test EDX,EDX
          je L_402170
          lea ESI,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+4],OFFSET _cpuKey
          mov DWORD PTR [ESP],ESI
          call _XeCryptAesKey
L_40205b:
          lea EBP,DWORD PTR [ESP+36]
          lea EAX,DWORD PTR [EBX+304]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],EAX
          call _XeCryptAesEcb
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [EBX+304],EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [EBX+308],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [EBX+312],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [EBX+316],EAX
          mov DWORD PTR [ESP+4],EBP
          lea EBP,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],ESI
          call _XeCryptAesKey
          mov EAX,DWORD PTR [EBX+288]
          mov DWORD PTR [ESP+52],EAX
          mov EAX,DWORD PTR [EBX+292]
          mov DWORD PTR [ESP+56],EAX
          mov EAX,DWORD PTR [EBX+296]
          mov DWORD PTR [ESP+60],EAX
          mov EAX,DWORD PTR [EBX+300]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [ESP+8],16
          mov DWORD PTR [ESP+64],EAX
          lea EAX,DWORD PTR [EBX+320]
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+4],EAX
          call _XeCryptAesCbc
          lea EAX,DWORD PTR [EBX+336]
          lea EDX,DWORD PTR [EDI-336]
          mov DWORD PTR [ESP],ESI
          lea ESI,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],EAX
          call _XeCryptAesCbc
          mov DWORD PTR [ESP+20],ESI
          mov DWORD PTR [ESP+16],336
          mov DWORD PTR [ESP+12],20
          mov DWORD PTR [ESP+8],12
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          call FUN_41db70
          test EAX,EAX
          jne L_402190
L_402163:
          add ESP,588
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_402170:
          lea ESI,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+4],OFFSET L_47a12c
          mov DWORD PTR [ESP],ESI
          call _XeCryptAesKey
          jmp L_40205b
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_402190:
          mov EAX,DWORD PTR [L_47a144]
          test EAX,EAX
          je L_4021a8
          mov DWORD PTR [ESP],EBX
          call _getBeU32
          cmp EAX,1129466960
          je L_4021c0
L_4021a8:
          add ESP,588
          mov EAX,1
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
L_4021c0:
          mov EAX,DWORD PTR [L_47a144]
          add EBX,32
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],EAX
          call _XeKeysPkcs1Verify
          test EAX,EAX
          jne L_4021f2
          mov DWORD PTR [ESP+4],OFFSET L_44c14e
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4021a8
L_4021f2:
          mov DWORD PTR [ESP+4],OFFSET L_44c143
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_402163
FUN_402210:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,556
          mov EBX,DWORD PTR [ESP+580]
          mov ESI,DWORD PTR [ESP+576]
          mov EBP,DWORD PTR [ESP+584]
          mov DWORD PTR [ESP],EBX
          call _malloc
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],ESI
          mov EDI,EAX
          mov DWORD PTR [ESP],EAX
          call _memcpy
          test EBP,EBP
          mov DWORD PTR [ESP+40],0
          mov DWORD PTR [ESP+44],0
          mov DWORD PTR [ESP+48],0
          mov DWORD PTR [ESP+52],0
          jne L_4022d0
          lea EBP,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+4],OFFSET L_47a12c
          mov DWORD PTR [ESP],EBP
          call _XeCryptAesKey
L_402281:
          lea EAX,DWORD PTR [ESP+40]
          add ESI,304
          sub EBX,304
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+16],EAX
          lea EAX,DWORD PTR [EDI+304]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+4],EAX
          call _XeCryptAesCbc
          mov DWORD PTR [ESP+576],EDI
          add ESP,556
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _free
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4022d0:
          lea EBP,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+4],OFFSET _cpuKey
          mov DWORD PTR [ESP],EBP
          call _XeCryptAesKey
          jmp L_402281
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4022f0:
          mov EAX,DWORD PTR [L_47a144]
          test EAX,EAX
          je L_402400
          push EBX
          mov EAX,1
          sub ESP,120
          cmp DWORD PTR [ESP+132],287
          jbe L_4023d8
          mov EDX,DWORD PTR [ESP+128]
          lea EAX,DWORD PTR [ESP+76]
          lea EBX,DWORD PTR [ESP+92]
          mov DWORD PTR [ESP+36],20
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+32],EBX
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],32
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+76],0
          mov DWORD PTR [ESP+80],0
          mov DWORD PTR [ESP+84],0
          mov DWORD PTR [ESP+88],0
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [L_47a144]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+128]
          add EAX,32
          mov DWORD PTR [ESP+4],EAX
          call _XeKeysPkcs1Verify
          mov DWORD PTR [ESP+60],EAX
          test EAX,EAX
          mov EAX,DWORD PTR [ESP+136]
          mov DWORD PTR [ESP+8],EAX
          je L_4023e0
          mov DWORD PTR [ESP+4],OFFSET L_44c168
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+60]
L_4023d8:
          add ESP,120
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4023e0:
          mov DWORD PTR [ESP+4],OFFSET L_44c176
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+60]
          add ESP,120
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_402400:
          mov EAX,1
          ret 
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_402410:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,124
          mov EBX,DWORD PTR [ESP+148]
          mov ECX,DWORD PTR [ESP+144]
          test EBX,EBX
          je L_402500
          xor ESI,ESI
          xor EDI,EDI
L_402431:
          lea EBX,DWORD PTR [ECX+EDI*1]
          cmp BYTE PTR [EBX],68
          jne L_402440
          cmp BYTE PTR [ECX+EDI*1+1],65
          je L_402464
L_402440:
          mov DWORD PTR [ESP+4],OFFSET L_44c1c0
          mov DWORD PTR [ESP],1
          call _log_printf
L_402454:
          xor EAX,EAX
          cmp ESI,2
          sete AL
L_40245c:
          add ESP,124
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_402464:
          cmp BYTE PTR [ECX+EDI*1+2],69
          jne L_402440
          cmp BYTE PTR [ECX+EDI*1+3],80
          jne L_402440
          movzx EAX,BYTE PTR [ECX+EDI*1+4]
          movzx EBP,BYTE PTR [ECX+EDI*1+5]
          add ESI,1
          mov EDX,DWORD PTR [L_47a144]
          shl EAX,8
          add EAX,EBP
          test EDX,EDX
          movzx EBP,AX
          je L_402497
          cmp AX,287
          ja L_402507
L_402497:
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+60],ECX
          call FUN_402210
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],336
          mov DWORD PTR [ESP+12],20
          mov DWORD PTR [ESP+8],12
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBX
          call FUN_41db70
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+60]
          je L_4025c0
L_4024e7:
          add EDI,EBP
          cmp DWORD PTR [ESP+148],EDI
          ja L_402431
          jmp L_402454
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_402500:
          xor EAX,EAX
          jmp L_40245c
L_402507:
          lea EAX,DWORD PTR [ESP+92]
          mov DWORD PTR [ESP+36],20
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+32],EAX
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],32
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+60],ECX
          mov DWORD PTR [ESP+76],0
          mov DWORD PTR [ESP+80],0
          mov DWORD PTR [ESP+84],0
          mov DWORD PTR [ESP+88],0
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [L_47a144]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [EBX+32]
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+92]
          mov DWORD PTR [ESP],EAX
          call _XeKeysPkcs1Verify
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+60]
          je L_4025e9
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44c168
          mov DWORD PTR [ESP],1
          call _log_printf
          mov ECX,DWORD PTR [ESP+60]
          jmp L_402497
L_4025c0:
          mov DWORD PTR [ESP+4],OFFSET L_44c188
          mov DWORD PTR [ESP],1
          xor ESI,ESI
          call _log_printf
          mov EAX,DWORD PTR [ESP+148]
          mov ECX,DWORD PTR [ESP+60]
          lea EDI,DWORD PTR [EAX+1]
          jmp L_4024e7
L_4025e9:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44c176
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+60],ECX
          call _log_printf
          mov ECX,DWORD PTR [ESP+60]
          jmp L_402497
          .byte 0x66
          .byte 0x90
L_402610:
          push EDI
          push ESI
          push EBX
          sub ESP,80
          mov ESI,DWORD PTR [ESP+96]
          lea EAX,DWORD PTR [ESI+272]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          mov EBX,DWORD PTR [L_47a144]
          test EAX,EAX
          cmovns EBX,DWORD PTR [_masterPub]
          test EBX,EBX
          je L_4026f0
          lea EAX,DWORD PTR [ESI+256]
          lea EDI,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+36],20
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],64
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET _cpuKey
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EDI
          call _XeKeysPkcs1Verify
          test EAX,EAX
          mov EBX,EAX
          jne L_4026d0
          mov DWORD PTR [ESP+4],OFFSET L_44c200
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,80
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4026d0:
          mov DWORD PTR [ESP+4],OFFSET L_44c143
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,80
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4026f0:
          mov DWORD PTR [ESP+4],OFFSET L_44c214
          mov DWORD PTR [ESP],1
          mov EBX,1
          call _log_printf
          add ESP,80
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_402720:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,604
          mov EBX,DWORD PTR [ESP+624]
          lea EAX,DWORD PTR [EBX+272]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          mov ESI,DWORD PTR [L_47a144]
          test EAX,EAX
          cmovns ESI,DWORD PTR [_masterPub]
          test ESI,ESI
          je L_4029b0
          lea EAX,DWORD PTR [EBX+256]
          lea EDI,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP+36],20
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],64
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET _cpuKey
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EDI
          call _XeKeysPkcs1Verify
          test EAX,EAX
          jne L_402830
          mov DWORD PTR [ESP+4],OFFSET L_44c200
          mov DWORD PTR [ESP],1
          call _log_printf
L_4027d4:
          mov EAX,DWORD PTR [EBX+256]
          cmp DWORD PTR [ESP+628],16384
          mov DWORD PTR [ESP+68],EAX
          mov EAX,DWORD PTR [EBX+260]
          mov DWORD PTR [ESP+72],EAX
          mov EAX,DWORD PTR [EBX+264]
          mov DWORD PTR [ESP+76],EAX
          mov EAX,DWORD PTR [EBX+268]
          mov DWORD PTR [ESP+80],EAX
          je L_402850
          mov DWORD PTR [ESP+4],OFFSET L_44c250
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
L_40281f:
          add ESP,604
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_402830:
          mov DWORD PTR [ESP+4],OFFSET L_44c143
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4027d4
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_402850:
          lea EAX,DWORD PTR [EBX+284]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          cmp EAX,16383
          ja L_4029d0
          mov ESI,DWORD PTR [ESP+628]
          lea EDI,DWORD PTR [EBX+EAX*1]
          lea EBP,DWORD PTR [ESP+84]
          add EBX,300
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+24],EBP
          mov DWORD PTR [ESP+16],0
          sub ESI,EAX
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EDI
          call _XeCryptSha
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBX
          call _memcmp
          test EAX,EAX
          je L_402990
          lea EAX,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP+4],OFFSET _cpuKey
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+60],EAX
          call _XeCryptAesKey
          mov EAX,DWORD PTR [ESP+60]
          lea EDX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          call _XeCryptAesCbc
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+24],EBP
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EDI
          call _XeCryptSha
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBX
          call _memcmp
          mov EDX,EAX
          mov EAX,1
          test EDX,EDX
          je L_40281f
          mov DWORD PTR [ESP+4],OFFSET L_44c2c0
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
          jmp L_40281f
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_402990:
          mov DWORD PTR [ESP+4],OFFSET L_44c2a2
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_40281f
          .byte 0x66
          .byte 0x90
L_4029b0:
          mov DWORD PTR [ESP+4],OFFSET L_44c214
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4027d4
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4029d0:
          mov DWORD PTR [ESP+4],OFFSET L_44c278
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,604
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4029f1:
          jmp FUN_402a00
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
FUN_402a00:
          push ESI
          push EBX
          sub ESP,68
          mov ESI,DWORD PTR [ESP+80]
          lea EBX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+24],EBX
          mov DWORD PTR [ESP+12],0
          lea EAX,DWORD PTR [ESI+20]
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],492
          mov DWORD PTR [ESP],EAX
          call _XeCryptSha
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],20
          call _memcmp
          test EAX,EAX
          sete AL
          add ESP,68
          movzx EAX,AL
          pop EBX
          pop ESI
          ret 
          .byte 0x66
          .byte 0x90
L_402a70:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov ESI,DWORD PTR [ESP+96]
          mov EBP,DWORD PTR [ESP+104]
          test ESI,ESI
          je L_402c4f
          movzx EAX,BYTE PTR [ESI]
          and EAX,67
          cmp AL,67
          jne L_402bc0
          cmp BYTE PTR [ESI+1],66
          jne L_402bc0
          lea EAX,DWORD PTR [ESI+12]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          lea EDI,DWORD PTR [EAX+15]
          mov DWORD PTR [ESP+4],1
          and EDI,4294967280
          mov DWORD PTR [ESP],EDI
          call _calloc
          test EAX,EAX
          mov EBX,EAX
          je L_402c25
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP+8],EDI
          lea ESI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call _memcpy
          lea EAX,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+32],ESI
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a10c
          call _XeCryptHmacSha
          lea EAX,DWORD PTR [EDI-32]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [EBX+32]
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptRc4
          test EBP,EBP
          je L_402b6b
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [EBP],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [EBP+4],EAX
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [EBP+8],EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [EBP+12],EAX
L_402b6b:
          mov EAX,DWORD PTR [L_47a13c]
          test EAX,EAX
          je L_402be0
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EBX
          call _cbVerifySig
          test EAX,EAX
          movzx EAX,BYTE PTR [EBX]
          mov DWORD PTR [ESP+8],EAX
          je L_402c05
          mov DWORD PTR [ESP+4],OFFSET L_44c2fc
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDX,DWORD PTR [ESP+100]
          test EDX,EDX
          je L_402bad
L_402ba7:
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [EAX],EDI
L_402bad:
          add ESP,76
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_402bb7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_402bc0:
          mov DWORD PTR [ESP+4],OFFSET L_44c3f0
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call _log_printf
          add ESP,76
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_402be0:
          movzx EAX,BYTE PTR [EBX]
          mov DWORD PTR [ESP+4],OFFSET L_44c370
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+100]
          test EAX,EAX
          jne L_402ba7
          jmp L_402bad
L_402c05:
          mov DWORD PTR [ESP+4],OFFSET L_44c328
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP],EBX
          xor EBX,EBX
          call _free
          jmp L_402bad
L_402c25:
          movzx EAX,BYTE PTR [ESI+1]
          xor EBX,EBX
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [ESI]
          mov DWORD PTR [ESP+4],OFFSET L_44c3b8
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_402bad
L_402c4f:
          mov DWORD PTR [ESP+4],OFFSET L_44c424
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call _log_printf
          jmp L_402bad
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_402c70:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EBP,DWORD PTR [ESP+96]
          mov EDI,DWORD PTR [ESP+116]
          test EBP,EBP
          je L_402e50
          mov EAX,DWORD PTR [ESP+108]
          test EAX,EAX
          je L_402e50
          movzx EAX,BYTE PTR [EBP]
          and EAX,67
          cmp AL,67
          jne L_402df3
          movzx EAX,BYTE PTR [EBP+1]
          sub EAX,67
          cmp AL,1
          ja L_402df3
          lea EAX,DWORD PTR [EBP+12]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          lea ESI,DWORD PTR [EAX+15]
          mov DWORD PTR [ESP+4],1
          and ESI,4294967280
          mov DWORD PTR [ESP],ESI
          call _calloc
          test EAX,EAX
          mov EBX,EAX
          je L_402e93
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP+8],ESI
          lea EBP,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+108]
          lea EDX,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+32],EBP
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          call _XeCryptHmacSha
          lea EDX,DWORD PTR [ESI-32]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+12],EDX
          lea EDX,DWORD PTR [EBX+32]
          mov DWORD PTR [ESP+8],EDX
          call _XeCryptRc4
          test EDI,EDI
          je L_402d7c
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [EDI],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [EDI+4],EAX
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [EDI+8],EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [EDI+12],EAX
L_402d7c:
          mov EDI,DWORD PTR [ESP+100]
          test EDI,EDI
          je L_402e13
          mov ECX,DWORD PTR [ESP+104]
          test ECX,ECX
          .byte 0x0f,0x84; .long L_402e13-.-4   # je L_402e13
          mov EAX,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP+8],EAX
          call _blVerifySig
          test EAX,EAX
          movzx EAX,BYTE PTR [EBX+1]
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [EBX]
          mov DWORD PTR [ESP+8],EAX
          je L_402e70
          mov DWORD PTR [ESP+4],OFFSET L_44c45c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDX,DWORD PTR [ESP+112]
          test EDX,EDX
          je L_402e09
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [EAX],ESI
L_402de9:
          add ESP,76
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_402df3:
          mov DWORD PTR [ESP+4],OFFSET L_44c518
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call _log_printf
L_402e09:
          add ESP,76
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_402e13:
          movzx EAX,BYTE PTR [EBX+1]
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [EBX]
          mov DWORD PTR [ESP+4],OFFSET L_44c4d0
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+112]
          test EAX,EAX
          je L_402e09
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [EAX],ESI
          jmp L_402de9
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_402e50:
          mov DWORD PTR [ESP+4],OFFSET L_44c54c
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call _log_printf
          jmp L_402e09
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_402e70:
          mov DWORD PTR [ESP+4],OFFSET L_44c488
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP],EBX
          xor EBX,EBX
          call _free
          jmp L_402e09
L_402e93:
          movzx EAX,BYTE PTR [EBP+1]
          xor EBX,EBX
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [EBP]
          mov DWORD PTR [ESP+4],OFFSET L_44c3b8
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_402e09
          .byte 0x66
          .byte 0x90
L_402ec0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EBP,DWORD PTR [ESP+96]
          mov EDI,DWORD PTR [ESP+104]
          test EBP,EBP
          je L_403065
          test EDI,EDI
          je L_403065
          movzx EAX,BYTE PTR [EBP]
          and EAX,67
          cmp AL,67
          jne L_403000
          cmp BYTE PTR [EBP+1],69
          jne L_403000
          lea EAX,DWORD PTR [EBP+12]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          lea ESI,DWORD PTR [EAX+15]
          mov DWORD PTR [ESP+4],1
          and ESI,4294967280
          mov DWORD PTR [ESP],ESI
          call _calloc
          test EAX,EAX
          mov EBX,EAX
          je L_403045
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP+8],ESI
          lea EBP,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call _memcpy
          lea EAX,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+32],EBP
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],EDI
          call _XeCryptHmacSha
          lea EAX,DWORD PTR [ESI-32]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [EBX+32]
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptRc4
          mov ECX,DWORD PTR [ESP+108]
          test ECX,ECX
          je L_403020
          mov EAX,DWORD PTR [ESP+108]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call _blCheckHash
          test EAX,EAX
          movzx EAX,BYTE PTR [EBX+1]
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [EBX]
          mov DWORD PTR [ESP+8],EAX
          je L_403080
          mov DWORD PTR [ESP+4],OFFSET L_44c588
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDX,DWORD PTR [ESP+100]
          test EDX,EDX
          je L_402ff5
L_402fef:
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [EAX],ESI
L_402ff5:
          add ESP,76
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_403000:
          mov DWORD PTR [ESP+4],OFFSET L_44c67c
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call _log_printf
          add ESP,76
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_403020:
          movzx EAX,BYTE PTR [EBX]
          mov DWORD PTR [ESP+4],OFFSET L_44c5fc
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+100]
          test EAX,EAX
          jne L_402fef
          jmp L_402ff5
L_403045:
          movzx EAX,BYTE PTR [EBP]
          mov DWORD PTR [ESP+4],OFFSET L_44c644
          xor EBX,EBX
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_402ff5
L_403065:
          mov DWORD PTR [ESP+4],OFFSET L_44c6b0
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call _log_printf
          jmp L_402ff5
L_403080:
          mov DWORD PTR [ESP+4],OFFSET L_44c5b4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP],EBX
          xor EBX,EBX
          call _free
          jmp L_402ff5
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.section .rdata,"dr"
.p2align 2
L_44c064:
          .string "CB decrypted OK, pairing bytes extracted as: 0x%08x\n"
          .zero 3
L_44c09c:
          .string "***** WARNING: CB decrypt failed! Unable to get pairing data!\n"
          .zero 1
L_44c0dc:
          .string "CF slot 0 decrypted ok LDV 0x%02x Pairing: 0x%06x\n"
          .zero 1
L_44c110:
          .string "CF slot 1 decrypted ok LDV 0x%02x Pairing: 0x%06x\n"
L_44c143:
          .string "sig good! "
L_44c14e:
          .string "\nsignature check FAILED!\n"
L_44c168:
          .string "sig %d good! "
L_44c176:
          .string "\nsig %d FAIL! "
          .zero 3
L_44c188:
          .string "\n******* ERROR: dae hash incorrect, could not decrypt!\n"
L_44c1c0:
          .string "\n******* ERROR: dae segment does not have the expected header!\n"
L_44c200:
          .string "\nsignature FAILED!\n"
L_44c214:
          .string "pub key to verify signature is not available, skipping!\n"
          .zero 3
L_44c250:
          .string "**** ERROR: FCRT decrypt invalid size!\n"
L_44c278:
          .string "**** ERROR: FCRT decrypt invalid offset!\n"
L_44c2a2:
          .string "FCRT was already decrypted..."
L_44c2c0:
          .string "\n******* ERROR: FCRT hash check failed, could not decrypt!\n"
L_44c2fc:
          .string "%cB signature OK! Decryption successful!\n"
          .zero 2
L_44c328:
          .string "***** ERROR: %cB signature invalid, corrupted or decryption failed!\n"
          .zero 3
L_44c370:
          .string "***** WARNING: could not check %cB signature, 1BL RSA key not loaded!\n"
          .zero 1
L_44c3b8:
          .string "***** WARNING: Unable to allocate 0x%x bytes for %c%c!\n"
L_44c3f0:
          .string "***** WARNING: CB/SB does not have valid magic!\n"
          .zero 3
L_44c424:
          .string "***** WARNING: CB/SB decrypt not provided with data!\n"
          .zero 2
L_44c45c:
          .string "%c%c signature OK! Decryption successful!\n"
          .zero 1
L_44c488:
          .string "***** ERROR: %c%c signature invalid, corrupted or decryption failed!\n"
          .zero 2
L_44c4d0:
          .string "***** WARNING: could not check %c%c signature, 1BL RSA key not loaded!\n"
L_44c518:
          .string "***** WARNING: SC/SD/CD does not have valid magic!\n"
L_44c54c:
          .string "***** WARNING: SC/SD/CD decrypt not provided with data!\n"
          .zero 3
L_44c588:
          .string "%c%c hash check OK! Decryption successful!\n"
L_44c5b4:
          .string "***** ERROR: %c%c hash check invalid, corrupted or decryption failed!\n"
          .zero 1
L_44c5fc:
          .string "***** WARNING: could not check %cE signature, 1BL RSA key not loaded!\n"
          .zero 1
L_44c644:
          .string "***** WARNING: Unable to allocate 0x%x bytes for %cE!\n"
          .zero 1
L_44c67c:
          .string "***** WARNING: SE/CE does not have valid magic!\n"
          .zero 3
L_44c6b0:
          .string "***** WARNING: SE/CE decrypt not provided with data!\n"
          .zero 2

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
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_401630 - .
          .byte 0xf3
          .byte 0x0
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
          .byte 0x70
          .byte 0x2
          .byte 0xe4
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x44
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
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x58
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_401730 - .
          .byte 0xa0
          .byte 0x0
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
          .byte 0x90
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x94
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4017d0 - .
          .byte 0x36
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
          .byte 0x70
          .byte 0x52
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
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_401910 - .
          .byte 0xe3
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
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x43
          .byte 0xe
          .byte 0x50
          .byte 0x52
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x41
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
          .byte 0x43
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_401a00 - .
          .byte 0xd5
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
          .byte 0x45
          .byte 0xe
          .byte 0x70
          .byte 0x4f
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
          .byte 0x42
          .byte 0xb
          .byte 0x2
          .byte 0x59
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
          .byte 0x5c
          .byte 0x1
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x43
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
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7c
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_401ce0 - .
          .byte 0xd3
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
          .byte 0x43
          .byte 0xe
          .byte 0x50
          .byte 0x53
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x41
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
          .byte 0x44
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_401dc0 - .
          .byte 0x97
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0x50
          .byte 0x2
          .byte 0x8c
          .byte 0xe
          .byte 0xc
          .byte 0x44
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe0
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_401e60 - .
          .byte 0x1b
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
          .byte 0x80
          .byte 0x1
          .byte 0x3
          .byte 0xc
          .byte 0x1
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x44
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
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_401f80 - .
          .byte 0x9c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4c
          .byte 0xe
          .byte 0x30
          .byte 0x5b
          .byte 0xe
          .byte 0x4
          .byte 0x59
          .byte 0xe
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_402020 - .
          .byte 0xf0
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
          .byte 0x46
          .byte 0xe
          .byte 0xe0
          .byte 0x4
          .byte 0x3
          .byte 0x3f
          .byte 0x1
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
          .byte 0x43
          .byte 0xb
          .byte 0x7e
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x46
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
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x94
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_402210 - .
          .byte 0xd6
          .byte 0x0
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
          .byte 0x46
          .byte 0xe
          .byte 0xc0
          .byte 0x4
          .byte 0x2
          .byte 0xaa
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
          .byte 0x48
          .byte 0xb
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd4
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_4022f0 - .
          .byte 0x16
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4e
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x48
          .byte 0xe
          .byte 0x80
          .byte 0x1
          .byte 0x2
          .byte 0xd5
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x5b
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_402410 - .
          .byte 0xfe
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
          .byte 0x90
          .byte 0x1
          .byte 0x2
          .byte 0x48
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long L_402610 - .
          .byte 0x2
          .byte 0x1
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
          .byte 0x43
          .byte 0xe
          .byte 0x60
          .byte 0x2
          .byte 0xac
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x43
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
          .byte 0x49
          .byte 0xb
          .byte 0x57
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x43
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
          .byte 0x44
          .byte 0xb
          .byte 0x5c
          .byte 0xe
          .byte 0x10
          .byte 0x43
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x98
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_402720 - .
          .byte 0xd1
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
          .byte 0x46
          .byte 0xe
          .byte 0xf0
          .byte 0x4
          .byte 0x2
          .byte 0xfb
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
          .byte 0x47
          .byte 0xb
          .byte 0x3
          .byte 0xba
          .byte 0x1
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf0
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_402a00 - .
          .byte 0x6e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0x50
          .byte 0x2
          .byte 0x63
          .byte 0xe
          .byte 0xc
          .byte 0x44
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long L_402a70 - .
          .byte 0xfa
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
          .byte 0x60
          .byte 0x3
          .byte 0x39
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
          .byte 0x4a
          .byte 0xb
          .byte 0x59
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x74
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long L_402c70 - .
          .byte 0x4e
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
          .byte 0x60
          .byte 0x3
          .byte 0x75
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
          .byte 0x59
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xcc
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long L_402ec0 - .
          .byte 0xe3
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
          .byte 0x60
          .byte 0x3
          .byte 0x31
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
          .byte 0x42
          .byte 0xb
          .byte 0x59
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
