# app/filelist_ini.s -- "parsing ini at", file list ini labels
#
# mixed: `#@C name` lines are functions from filelist_ini.c (re/splice.py)
#
# original placement:
#   .data          0044a020-0044a480
#   .eh_frame      00466040-004663b0
#   .rdata         0044fb60-00450420
#   .rdata$zzz     00463828-00463854
#   .text          00408ec0-0040b130

.intel_syntax noprefix
.globl FUN_409430
.globl FUN_40aad0
.globl FUN_40abf0
.globl FUN_40acf0
.globl FUN_40ade0
.globl FUN_40aef0
.globl L_450000

.text
.p2align 4
FUN_408ec0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,2124
          lea EBP,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],OFFSET L_47ad4c
          mov DWORD PTR [ESP],EBP
          call _strcpy
          mov DWORD PTR [ESP],EBP
          call FUN_4481c0
          test EAX,EAX
          je L_408f77
          lea ESI,DWORD PTR [ESP+1088]
          mov EDI,EAX
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_408f00:
          mov DWORD PTR [ESP],EDI
          call FUN_448360
          test EAX,EAX
          mov EBX,EAX
          je L_408f6f
L_408f0e:
          add EBX,8
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          call _strcpy
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call _strcat
          lea EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call FUN_448820
          test EAX,EAX
          js L_408f00
          mov DWORD PTR [ESP+4],OFFSET L_44a340
          mov DWORD PTR [ESP],EBX
          call FUN_4491d8
          test EAX,EAX
          jne L_408f82
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_44a340
          call _strcpy
          mov DWORD PTR [ESP],EDI
          call FUN_448360
          test EAX,EAX
          mov EBX,EAX
          jne L_408f0e
L_408f6f:
          mov DWORD PTR [ESP],EDI
          call FUN_448470
L_408f77:
          add ESP,2124
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_408f82:
          mov DWORD PTR [ESP+4],OFFSET L_44a360
          mov DWORD PTR [ESP],EBX
          call FUN_4491d8
          test EAX,EAX
          jne L_408fb0
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_44a360
          call _strcpy
          jmp L_408f00
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_408fb0:
          mov DWORD PTR [ESP+4],OFFSET L_44a3e0
          mov DWORD PTR [ESP],EBX
          call FUN_4491d8
          test EAX,EAX
          jne L_408f00
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_44a3e0
          call _strcpy
          jmp L_408f00
          .byte 0x8d
          .byte 0x76
          .byte 0x0
FUN_408fe0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EAX,DWORD PTR [ESP+84]
          mov EDI,DWORD PTR [ESP+80]
          add EAX,1
          mov ESI,EAX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+32],EAX
          call _malloc
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+40],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+84]
          test EAX,EAX
          jle L_4092ca
          mov EBP,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+28],0
          jmp L_40903d
          .byte 0x66
          .byte 0x90
L_409030:
          add EAX,1
          mov DWORD PTR [ESP+28],EAX
L_409037:
          cmp EBP,DWORD PTR [ESP+28]
          jle L_4090bb
L_40903d:
          mov EAX,DWORD PTR [ESP+28]
          cmp BYTE PTR [EDI+EAX*1],59
          jne L_409030
          mov EBX,EAX
          add EAX,1
          lea ECX,DWORD PTR [EDI+EAX*1]
          mov DWORD PTR [ESP+36],EAX
          movzx EDX,BYTE PTR [ECX]
          mov DWORD PTR [ESP+44],ECX
          cmp DL,255
          setne CL
          cmp DL,10
          setne DL
          test CL,DL
          je L_4092c3
          cmp EAX,EBP
          jge L_4092c3
          mov EAX,EBX
          xor EBX,EBX
          add EAX,2
          jmp L_409086
          .byte 0x90
L_409080:
          cmp EBP,EAX
          jle L_4090a0
          mov EAX,ESI
L_409086:
          movzx EDX,BYTE PTR [EDI+EAX*1]
          add EBX,1
          lea ESI,DWORD PTR [EAX+1]
          cmp DL,10
          setne CL
          cmp DL,255
          setne DL
          test CL,DL
          jne L_409080
L_4090a0:
          mov EDX,EBP
          sub EDX,DWORD PTR [ESP+36]
          sub EDX,EBX
          test EDX,EDX
          jg L_409270
          add DWORD PTR [ESP+28],2
          cmp EBP,DWORD PTR [ESP+28]
          jg L_40903d
L_4090bb:
          test EBP,EBP
          jle L_409256
          lea EAX,DWORD PTR [EDI+EBP*1]
          mov EBX,EDI
          mov DWORD PTR [ESP+28],EDI
          mov ESI,EAX
          .byte 0x66   # nop
          nop
L_4090d0:
          movzx ECX,BYTE PTR [EBX]
          mov EDX,65
          xor EAX,EAX
          jmp L_4090f3
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4090e0:
          add EAX,1
          cmp EAX,74
          je L_4092b0
          movzx EDX,BYTE PTR [EAX+L_450380]
L_4090f3:
          cmp CL,DL
          jne L_4090e0
          add EBX,1
          cmp ESI,EBX
          jne L_4090d0
L_4090fe:
          mov ESI,DWORD PTR [ESP+28]
          xor EAX,EAX
          jmp L_40911a
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_409110:
          add EAX,1
          add ESI,1
          cmp EBP,EAX
          je L_40913c
L_40911a:
          cmp BYTE PTR [ESI],59
          jne L_409110
          test EAX,EAX
          je L_40912f
          cmp BYTE PTR [ESI-1],10
          je L_40912f
          cmp BYTE PTR [ESI+1],10
          jne L_409110
L_40912f:
          add EAX,1
          mov BYTE PTR [ESI],32
          add ESI,1
          cmp EBP,EAX
          jne L_40911a
L_40913c:
          mov EAX,DWORD PTR [ESP+32]
          mov ESI,DWORD PTR [ESP+40]
          xor EBX,EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],ESI
          call _memcpy
          jmp L_409167
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_409160:
          add EBX,1
          cmp EBP,EBX
          jle L_4091ab
L_409167:
          lea EAX,DWORD PTR [EDI+EBX*1]
          cmp BYTE PTR [EAX],32
          jne L_409160
          mov EDX,EBP
          lea ECX,DWORD PTR [ESI+EBX*1+1]
          mov DWORD PTR [ESP],EAX
          sub EDX,EBX
          sub EBX,1
          sub EBP,1
          sub EDX,1
          mov DWORD PTR [ESP+4],ECX
          add EBX,1
          mov DWORD PTR [ESP+8],EDX
          call _memcpy
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call _memcpy
          cmp EBP,EBX
          jg L_409167
L_4091ab:
          test EBP,EBP
          je L_4092e6
          mov EAX,EDI
          lea ECX,DWORD PTR [EDI+EBP*1]
          jmp L_4091cc
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4091c0:
          cmp DL,59
          je L_4091d4
          add EAX,1
          cmp EAX,ECX
          je L_4091de
L_4091cc:
          movzx EDX,BYTE PTR [EAX]
          cmp DL,10
          jne L_4091c0
L_4091d4:
          mov BYTE PTR [EAX],0
          add EAX,1
          cmp EAX,ECX
          jne L_4091cc
L_4091de:
          mov EAX,DWORD PTR [ESP+32]
          mov ESI,DWORD PTR [ESP+40]
          xor EBX,EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],ESI
          call _memcpy
          jmp L_409206
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_409200:
          cmp EBP,EAX
          mov EBX,EAX
          jle L_409250
L_409206:
          lea EDX,DWORD PTR [EDI+EBX*1]
          lea EAX,DWORD PTR [EBX+1]
          cmp BYTE PTR [EDX],0
          jne L_409200
          cmp BYTE PTR [EDI+EBX*1+1],0
          jne L_409200
          mov ECX,EBP
          add EAX,ESI
          mov DWORD PTR [ESP],EDX
          sub ECX,EBX
          mov DWORD PTR [ESP+4],EAX
          sub EBP,1
          sub ECX,1
          mov DWORD PTR [ESP+8],ECX
          call _memcpy
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call _memcpy
          mov EAX,EBX
          cmp EBP,EAX
          mov EBX,EAX
          jg L_409206
L_409250:
          cmp DWORD PTR [ESP+84],EBP
          jl L_40925d
L_409256:
          mov BYTE PTR [EDI+EBP*1],0
          add EBP,1
L_40925d:
          add ESP,60
          mov EAX,EBP
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_409267:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_409270:
          mov ESI,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+8],EDX
          sub EBP,EBX
          add EAX,ESI
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+28],EAX
          jmp L_409037
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4092b0:
          mov BYTE PTR [EBX],32
          add EBX,1
          cmp ESI,EBX
          jne L_4090d0
          jmp L_4090fe
L_4092c3:
          xor EBX,EBX
          jmp L_4090a0
L_4092ca:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov EBP,DWORD PTR [ESP+84]
L_4092e6:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EAX
          call _memcpy
          jmp L_409250
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
L_409310:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EBP,DWORD PTR [ESP+72]
          mov EDI,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP],EBP
          call _strlen
          mov ECX,DWORD PTR [ESP+68]
          sub ECX,EAX
          test ECX,ECX
          mov DWORD PTR [ESP+28],ECX
          jle L_4093b0
          movsx ECX,BYTE PTR [EBP]
          lea ESI,DWORD PTR [EAX+1]
          mov DWORD PTR [ESP+20],ESI
          mov DWORD PTR [ESP+24],ECX
          xor ECX,ECX
          jmp L_409359
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_409350:
          add ECX,1
          cmp ECX,DWORD PTR [ESP+28]
          je L_4093b0
L_409359:
          movzx EDX,BYTE PTR [EDI+ECX*1]
          cmp EDX,DWORD PTR [ESP+24]
          jne L_409350
          xor EDX,EDX
          test EAX,EAX
          jg L_409383
          jmp L_40938a
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_409370:
          lea EBX,DWORD PTR [EDI+EDX*1]
          movzx ESI,BYTE PTR [EBX+ECX*1]
          movsx EBX,BYTE PTR [EBP+EDX*1]
          cmp ESI,EBX
          cmovne EDX,DWORD PTR [ESP+20]
L_409383:
          add EDX,1
          cmp EAX,EDX
          jg L_409370
L_40938a:
          cmp EAX,EDX
          jne L_409350
          mov EBX,DWORD PTR [ESP+76]
          lea EDX,DWORD PTR [EAX+ECX*1]
          test EBX,EBX
          jne L_4093bf
          cmp BYTE PTR [EDI+EDX*1],0
          je L_409350
L_40939f:
          add ESP,44
          mov EAX,EDX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4093b0:
          add ESP,44
          mov EDX,4294967295
          pop EBX
          mov EAX,EDX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4093bf:
          cmp BYTE PTR [EDI+EDX*1],1
          adc EDX,0
          jmp L_40939f
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4093d0:
          push ESI
          push EBX
          mov EBX,DWORD PTR [ESP+20]
          mov ESI,DWORD PTR [ESP+12]
          mov ECX,DWORD PTR [ESP+16]
          test EBX,EBX
          jle L_409402
          movzx EAX,BYTE PTR [ESI]
          movsx ECX,CL
          cmp EAX,ECX
          mov EAX,0
          jne L_4093fb
          jmp L_409407
L_4093f3:
          movzx EDX,BYTE PTR [ESI+EAX*1]
          cmp EDX,ECX
          je L_409407
L_4093fb:
          add EAX,1
          cmp EBX,EAX
          jne L_4093f3
L_409402:
          mov EAX,4294967295
L_409407:
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_409410:
          cmp BYTE PTR [L_47ad4c],0
          jne L_409420
          repz ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_409420:
          jmp FUN_408ec0
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
FUN_409430:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1180
          mov ESI,DWORD PTR [ESP+1200]
          mov DWORD PTR [ESP+4],OFFSET L_44fb60
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],ESI
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44fb84
          mov DWORD PTR [ESP],ESI
          call _fopen
          test EAX,EAX
          je L_409dbc
          mov DWORD PTR [ESP],EAX
          mov EBX,EAX
          call _getFileSize
          mov EDI,EAX
          lea EAX,DWORD PTR [EAX+1]
          mov DWORD PTR [ESP],EAX
          call _malloc
          test EAX,EAX
          mov DWORD PTR [ESP+44],EAX
          je L_409df5
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],1
          mov EBP,EAX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          call _fread
          mov DWORD PTR [ESP],EBX
          call _fclose
          cmp BYTE PTR [EBP],255
          je L_409732
          cmp BYTE PTR [EBP+1],255
          je L_409732
          mov ESI,DWORD PTR [ESP+44]
          mov BYTE PTR [ESI+EDI*1],255
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          call FUN_408fe0
          mov DWORD PTR [ESP+48],EAX
          mov BYTE PTR [ESI+EAX*1],0
          sub EAX,9
          test EAX,EAX
          mov EDI,EAX
          mov DWORD PTR [ESP+76],EAX
          jle L_40951f
          xor EAX,EAX
          mov EBX,10
          jmp L_409510
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_409500:
          add EAX,1
          cmp EAX,EDI
          je L_40951f
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_409510:
          xor EBP,EBP
          cmp BYTE PTR [ESI+EAX*1],91
          je L_409573
          add EAX,1
          cmp EAX,EDI
          jne L_409510
L_40951f:
          mov DWORD PTR [ESP+4],OFFSET L_44fcdc
L_409527:
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP+52],0
          mov EAX,DWORD PTR [ESP+52]
          add ESP,1180
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_409560:
          lea EDX,DWORD PTR [ESI+EBP*1]
          movzx ECX,BYTE PTR [EDX+EAX*1]
          movsx EDX,BYTE PTR [EBP+L_44fc48]
          cmp ECX,EDX
          cmovne EBP,EBX
L_409573:
          add EBP,1
          cmp EBP,8
          jle L_409560
          cmp EBP,9
          jne L_409500
          mov ESI,DWORD PTR [ESP+44]
          xor EDX,EDX
          mov EBX,OFFSET L_4c9364
          mov ECX,16
          mov EDI,EBX
          cmp BYTE PTR [ESI+EAX*1+9],0
          sete DL
          lea EDX,DWORD PTR [EDX+EAX*1+9]
          xor EAX,EAX
          rep stosd DWORD PTR ES:[EDI]
          add EDX,ESI
          jmp L_4095bc
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4095b0:
          add EAX,1
          cmp EAX,64
          je L_409deb
L_4095bc:
          cmp BYTE PTR [EDX+EAX*1],0
          jne L_4095b0
L_4095c2:
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],OFFSET L_4c9364
          call FUN_449060
          mov DWORD PTR [ESP+8],OFFSET L_4c9364
          mov DWORD PTR [ESP+4],OFFSET L_44fc52
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [_g479ea8]
          cmp EAX,2
          je L_40a161
          lea EDX,DWORD PTR [EAX-6]
          cmp EDX,1
          jbe L_40a698
          lea EDX,DWORD PTR [EAX-8]
          cmp EDX,1
          jbe L_40a6c9
          lea EDX,DWORD PTR [EAX-4]
          mov DWORD PTR [L_4c4f98],14
          cmp EDX,1
          jbe L_40a747
          cmp EAX,1
          mov DWORD PTR [L_479e84],OFFSET L_44a08c
          je L_40a1a5
          mov ESI,DWORD PTR [L_479eb4]
          test ESI,ESI
          jne L_40a11e
          mov EBX,DWORD PTR [L_479eb0]
          mov DWORD PTR [ESP+12],OFFSET L_47a94c
          mov DWORD PTR [ESP+8],OFFSET L_4c9364
          test EBX,EBX
          je L_40a111
          mov DWORD PTR [ESP+4],OFFSET L_44fcbf
L_409675:
          lea EAX,DWORD PTR [ESP+144]
          mov EBP,6
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+64],EAX
          call _sprintf
L_40968d:
          mov EAX,DWORD PTR [L_4c4f98]
          mov DWORD PTR [ESP],OFFSET L_47a94c
          sub EAX,2
          mov DWORD PTR [L_4c4f9c],EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],EAX
          call _strcpy
          cmp BYTE PTR [L_47ad4c],0
          jne L_409db2
L_4096bb:
          mov ECX,DWORD PTR [L_4c4f98]
          xor ESI,ESI
          xor EDI,EDI
          mov EBX,OFFSET L_4bbd50
          test ECX,ECX
          jle L_409798
L_4096d2:
          mov EAX,DWORD PTR [_g479ea8]
          cmp EAX,2
          je L_409a90
          lea EDX,DWORD PTR [EAX-6]
          cmp EDX,1
          jbe L_409c20
          lea EDX,DWORD PTR [EAX-4]
          cmp EDX,1
          jbe L_409c60
          lea EDX,DWORD PTR [EAX-8]
          cmp EDX,1
          jbe L_409ce0
          mov EDX,DWORD PTR [ESI+L_44a2a0+4]
          mov DWORD PTR [EBX+1028],EDX
          mov EDX,DWORD PTR [ESI+L_44a204+156]
          mov DWORD PTR [EBX+1032],EDX
L_40971c:
          cmp DWORD PTR [EBX+1028],27
          ja L_409780
          mov EDX,DWORD PTR [EBX+1028]
          jmp DWORD PTR [EDX*4+L_4501e8]
L_409732:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44fbe8
L_40973e:
          mov DWORD PTR [ESP],0
L_409745:
          call _log_printf
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP+52],0
L_40975e:
          mov EAX,DWORD PTR [ESP+52]
          add ESP,1180
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_409770:
          mov DWORD PTR [ESP+4],OFFSET L_44a400
          mov DWORD PTR [ESP],EBX
          call _strcpy
L_409780:
          add EDI,1
          add EBX,1068
          add ESI,8
          cmp DWORD PTR [L_4c4f98],EDI
          jg L_4096d2
L_409798:
          cmp BYTE PTR [L_4c4f54],0
          je L_409d55
          mov EAX,DWORD PTR [L_479ea4]
          mov DWORD PTR [ESP+12],OFFSET L_4c4f54
          mov DWORD PTR [ESP+4],OFFSET L_44fd1d
          and EAX,7
          mov EAX,DWORD PTR [EAX*4+L_450400]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+94]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+72],EAX
          call _sprintf
L_4097d8:
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP],EAX
          call _strlen
          mov EDI,DWORD PTR [ESP+48]
          sub EDI,EAX
          test EDI,EDI
          mov DWORD PTR [ESP+56],EDI
          jle L_40a0fc
          movsx EDI,BYTE PTR [ESP+94]
          mov DWORD PTR [ESP+60],EBP
          xor ECX,ECX
          mov EBP,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+52],EDI
          lea EDI,DWORD PTR [EAX+1]
          jmp L_40981d
          .byte 0x66
          .byte 0x90
L_409810:
          add ECX,1
          cmp ECX,DWORD PTR [ESP+56]
          je L_40a0fc
L_40981d:
          movzx EDX,BYTE PTR [EBP+ECX*1]
          cmp EDX,DWORD PTR [ESP+52]
          jne L_409810
          xor EDX,EDX
          test EAX,EAX
          jg L_409842
          jmp L_409849
L_409830:
          lea EBX,DWORD PTR [EBP+EDX*1]
          movzx ESI,BYTE PTR [EBX+ECX*1]
          movsx EBX,BYTE PTR [ESP+EDX*1+94]
          cmp ESI,EBX
          cmovne EDX,EDI
L_409842:
          add EDX,1
          cmp EAX,EDX
          jg L_409830
L_409849:
          cmp EAX,EDX
          jne L_409810
          mov EDI,DWORD PTR [ESP+44]
          add EAX,ECX
          mov EBP,DWORD PTR [ESP+60]
          cmp BYTE PTR [EDI+EAX*1],1
          mov DWORD PTR [ESP+4],OFFSET L_44fd2d
          mov DWORD PTR [ESP],1
          adc EAX,0
          mov EDI,EAX
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov ECX,DWORD PTR [ESP+48]
          sub ECX,EDI
          test ECX,ECX
          jle L_40a8c3
          mov EAX,DWORD PTR [ESP+44]
          xor EDX,EDX
          add EAX,EDI
          cmp BYTE PTR [EAX],91
          jne L_4098a6
          jmp L_4098b2
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4098a0:
          cmp BYTE PTR [EAX+EDX*1],91
          je L_4098b2
L_4098a6:
          add EDX,1
          cmp ECX,EDX
          jne L_4098a0
          mov EDX,4294967295
L_4098b2:
          xor ESI,ESI
          add EDX,EDI
          mov DWORD PTR [ESP+68],EBP
          mov DWORD PTR [ESP+60],EDX
          mov EBP,ESI
          mov ESI,EDI
L_4098c2:
          mov ECX,DWORD PTR [ESP+48]
          sub ECX,ESI
          test ECX,ECX
          jle L_409911
          movzx EBX,BYTE PTR [EAX]
          xor EDX,EDX
          cmp BL,44
          jne L_4098ea
          jmp L_4098fa
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4098e0:
          cmp BYTE PTR [EAX+EDX*1],44
          je L_409c03
L_4098ea:
          add EDX,1
          cmp ECX,EDX
          jne L_4098e0
          test BL,BL
          je L_409911
          mov EDX,4294967295
L_4098fa:
          xor EBX,EBX
          jmp L_40990a
          .byte 0x66
          .byte 0x90
L_409900:
          cmp BYTE PTR [EAX+EBX*1],0
          je L_409ab0
L_40990a:
          add EBX,1
          cmp ECX,EBX
          jne L_409900
L_409911:
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+4],OFFSET L_44fd44
          mov DWORD PTR [ESP+8],EAX
          jmp L_40973e
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_409930:
          mov DWORD PTR [ESP+4],OFFSET L_44a440
          mov DWORD PTR [ESP],EBX
          call _strcpy
          jmp L_409780
L_409945:
          cmp EAX,2
          je L_409d85
          mov DWORD PTR [ESP+4],OFFSET L_44a3a0
          mov DWORD PTR [ESP],EBX
          call _strcpy
          jmp L_409780
L_409963:
          mov DWORD PTR [ESP+4],OFFSET L_44a3e0
          mov DWORD PTR [ESP],EBX
          call _strcpy
          mov EAX,DWORD PTR [_g479ea8]
          cmp EAX,2
          je L_4099a7
          mov EDX,DWORD PTR [L_479eb0]
          test EDX,EDX
          je L_409cfd
          mov EAX,DWORD PTR [L_479eb4]
          mov DWORD PTR [ESP],EBX
          test EAX,EAX
          je L_409d9a
          call _strlen
          mov DWORD PTR [EBX+EAX*1],7156327
L_4099a7:
          mov EAX,DWORD PTR [L_479ea4]
          mov DWORD PTR [ESP],EBX
          and EAX,7
          mov EAX,DWORD PTR [EAX*4+L_450400]
          mov DWORD PTR [ESP+4],EAX
          call _strcat
L_4099c2:
          mov DWORD PTR [ESP+4],OFFSET L_47a14c
          mov DWORD PTR [ESP],EBX
          call _strcat
          cmp BYTE PTR [L_4c4f54],0
          jne L_409d40
L_4099df:
          mov DWORD PTR [ESP],EBX
          call _strlen
          add EAX,EBX
          mov DWORD PTR [EAX],1852400174
          mov BYTE PTR [EAX+4],0
          jmp L_409780
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_409a00:
          mov DWORD PTR [ESP+4],OFFSET L_44a420
          mov DWORD PTR [ESP],EBX
          call _strcpy
          jmp L_409780
L_409a15:
          mov DWORD PTR [ESP+4],OFFSET L_44a460
          mov DWORD PTR [ESP],EBX
          call _strcpy
          jmp L_409780
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_409a30:
          mov DWORD PTR [ESP+4],OFFSET L_44a320
          mov DWORD PTR [ESP],EBX
          call _strcpy
          jmp L_409780
L_409a45:
          mov DWORD PTR [ESP+4],OFFSET L_44a360
          mov DWORD PTR [ESP],EBX
          call _strcpy
          jmp L_409780
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_409a60:
          mov DWORD PTR [ESP+4],OFFSET L_44a340
          mov DWORD PTR [ESP],EBX
          call _strcpy
          jmp L_409780
L_409a75:
          mov DWORD PTR [ESP+4],OFFSET L_44a380
          mov DWORD PTR [ESP],EBX
          call _strcpy
          jmp L_409780
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_409a90:
          mov EDX,DWORD PTR [ESI+L_44a200+4]
          mov DWORD PTR [EBX+1028],EDX
          mov EDX,DWORD PTR [ESI+L_44a1a4+92]
          mov DWORD PTR [EBX+1032],EDX
          jmp L_40971c
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_409ab0:
          cmp EDX,EBX
          mov DWORD PTR [ESP+52],1
          jle L_409b80
L_409ac0:
          mov EDX,EBX
L_409ac2:
          lea EDI,DWORD PTR [EBP*4]
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP+56],EDI
          add EDI,DWORD PTR [L_479e84]
          imul EAX,DWORD PTR [EDI],1068
          add EAX,OFFSET L_4bbd50
          mov DWORD PTR [ESP],EAX
          call FUN_449060
          imul EAX,DWORD PTR [EDI],1068
          mov EDX,DWORD PTR [ESP+52]
          test EDX,EDX
          mov BYTE PTR [EBX+EAX*1+L_4bbd50],0
          lea EAX,DWORD PTR [EBX+ESI*1]
          lea ESI,DWORD PTR [EAX+1]
          jne L_409ba0
          mov EDX,DWORD PTR [ESP+48]
          mov ECX,DWORD PTR [ESP+44]
          sub EDX,ESI
          add ECX,ESI
          test EDX,EDX
          jle L_409b42
          cmp BYTE PTR [ECX],0
          je L_409c3d
          xor EBX,EBX
          add EAX,DWORD PTR [ESP+44]
          jmp L_409b3b
          .byte 0x90
L_409b30:
          cmp BYTE PTR [EAX+EBX*1+1],0
          je L_409c80
L_409b3b:
          add EBX,1
          cmp EDX,EBX
          jne L_409b30
L_409b42:
          imul EAX,DWORD PTR [EDI],1068
          mov DWORD PTR [ESP+4],OFFSET L_44fd78
          mov DWORD PTR [ESP],0
          add EAX,OFFSET L_4bbd50
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call _free
          jmp L_40975e
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_409b80:
          test EDX,EDX
          js L_409911
          mov EBX,EDX
          mov DWORD PTR [ESP+52],0
          jmp L_409ac0
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_409ba0:
          imul EAX,DWORD PTR [EDI],1068
          mov DWORD PTR [EAX+L_4bc150],0
L_409bb0:
          imul EAX,DWORD PTR [EDI],1068
          add EBP,1
          mov DWORD PTR [ESP+4],OFFSET L_44fdba
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EBP
          mov EDX,DWORD PTR [EAX+L_4bc150]
          add EAX,OFFSET L_4bbd50
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+16],EDX
          call _log_printf
          cmp ESI,DWORD PTR [ESP+60]
          jg L_409f6a
          cmp DWORD PTR [ESP+68],EBP
          je L_409e1a
          mov EAX,DWORD PTR [ESP+44]
          add EAX,ESI
          jmp L_4098c2
L_409c03:
          test BL,BL
          jne L_4098fa
          xor EDX,EDX
          mov DWORD PTR [ESP+52],1
          xor EBX,EBX
          jmp L_409ac2
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_409c20:
          mov EDX,DWORD PTR [ESI+L_44a1a0+4]
          mov DWORD PTR [EBX+1028],EDX
          mov EDX,DWORD PTR [ESI+L_44a144+92]
          mov DWORD PTR [EBX+1032],EDX
          jmp L_40971c
L_409c3d:
          imul EAX,DWORD PTR [EDI],1068
          xor EBX,EBX
          mov DWORD PTR [EAX+L_4bc150],0
L_409c4f:
          lea ESI,DWORD PTR [ESI+EBX*1+1]
          jmp L_409bb0
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_409c60:
          mov EDX,DWORD PTR [ESI+L_44a0c0+4]
          mov DWORD PTR [EBX+1028],EDX
          mov EDX,DWORD PTR [ESI+L_44a0c0]
          mov DWORD PTR [EBX+1032],EDX
          jmp L_40971c
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_409c80:
          cmp EBX,8
          jne L_409b42
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP],EAX
          call FUN_449060
          mov BYTE PTR [ESP+152],0
          mov EDI,DWORD PTR [EDI]
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],0
          imul EDI,EDI,1068
          mov DWORD PTR [ESP],EAX
          call _myatox32
          mov DWORD PTR [EDI+L_4bc150],EAX
          mov EDI,DWORD PTR [ESP+56]
          add EDI,DWORD PTR [L_479e84]
          jmp L_409c4f
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_409ce0:
          mov EDX,DWORD PTR [ESI+L_44a140+4]
          mov DWORD PTR [EBX+1028],EDX
          mov EDX,DWORD PTR [ESI+L_44a0c4+124]
          mov DWORD PTR [EBX+1032],EDX
          jmp L_40971c
L_409cfd:
          sub EAX,4
          cmp EAX,1
          jbe L_40a6fa
          mov EAX,DWORD PTR [L_479ea4]
          mov DWORD PTR [ESP],EBX
          and EAX,7
          cmp EAX,5
          je L_40a72e
          cmp EAX,6
          je L_40a7e9
          cmp EAX,7
          je L_40a13b
          call _strlen
          mov DWORD PTR [EBX+EAX*1],7627110
          jmp L_4099c2
L_409d40:
          mov DWORD PTR [ESP+4],OFFSET L_4c4f54
          mov DWORD PTR [ESP],EBX
          call _strcat
          jmp L_4099df
L_409d55:
          mov EAX,DWORD PTR [L_479ea4]
          mov DWORD PTR [ESP+4],OFFSET L_44fd26
          and EAX,7
          mov EAX,DWORD PTR [EAX*4+L_450400]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+94]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+72],EAX
          call _sprintf
          jmp L_4097d8
L_409d85:
          mov DWORD PTR [ESP+4],OFFSET L_44a3c0
          mov DWORD PTR [ESP],EBX
          call _strcpy
          jmp L_409780
L_409d9a:
          call _strlen
          mov ECX,12903
          add EAX,EBX
          mov WORD PTR [EAX],CX
          mov BYTE PTR [EAX+2],0
          jmp L_4099a7
L_409db2:
          call FUN_408ec0
          jmp L_4096bb
L_409dbc:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44fb88
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+52],0
          mov EAX,DWORD PTR [ESP+52]
          add ESP,1180
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_409deb:
          mov EAX,63
          jmp L_4095c2
L_409df5:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44fbb0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+52],0
          jmp L_40975e
L_409e1a:
          mov EAX,DWORD PTR [_g479ea8]
          cmp EAX,2
          je L_409e2d
          cmp EAX,5
          jbe L_40a1c2
L_409e2d:
          mov EAX,DWORD PTR [ESP+48]
          sub EAX,10
          test EAX,EAX
          mov DWORD PTR [ESP+56],EAX
          jle L_40a8aa
          xor EDX,EDX
          mov ESI,11
          mov EDI,DWORD PTR [ESP+44]
          mov EBP,EAX
          jmp L_409e5b
          .byte 0x90
L_409e50:
          add EDX,1
          cmp EDX,EBP
          je L_40a8aa
L_409e5b:
          xor EAX,EAX
          cmp BYTE PTR [EDI+EDX*1],91
          jne L_409e50
          add EAX,1
          cmp EAX,9
          jg L_409e8b
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_409e70:
          lea ECX,DWORD PTR [EDI+EAX*1]
          movzx EBX,BYTE PTR [ECX+EDX*1]
          movsx ECX,BYTE PTR [EAX+L_44fe85]
          cmp EBX,ECX
          cmovne EAX,ESI
          add EAX,1
          cmp EAX,9
          jle L_409e70
L_409e8b:
          cmp EAX,10
          jne L_409e50
          mov EAX,DWORD PTR [ESP+44]
          cmp BYTE PTR [EAX+EDX*1+10],0
          sete AL
          movzx EAX,AL
          lea EDI,DWORD PTR [EAX+EDX*1+10]
          mov EDX,DWORD PTR [ESP+48]
          sub EDX,EDI
          test EDX,EDX
          jle L_409ed0
          mov EAX,DWORD PTR [ESP+44]
          lea EBP,DWORD PTR [EAX+EDI*1]
          cmp BYTE PTR [EBP],91
          je L_40a97b
          xor EAX,EAX
          jmp L_409ec9
L_409ec2:
          cmp BYTE PTR [EBP+EAX*1],91
          je L_409ed5
L_409ec9:
          add EAX,1
          cmp EDX,EAX
          jne L_409ec2
L_409ed0:
          mov EAX,4294967295
L_409ed5:
          add EAX,EDI
          mov DWORD PTR [ESP+4],OFFSET L_44fe90
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+52],EAX
          call _log_printf
          mov EAX,DWORD PTR [L_4c8fe0]
          cmp EAX,15
          mov ESI,EAX
          jg L_40a9a8
          mov EAX,DWORD PTR [ESP+44]
          lea EBP,DWORD PTR [EAX+EDI*1]
L_409f06:
          mov EAX,ESI
          mov ECX,EBP
          mov EBP,EDI
          imul ESI,ESI,1028
          mov EDI,EAX
          add ESI,OFFSET L_4c4fa0
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_409f20:
          mov EDX,DWORD PTR [ESP+48]
          sub EDX,EBP
          test EDX,EDX
          jle L_409f5d
          movzx EBX,BYTE PTR [ECX]
          xor EAX,EAX
          test BL,BL
          jne L_409f3b
          jmp L_409f4c
L_409f35:
          cmp BYTE PTR [ECX+EAX*1],0
          je L_409f7f
L_409f3b:
          add EAX,1
          cmp EDX,EAX
          jne L_409f35
          cmp BL,44
          je L_409f5d
          mov EAX,4294967295
L_409f4c:
          xor EBX,EBX
          jmp L_409f56
L_409f50:
          cmp BYTE PTR [ECX+EBX*1],44
          je L_409f90
L_409f56:
          add EBX,1
          cmp EDX,EBX
          jne L_409f50
L_409f5d:
          mov DWORD PTR [ESP+4],OFFSET L_44feb0
          jmp L_409527
L_409f6a:
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+4],OFFSET L_44fdd8
          mov DWORD PTR [ESP+8],EAX
          jmp L_40973e
L_409f7f:
          cmp BL,44
          jne L_409f4c
          xor EAX,EAX
          xor EBX,EBX
          jmp L_409fa2
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_409f90:
          cmp EBX,EAX
          jge L_409f5d
          cmp EBX,1023
          jg L_40a8e4
          mov EAX,EBX
L_409fa2:
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],ESI
          call FUN_449060
          imul EAX,EDI,1028
          mov EDX,DWORD PTR [ESP+48]
          mov ECX,DWORD PTR [ESP+44]
          mov BYTE PTR [EBX+EAX*1+L_4c4fa0],0
          lea EAX,DWORD PTR [EBX+EBP*1]
          lea EBX,DWORD PTR [EAX+1]
          sub EDX,EBX
          add ECX,EBX
          test EDX,EDX
          jle L_40a002
          cmp BYTE PTR [ECX],0
          je L_40a8d3
          xor EBP,EBP
          add EAX,DWORD PTR [ESP+44]
          jmp L_409ffb
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_409ff0:
          cmp BYTE PTR [EAX+EBP*1+1],0
          je L_40a0ec
L_409ffb:
          add EBP,1
          cmp EDX,EBP
          jne L_409ff0
L_40a002:
          mov EAX,4294967295
          mov EBP,4294967295
L_40a00c:
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP],EAX
          call FUN_449060
          mov EAX,DWORD PTR [ESP+64]
          mov BYTE PTR [ESP+EBP*1+144],0
          lea EBP,DWORD PTR [EBX+EBP*1+1]
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EAX
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [ESI+1024],EAX
          je L_40a8f1
          mov ECX,DWORD PTR [L_4c8fe0]
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44ff40
          mov DWORD PTR [ESP],1
          lea EDX,DWORD PTR [ECX+1]
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [L_4c8fe0],EDX
          call _log_printf
          cmp EBP,DWORD PTR [ESP+52]
          jl L_40a0ce
L_40a084:
          xor EDX,EDX
          mov ESI,10
          mov EDI,DWORD PTR [ESP+44]
          mov EBP,DWORD PTR [ESP+76]
          jmp L_40a0c4
L_40a095:
          lea ECX,DWORD PTR [EDI+EAX*1]
          movzx EBX,BYTE PTR [ECX+EDX*1]
          movsx ECX,BYTE PTR [EAX+L_450034]
          cmp EBX,ECX
          cmovne EAX,ESI
L_40a0a8:
          add EAX,1
          cmp EAX,8
          jle L_40a095
          cmp EAX,9
          je L_40a1f5
L_40a0b9:
          add EDX,1
          cmp EDX,EBP
          jge L_40a941
L_40a0c4:
          xor EAX,EAX
          cmp BYTE PTR [EDI+EDX*1],91
          jne L_40a0b9
          jmp L_40a0a8
L_40a0ce:
          add EDI,1
          add ESI,1028
          cmp EDI,16
          je L_40a9fb
          mov EAX,DWORD PTR [ESP+44]
          lea ECX,DWORD PTR [EAX+EBP*1]
          jmp L_409f20
L_40a0ec:
          cmp EBP,10
          jg L_40a8d3
          mov EAX,EBP
          jmp L_40a00c
L_40a0fc:
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+4],OFFSET L_44fe20
          mov DWORD PTR [ESP+8],EAX
          jmp L_40973e
L_40a111:
          mov DWORD PTR [ESP+4],OFFSET L_44fccc
          jmp L_409675
L_40a11e:
          mov DWORD PTR [ESP+12],OFFSET L_47a94c
          mov DWORD PTR [ESP+8],OFFSET L_4c9364
          mov DWORD PTR [ESP+4],OFFSET L_44fcb1
          jmp L_409675
L_40a13b:
          call _strlen
          mov ECX,29285
          add EAX,EBX
          mov DWORD PTR [EAX],1668180343
          mov DWORD PTR [EAX+4],1953719656
          mov WORD PTR [EAX+8],CX
          mov BYTE PTR [EAX+10],0
          jmp L_4099c2
L_40a161:
          lea EAX,DWORD PTR [ESP+144]
          mov DWORD PTR [ESP+12],OFFSET L_47a94c
          mov DWORD PTR [ESP+8],OFFSET L_4c9364
          mov DWORD PTR [ESP+4],OFFSET L_44fc62
          mov DWORD PTR [L_4c4f98],19
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+64],EAX
          mov DWORD PTR [L_479e84],OFFSET L_44a020
          call _sprintf
          jmp L_40968d
L_40a1a5:
          mov DWORD PTR [ESP+12],OFFSET L_47a94c
          mov DWORD PTR [ESP+8],OFFSET L_4c9364
          mov DWORD PTR [ESP+4],OFFSET L_44fca0
          jmp L_409675
L_40a1c2:
          mov DWORD PTR [ESP+8],4
          mov DWORD PTR [ESP+4],OFFSET L_44fe5a
          mov DWORD PTR [ESP],OFFSET L_4bce00
          call _strnicmp
          test EAX,EAX
          jne L_40a909
          mov DWORD PTR [L_479eb8],0
          jmp L_409e2d
L_40a1f5:
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [L_4bbd4c],0
          mov EBP,OFFSET L_47b94c
          cmp BYTE PTR [EAX+EDX*1+9],0
          mov DWORD PTR [ESP+4],OFFSET L_45003e
          mov DWORD PTR [ESP],1
          sete AL
          movzx EAX,AL
          lea EDI,DWORD PTR [EAX+EDX*1+9]
          call _log_printf
          mov ESI,EDI
          mov DWORD PTR [ESP+52],0
L_40a235:
          mov EDI,DWORD PTR [ESP+48]
          mov EAX,DWORD PTR [ESP+44]
          sub EDI,ESI
          lea ECX,DWORD PTR [EAX+ESI*1]
          test EDI,EDI
          jle L_40a89b
          movzx EAX,BYTE PTR [ECX]
          xor EBX,EBX
          test AL,AL
          jne L_40a25f
          jmp L_40a273
L_40a255:
          cmp BYTE PTR [ECX+EBX*1],0
          je L_40a591
L_40a25f:
          add EBX,1
          cmp EDI,EBX
          jne L_40a255
          cmp AL,44
          je L_40a89b
          mov EBX,4294967295
L_40a273:
          xor EAX,EAX
          jmp L_40a28a
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40a280:
          cmp BYTE PTR [ECX+EAX*1],44
          je L_40a5e0
L_40a28a:
          add EAX,1
          cmp EDI,EAX
          jne L_40a280
L_40a291:
          mov EDI,1
L_40a296:
          cmp EBX,1023
          jg L_40a92c
L_40a2a2:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP],EBP
          call FUN_449060
          mov EAX,DWORD PTR [ESP+52]
          shl EAX,10
          cmp EBX,21
          mov BYTE PTR [EBX+EAX*1+L_47b94c],0
          jle L_40a2f2
          mov DWORD PTR [ESP+4],47
          mov DWORD PTR [ESP],EBP
          call FUN_449058
          test EAX,EAX
          je L_40a85e
L_40a2de:
          add EAX,1
L_40a2e1:
          mov DWORD PTR [ESP],EAX
          call _strlen
          cmp EAX,21
          ja L_40a94e
L_40a2f2:
          mov ECX,DWORD PTR [ESP+52]
          lea EAX,DWORD PTR [EBX+ESI*1]
          sub EBX,1
          lea ESI,DWORD PTR [EAX+1]
          shl ECX,10
          movzx ECX,BYTE PTR [EBX+ECX*1+L_47b94c]
          sub ECX,49
          cmp CL,1
          jbe L_40a5cc
L_40a316:
          test EDI,EDI
          jne L_40a363
L_40a31a:
          mov ECX,DWORD PTR [ESP+48]
          mov EDX,DWORD PTR [ESP+44]
          sub ECX,ESI
          mov EDI,EDX
          add EDI,ESI
          test ECX,ECX
          jle L_40a352
          cmp BYTE PTR [EDI],0
          je L_40a5f1
          xor EBX,EBX
          add EAX,EDX
          jmp L_40a34b
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_40a340:
          cmp BYTE PTR [EAX+EBX*1+1],0
          je L_40a60d
L_40a34b:
          add EBX,1
          cmp ECX,EBX
          jne L_40a340
L_40a352:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44fd78
          jmp L_40973e
L_40a363:
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [EAX*4+L_4bb94c],0
          xor EAX,EAX
L_40a374:
          mov EDI,DWORD PTR [L_4bbd4c]
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44fdba
          mov DWORD PTR [ESP],1
          lea ECX,DWORD PTR [EDI+1]
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [L_4bbd4c],ECX
          call _log_printf
          cmp ESI,DWORD PTR [ESP+48]
          jl L_40a572
L_40a3ad:
          mov EAX,DWORD PTR [ESP+56]
          xor EDX,EDX
          mov EDI,11
          test EAX,EAX
          jle L_40a941
          mov EBP,DWORD PTR [ESP+44]
          jmp L_40a3d3
L_40a3c6:
          add EDX,1
          cmp EDX,DWORD PTR [ESP+56]
          je L_40a941
L_40a3d3:
          xor EAX,EAX
          cmp BYTE PTR [EBP+EDX*1],91
          lea ESI,DWORD PTR [EBP+EDX*1]
          jne L_40a3c6
          jmp L_40a3f2
L_40a3e2:
          movzx EBX,BYTE PTR [ESI+EAX*1]
          movsx ECX,BYTE PTR [EAX+L_450149]
          cmp EBX,ECX
          cmovne EAX,EDI
L_40a3f2:
          add EAX,1
          cmp EAX,9
          jle L_40a3e2
          cmp EAX,10
          jne L_40a3c6
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [_buildMode],0
          cmp BYTE PTR [EAX+EDX*1+10],0
          mov DWORD PTR [ESP+4],OFFSET L_450154
          mov DWORD PTR [ESP],1
          sete AL
          movzx EAX,AL
          lea EDI,DWORD PTR [EAX+EDX*1+10]
          call _log_printf
          mov ECX,DWORD PTR [ESP+48]
          sub ECX,EDI
          test ECX,ECX
          jle L_40a9eb
          mov EAX,DWORD PTR [ESP+44]
          xor EDX,EDX
          add EAX,EDI
          cmp BYTE PTR [EAX],91
          jne L_40a456
          jmp L_40a462
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_40a450:
          cmp BYTE PTR [EAX+EDX*1],91
          je L_40a462
L_40a456:
          add EDX,1
          cmp ECX,EDX
          jne L_40a450
          mov EDX,4294967295
L_40a462:
          lea ESI,DWORD PTR [EDX+EDI*1]
          xor EBP,EBP
          mov DWORD PTR [ESP+52],OFFSET _flashFiles
          mov DWORD PTR [ESP+56],ESI
          mov ESI,EBP
          mov EBP,EDI
          mov EDI,ESI
L_40a479:
          mov EDX,DWORD PTR [ESP+48]
          sub EDX,EBP
          test EDX,EDX
          jle L_40a76e
          movzx ECX,BYTE PTR [EAX]
          xor EBX,EBX
          cmp CL,44
          jne L_40a49d
          jmp L_40a4b1
L_40a493:
          cmp BYTE PTR [EAX+EBX*1],44
          je L_40a66f
L_40a49d:
          add EBX,1
          cmp EDX,EBX
          jne L_40a493
          test CL,CL
          je L_40a76e
          mov EBX,4294967295
L_40a4b1:
          xor ESI,ESI
          jmp L_40a4bf
L_40a4b5:
          cmp BYTE PTR [EAX+ESI*1],0
          je L_40a680
L_40a4bf:
          add ESI,1
          cmp EDX,ESI
          jne L_40a4b5
          test EBX,EBX
          js L_40a76e
          mov EDX,4294967295
          mov ESI,4294967295
L_40a4d8:
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+52]
          lea EBP,DWORD PTR [EBP+ESI*1+1]
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP],EAX
          call FUN_449060
          imul EAX,EDI,22
          mov BYTE PTR [ESI+EAX*1+_flashFiles],0
          mov DWORD PTR [EDI*4+L_4c9138],0
          xor EAX,EAX
L_40a508:
          mov ESI,DWORD PTR [_buildMode]
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+4],OFFSET L_44fdba
          mov DWORD PTR [ESP],1
          lea EDX,DWORD PTR [ESI+1]
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [_buildMode],EDX
          call _log_printf
          cmp EBP,DWORD PTR [ESP+56]
          jl L_40a653
L_40a545:
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP+4],OFFSET L_4501c0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+52],1
          jmp L_40975e
L_40a572:
          add DWORD PTR [ESP+52],1
          add EBP,1024
          mov EAX,DWORD PTR [ESP+52]
          cmp EAX,256
          jne L_40a235
          jmp L_40a3ad
L_40a591:
          cmp AL,44
          jne L_40a273
          mov EAX,DWORD PTR [ESP+52]
          lea ECX,DWORD PTR [ESI+1]
          shl EAX,10
          mov BYTE PTR [EAX+L_47b94c],0
          add EAX,OFFSET L_479ea0
          movzx EAX,BYTE PTR [EAX+6827]
          sub EAX,49
          cmp AL,1
          mov EAX,ESI
          mov ESI,ECX
          ja L_40a31a
          mov EBX,4294967295
          xor EDI,EDI
L_40a5cc:
          mov ECX,DWORD PTR [ESP+52]
          shl ECX,10
          mov BYTE PTR [EBX+ECX*1+L_47b94c],0
          jmp L_40a316
L_40a5e0:
          cmp EAX,EBX
          jge L_40a291
          mov EBX,EAX
          xor EDI,EDI
          jmp L_40a296
L_40a5f1:
          mov EAX,DWORD PTR [ESP+52]
          xor EBX,EBX
          mov DWORD PTR [EAX*4+L_4bb94c],0
          xor EAX,EAX
L_40a604:
          lea ESI,DWORD PTR [ESI+EBX*1+1]
          jmp L_40a374
L_40a60d:
          cmp EBX,8
          jne L_40a352
          mov DWORD PTR [ESP+4],EDI
          mov EDI,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP],EDI
          call FUN_449060
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],0
          mov BYTE PTR [ESP+152],0
          call _myatox32
          mov EDI,DWORD PTR [ESP+52]
          mov DWORD PTR [EDI*4+L_4bb94c],EAX
          jmp L_40a604
L_40a653:
          add EDI,1
          add DWORD PTR [ESP+52],22
          cmp EDI,10
          je L_40a545
          mov EAX,DWORD PTR [ESP+44]
          add EAX,EBP
          jmp L_40a479
L_40a66f:
          test CL,CL
          jne L_40a4b1
          xor EDX,EDX
          xor ESI,ESI
          jmp L_40a4d8
L_40a680:
          cmp EBX,ESI
          jle L_40a87d
          cmp ESI,21
          jg L_40a886
          mov EDX,ESI
          jmp L_40a4d8
L_40a698:
          mov DWORD PTR [L_4c4f98],11
          mov DWORD PTR [L_479e84],OFFSET L_44a074
          mov DWORD PTR [ESP+12],OFFSET L_47a94c
          mov DWORD PTR [ESP+8],OFFSET L_4c9364
          mov DWORD PTR [ESP+4],OFFSET L_44fc71
          jmp L_409675
L_40a6c9:
          mov DWORD PTR [L_4c4f98],12
          mov DWORD PTR [L_479e84],OFFSET L_44a05c
          mov DWORD PTR [ESP+12],OFFSET L_47a94c
          mov DWORD PTR [ESP+8],OFFSET L_4c9364
          mov DWORD PTR [ESP+4],OFFSET L_44fc80
          jmp L_409675
L_40a6fa:
          mov DWORD PTR [ESP],EBX
          call _strlen
          mov DWORD PTR [EBX+EAX*1],7156327
          mov EDX,DWORD PTR [L_479ea4]
          lea EAX,DWORD PTR [EBX+EAX*1+3]
          mov DWORD PTR [ESP],EAX
          and EDX,7
          mov EDX,DWORD PTR [EDX*4+L_450400]
          mov DWORD PTR [ESP+4],EDX
          call _strcpy
          jmp L_4099c2
L_40a72e:
          call _strlen
          add EAX,EBX
          mov DWORD PTR [EAX],1852404340
          mov DWORD PTR [EAX+4],7959657
          jmp L_4099c2
L_40a747:
          mov DWORD PTR [L_479e84],OFFSET L_44a044
          mov DWORD PTR [ESP+12],OFFSET L_47a94c
          mov DWORD PTR [ESP+8],OFFSET L_4c9364
          mov DWORD PTR [ESP+4],OFFSET L_44fc90
          jmp L_409675
L_40a76e:
          mov EBX,4294967295
L_40a773:
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EAX
          call FUN_449060
          imul EAX,EDI,22
          mov EDX,DWORD PTR [ESP+48]
          mov ECX,DWORD PTR [ESP+44]
          mov BYTE PTR [EBX+EAX*1+_flashFiles],0
          lea EAX,DWORD PTR [EBX+EBP*1]
          lea ESI,DWORD PTR [EAX+1]
          sub EDX,ESI
          lea EBP,DWORD PTR [ECX+ESI*1]
          test EDX,EDX
          jle L_40a7ce
          cmp BYTE PTR [EBP],0
          je L_40a84d
          xor EBX,EBX
          add EAX,ECX
          jmp L_40a7c7
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40a7c0:
          cmp BYTE PTR [EAX+EBX*1+1],0
          je L_40a808
L_40a7c7:
          add EBX,1
          cmp EDX,EBX
          jne L_40a7c0
L_40a7ce:
          mov EAX,EDI
          mov DWORD PTR [ESP+4],OFFSET L_44fd78
          shl EAX,10
          add EAX,OFFSET L_47b94c
          mov DWORD PTR [ESP+8],EAX
          jmp L_40973e
L_40a7e9:
          call _strlen
          mov EDX,24942
          add EAX,EBX
          mov DWORD PTR [EAX],1869770595
          mov WORD PTR [EAX+4],DX
          mov BYTE PTR [EAX+6],0
          jmp L_4099c2
L_40a808:
          cmp EBX,8
          jne L_40a7ce
          mov DWORD PTR [ESP+4],EBP
          mov EBP,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP],EBP
          call FUN_449060
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EBP
          mov BYTE PTR [ESP+152],0
          call _myatox32
          mov DWORD PTR [EDI*4+L_4c9138],EAX
L_40a844:
          lea EBP,DWORD PTR [EBX+ESI*1+1]
          jmp L_40a508
L_40a84d:
          mov DWORD PTR [EDI*4+L_4c9138],0
          xor EAX,EAX
          xor EBX,EBX
          jmp L_40a844
L_40a85e:
          mov DWORD PTR [ESP+4],92
          mov DWORD PTR [ESP],EBP
          call FUN_449058
          test EAX,EAX
          jne L_40a2de
          mov EAX,EBP
          jmp L_40a2e1
L_40a87d:
          cmp EBX,21
          jle L_40a773
L_40a886:
          mov DWORD PTR [ESP+8],21
          mov DWORD PTR [ESP+4],OFFSET L_450174
          jmp L_40973e
L_40a89b:
          mov EDI,1
          mov EBX,4294967295
          jmp L_40a2a2
L_40a8aa:
          mov DWORD PTR [ESP+4],OFFSET L_450010
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_40a084
L_40a8c3:
          mov EAX,DWORD PTR [ESP+44]
          mov EDX,4294967295
          add EAX,EDI
          jmp L_4098b2
L_40a8d3:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44fef0
          jmp L_40973e
L_40a8e4:
          mov DWORD PTR [ESP+4],OFFSET L_44ff98
          jmp L_409527
L_40a8f1:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44ff60
          mov DWORD PTR [ESP],1
          jmp L_409745
L_40a909:
          mov DWORD PTR [ESP+4],OFFSET L_44fe60
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [L_479eb8],1
          jmp L_409e2d
L_40a92c:
          mov DWORD PTR [ESP+8],1023
          mov DWORD PTR [ESP+4],OFFSET L_4500bc
          jmp L_40973e
L_40a941:
          mov DWORD PTR [ESP+4],OFFSET L_450108
          jmp L_409527
L_40a94e:
          mov DWORD PTR [ESP+8],21
          mov DWORD PTR [ESP+4],OFFSET L_45005c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_4500a7
          jmp L_40973e
L_40a97b:
          mov DWORD PTR [ESP+4],OFFSET L_44fe90
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_4c8fe0]
          cmp EAX,15
          mov ESI,EAX
          jg L_40a084
          mov DWORD PTR [ESP+52],EDI
          jmp L_409f06
L_40a9a8:
          cmp DWORD PTR [ESP+52],EDI
          jle L_40a084
L_40a9b2:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],OFFSET L_44ffd0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP+52],0
          jmp L_40975e
L_40a9eb:
          mov EAX,DWORD PTR [ESP+44]
          mov EDX,4294967295
          add EAX,EDI
          jmp L_40a462
L_40a9fb:
          mov EAX,DWORD PTR [L_4c8fe0]
          jmp L_40a9b2
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
#@C _getIniValue
          .byte 0x8d
          .byte 0x76
          .byte 0x0
FUN_40aad0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EBX,DWORD PTR [_iniSize]
          mov EDI,DWORD PTR [ESP+80]
          test EBX,EBX
          jne L_40aaf1
L_40aae5:
          mov EAX,DWORD PTR [ESP+84]
L_40aae9:
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_40aaf1:
          mov EAX,DWORD PTR [_iniBuf]
          mov DWORD PTR [ESP],EDI
          mov ESI,EAX
          mov DWORD PTR [ESP+24],EAX
          call _strlen
          sub EBX,EAX
          test EBX,EBX
          mov DWORD PTR [ESP+36],EBX
          jle L_40aae5
          movsx ECX,BYTE PTR [EDI]
          add ESI,EAX
          mov DWORD PTR [ESP+28],ESI
          xor ESI,ESI
          mov DWORD PTR [ESP+32],ECX
          lea ECX,DWORD PTR [EAX+1]
          mov DWORD PTR [ESP+44],ECX
          jmp L_40ab3e
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40ab30:
          add ESI,1
          add DWORD PTR [ESP+28],1
          cmp ESI,DWORD PTR [ESP+36]
          je L_40aae5
L_40ab3e:
          mov EBX,DWORD PTR [ESP+24]
          movzx EDX,BYTE PTR [EBX+ESI*1]
          cmp EDX,DWORD PTR [ESP+32]
          jne L_40ab30
          xor EDX,EDX
          test EAX,EAX
          jle L_40ab79
          lea EBP,DWORD PTR [EBX+ESI*1]
          mov DWORD PTR [ESP+40],ESI
          mov ESI,DWORD PTR [ESP+44]
          jmp L_40ab6e
          nop
L_40ab60:
          movzx EBX,BYTE PTR [EBP+EDX*1]
          movsx ECX,BYTE PTR [EDI+EDX*1]
          cmp EBX,ECX
          cmovne EDX,ESI
L_40ab6e:
          add EDX,1
          cmp EAX,EDX
          jg L_40ab60
          mov ESI,DWORD PTR [ESP+40]
L_40ab79:
          cmp EAX,EDX
          jne L_40ab30
          mov EBX,DWORD PTR [ESP+28]
          lea EDX,DWORD PTR [EAX+ESI*1]
          cmp BYTE PTR [EBX],0
          je L_40ab30
          cmp EDX,-1
          je L_40aae5
          mov DWORD PTR [ESP+8],4
          mov DWORD PTR [ESP+4],OFFSET L_450258
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          mov EDX,EAX
          mov EAX,1
          test EDX,EDX
          je L_40aae9
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_45025d
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          mov EDX,EAX
          xor EAX,EAX
          test EDX,EDX
          jne L_40aae5
          jmp L_40aae9
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_40abf0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EBX,DWORD PTR [_iniSize]
          mov EDI,DWORD PTR [ESP+80]
          test EBX,EBX
          je L_40ace0
          mov EAX,DWORD PTR [_iniBuf]
          mov DWORD PTR [ESP],EDI
          mov ESI,EAX
          mov DWORD PTR [ESP+24],EAX
          call _strlen
          sub EBX,EAX
          test EBX,EBX
          mov DWORD PTR [ESP+36],EBX
          jle L_40ace0
          movsx ECX,BYTE PTR [EDI]
          add ESI,EAX
          mov DWORD PTR [ESP+28],ESI
          xor ESI,ESI
          mov DWORD PTR [ESP+32],ECX
          lea ECX,DWORD PTR [EAX+1]
          mov DWORD PTR [ESP+44],ECX
          jmp L_40ac54
L_40ac42:
          add ESI,1
          add DWORD PTR [ESP+28],1
          cmp ESI,DWORD PTR [ESP+36]
          je L_40ace0
L_40ac54:
          mov EBX,DWORD PTR [ESP+24]
          movzx EDX,BYTE PTR [EBX+ESI*1]
          cmp EDX,DWORD PTR [ESP+32]
          jne L_40ac42
          xor EDX,EDX
          test EAX,EAX
          jle L_40ac8e
          lea EBP,DWORD PTR [EBX+ESI*1]
          mov DWORD PTR [ESP+40],ESI
          mov ESI,DWORD PTR [ESP+44]
          jmp L_40ac83
L_40ac75:
          movzx EBX,BYTE PTR [EBP+EDX*1]
          movsx ECX,BYTE PTR [EDI+EDX*1]
          cmp EBX,ECX
          cmovne EDX,ESI
L_40ac83:
          add EDX,1
          cmp EAX,EDX
          jg L_40ac75
          mov ESI,DWORD PTR [ESP+40]
L_40ac8e:
          cmp EAX,EDX
          jne L_40ac42
          mov EBX,DWORD PTR [ESP+28]
          lea EDX,DWORD PTR [EAX+ESI*1]
          cmp BYTE PTR [EBX],0
          je L_40ac42
          cmp EDX,-1
          je L_40ace0
          mov DWORD PTR [ESP+8],4
          mov DWORD PTR [ESP+4],OFFSET L_450258
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          je L_40ace0
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_45025d
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          mov EDX,EAX
          mov EAX,EBX
          test EDX,EDX
          jne L_40ace2
          nop
L_40ace0:
          xor EAX,EAX
L_40ace2:
          add ESP,60
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
FUN_40acf0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EBX,DWORD PTR [_iniSize]
          mov EAX,DWORD PTR [ESP+84]
          mov EDI,DWORD PTR [ESP+80]
          test EBX,EBX
          mov DWORD PTR [ESP+44],EAX
          jne L_40ad20
L_40ad0d:
          mov EAX,DWORD PTR [ESP+44]
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40ad20:
          mov EAX,DWORD PTR [_iniBuf]
          mov DWORD PTR [ESP],EDI
          mov ESI,EAX
          mov DWORD PTR [ESP+20],EAX
          call _strlen
          sub EBX,EAX
          test EBX,EBX
          mov DWORD PTR [ESP+32],EBX
          jle L_40ad0d
          movsx ECX,BYTE PTR [EDI]
          add ESI,EAX
          mov DWORD PTR [ESP+24],ESI
          xor ESI,ESI
          mov DWORD PTR [ESP+28],ECX
          lea ECX,DWORD PTR [EAX+1]
          mov DWORD PTR [ESP+40],ECX
          jmp L_40ad63
L_40ad55:
          add ESI,1
          add DWORD PTR [ESP+24],1
          cmp ESI,DWORD PTR [ESP+32]
          je L_40ad0d
L_40ad63:
          mov EBX,DWORD PTR [ESP+20]
          movzx EDX,BYTE PTR [EBX+ESI*1]
          cmp EDX,DWORD PTR [ESP+28]
          jne L_40ad55
          xor EDX,EDX
          test EAX,EAX
          jle L_40ad9d
          lea EBP,DWORD PTR [EBX+ESI*1]
          mov DWORD PTR [ESP+36],ESI
          mov ESI,DWORD PTR [ESP+40]
          jmp L_40ad92
L_40ad84:
          movzx EBX,BYTE PTR [EBP+EDX*1]
          movsx ECX,BYTE PTR [EDI+EDX*1]
          cmp EBX,ECX
          cmovne EDX,ESI
L_40ad92:
          add EDX,1
          cmp EAX,EDX
          jg L_40ad84
          mov ESI,DWORD PTR [ESP+36]
L_40ad9d:
          cmp EAX,EDX
          jne L_40ad55
          mov EBX,DWORD PTR [ESP+24]
          lea EDX,DWORD PTR [EAX+ESI*1]
          cmp BYTE PTR [EBX],0
          je L_40ad55
          cmp EDX,-1
          je L_40ad0d
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+84],EAX
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+80],EAX
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _myatou32
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
FUN_40ade0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EBX,DWORD PTR [_iniSize]
          mov EDI,DWORD PTR [ESP+80]
          test EBX,EBX
          je L_40aee0
          mov EAX,DWORD PTR [_iniBuf]
          mov DWORD PTR [ESP],EDI
          mov ESI,EAX
          mov DWORD PTR [ESP+24],EAX
          call _strlen
          sub EBX,EAX
          test EBX,EBX
          mov DWORD PTR [ESP+36],EBX
          jle L_40aee0
          movsx EBX,BYTE PTR [EDI]
          lea ECX,DWORD PTR [EAX+1]
          add ESI,EAX
          mov DWORD PTR [ESP+28],ESI
          xor ESI,ESI
          mov DWORD PTR [ESP+44],ECX
          mov DWORD PTR [ESP+32],EBX
          jmp L_40ae44
L_40ae32:
          add ESI,1
          add DWORD PTR [ESP+28],1
          cmp ESI,DWORD PTR [ESP+36]
          je L_40aee0
L_40ae44:
          mov EBX,DWORD PTR [ESP+24]
          movzx EDX,BYTE PTR [EBX+ESI*1]
          cmp EDX,DWORD PTR [ESP+32]
          jne L_40ae32
          xor EDX,EDX
          test EAX,EAX
          jle L_40ae7e
          lea EBP,DWORD PTR [EBX+ESI*1]
          mov DWORD PTR [ESP+40],ESI
          mov ESI,DWORD PTR [ESP+44]
          jmp L_40ae73
L_40ae65:
          movzx EBX,BYTE PTR [EBP+EDX*1]
          movsx ECX,BYTE PTR [EDI+EDX*1]
          cmp EBX,ECX
          cmovne EDX,ESI
L_40ae73:
          add EDX,1
          cmp EAX,EDX
          jg L_40ae65
          mov ESI,DWORD PTR [ESP+40]
L_40ae7e:
          cmp EAX,EDX
          jne L_40ae32
          mov EBX,DWORD PTR [ESP+28]
          lea ECX,DWORD PTR [EAX+ESI*1]
          movzx EDX,BYTE PTR [EBX]
          test DL,DL
          je L_40ae32
          cmp ECX,-1
          je L_40aee0
          cmp DL,48
          je L_40aeb4
L_40ae9a:
          mov EDI,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          call _validateString
          test EAX,EAX
          jne L_40aee0
          add ESP,60
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_40aeb4:
          movsx EAX,BYTE PTR [EBX+1]
          mov DWORD PTR [ESP],EAX
          call _myatol
          cmp AL,120
          jne L_40ae9a
          mov EDI,DWORD PTR [ESP+28]
          mov EAX,EDI
          add EAX,2
          mov DWORD PTR [ESP],EAX
          call _validateString
          mov EDX,EAX
          mov EAX,EDI
          test EDX,EDX
          je L_40aee2
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_40aee0:
          xor EAX,EAX
L_40aee2:
          add ESP,60
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
FUN_40aef0:
          push EDI
          push ESI
          push EBX
          sub ESP,1040
          lea EBX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+4],OFFSET L_47ad4c
          mov DWORD PTR [ESP],EBX
          call _strcpy
          mov EDX,EBX
L_40af0f:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_40af0f
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          mov DWORD PTR [EDX],1769238639
          mov DWORD PTR [EDX+4],779316847
          mov DWORD PTR [EDX+8],6909545
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_450264
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44fb84
          mov DWORD PTR [ESP],EBX
          call _fopen
          test EAX,EAX
          mov EDI,EAX
          je L_40b0e0
          mov DWORD PTR [ESP],EAX
          call _getFileSize
          lea ESI,DWORD PTR [EAX+1]
          mov DWORD PTR [_iniSize],EAX
          mov DWORD PTR [ESP],ESI
          call _malloc
          test EAX,EAX
          mov DWORD PTR [_iniBuf],EAX
          je L_40b104
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],255
          mov DWORD PTR [ESP],EAX
          call _memset
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_4502cd
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [_iniSize]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [_iniBuf]
          mov DWORD PTR [ESP],EAX
          call _fread
          mov DWORD PTR [ESP],EDI
          call _fclose
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_4502dd
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [_iniBuf]
          cmp BYTE PTR [EAX],255
          je L_40b093
          cmp BYTE PTR [EAX+1],255
          je L_40b093
          mov EDX,DWORD PTR [_iniSize]
          mov BYTE PTR [EAX+EDX*1],255
          mov DWORD PTR [ESP+4],OFFSET L_450347
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [_iniSize]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [_iniBuf]
          mov DWORD PTR [ESP],EAX
          call FUN_408fe0
          mov DWORD PTR [ESP+4],OFFSET L_4502dd
          mov DWORD PTR [ESP],1
          mov DWORD PTR [_iniSize],EAX
          call _log_printf
          mov EAX,DWORD PTR [_iniSize]
          mov EDX,DWORD PTR [_iniBuf]
          mov BYTE PTR [EDX+EAX*1],0
          mov EAX,1
L_40b089:
          add ESP,1040
          pop EBX
          pop ESI
          pop EDI
          ret 
L_40b093:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_4502e4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [_iniBuf]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [_iniBuf],0
          mov DWORD PTR [_iniSize],0
          add ESP,1040
          pop EBX
          xor EAX,EAX
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
L_40b0e0:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_450290
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,1040
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          ret 
L_40b104:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_44fbb0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP],EDI
          call _fclose
          xor EAX,EAX
          jmp L_40b089
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.data
.p2align 5
L_44a020:
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_44a044:
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_44a05c:
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_44a074:
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_44a08c:
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_44a0c0:
          .zero 4
L_44a0c4:
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7
          .byte 0x0
          .byte 0x19
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb
          .byte 0x0
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xa
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x0
          .byte 0xc
          .byte 0x0
          .byte 0x17
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x1a
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xbe
          .byte 0xfe
          .byte 0x3
          .byte 0x1b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_44a140:
          .zero 4
L_44a144:
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc0
          .byte 0x0
          .byte 0x0
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xe
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb
          .byte 0x0
          .byte 0xf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x1a
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xbe
          .byte 0xfe
          .byte 0x3
          .byte 0x1b
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_44a1a0:
          .zero 4
L_44a1a4:
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xe
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb
          .byte 0x0
          .byte 0xf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x1a
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xbe
          .byte 0xfe
          .byte 0x3
          .byte 0x1b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_44a200:
          .zero 4
L_44a204:
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x11
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x12
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x13
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x15
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x0
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xa
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9
          .byte 0x0
          .byte 0x16
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x9
          .byte 0x0
          .byte 0x17
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x9
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x50
          .byte 0x9
          .byte 0x0
          .byte 0x19
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x50
          .byte 0xd
          .byte 0x0
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x1a
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xbe
          .byte 0xfe
          .byte 0x3
          .byte 0x1b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_44a2a0:
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7
          .byte 0x0
          .byte 0x19
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb
          .byte 0x0
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xa
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x0
          .byte 0xc
          .byte 0x0
          .byte 0x17
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x1a
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xbe
          .byte 0xfe
          .byte 0x3
          .byte 0x1b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_44a320:
          .string "none"
          .zero 27
L_44a340:
          .string "smc.bin"
          .zero 24
L_44a360:
          .string "kv.bin"
          .zero 25
L_44a380:
          .string "kv_alt.bin"
          .zero 21
L_44a3a0:
          .string "xell-gggggg.bin"
          .zero 16
L_44a3c0:
          .string "xell-2f.bin"
          .zero 20
L_44a3e0:
          .string "patches_"
          .zero 23
L_44a400:
          .string "smc_config.bin"
          .zero 17
L_44a420:
          .string "freeboot.bin"
          .zero 19
L_44a440:
          .string "fuses.bin"
          .zero 22
L_44a460:
          .string "payload.bin"
          .zero 20

.section .rdata,"dr"
.p2align 5
L_44fb60:
          .string "\n------ parsing ini at '%s' ------\n"
L_44fb84:
          .string "rb"
          .zero 1
L_44fb88:
          .string "\n******* ERROR: could not open '%s'\n"
          .zero 3
L_44fbb0:
          .string "******* ERROR loading %s, unable to allocate memory\n"
          .zero 3
L_44fbe8:
          .string "\n\n***** ERROR: File descriptor ini %s\nappears to be a multi byte file, not an ascii only file!\n"
L_44fc48:
          .ascii "["
          .string "version]"
L_44fc52:
          .ascii "i"
          .string "ni version %s\n"
L_44fc62:
          .string "%s_jtag_%s.bin"
L_44fc71:
          .string "%s_devk_%s.bin"
L_44fc80:
          .string "%s_testk_%s.bin"
L_44fc90:
          .string "%s_devgl_%s.bin"
L_44fca0:
          .string "%s_retail_%s.bin"
L_44fcb1:
          .string "%s_g2m_%s.bin"
L_44fcbf:
          .string "%s_g2_%s.bin"
L_44fccc:
          .string "%s_gg_%s.bin"
          .zero 3
L_44fcdc:
          .string "\n******* ERROR: could not find label [version] in file list ini\n"
L_44fd1d:
          .string "[%sbl%s]"
L_44fd26:
          .string "[%sbl]"
L_44fd2d:
          .string "\nini: label %s found\n"
          .zero 1
L_44fd44:
          .string "\n******* ERROR: ini problem, error in %s section!\n"
          .zero 1
L_44fd78:
          .string "\n******* ERROR: crc data for file '%s' in ini is incorrect size!\n"
L_44fdba:
          .string "found (%d) '%s' crc: 0x%08x\n"
          .zero 1
L_44fdd8:
          .string "\n******* ERROR: ini problem, can't find enough data for %s section!\n"
          .zero 3
L_44fe20:
          .string "\n******* ERROR: could not find label %s in file list ini\n"
L_44fe5a:
          .string "none"
          .zero 1
L_44fe60:
          .string "ini dictates dual CB for this model\n"
L_44fe85:
          .ascii "["
          .string "rawpatch]"
L_44fe90:
          .ascii "\n"
          .string "ini: label [rawpatch] found\n"
          .zero 2
L_44feb0:
          .string "\n******* ERROR: an entry in [rawpatch] is missing offset info!\n"
L_44fef0:
          .string "\n******* ERROR: offset data for file '%s' is either too large or too small!\n"
          .zero 3
L_44ff40:
          .string "found (%d) '%s' offset: 0x%08x\n"
L_44ff60:
          .string "***** ERROR: [rawpatch] '%s' length is unintelligible!\n"
L_44ff98:
          .string "\n******* ERROR: file name in [rawpatch] is too long!\n"
          .zero 2
L_44ffd0:
          .ascii "\n******* ERROR: %d of %d [rawpatch] slots are al"
L_450000:
          .string "ready full!\n"
          .zero 3
L_450010:
          .string "\n[rawpatch] label not found in ini\n"
L_450034:
          .ascii "["
          .string "flashfs]"
L_45003e:
          .ascii "\n"
          .string "ini: label [flashfs] found\n"
          .zero 1
L_45005c:
          .string "\n******* ERROR: file in [flashfs] has greater than %d chars in it's name!\n"
L_4500a7:
          .string "\n        Line: %s\n"
          .zero 2
L_4500bc:
          .string "\n******* ERROR: file in [flashfs] has greater than %d chars in it's path!\n"
          .zero 1
L_450108:
          .string "\n******* ERROR: could not find label [flashfs] in file list ini\n"
L_450149:
          .ascii "["
          .string "security]"
L_450154:
          .ascii "\n"
          .string "ini: label [security] found\n"
          .zero 2
L_450174:
          .string "\n******* ERROR: file in [security] has greater than %d chars in it's name!\n"
L_4501c0:
          .string "------ ini parsing completed ------\n\n"
          .zero 2
L_4501e8:
          .long L_409a30
          .long L_409a15
          .long L_409a60
          .long L_409a45
          .long L_409a75
          .long L_409780
          .long L_409780
          .long L_409780
          .long L_409780
          .long L_409780
          .long L_409780
          .long L_409780
          .long L_409780
          .long L_409780
          .long L_409780
          .long L_409780
          .long L_409780
          .long L_409780
          .long L_409780
          .long L_409780
          .long L_409780
          .long L_409780
          .long L_409a00
          .long L_409963
          .long L_409930
          .long L_409945
          .long L_409a30
          .long L_409770
L_450258:
          .string "true"
L_45025d:
          .string "false"
          .zero 1
L_450264:
          .string "\n------ parsing user ini at '%s' ------\n"
          .zero 3
L_450290:
          .string "\n******* WARNING: could not open user ini at '%s', skipping\n"
L_4502cd:
          .string "loading file..."
L_4502dd:
          .string "done!\n"
L_4502e4:
          .string "***** WARNING: User ini %s\nappears to be a multi byte file, not an ascii only file - ignoring it!\n"
L_450347:
          .string "pre-parsing and sanitizing\n"
          .zero 29
L_450380:
          .ascii "A"
          .ascii "BCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,;[]_\n\\/-$:"
L_4503ca:
          .string "xenon"
L_4503d0:
          .string "zephyr"
L_4503d7:
          .string "falcon"
L_4503de:
          .string "jasper"
L_4503e5:
          .string "trinity"
L_4503ed:
          .string "corona"
L_4503f4:
          .string "winchester"
          .zero 1
L_450400:
          .zero 4
          .long L_4503ca
          .long L_4503d0
          .long L_4503d7
          .long L_4503de
          .long L_4503e5
          .long L_4503ed
          .long L_4503f4

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
          .long FUN_408ec0 - .
          .byte 0x1d
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
          .byte 0x10
          .byte 0x2
          .byte 0xb3
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_408fe0 - .
          .byte 0x23
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
          .byte 0x50
          .byte 0x3
          .byte 0x79
          .byte 0x2
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_409310 - .
          .byte 0xb8
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
          .byte 0x8b
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
          .byte 0x48
          .byte 0xb
          .byte 0x43
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x46
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
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_4093d0 - .
          .byte 0x3a
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
          .byte 0x76
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_409410 - .
          .byte 0x15
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_409430 - .
          .byte 0xd2
          .byte 0x15
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
          .byte 0xb0
          .byte 0x9
          .byte 0x3
          .byte 0x17
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
          .byte 0x4b
          .byte 0xb
          .byte 0x3
          .byte 0x8
          .byte 0x2
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
          .byte 0x3
          .byte 0x76
          .byte 0x6
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
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa0
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _getIniValue - .
          .byte 0xbd
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
          .byte 0x45
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0xa1
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
          .byte 0x43
          .byte 0xe
          .byte 0x14
          .byte 0x45
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf4
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_40aad0 - .
          .byte 0x16
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
          .byte 0x50
          .byte 0x55
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
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_40abf0 - .
          .byte 0xfa
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
          .byte 0x50
          .byte 0x2
          .byte 0xee
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
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_40acf0 - .
          .byte 0xe2
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
          .byte 0x50
          .byte 0x5d
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
          .byte 0x2
          .byte 0xa9
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
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc4
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_40ade0 - .
          .byte 0xa
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
          .byte 0x50
          .byte 0x2
          .byte 0xc6
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
          .byte 0x71
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
          .byte 0x58
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_40aef0 - .
          .byte 0x3b
          .byte 0x2
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
          .byte 0x46
          .byte 0xe
          .byte 0xa0
          .byte 0x8
          .byte 0x3
          .byte 0x96
          .byte 0x1
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
          .byte 0x41
          .byte 0xb
          .byte 0x7f
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x43
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x49
          .byte 0xb
          .byte 0x5e
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
          .byte 0x41
          .byte 0xb
