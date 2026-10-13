# app/timeutil.s -- gmtime/mktime/rand, date arithmetic constants
#
# original placement:
#   .eh_frame      004663b0-00466590
#   .rdata         00450420-00450480
#   .rdata$zzz     00463854-00463880
#   .text          0040b130-0040bd30

.intel_syntax noprefix
.globl FUN_40b700
.globl FUN_40b910
.globl FUN_40ba30
.globl FUN_40bae0

.text
.p2align 4
L_40b130:
          push EBP
          push EDI
          xor EAX,EAX
          push ESI
          push EBX
          sub ESP,28
          mov ECX,DWORD PTR [ESP+48]
          movzx EDI,WORD PTR [ECX+12]
          cmp DI,999
          ja L_40b319
          movzx EBP,WORD PTR [ECX+10]
          cmp BP,59
          ja L_40b319
          movzx ESI,WORD PTR [ECX+8]
          cmp SI,59
          ja L_40b319
          movzx EBX,WORD PTR [ECX+6]
          cmp BX,23
          mov WORD PTR [ESP+4],BX
          ja L_40b319
          movzx EDX,WORD PTR [ECX+2]
          mov EBX,EDX
          mov WORD PTR [ESP+8],DX
          sub EDX,1
          cmp DX,11
          ja L_40b319
          movzx EDX,WORD PTR [ECX+4]
          test DX,DX
          je L_40b319
          movzx EAX,DX
          cmp BX,2
          mov DWORD PTR [ESP+16],EAX
          mov EAX,1
          je L_40b1f2
          movzx EDX,WORD PTR [ECX]
          xor EAX,EAX
          test DL,3
          jne L_40b1f2
          movzx EAX,DX
          mov EDX,1374389535
          mov DWORD PTR [ESP+20],EAX
          imul EDX
          mov EAX,1
          mov EBX,EDX
          shr EDX,5
          imul EDX,EDX,100
          cmp DWORD PTR [ESP+20],EDX
          jne L_40b1f2
          mov EDX,EBX
          shr EDX,7
          imul EAX,EDX,400
          cmp DWORD PTR [ESP+20],EAX
          sete AL
          movzx EAX,AL
L_40b1f2:
          movzx EDX,WORD PTR [ESP+8]
          mov EBX,EDX
          lea EDX,DWORD PTR [EAX+EAX*1]
          mov DWORD PTR [ESP+20],EBX
          add EAX,EDX
          lea EDX,DWORD PTR [EBX+EAX*4-1]
          xor EAX,EAX
          mov EBX,DWORD PTR [ESP+16]
          cmp EBX,DWORD PTR [EDX*4+L_450420]
          jg L_40b319
          movzx EDX,WORD PTR [ECX]
          cmp DX,1600
          jbe L_40b319
          cmp WORD PTR [ESP+8],2
          mov EAX,DWORD PTR [ESP+20]
          ja L_40b321
          add EAX,13
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [EDX-1]
L_40b241:
          imul ECX,EAX,36525
          mov EBX,EAX
          mov EAX,1374389535
          imul ECX
          sar ECX,31
          mov EAX,1374389535
          sar EDX,5
          sub EDX,ECX
          mov ECX,EDX
          imul EBX
          mov EAX,EBX
          mov EBX,24
          sar EAX,31
          sar EDX,5
          sub EDX,EAX
          lea EAX,DWORD PTR [EDX+EDX*2+3]
          sar EAX,2
          sub ECX,EAX
          imul EAX,DWORD PTR [ESP+8],1959
          sar EAX,6
          add ECX,EAX
          mov EAX,DWORD PTR [ESP+16]
          lea ECX,DWORD PTR [EAX+ECX*1-584817]
          mov EAX,EBX
          imul ECX
          mov ECX,60
          mov DWORD PTR [ESP+8],EAX
          movzx EAX,WORD PTR [ESP+4]
          mov DWORD PTR [ESP+12],EDX
          xor EDX,EDX
          add EAX,DWORD PTR [ESP+8]
          adc EDX,DWORD PTR [ESP+12]
          imul EBX,EDX,60
          mul ECX
          mov DWORD PTR [ESP+4],EBX
          mov EBX,DWORD PTR [ESP+4]
          mov ECX,EAX
          movzx EAX,SI
          mov ESI,60
          add EBX,EDX
          xor EDX,EDX
          add EAX,ECX
          adc EDX,EBX
          movzx ECX,BP
          imul EBX,EDX,60
          mul ESI
          add EDX,EBX
          xor EBX,EBX
          add EAX,ECX
          adc EDX,EBX
          mov ECX,1000
          imul EBP,EDX,1000
          mul ECX
          mov ECX,EAX
          mov EBX,EDX
          movzx EAX,DI
          add EBX,EBP
          xor EDX,EDX
          add EAX,ECX
          adc EDX,EBX
          mov ECX,10000
          imul EBX,EDX,10000
          mul ECX
          mov ECX,DWORD PTR [ESP+52]
          add EDX,EBX
          mov DWORD PTR [ECX],EAX
          mov EAX,1
          mov DWORD PTR [ECX+4],EDX
L_40b319:
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_40b321:
          add EAX,1
          mov DWORD PTR [ESP+8],EAX
          movzx EAX,DX
          jmp L_40b241
L_40b330:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EAX,DWORD PTR [ESP+48]
          mov EBX,DWORD PTR [ESP+52]
          mov ESI,DWORD PTR [EAX]
          mov EDI,DWORD PTR [EAX+4]
          mov DWORD PTR [ESP+8],10000000
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EDI
          call FUN_447d70
          mov DWORD PTR [ESP+8],10000
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDX
          call FUN_447c30
          mov WORD PTR [EBX+12],AX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP+8],10000000
          mov DWORD PTR [ESP+12],0
          call FUN_447c30
          mov DWORD PTR [ESP+8],86400
          mov ESI,EAX
          mov EDI,EDX
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDX
          call FUN_447f20
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EDI
          mov EBP,EAX
          mov DWORD PTR [ESP+8],86400
          mov DWORD PTR [ESP+12],0
          call FUN_448040
          mov ECX,EAX
          mov EDX,2443359173
          mov EAX,ECX
          imul EDX
          mov EAX,ECX
          sar EAX,31
          add EDX,ECX
          sar EDX,11
          sub EDX,EAX
          mov WORD PTR [EBX+6],DX
          imul EDX,EDX,3600
          sub ECX,EDX
          mov EDX,2290649225
          mov EAX,ECX
          imul EDX
          mov EAX,ECX
          sar EAX,31
          add EDX,ECX
          sar EDX,5
          sub EDX,EAX
          mov WORD PTR [EBX+8],DX
          imul EDX,EDX,60
          sub ECX,EDX
          mov EDX,2454267027
          mov WORD PTR [EBX+10],CX
          lea ECX,DWORD PTR [EBP+1]
          mov EAX,ECX
          imul EDX
          mov EAX,ECX
          sar EAX,31
          add EDX,ECX
          sar EDX,2
          sub EDX,EAX
          lea EAX,DWORD PTR [EDX*8]
          sub EAX,EDX
          mov EDX,963315389
          sub ECX,EAX
          mov WORD PTR [EBX+14],CX
          lea ECX,DWORD PTR [EBP*4+1227]
          mov EAX,ECX
          sar ECX,31
          imul EDX
          sar EDX,15
          sub EDX,ECX
          lea EDX,DWORD PTR [EDX+EDX*2+3]
          lea EAX,DWORD PTR [EDX+3]
          test EDX,EDX
          cmovns EAX,EDX
          mov EDX,2408239021
          sar EAX,2
          lea EDI,DWORD PTR [EAX+EBP*1+28188]
          lea EAX,DWORD PTR [EDI+EDI*4]
          lea ECX,DWORD PTR [EAX*4-2442]
          mov EAX,ECX
          imul EDX
          lea ESI,DWORD PTR [EDX+ECX*1]
          sar ECX,31
          mov EDX,1122523357
          sar ESI,12
          sub ESI,ECX
          imul EAX,ESI,-1461
          lea ECX,DWORD PTR [EAX+3]
          test EAX,EAX
          cmovns ECX,EAX
          sar ECX,2
          add ECX,EDI
          mov EDI,ECX
          shl EDI,6
          mov EAX,EDI
          sar EDI,31
          imul EDX
          sar EDX,9
          sub EDX,EDI
          lea EDI,DWORD PTR [ESI+1524]
          cmp EDX,13
          lea EAX,DWORD PTR [EDX-1]
          jle L_40b4d2
          lea EAX,DWORD PTR [EDX-13]
          lea EDI,DWORD PTR [ESI+1525]
L_40b4d2:
          imul EDX,EDX,1959
          mov WORD PTR [EBX+2],AX
          mov WORD PTR [EBX],DI
          lea EAX,DWORD PTR [EDX+63]
          test EDX,EDX
          cmovs EDX,EAX
          sar EDX,6
          sub ECX,EDX
          mov WORD PTR [EBX+4],CX
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
L_40b500:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EAX,DWORD PTR [ESP+64]
          mov EDI,DWORD PTR [ESP+68]
          mov ESI,DWORD PTR [EAX]
          mov EBX,DWORD PTR [EAX+4]
          mov DWORD PTR [ESP+8],10000000
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EBX
          call FUN_447d70
          mov DWORD PTR [ESP+8],10000
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDX
          call FUN_447c30
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],10000000
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+28],EAX
          call FUN_447c30
          mov DWORD PTR [ESP+8],86400
          mov EBX,EAX
          mov ESI,EDX
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDX
          call FUN_447f20
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],ESI
          mov EBP,EAX
          mov DWORD PTR [ESP+8],86400
          mov DWORD PTR [ESP+12],0
          call FUN_448040
          mov ECX,EAX
          mov EDX,2443359173
          mov EAX,ECX
          imul EDX
          mov EAX,ECX
          sar EAX,31
          lea EBX,DWORD PTR [EDX+ECX*1]
          mov EDX,2290649225
          sar EBX,11
          sub EBX,EAX
          imul EAX,EBX,3600
          sub ECX,EAX
          mov EAX,ECX
          imul EDX
          mov EAX,ECX
          sar EAX,31
          add EDX,ECX
          sar EDX,5
          sub EDX,EAX
          imul EAX,EDX,60
          mov DWORD PTR [ESP+16],EDX
          mov EDX,2454267027
          sub ECX,EAX
          mov DWORD PTR [ESP+20],ECX
          lea ECX,DWORD PTR [EBP+1]
          mov EAX,ECX
          imul EDX
          mov EAX,ECX
          sar EAX,31
          add EDX,ECX
          sar EDX,2
          sub EDX,EAX
          lea EAX,DWORD PTR [EDX*8]
          sub EAX,EDX
          mov EDX,963315389
          sub ECX,EAX
          mov DWORD PTR [ESP+24],ECX
          lea ECX,DWORD PTR [EBP*4+1227]
          mov EAX,ECX
          sar ECX,31
          imul EDX
          sar EDX,15
          sub EDX,ECX
          lea EDX,DWORD PTR [EDX+EDX*2+3]
          lea EAX,DWORD PTR [EDX+3]
          test EDX,EDX
          cmovns EAX,EDX
          mov EDX,2408239021
          sar EAX,2
          lea EBP,DWORD PTR [EAX+EBP*1+28188]
          lea EAX,DWORD PTR [EBP+EBP*4]
          lea ESI,DWORD PTR [EAX*4-2442]
          mov EAX,ESI
          imul EDX
          lea ECX,DWORD PTR [EDX+ESI*1]
          sar ESI,31
          mov EDX,1122523357
          sar ECX,12
          sub ECX,ESI
          imul EAX,ECX,-1461
          lea ESI,DWORD PTR [EAX+3]
          test EAX,EAX
          cmovns ESI,EAX
          sar ESI,2
          add ESI,EBP
          mov EBP,ESI
          shl EBP,6
          mov EAX,EBP
          sar EBP,31
          imul EDX
          sar EDX,9
          sub EDX,EBP
          lea EBP,DWORD PTR [ECX+1524]
          cmp EDX,13
          lea EAX,DWORD PTR [EDX-1]
          jle L_40b6a0
          lea EAX,DWORD PTR [EDX-13]
          lea EBP,DWORD PTR [ECX+1525]
L_40b6a0:
          imul EDX,EDX,1959
          mov WORD PTR [EDI+2],AX
          mov WORD PTR [EDI],BP
          mov WORD PTR [EDI+8],BX
          lea EAX,DWORD PTR [EDX+63]
          test EDX,EDX
          cmovs EDX,EAX
          movzx EAX,WORD PTR [ESP+16]
          sar EDX,6
          sub ESI,EDX
          mov WORD PTR [EDI+6],SI
          mov WORD PTR [EDI+10],AX
          movzx EAX,WORD PTR [ESP+20]
          mov WORD PTR [EDI+12],AX
          movzx EAX,WORD PTR [ESP+28]
          mov WORD PTR [EDI+14],AX
          movzx EAX,WORD PTR [ESP+24]
          mov WORD PTR [EDI+4],AX
          add ESP,44
          mov EAX,1
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
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_40b700:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EAX,DWORD PTR [ESP+48]
          movzx EDI,WORD PTR [EAX+10]
          movzx ECX,WORD PTR [EAX+14]
          movzx EDX,WORD PTR [EAX+2]
          movzx ESI,WORD PTR [EAX+8]
          movzx EBX,WORD PTR [EAX+6]
          mov EBP,EDI
          mov WORD PTR [ESP+2],DI
          movzx EDI,WORD PTR [EAX+12]
          cmp CX,999
          mov WORD PTR [ESP],DX
          mov WORD PTR [ESP+6],CX
          seta DL
          cmp DI,59
          mov WORD PTR [ESP+4],DI
          seta CL
          mov EDI,ECX
          or EDI,EDX
          cmp BP,59
          seta DL
          or EDI,EDX
          cmp SI,23
          seta DL
          or EDX,EDI
          test BX,BX
          sete CL
          or CL,DL
          jne L_40b8d0
          movzx EDI,WORD PTR [ESP]
          mov EDX,EDI
          sub EDX,1
          cmp DX,11
          ja L_40b8d0
          movzx EBP,WORD PTR [EAX]
          cmp DI,2
          movzx EAX,BX
          mov DWORD PTR [ESP+8],EAX
          je L_40b8e6
          movzx EAX,BP
          xor EDX,EDX
          test EBP,3
          mov DWORD PTR [ESP+12],EAX
          mov ECX,EAX
          mov EDI,EAX
          jne L_40b7cf
          mov EBX,1374389535
          imul EBX
          mov EBX,EDX
          shr EDX,5
          imul EAX,EDX,100
          mov EDX,1
          cmp ECX,EAX
          jne L_40b7cf
          shr EBX,7
          xor EDX,EDX
          imul EAX,EBX,400
          cmp ECX,EAX
          sete DL
L_40b7cf:
          movzx ECX,WORD PTR [ESP]
          lea EAX,DWORD PTR [EDX+EDX*1]
          add EAX,EDX
          mov EDX,DWORD PTR [ESP+8]
          movzx EBX,CX
          lea EAX,DWORD PTR [EBX+EAX*4-1]
          cmp EDX,DWORD PTR [EAX*4+L_450420]
          jg L_40b8d0
          cmp BP,1600
          jbe L_40b8d0
          cmp CX,2
          lea EBP,DWORD PTR [EBX+1]
          jbe L_40b900
L_40b808:
          imul ECX,EDI,36525
          mov EBX,1374389535
          imul EBP,EBP,1959
          mov EAX,ECX
          imul EBX
          mov EAX,ECX
          sar EBP,6
          sar EAX,31
          sar EDX,5
          sub EDX,EAX
          mov EAX,EDI
          sar EDI,31
          mov ECX,EDX
          imul EBX
          sar EDX,5
          sub EDX,EDI
          xor EDI,EDI
          lea EAX,DWORD PTR [EDX+EDX*2+3]
          sar EAX,2
          sub ECX,EAX
          mov EAX,DWORD PTR [ESP+8]
          add ECX,EBP
          lea EDX,DWORD PTR [EAX+ECX*1-584817]
          mov EAX,24
          imul EDX
          add EAX,ESI
          adc EDX,EDI
          mov EDI,60
          xor EBX,EBX
          imul ECX,EDX,60
          mul EDI
          add EDX,ECX
          movzx ECX,WORD PTR [ESP+2]
          add EAX,ECX
          mov ECX,1000
          adc EDX,EBX
          imul EBX,EDX,60
          mul EDI
          movzx EDI,WORD PTR [ESP+4]
          add EDX,EBX
          mov ESI,EDI
          xor EDI,EDI
          add ESI,EAX
          mov EAX,ECX
          adc EDI,EDX
          mul ESI
          imul EBX,EDI,1000
          mov ESI,EAX
          movzx EAX,WORD PTR [ESP+6]
          mov EDI,EDX
          add EDI,EBX
          xor EDX,EDX
          add ESI,EAX
          mov EAX,10000
          adc EDI,EDX
          imul EBX,EDI,10000
          mul ESI
          mov ESI,DWORD PTR [ESP+52]
          add EBX,EDX
          mov DWORD PTR [ESI],EAX
          mov EAX,1
          mov DWORD PTR [ESI+4],EBX
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
L_40b8d0:
          call DWORD PTR [_errno]
          mov DWORD PTR [EAX],22
          add ESP,28
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_40b8e6:
          cmp DWORD PTR [ESP+8],29
          jg L_40b8d0
          cmp BP,1600
          jbe L_40b8d0
          movzx EAX,BP
          mov EBX,2
          mov DWORD PTR [ESP+12],EAX
L_40b900:
          mov EDI,DWORD PTR [ESP+12]
          lea EBP,DWORD PTR [EBX+13]
          sub EDI,1
          jmp L_40b808
          .byte 0x90
FUN_40b910:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov ECX,DWORD PTR [ESP+68]
          mov EAX,DWORD PTR [ESP+64]
          test ECX,ECX
          je L_40ba00
          mov EDX,DWORD PTR [ESP+72]
          test EDX,EDX
          je L_40ba00
          mov EBX,DWORD PTR [EAX]
          mov EBP,DWORD PTR [EAX+4]
          mov DWORD PTR [ESP+8],10000000
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EBP
          call FUN_447c30
          mov DWORD PTR [ESP+8],10000000
          mov DWORD PTR [ESP+12],0
          mov ESI,EAX
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EBP
          mov EDI,EDX
          call FUN_447d70
          or EDX,EAX
          jne L_40ba20
          add ESI,1240428288
          adc EDI,-3
L_40b985:
          mov EAX,ESI
          and EAX,1
          test EAX,EAX
          je L_40b994
          add ESI,1
          adc EDI,0
L_40b994:
          cmp EDI,0
          ja L_40ba00
          lea EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+28],ESI
          mov DWORD PTR [ESP],EAX
          call FUN_449110
          movzx ECX,WORD PTR [EAX+8]
          movzx EDX,WORD PTR [EAX+4]
          mov ESI,DWORD PTR [EAX]
          mov EDI,DWORD PTR [ESP+72]
          mov EBX,DWORD PTR [ESP+68]
          shl EDX,5
          shl ECX,11
          add ECX,EDX
          mov EDX,ESI
          shr EDX,31
          add EDX,ESI
          sar EDX,1
          add EDX,ECX
          mov WORD PTR [EDI],DX
          movzx EDI,WORD PTR [EAX+20]
          lea EDX,DWORD PTR [EDI-80]
          movzx EDI,WORD PTR [EAX+16]
          mov ECX,EDX
          shl ECX,9
          lea EDX,DWORD PTR [EDI+1]
          shl EDX,5
          add EDX,ECX
          add DX,WORD PTR [EAX+12]
          mov EAX,1
          mov WORD PTR [EBX],DX
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_40ba00:
          call DWORD PTR [_errno]
          mov DWORD PTR [EAX],22
          add ESP,44
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40ba20:
          add ESI,1240428289
          adc EDI,-3
          jmp L_40b985
          .byte 0x66
          .byte 0x90
FUN_40ba30:
          sub ESP,76
          mov EDX,DWORD PTR [ESP+84]
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+60],4294967295
          mov ECX,EDX
          and ECX,31
          add ECX,ECX
          mov DWORD PTR [ESP+28],ECX
          mov ECX,EDX
          shr DX,11
          movzx EDX,DX
          shr CX,5
          mov DWORD PTR [ESP+36],EDX
          mov EDX,EAX
          and ECX,63
          and EDX,31
          mov DWORD PTR [ESP+32],ECX
          mov DWORD PTR [ESP+40],EDX
          mov EDX,EAX
          shr AX,9
          movzx EAX,AX
          shr DX,5
          add EAX,80
          and EDX,15
          mov DWORD PTR [ESP+48],EAX
          lea EAX,DWORD PTR [ESP+28]
          sub EDX,1
          mov DWORD PTR [ESP+44],EDX
          mov DWORD PTR [ESP],EAX
          call FUN_4490e8
          mov DWORD PTR [ESP+24],EAX
          lea EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],EAX
          call FUN_449110
          mov DWORD PTR [ESP],EAX
          call FUN_4490e8
          mov EDX,EAX
          mov EAX,DWORD PTR [ESP+24]
          mov ECX,DWORD PTR [ESP+88]
          add EAX,EAX
          sub EAX,EDX
          mov EDX,10000000
          mul EDX
          add EAX,3577643008
          adc EDX,27111902
          mov DWORD PTR [ECX],EAX
          mov EAX,1
          mov DWORD PTR [ECX+4],EDX
          add ESP,76
          ret 
          .byte 0x90
FUN_40bae0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov DWORD PTR [ESP],0
          mov EDI,DWORD PTR [ESP+64]
          call FUN_449050
          mov EBX,EAX
          mov EAX,10000000
          mov DWORD PTR [ESP+8],10000000
          imul EBX
          mov DWORD PTR [ESP+12],0
          add EAX,3577643008
          adc EDX,27111902
          mov DWORD PTR [ESP],EAX
          mov EBX,EAX
          mov DWORD PTR [ESP+4],EDX
          mov ESI,EDX
          call FUN_447d70
          mov DWORD PTR [ESP+8],10000
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDX
          call FUN_447c30
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP+8],10000000
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+28],EAX
          call FUN_447c30
          mov DWORD PTR [ESP+8],86400
          mov EBX,EAX
          mov ESI,EDX
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDX
          call FUN_447f20
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],ESI
          mov EBP,EAX
          mov DWORD PTR [ESP+8],86400
          mov DWORD PTR [ESP+12],0
          call FUN_448040
          mov ECX,EAX
          mov EDX,2443359173
          mov EAX,ECX
          imul EDX
          mov EAX,ECX
          sar EAX,31
          lea EBX,DWORD PTR [EDX+ECX*1]
          mov EDX,2290649225
          sar EBX,11
          sub EBX,EAX
          imul EAX,EBX,3600
          sub ECX,EAX
          mov EAX,ECX
          imul EDX
          mov EAX,ECX
          sar EAX,31
          add EDX,ECX
          sar EDX,5
          sub EDX,EAX
          imul EAX,EDX,60
          mov DWORD PTR [ESP+16],EDX
          mov EDX,2454267027
          sub ECX,EAX
          mov DWORD PTR [ESP+20],ECX
          lea ECX,DWORD PTR [EBP+1]
          mov EAX,ECX
          imul EDX
          mov EAX,ECX
          sar EAX,31
          add EDX,ECX
          sar EDX,2
          sub EDX,EAX
          lea EAX,DWORD PTR [EDX*8]
          sub EAX,EDX
          mov EDX,963315389
          sub ECX,EAX
          mov DWORD PTR [ESP+24],ECX
          lea ECX,DWORD PTR [EBP*4+1227]
          mov EAX,ECX
          sar ECX,31
          imul EDX
          sar EDX,15
          sub EDX,ECX
          lea EDX,DWORD PTR [EDX+EDX*2+3]
          lea EAX,DWORD PTR [EDX+3]
          test EDX,EDX
          cmovns EAX,EDX
          mov EDX,2408239021
          sar EAX,2
          lea EBP,DWORD PTR [EAX+EBP*1+28188]
          lea EAX,DWORD PTR [EBP+EBP*4]
          lea ESI,DWORD PTR [EAX*4-2442]
          mov EAX,ESI
          imul EDX
          lea ECX,DWORD PTR [EDX+ESI*1]
          sar ESI,31
          mov EDX,1122523357
          sar ECX,12
          sub ECX,ESI
          imul EAX,ECX,-1461
          lea ESI,DWORD PTR [EAX+3]
          test EAX,EAX
          cmovns ESI,EAX
          sar ESI,2
          add ESI,EBP
          mov EBP,ESI
          shl EBP,6
          mov EAX,EBP
          sar EBP,31
          imul EDX
          sar EDX,9
          sub EDX,EBP
          lea EBP,DWORD PTR [ECX+1524]
          cmp EDX,13
          lea EAX,DWORD PTR [EDX-1]
          jle L_40bc9b
          lea EAX,DWORD PTR [EDX-13]
          lea EBP,DWORD PTR [ECX+1525]
L_40bc9b:
          imul EDX,EDX,1959
          mov WORD PTR [EDI+2],AX
          mov WORD PTR [EDI],BP
          mov WORD PTR [EDI+8],BX
          lea EAX,DWORD PTR [EDX+63]
          test EDX,EDX
          cmovs EDX,EAX
          movzx EAX,WORD PTR [ESP+16]
          sar EDX,6
          sub ESI,EDX
          mov WORD PTR [EDI+6],SI
          mov WORD PTR [EDI+10],AX
          movzx EAX,WORD PTR [ESP+20]
          mov WORD PTR [EDI+12],AX
          movzx EAX,WORD PTR [ESP+28]
          mov WORD PTR [EDI+14],AX
          movzx EAX,WORD PTR [ESP+24]
          mov WORD PTR [EDI+4],AX
          mov DWORD PTR [ESP],0
          call FUN_449050
          mov DWORD PTR [ESP],EAX
          call FUN_449090
          call FUN_4490c0
          mov EDX,107481665
          mov ECX,EAX
          mul EDX
          mov EAX,ECX
          sub EAX,EDX
          shr EAX,1
          add EDX,EAX
          shr EDX,9
          imul EDX,EDX,999
          sub ECX,EDX
          mov WORD PTR [EDI+14],CX
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
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
          .byte 0x90

.section .rdata,"dr"
.p2align 5
L_450420:
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x0

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
          .long L_40b130 - .
          .byte 0x0
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
          .byte 0x30
          .byte 0x3
          .byte 0xe3
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
          .long L_40b330 - .
          .byte 0xc8
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
          .byte 0x3
          .byte 0xbc
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_40b500 - .
          .byte 0xf3
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
          .byte 0x3
          .byte 0xe2
          .byte 0x1
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xdc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40b700 - .
          .byte 0xf
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
          .byte 0x30
          .byte 0x3
          .byte 0xbf
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
          .byte 0x46
          .byte 0xb
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
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_40b910 - .
          .byte 0x1e
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
          .byte 0xe1
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
          .byte 0x4b
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8c
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_40ba30 - .
          .byte 0xaf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x50
          .byte 0x2
          .byte 0xab
          .byte 0xe
          .byte 0x4
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa4
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_40bae0 - .
          .byte 0x42
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
          .byte 0x40
          .byte 0x3
          .byte 0x36
          .byte 0x2
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
