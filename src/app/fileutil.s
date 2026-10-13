# app/fileutil.s -- file read/write/dump helpers, mkdir; called by almost every unit
#
# original placement:
#   .data          0044a6e0-0044a700
#   .eh_frame      00469410-00469d48
#   .rdata         00457a80-00457df0
#   .rdata$zzz     00463a90-00463abc
#   .text          00420a90-004236f0

.intel_syntax noprefix
.globl FUN_420a90
.globl FUN_420ab0
.globl FUN_420ad0
.globl FUN_420af0
.globl FUN_420b00
.globl FUN_420b20
.globl FUN_420b50
.globl FUN_420bb0
.globl FUN_420d00
.globl FUN_420d80
.globl FUN_420e40
.globl FUN_420f10
.globl FUN_421000
.globl FUN_4210b0
.globl FUN_421170
.globl FUN_421200
.globl FUN_421300
.globl FUN_421380
.globl FUN_421840
.globl FUN_421860
.globl FUN_421de0
.globl FUN_422350
.globl FUN_4223b0
.globl FUN_4223f0
.globl FUN_422420
.globl FUN_4224d0
.globl FUN_4225a0
.globl FUN_4225d0
.globl FUN_422670
.globl FUN_422aa0
.globl FUN_422ae0
.globl FUN_422b10
.globl FUN_4232e0
.globl FUN_423370
.globl FUN_4233b0
.globl FUN_423420
.globl FUN_423490
.globl FUN_423650

.text
.p2align 4
FUN_420a90:
          mov EDX,DWORD PTR [ESP+4]
          mov EAX,DWORD PTR [L_44a6e0]
          cmp EDX,6
          jle L_420aa0
          repz ret 
L_420aa0:
          mov EAX,DWORD PTR [EDX*4+L_44a6e0]
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_420ab0:
          mov ECX,DWORD PTR [ESP+4]
          movzx EAX,BYTE PTR [ECX]
          shl EAX,8
          mov EDX,EAX
          movzx EAX,BYTE PTR [ECX+1]
          or EAX,EDX
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
FUN_420ad0:
          mov EAX,DWORD PTR [ESP+4]
          mov EAX,DWORD PTR [EAX]
          bswap EAX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_420ae0:
          mov EAX,DWORD PTR [ESP+4]
          mov EDX,DWORD PTR [EAX]
          mov EAX,DWORD PTR [EAX+4]
          bswap EDX
          bswap EAX
          ret 
          .byte 0x66
          .byte 0x90
FUN_420af0:
          mov EAX,DWORD PTR [ESP+4]
          mov EAX,DWORD PTR [EAX]
          ret 
L_420af7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_420b00:
          mov EDX,DWORD PTR [ESP+4]
          mov EAX,DWORD PTR [ESP+8]
          mov ECX,EDX
          mov BYTE PTR [EAX+1],DL
          shr CX,8
          mov BYTE PTR [EAX],CL
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_420b20:
          mov EDX,DWORD PTR [ESP+4]
          mov EAX,DWORD PTR [ESP+8]
          mov ECX,EDX
          mov BYTE PTR [EAX+3],DL
          shr ECX,24
          mov BYTE PTR [EAX],CL
          mov ECX,EDX
          shr ECX,16
          mov BYTE PTR [EAX+1],CL
          mov ECX,EDX
          shr ECX,8
          mov BYTE PTR [EAX+2],CL
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
FUN_420b50:
          push EDI
          push ESI
          push EBX
          mov ECX,DWORD PTR [ESP+16]
          mov EBX,DWORD PTR [ESP+20]
          mov EAX,DWORD PTR [ESP+24]
          mov ESI,ECX
          shrd ESI,EBX,8
          mov BYTE PTR [EAX+7],CL
          mov BYTE PTR [EAX+3],BL
          mov EDX,ESI
          mov ESI,ECX
          shrd ESI,EBX,16
          mov BYTE PTR [EAX+6],DL
          mov EDX,ESI
          mov ESI,ECX
          shrd ESI,EBX,24
          mov BYTE PTR [EAX+5],DL
          mov EDX,ESI
          mov BYTE PTR [EAX+4],DL
          mov EDX,EBX
          shr EDX,8
          mov BYTE PTR [EAX+2],DL
          mov EDX,EBX
          shr EDX,16
          mov BYTE PTR [EAX+1],DL
          mov EDX,EBX
          shr EDX,24
          mov BYTE PTR [EAX],DL
          pop EBX
          pop ESI
          pop EDI
          ret 
L_420ba1:
          jmp FUN_420bb0
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
FUN_420bb0:
          push EBP
          push EDI
          push ESI
          push EBX
          xor EBX,EBX
          sub ESP,28
          mov EDI,DWORD PTR [ESP+52]
          mov EBP,DWORD PTR [ESP+48]
          mov ESI,DWORD PTR [ESP+56]
          test EDI,EDI
          jne L_420bf0
          jmp L_420c10
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_420bd0:
          movzx EAX,BYTE PTR [EBP+EBX*1]
          mov DWORD PTR [ESP+4],OFFSET L_457a86
          add EBX,1
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          cmp EBX,EDI
          je L_420c10
L_420bf0:
          test BL,15
          jne L_420bd0
          mov DWORD PTR [ESP+4],OFFSET L_457a82
          mov DWORD PTR [ESP],ESI
          call FUN_433690
          jmp L_420bd0
L_420c07:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_420c10:
          mov DWORD PTR [ESP+48],ESI
          mov DWORD PTR [ESP+52],OFFSET L_457a80
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp FUN_433690
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_420c30:
          push EDI
          push ESI
          push EBX
          sub ESP,32
          mov EBX,DWORD PTR [ESP+52]
          mov ESI,DWORD PTR [ESP+56]
          mov EDI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],OFFSET L_457a8c
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EDI
          call FUN_433690
          test EBX,EBX
          setne DL
          test ESI,ESI
          setne AL
          test DL,AL
          je L_420c74
          test EDI,EDI
          jne L_420ca3
L_420c74:
          mov DWORD PTR [ESP+4],OFFSET L_457abf
          mov DWORD PTR [ESP],1
          call FUN_433690
L_420c88:
          mov DWORD PTR [ESP+52],OFFSET L_457ad6
          mov DWORD PTR [ESP+48],1
          add ESP,32
          pop EBX
          pop ESI
          pop EDI
          jmp FUN_433690
L_420ca3:
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],OFFSET L_457aaf
          call _fopen
          test EAX,EAX
          mov EDI,EAX
          je L_420ce0
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call FUN_449118
          mov DWORD PTR [ESP],EDI
          call _fclose
          jmp L_420c88
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_420ce0:
          mov DWORD PTR [ESP+4],OFFSET L_457ab2
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_420c88
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_420d00:
          push ESI
          push EBX
          sub ESP,20
          mov EAX,DWORD PTR [ESP+32]
          mov EBX,DWORD PTR [ESP+40]
          test EAX,EAX
          setne CL
          test EBX,EBX
          setne DL
          test CL,DL
          je L_420d70
          mov EDX,DWORD PTR [ESP+36]
          test EDX,EDX
          je L_420d70
          mov DWORD PTR [ESP+4],OFFSET L_457aaf
          mov DWORD PTR [ESP],EAX
          call _fopen
          test EAX,EAX
          mov ESI,EAX
          je L_420d70
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],1
          xor EBX,EBX
          mov DWORD PTR [ESP],EAX
          call FUN_449118
          mov DWORD PTR [ESP],ESI
          cmp EAX,1
          sete BL
          call _fclose
          add ESP,20
          mov EAX,EBX
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_420d70:
          xor EBX,EBX
          add ESP,20
          mov EAX,EBX
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_420d80:
          push EDI
          push ESI
          push EBX
          sub ESP,1040
          mov EBX,DWORD PTR [ESP+1060]
          mov ESI,DWORD PTR [ESP+1064]
          mov EAX,DWORD PTR [ESP+1056]
          test EBX,EBX
          setne CL
          test ESI,ESI
          setne DL
          test CL,DL
          je L_420dd7
          test EAX,EAX
          je L_420dd7
          lea EDI,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EDI
          call FUN_449080
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EDI
          call FUN_449088
          mov EAX,DWORD PTR [ESP+1068]
          test EAX,EAX
          jne L_420de5
L_420dd7:
          add ESP,1040
          xor EBX,EBX
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          ret 
L_420de5:
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],OFFSET L_457aaf
          call _fopen
          test EAX,EAX
          mov EDI,EAX
          je L_420dd7
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+1068]
          xor EBX,EBX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EAX
          call FUN_449118
          mov DWORD PTR [ESP],EDI
          cmp EAX,1
          sete BL
          call _fclose
          add ESP,1040
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_420e40:
          push EDI
          push ESI
          push EBX
          sub ESP,1040
          mov ESI,DWORD PTR [ESP+1060]
          mov EBX,DWORD PTR [ESP+1064]
          mov EAX,DWORD PTR [ESP+1056]
          test ESI,ESI
          setne CL
          test EBX,EBX
          setne DL
          test CL,DL
          je L_420ef5
          test EAX,EAX
          .byte 0x0f,0x84; .long L_420ef5-.-4   # je L_420ef5
          lea EDI,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EDI
          call FUN_449080
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EDI
          call FUN_449088
          mov DWORD PTR [ESP+4],OFFSET L_457aaf
          mov DWORD PTR [ESP],EDI
          call _fopen
          test EAX,EAX
          mov ESI,EAX
          je L_420ef5
          lea EDI,DWORD PTR [EBX+16]
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_420eb0:
          movzx EAX,BYTE PTR [EBX]
          mov DWORD PTR [ESP+4],OFFSET L_457adf
          add EBX,1
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call FUN_449158
          cmp EBX,EDI
          jne L_420eb0
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],10
          call FUN_449150
          mov DWORD PTR [ESP],ESI
          call _fclose
          add ESP,1040
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          ret 
L_420ef5:
          add ESP,1040
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          ret 
L_420f01:
          jmp FUN_420f10
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
FUN_420f10:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1052
          mov EBX,DWORD PTR [ESP+1076]
          mov EDI,DWORD PTR [ESP+1080]
          mov EAX,DWORD PTR [ESP+1072]
          test EBX,EBX
          setne CL
          test EDI,EDI
          setne DL
          test CL,DL
          .byte 0x0f,0x84; .long L_420fbe-.-4   # je L_420fbe
          test EAX,EAX
          je L_420fbe
          lea ESI,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],ESI
          call FUN_449080
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EBX
          call FUN_449088
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],OFFSET L_457aaf
          call _fopen
          test EAX,EAX
          mov ESI,EAX
          je L_420fbe
          xor EBP,EBP
          xor EBX,EBX
          jmp L_420fa0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_420f80:
          movzx EAX,BYTE PTR [EDI+EBX*1]
          mov DWORD PTR [ESP+4],OFFSET L_457adf
          add EBX,1
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call FUN_449158
          cmp EBX,96
          je L_420fd0
L_420fa0:
          test BL,7
          jne L_420f80
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_457ae4
          add EBP,1
          mov DWORD PTR [ESP],ESI
          call FUN_449158
          jmp L_420f80
L_420fbe:
          add ESP,1052
          xor EAX,EAX
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
L_420fd0:
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],10
          call FUN_449150
          mov DWORD PTR [ESP],ESI
          call _fclose
          add ESP,1052
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
FUN_421000:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,24
          mov ESI,DWORD PTR [ESP+56]
          mov EAX,DWORD PTR [ESP+48]
          mov EDI,DWORD PTR [ESP+44]
          mov EBP,DWORD PTR [ESP+52]
          sub EAX,ESI
          mov DWORD PTR [ESP+12],EAX
          js L_421090
          movzx EAX,BYTE PTR [EBP]
          mov EBX,EDI
          xor EDX,EDX
          mov BYTE PTR [ESP+11],AL
          lea EAX,DWORD PTR [ESI+1]
          mov DWORD PTR [ESP+20],EAX
          jmp L_421040
L_421034:
          add EDX,1
          add EBX,1
          cmp EDX,DWORD PTR [ESP+12]
          jg L_421090
L_421040:
          movzx EAX,BYTE PTR [ESP+11]
          mov DWORD PTR [ESP+4],EBX
          cmp BYTE PTR [EBX],AL
          jne L_421034
          xor EAX,EAX
          test ESI,ESI
          jle L_42107a
          mov DWORD PTR [ESP+16],EBX
          mov EBX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP],EBX
          jmp L_42106f
L_421060:
          lea ECX,DWORD PTR [EDI+EAX*1]
          movzx EBX,BYTE PTR [EBP+EAX*1]
          cmp BYTE PTR [ECX+EDX*1],BL
          cmovne EAX,DWORD PTR [ESP]
L_42106f:
          add EAX,1
          cmp ESI,EAX
          jg L_421060
          mov EBX,DWORD PTR [ESP+16]
L_42107a:
          cmp ESI,EAX
          jne L_421034
          mov EAX,DWORD PTR [ESP+4]
          add ESP,24
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
L_421090:
          mov DWORD PTR [ESP+4],0
          mov EAX,DWORD PTR [ESP+4]
          add ESP,24
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
          .byte 0xbf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_4210b0:
          push EBP
          push EDI
          xor ECX,ECX
          push ESI
          push EBX
          sub ESP,24
          mov EBP,DWORD PTR [ESP+56]
          cmp ECX,DWORD PTR [ESP+48]
          mov EDI,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+20],0
          lea EAX,DWORD PTR [EBP+1]
          mov DWORD PTR [ESP+16],EAX
          jge L_421163
L_4210da:
          mov EAX,DWORD PTR [ESP+48]
          sub EAX,ECX
          cmp EBP,EAX
          jg L_421163
          sub EAX,EBP
          mov ESI,DWORD PTR [ESP+44]
          xor EDX,EDX
          mov DWORD PTR [ESP+8],EAX
          movzx EAX,BYTE PTR [EDI]
          add ESI,ECX
          mov EBX,ESI
          mov BYTE PTR [ESP+7],AL
          jmp L_42110c
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_421100:
          add EDX,1
          add EBX,1
          cmp EDX,DWORD PTR [ESP+8]
          jg L_421163
L_42110c:
          movzx EAX,BYTE PTR [ESP+7]
          cmp BYTE PTR [EBX],AL
          jne L_421100
          xor EAX,EAX
          test EBP,EBP
          jle L_421149
          mov DWORD PTR [ESP+12],EBX
          mov EBX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP],EBX
          jmp L_42113e
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_421130:
          lea ECX,DWORD PTR [ESI+EAX*1]
          movzx EBX,BYTE PTR [EDI+EAX*1]
          cmp BYTE PTR [ECX+EDX*1],BL
          cmovne EAX,DWORD PTR [ESP]
L_42113e:
          add EAX,1
          cmp EBP,EAX
          jg L_421130
          mov EBX,DWORD PTR [ESP+12]
L_421149:
          cmp EBP,EAX
          jne L_421100
          sub EBX,DWORD PTR [ESP+44]
          add DWORD PTR [ESP+20],1
          lea ECX,DWORD PTR [EBX+EBP*1]
          cmp ECX,DWORD PTR [ESP+48]
          jl L_4210da
L_421163:
          mov EAX,DWORD PTR [ESP+20]
          add ESP,24
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
FUN_421170:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,8
          mov ESI,DWORD PTR [ESP+40]
          mov EAX,DWORD PTR [ESP+32]
          mov EBX,DWORD PTR [ESP+28]
          mov EDI,DWORD PTR [ESP+36]
          sub EAX,ESI
          mov DWORD PTR [ESP+4],EAX
          js L_4211f0
          movzx EAX,BYTE PTR [EDI]
          xor EDX,EDX
          lea EBP,DWORD PTR [ESI+1]
          mov BYTE PTR [ESP+3],AL
          jmp L_4211a9
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4211a0:
          add EDX,1
          cmp EDX,DWORD PTR [ESP+4]
          jg L_4211f0
L_4211a9:
          movzx EAX,BYTE PTR [ESP+3]
          cmp BYTE PTR [EBX+EDX*1],AL
          jne L_4211a0
          xor EAX,EAX
          test ESI,ESI
          jle L_4211db
          mov DWORD PTR [ESP+28],EBX
          jmp L_4211d0
          .byte 0x90
L_4211c0:
          mov ECX,DWORD PTR [ESP+28]
          movzx EBX,BYTE PTR [EDI+EAX*1]
          add ECX,EAX
          cmp BYTE PTR [ECX+EDX*1],BL
          cmovne EAX,EBP
L_4211d0:
          add EAX,1
          cmp ESI,EAX
          jg L_4211c0
          mov EBX,DWORD PTR [ESP+28]
L_4211db:
          cmp ESI,EAX
          jne L_4211a0
          add ESP,8
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4211f0:
          add ESP,8
          xor EAX,EAX
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
FUN_421200:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EBX,DWORD PTR [ESP+76]
          mov EAX,DWORD PTR [ESP+68]
          mov EDI,DWORD PTR [ESP+64]
          mov EBP,DWORD PTR [ESP+72]
          sub EAX,EBX
          mov DWORD PTR [ESP+20],EAX
          js L_4212c0
          movzx EAX,BYTE PTR [EBP]
          mov ESI,EDI
          xor EDX,EDX
          mov BYTE PTR [ESP+19],AL
          lea EAX,DWORD PTR [EBX+1]
          mov DWORD PTR [ESP+28],EAX
          jmp L_42124c
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_421240:
          add EDX,1
          add ESI,1
          cmp EDX,DWORD PTR [ESP+20]
          jg L_4212c0
L_42124c:
          movzx EAX,BYTE PTR [ESP+19]
          cmp BYTE PTR [ESI],AL
          jne L_421240
          xor EAX,EAX
          test EBX,EBX
          jle L_42128f
          mov DWORD PTR [ESP+24],ESI
          mov DWORD PTR [ESP+76],EBX
          mov ESI,DWORD PTR [ESP+28]
          jmp L_42127e
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_421270:
          lea ECX,DWORD PTR [EDI+EAX*1]
          movzx EBX,BYTE PTR [EBP+EAX*1]
          cmp BYTE PTR [ECX+EDX*1],BL
          cmovne EAX,ESI
L_42127e:
          add EAX,1
          cmp DWORD PTR [ESP+76],EAX
          jg L_421270
          mov ESI,DWORD PTR [ESP+24]
          mov EBX,DWORD PTR [ESP+76]
L_42128f:
          cmp EBX,EAX
          jne L_421240
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          add ESP,44
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
L_4212c0:
          add ESP,44
          xor EAX,EAX
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
L_4212d0:
          mov EDX,DWORD PTR [ESP+4]
          lea EAX,DWORD PTR [EDX-97]
          cmp AL,5
          jbe L_4212f4
          lea EAX,DWORD PTR [EDX-48]
          cmp AL,9
          jbe L_4212f2
          lea EAX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp AL,5
          mov EAX,4294967295
          cmovbe EAX,EDX
L_4212f2:
          repz ret 
L_4212f4:
          lea EAX,DWORD PTR [EDX-87]
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_421300:
          push EBX
          mov EBX,DWORD PTR [ESP+8]
          movzx EDX,BYTE PTR [EBX]
          lea EAX,DWORD PTR [EDX-97]
          cmp AL,5
          ja L_421340
          sub EDX,87
          shl EDX,4
L_421315:
          movzx ECX,BYTE PTR [EBX+1]
          lea EAX,DWORD PTR [ECX-97]
          cmp AL,5
          jbe L_421357
L_421320:
          lea EBX,DWORD PTR [ECX-48]
          cmp BL,9
          jbe L_421375
          lea EAX,DWORD PTR [ECX-65]
          mov EBX,15
          sub ECX,55
          cmp AL,5
          cmova ECX,EBX
          lea EAX,DWORD PTR [EDX+ECX*1]
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_421340:
          lea EAX,DWORD PTR [EDX-48]
          cmp AL,9
          ja L_421360
          movzx ECX,BYTE PTR [EBX+1]
          shl EAX,4
          mov EDX,EAX
          lea EAX,DWORD PTR [ECX-97]
          cmp AL,5
          ja L_421320
L_421357:
          sub ECX,87
          lea EAX,DWORD PTR [EDX+ECX*1]
          pop EBX
          ret 
          .byte 0x90
L_421360:
          lea EAX,DWORD PTR [EDX-65]
          sub EDX,55
          shl EDX,4
          cmp AL,5
          mov EAX,4294967280
          cmova EDX,EAX
          jmp L_421315
L_421375:
          mov ECX,EBX
          lea EAX,DWORD PTR [EDX+ECX*1]
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_421380:
          push EBX
          mov ECX,DWORD PTR [ESP+8]
          xor EAX,EAX
          movzx EDX,BYTE PTR [ECX]
          test DL,DL
          je L_4216ed
          lea EAX,DWORD PTR [EDX-97]
          cmp AL,5
          ja L_4216f0
          lea EAX,DWORD PTR [EDX-87]
L_4213a0:
          movzx EDX,BYTE PTR [ECX+1]
          movzx EAX,AL
          test DL,DL
          je L_4216ed
          lea EBX,DWORD PTR [EDX-97]
          cmp BL,5
          ja L_421710
          sub EDX,87
L_4213be:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [ECX+2]
          test DL,DL
          je L_4216ed
          lea EBX,DWORD PTR [EDX-97]
          cmp BL,5
          jbe L_421740
          lea EBX,DWORD PTR [EDX-48]
          cmp BL,9
          jbe L_421750
          lea EBX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp BL,5
          ja L_421727
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_421400:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [ECX+3]
          test DL,DL
          je L_4216ed
          lea EBX,DWORD PTR [EDX-97]
          cmp BL,5
          jbe L_421760
          lea EBX,DWORD PTR [EDX-48]
          cmp BL,9
          jbe L_421770
          lea EBX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp BL,5
          ja L_421727
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_421440:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [ECX+4]
          test DL,DL
          je L_4216ed
          lea EBX,DWORD PTR [EDX-97]
          cmp BL,5
          jbe L_421768
          lea EBX,DWORD PTR [EDX-48]
          cmp BL,9
          jbe L_42177f
          lea EBX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp BL,5
          ja L_421727
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_421480:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [ECX+5]
          test DL,DL
          je L_4216ed
          lea EBX,DWORD PTR [EDX-97]
          cmp BL,5
          jbe L_421777
          lea EBX,DWORD PTR [EDX-48]
          cmp BL,9
          jbe L_421786
          lea EBX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp BL,5
          ja L_421727
L_4214bb:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [ECX+6]
          test DL,DL
          je L_4216ed
          lea EBX,DWORD PTR [EDX-97]
          cmp BL,5
          jbe L_42178d
          lea EBX,DWORD PTR [EDX-48]
          cmp BL,9
          jbe L_421795
          lea EBX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp BL,5
          ja L_421727
L_4214f6:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [ECX+7]
          test DL,DL
          je L_4216ed
          lea EBX,DWORD PTR [EDX-97]
          cmp BL,5
          jbe L_42179c
          lea EBX,DWORD PTR [EDX-48]
          cmp BL,9
          jbe L_4217d6
          lea EBX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp BL,5
          ja L_421727
L_421531:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [ECX+8]
          test DL,DL
          je L_4216ed
          lea EBX,DWORD PTR [EDX-97]
          cmp BL,5
          jbe L_4217ce
          lea EBX,DWORD PTR [EDX-48]
          cmp BL,9
          jbe L_4217f4
          lea EBX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp BL,5
          ja L_421727
L_42156c:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [ECX+9]
          test DL,DL
          je L_4216ed
          lea EBX,DWORD PTR [EDX-97]
          cmp BL,5
          jbe L_4217ec
          lea EBX,DWORD PTR [EDX-48]
          cmp BL,9
          jbe L_4217e5
          lea EBX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp BL,5
          ja L_421727
L_4215a7:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [ECX+10]
          test DL,DL
          je L_4216ed
          lea EBX,DWORD PTR [EDX-97]
          cmp BL,5
          jbe L_4217dd
          lea EBX,DWORD PTR [EDX-48]
          cmp BL,9
          jbe L_421830
          lea EBX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp BL,5
          ja L_421727
L_4215e2:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [ECX+11]
          test DL,DL
          je L_4216ed
          lea EBX,DWORD PTR [EDX-97]
          cmp BL,5
          jbe L_421828
          lea EBX,DWORD PTR [EDX-48]
          cmp BL,9
          jbe L_421821
          lea EBX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp BL,5
          ja L_421727
L_42161d:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [ECX+12]
          test DL,DL
          je L_4216ed
          lea EBX,DWORD PTR [EDX-97]
          cmp BL,5
          jbe L_421819
          lea EBX,DWORD PTR [EDX-48]
          cmp BL,9
          jbe L_421812
          lea EBX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp BL,5
          ja L_421727
L_421658:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [ECX+13]
          test DL,DL
          je L_4216ed
          lea EBX,DWORD PTR [EDX-97]
          cmp BL,5
          jbe L_42180a
          lea EBX,DWORD PTR [EDX-48]
          cmp BL,9
          jbe L_421803
          lea EBX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp BL,5
          ja L_421727
L_421693:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [ECX+14]
          test DL,DL
          je L_4216ed
          lea EBX,DWORD PTR [EDX-97]
          cmp BL,5
          jbe L_4217fb
          lea EBX,DWORD PTR [EDX-48]
          cmp BL,9
          jbe L_4217c0
          lea EBX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp BL,5
          ja L_421727
L_4216c6:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [ECX+15]
          test DL,DL
          je L_4216ed
          lea ECX,DWORD PTR [EDX-97]
          cmp CL,5
          ja L_4217a4
          sub EDX,87
L_4216e5:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
L_4216ed:
          pop EBX
          ret 
          .byte 0x90
L_4216f0:
          lea EAX,DWORD PTR [EDX-48]
          cmp AL,9
          jbe L_4213a0
          lea EBX,DWORD PTR [EDX-65]
          mov EAX,DWORD PTR [ESP+12]
          cmp BL,5
          ja L_4216ed
          lea EAX,DWORD PTR [EDX-55]
          jmp L_4213a0
          .byte 0x90
L_421710:
          lea EBX,DWORD PTR [EDX-48]
          cmp BL,9
          jbe L_421730
          lea EBX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp BL,5
          jbe L_4213be
L_421727:
          mov EAX,DWORD PTR [ESP+12]
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_421730:
          mov EDX,EBX
          jmp L_4213be
L_421737:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_421740:
          sub EDX,87
          jmp L_421400
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_421750:
          mov EDX,EBX
          jmp L_421400
L_421757:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_421760:
          sub EDX,87
          jmp L_421440
L_421768:
          sub EDX,87
          jmp L_421480
L_421770:
          mov EDX,EBX
          jmp L_421440
L_421777:
          sub EDX,87
          jmp L_4214bb
L_42177f:
          mov EDX,EBX
          jmp L_421480
L_421786:
          mov EDX,EBX
          jmp L_4214bb
L_42178d:
          sub EDX,87
          jmp L_4214f6
L_421795:
          mov EDX,EBX
          jmp L_4214f6
L_42179c:
          sub EDX,87
          jmp L_421531
L_4217a4:
          lea ECX,DWORD PTR [EDX-48]
          cmp CL,9
          jbe L_4217c7
          lea ECX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp CL,5
          jbe L_4216e5
          jmp L_421727
L_4217c0:
          mov EDX,EBX
          jmp L_4216c6
L_4217c7:
          mov EDX,ECX
          jmp L_4216e5
L_4217ce:
          sub EDX,87
          jmp L_42156c
L_4217d6:
          mov EDX,EBX
          jmp L_421531
L_4217dd:
          sub EDX,87
          jmp L_4215e2
L_4217e5:
          mov EDX,EBX
          jmp L_4215a7
L_4217ec:
          sub EDX,87
          jmp L_4215a7
L_4217f4:
          mov EDX,EBX
          jmp L_42156c
L_4217fb:
          sub EDX,87
          jmp L_4216c6
L_421803:
          mov EDX,EBX
          jmp L_421693
L_42180a:
          sub EDX,87
          jmp L_421693
L_421812:
          mov EDX,EBX
          jmp L_421658
L_421819:
          sub EDX,87
          jmp L_421658
L_421821:
          mov EDX,EBX
          jmp L_42161d
L_421828:
          sub EDX,87
          jmp L_42161d
L_421830:
          mov EDX,EBX
          jmp L_4215e2
L_421837:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_421840:
          mov EAX,DWORD PTR [ESP+4]
          lea ECX,DWORD PTR [EAX-65]
          lea EDX,DWORD PTR [EAX+32]
          cmp CL,24
          cmovbe EAX,EDX
          ret 
L_421851:
          jmp FUN_421860
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
FUN_421860:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov ESI,DWORD PTR [ESP+48]
          mov EBP,DWORD PTR [ESP+52]
          movzx EDI,BYTE PTR [ESI]
          mov EAX,EDI
          cmp AL,48
          je L_4218d0
L_421878:
          mov DWORD PTR [ESP],ESI
          mov EBX,EDI
          call _strlen
          test BL,BL
          je L_4218b1
          test EAX,EAX
          je L_4218b1
          test EAX,EAX
          jle L_4218c0
          mov EDX,ESI
          add EAX,ESI
          jmp L_42189b
L_421894:
          add EDX,1
          cmp EAX,EDX
          je L_4218c0
L_42189b:
          movzx ECX,BYTE PTR [EDX]
          lea EBX,DWORD PTR [ECX-48]
          cmp BL,9
          jbe L_421894
          and ECX,4294967263
          sub ECX,65
          cmp CL,5
          jbe L_421894
L_4218b1:
          add ESP,28
          mov EAX,EBP
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
L_4218c0:
          mov DWORD PTR [ESP+48],ESI
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _atoi
L_4218d0:
          movzx EAX,BYTE PTR [ESI+1]
          lea ECX,DWORD PTR [EAX-65]
          lea EDX,DWORD PTR [EAX+32]
          cmp CL,24
          cmovbe EAX,EDX
          cmp AL,120
          jne L_421878
          mov EAX,ESI
          add EAX,2
          je L_4218b1
          mov DWORD PTR [ESP],EAX
          call _strlen
          cmp BYTE PTR [ESI+2],0
          je L_4218b1
          test EAX,EAX
          je L_4218b1
          test EAX,EAX
          jle L_42192f
          mov EDX,ESI
          lea ECX,DWORD PTR [ESI+EAX*1]
          jmp L_421917
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_421910:
          add EDX,1
          cmp EDX,ECX
          je L_42192f
L_421917:
          movzx EAX,BYTE PTR [EDX+2]
          lea EBX,DWORD PTR [EAX-48]
          cmp BL,9
          jbe L_421910
          and EAX,4294967263
          sub EAX,65
          cmp AL,5
          jbe L_421910
          jmp L_4218b1
L_42192f:
          movzx EAX,BYTE PTR [ESI+2]
          test AL,AL
          je L_421cc0
          lea EDX,DWORD PTR [EAX-97]
          cmp DL,5
          jbe L_421cce
          lea EDX,DWORD PTR [EAX-48]
          cmp DL,9
          jbe L_421cd6
          lea EDX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp DL,5
          ja L_4218b1
L_421962:
          movzx EDX,BYTE PTR [ESI+3]
          movzx EAX,AL
          test DL,DL
          je L_421cc7
          lea ECX,DWORD PTR [EDX-97]
          cmp CL,5
          jbe L_421cdd
          lea ECX,DWORD PTR [EDX-48]
          cmp CL,9
          jbe L_421cf4
          lea ECX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp CL,5
          ja L_4218b1
L_421998:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [ESI+4]
          test DL,DL
          je L_421cc7
          lea ECX,DWORD PTR [EDX-97]
          cmp CL,5
          jbe L_421cec
          lea ECX,DWORD PTR [EDX-48]
          cmp CL,9
          jbe L_421cfb
          lea ECX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp CL,5
          ja L_4218b1
L_4219d3:
          shl EAX,4
          movzx EDX,DL
          add EDX,EAX
          movzx EAX,BYTE PTR [ESI+5]
          test AL,AL
          je L_421ce5
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_421d02
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_421d0a
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4218b1
L_421a0e:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [ESI+6]
          test AL,AL
          je L_421ce5
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_421d18
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_421d11
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4218b1
L_421a49:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [ESI+7]
          test AL,AL
          je L_421ce5
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_421d4a
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_421d43
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4218b1
L_421a84:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [ESI+8]
          test AL,AL
          je L_421ce5
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_421d52
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_421d3c
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4218b1
L_421abf:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [ESI+9]
          test AL,AL
          je L_421ce5
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_421dd1
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_421dca
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4218b1
L_421afa:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [ESI+10]
          test AL,AL
          je L_421ce5
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_421dc2
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_421dbb
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4218b1
L_421b35:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [ESI+11]
          test AL,AL
          je L_421ce5
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_421db3
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_421dac
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4218b1
L_421b70:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [ESI+12]
          test AL,AL
          je L_421ce5
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_421da4
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_421d9d
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4218b1
L_421bab:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [ESI+13]
          test AL,AL
          je L_421ce5
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_421d95
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_421d8e
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4218b1
L_421be6:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [ESI+14]
          test AL,AL
          je L_421ce5
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_421d86
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_421d7f
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4218b1
L_421c21:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [ESI+15]
          test AL,AL
          je L_421ce5
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_421d77
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_421d70
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4218b1
L_421c5c:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [ESI+16]
          test AL,AL
          je L_421ce5
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_421d68
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_421d61
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4218b1
L_421c93:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [ESI+17]
          test AL,AL
          je L_421ce5
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          ja L_421d20
          sub EAX,87
L_421cae:
          shl EDX,4
          movzx EAX,AL
          lea EBP,DWORD PTR [EAX+EDX*1]
          jmp L_4218b1
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_421cc0:
          xor EBP,EBP
          jmp L_4218b1
L_421cc7:
          mov EBP,EAX
          jmp L_4218b1
L_421cce:
          sub EAX,87
          jmp L_421962
L_421cd6:
          mov EAX,EDX
          jmp L_421962
L_421cdd:
          sub EDX,87
          jmp L_421998
L_421ce5:
          mov EBP,EDX
          jmp L_4218b1
L_421cec:
          sub EDX,87
          jmp L_4219d3
L_421cf4:
          mov EDX,ECX
          jmp L_421998
L_421cfb:
          mov EDX,ECX
          jmp L_4219d3
L_421d02:
          sub EAX,87
          jmp L_421a0e
L_421d0a:
          mov EAX,ECX
          jmp L_421a0e
L_421d11:
          mov EAX,ECX
          jmp L_421a49
L_421d18:
          sub EAX,87
          jmp L_421a49
L_421d20:
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_421d5a
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          jbe L_421cae
          jmp L_4218b1
L_421d3c:
          mov EAX,ECX
          jmp L_421abf
L_421d43:
          mov EAX,ECX
          jmp L_421a84
L_421d4a:
          sub EAX,87
          jmp L_421a84
L_421d52:
          sub EAX,87
          jmp L_421abf
L_421d5a:
          mov EAX,ECX
          jmp L_421cae
L_421d61:
          mov EAX,ECX
          jmp L_421c93
L_421d68:
          sub EAX,87
          jmp L_421c93
L_421d70:
          mov EAX,ECX
          jmp L_421c5c
L_421d77:
          sub EAX,87
          jmp L_421c5c
L_421d7f:
          mov EAX,ECX
          jmp L_421c21
L_421d86:
          sub EAX,87
          jmp L_421c21
L_421d8e:
          mov EAX,ECX
          jmp L_421be6
L_421d95:
          sub EAX,87
          jmp L_421be6
L_421d9d:
          mov EAX,ECX
          jmp L_421bab
L_421da4:
          sub EAX,87
          jmp L_421bab
L_421dac:
          mov EAX,ECX
          jmp L_421b70
L_421db3:
          sub EAX,87
          jmp L_421b70
L_421dbb:
          mov EAX,ECX
          jmp L_421b35
L_421dc2:
          sub EAX,87
          jmp L_421b35
L_421dca:
          mov EAX,ECX
          jmp L_421afa
L_421dd1:
          sub EAX,87
          jmp L_421afa
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_421de0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EBP,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EBP
          call _strlen
          cmp EAX,2
          movzx EDX,BYTE PTR [EBP]
          jbe L_421e05
          cmp DL,48
          je L_4221e0
L_421e05:
          test DL,DL
          je L_4221cc
          test EAX,EAX
          je L_4221cc
          test EAX,EAX
          jle L_421e43
          mov EDX,EBP
          add EAX,EBP
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_421e20:
          movzx ECX,BYTE PTR [EDX]
          lea ESI,DWORD PTR [ECX-48]
          mov EBX,ESI
          cmp BL,9
          jbe L_421e3c
          and ECX,4294967263
          sub ECX,65
          cmp CL,5
          ja L_4221cc
L_421e3c:
          add EDX,1
          cmp EDX,EAX
          jne L_421e20
L_421e43:
          movzx EDX,BYTE PTR [EBP]
          test DL,DL
          je L_422220
          lea EAX,DWORD PTR [EDX-97]
          cmp AL,5
          jbe L_422230
          lea EAX,DWORD PTR [EDX-48]
          cmp AL,9
          jbe L_421e70
          lea EAX,DWORD PTR [EDX-65]
          cmp AL,5
          ja L_4221cc
          lea EAX,DWORD PTR [EDX-55]
          nop
L_421e70:
          movzx EDX,BYTE PTR [EBP+1]
          movzx EAX,AL
          test DL,DL
          je L_422240
          lea ECX,DWORD PTR [EDX-97]
          cmp CL,5
          jbe L_422246
          lea ECX,DWORD PTR [EDX-48]
          cmp CL,9
          jbe L_42224e
          lea ECX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp CL,5
          ja L_4221cc
L_421ea6:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [EBP+2]
          test DL,DL
          je L_422240
          lea ECX,DWORD PTR [EDX-97]
          cmp CL,5
          jbe L_422255
          lea ECX,DWORD PTR [EDX-48]
          cmp CL,9
          jbe L_42225d
          lea ECX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp CL,5
          ja L_4221cc
L_421ee1:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [EBP+3]
          test DL,DL
          je L_422240
          lea ECX,DWORD PTR [EDX-97]
          cmp CL,5
          jbe L_422264
          lea ECX,DWORD PTR [EDX-48]
          cmp CL,9
          jbe L_42227d
          lea ECX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp CL,5
          ja L_4221cc
L_421f1c:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          movzx EDX,BYTE PTR [EBP+4]
          test DL,DL
          je L_422240
          lea ECX,DWORD PTR [EDX-97]
          cmp CL,5
          jbe L_422275
          lea ECX,DWORD PTR [EDX-48]
          cmp CL,9
          jbe L_422284
          lea ECX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp CL,5
          ja L_4221cc
L_421f57:
          shl EAX,4
          movzx EDX,DL
          add EDX,EAX
          movzx EAX,BYTE PTR [EBP+5]
          test AL,AL
          je L_42226c
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_42228b
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_422293
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4221cc
L_421f92:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [EBP+6]
          test AL,AL
          je L_42226c
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_422300
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_4222f9
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4221cc
L_421fcd:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [EBP+7]
          test AL,AL
          je L_42226c
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_4222f1
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_4222ea
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4221cc
L_422008:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [EBP+8]
          test AL,AL
          je L_42226c
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_42233c
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_422335
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4221cc
L_422043:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [EBP+9]
          test AL,AL
          je L_42226c
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_42232d
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_422326
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4221cc
L_42207e:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [EBP+10]
          test AL,AL
          je L_42226c
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_42231e
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_422317
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4221cc
L_4220b9:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [EBP+11]
          test AL,AL
          je L_42226c
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_42230f
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_422308
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4221cc
L_4220f4:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [EBP+12]
          test AL,AL
          je L_42226c
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_4222e2
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_4222db
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4221cc
L_42212f:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [EBP+13]
          test AL,AL
          je L_42226c
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_4222d3
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_4222cc
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4221cc
L_422166:
          shl EDX,4
          movzx EAX,AL
          add EDX,EAX
          movzx EAX,BYTE PTR [EBP+14]
          test AL,AL
          je L_42226c
          lea ECX,DWORD PTR [EAX-97]
          cmp CL,5
          jbe L_4222bd
          lea ECX,DWORD PTR [EAX-48]
          cmp CL,9
          jbe L_4222b6
          lea ECX,DWORD PTR [EAX-65]
          sub EAX,55
          cmp CL,5
          ja L_4221cc
L_42219d:
          shl EDX,4
          movzx EAX,AL
          add EAX,EDX
          movzx EDX,BYTE PTR [EBP+15]
          test DL,DL
          je L_422240
          lea ECX,DWORD PTR [EDX-97]
          cmp CL,5
          ja L_42229a
          sub EDX,87
L_4221c0:
          shl EAX,4
          movzx EDX,DL
          add EAX,EDX
          mov DWORD PTR [ESP+52],EAX
L_4221cc:
          mov EAX,DWORD PTR [ESP+52]
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
L_4221e0:
          movzx ECX,BYTE PTR [EBP+1]
          lea EDI,DWORD PTR [ECX-65]
          lea ESI,DWORD PTR [ECX+32]
          mov EBX,EDI
          cmp BL,24
          cmovbe ECX,ESI
          cmp CL,120
          jne L_421e05
          mov ESI,EBP
          add ESI,2
          je L_4221cc
          xor EAX,EAX
          or ECX,4294967295
          mov EDI,ESI
          repne scasb AL,BYTE PTR ES:[EDI]
          movzx EDX,BYTE PTR [EBP+2]
          mov EBP,ESI
          mov EAX,ECX
          not EAX
          sub EAX,1
          jmp L_421e05
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_422220:
          mov DWORD PTR [ESP+52],0
          jmp L_4221cc
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_422230:
          lea EAX,DWORD PTR [EDX-87]
          jmp L_421e70
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_422240:
          mov DWORD PTR [ESP+52],EAX
          jmp L_4221cc
L_422246:
          sub EDX,87
          jmp L_421ea6
L_42224e:
          mov EDX,ECX
          jmp L_421ea6
L_422255:
          sub EDX,87
          jmp L_421ee1
L_42225d:
          mov EDX,ECX
          jmp L_421ee1
L_422264:
          sub EDX,87
          jmp L_421f1c
L_42226c:
          mov DWORD PTR [ESP+52],EDX
          jmp L_4221cc
L_422275:
          sub EDX,87
          jmp L_421f57
L_42227d:
          mov EDX,ECX
          jmp L_421f1c
L_422284:
          mov EDX,ECX
          jmp L_421f57
L_42228b:
          sub EAX,87
          jmp L_421f92
L_422293:
          mov EAX,ECX
          jmp L_421f92
L_42229a:
          lea ECX,DWORD PTR [EDX-48]
          cmp CL,9
          jbe L_4222c5
          lea ECX,DWORD PTR [EDX-65]
          sub EDX,55
          cmp CL,5
          jbe L_4221c0
          jmp L_4221cc
L_4222b6:
          mov EAX,ECX
          jmp L_42219d
L_4222bd:
          sub EAX,87
          jmp L_42219d
L_4222c5:
          mov EDX,ECX
          jmp L_4221c0
L_4222cc:
          mov EAX,ECX
          jmp L_422166
L_4222d3:
          sub EAX,87
          jmp L_422166
L_4222db:
          mov EAX,ECX
          jmp L_42212f
L_4222e2:
          sub EAX,87
          jmp L_42212f
L_4222ea:
          mov EAX,ECX
          jmp L_422008
L_4222f1:
          sub EAX,87
          jmp L_422008
L_4222f9:
          mov EAX,ECX
          jmp L_421fcd
L_422300:
          sub EAX,87
          jmp L_421fcd
L_422308:
          mov EAX,ECX
          jmp L_4220f4
L_42230f:
          sub EAX,87
          jmp L_4220f4
L_422317:
          mov EAX,ECX
          jmp L_4220b9
L_42231e:
          sub EAX,87
          jmp L_4220b9
L_422326:
          mov EAX,ECX
          jmp L_42207e
L_42232d:
          sub EAX,87
          jmp L_42207e
L_422335:
          mov EAX,ECX
          jmp L_422043
L_42233c:
          sub EAX,87
          jmp L_422043
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_422350:
          push EBX
          sub ESP,24
          mov EBX,DWORD PTR [ESP+32]
          test EBX,EBX
          je L_42238b
          mov DWORD PTR [ESP],EBX
          call _strlen
          cmp BYTE PTR [EBX],0
          je L_42238b
          test EAX,EAX
          je L_42238b
          test EAX,EAX
          jle L_422399
          mov EDX,EBX
          add EAX,EBX
L_422375:
          movzx ECX,BYTE PTR [EDX]
          lea EBX,DWORD PTR [ECX-48]
          cmp BL,9
          jbe L_422392
          and ECX,4294967263
          sub ECX,65
          cmp CL,5
          jbe L_422392
L_42238b:
          add ESP,24
          xor EAX,EAX
          pop EBX
          ret 
L_422392:
          add EDX,1
          cmp EAX,EDX
          jne L_422375
L_422399:
          add ESP,24
          mov EAX,1
          pop EBX
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
FUN_4223b0:
          mov ECX,DWORD PTR [ESP+8]
          mov EDX,DWORD PTR [ESP+4]
          test ECX,ECX
          je L_4223dd
          cmp BYTE PTR [EDX],0
          jne L_4223e3
          lea EAX,DWORD PTR [EDX+1]
          add EDX,ECX
          jmp L_4223d9
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4223d0:
          add EAX,1
          cmp BYTE PTR [EAX-1],0
          jne L_4223e3
L_4223d9:
          cmp EAX,EDX
          jne L_4223d0
L_4223dd:
          mov EAX,1
          ret 
L_4223e3:
          xor EAX,EAX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_4223f0:
          push EBX
          mov ECX,DWORD PTR [ESP+16]
          mov EBX,DWORD PTR [ESP+12]
          mov EDX,DWORD PTR [ESP+8]
          test ECX,ECX
          lea EAX,DWORD PTR [EBX+ECX*1]
          jle L_422415
L_422404:
          movzx ECX,BYTE PTR [EAX-1]
          sub EAX,1
          add EDX,1
          mov BYTE PTR [EDX-1],CL
          cmp EAX,EBX
          jne L_422404
L_422415:
          pop EBX
          ret 
L_422417:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_422420:
          push ESI
          push EBX
          xor ESI,ESI
          sub ESP,20
          mov EBX,DWORD PTR [ESP+32]
          test EBX,EBX
          je L_422459
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EBX
          call FUN_449138
          mov DWORD PTR [ESP],EBX
          call FUN_449128
          mov DWORD PTR [ESP],EBX
          mov ESI,EAX
          call FUN_4490a8
L_422459:
          add ESP,20
          mov EAX,ESI
          pop EBX
          pop ESI
          ret 
L_422461:
          jmp L_422470
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
L_422470:
          push ESI
          push EBX
          xor ESI,ESI
          sub ESP,20
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_457af4
          mov DWORD PTR [ESP],EAX
          call _fopen
          test EAX,EAX
          je L_4224bb
          mov EBX,EAX
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EAX
          call FUN_449138
          mov DWORD PTR [ESP],EBX
          call FUN_449128
          mov DWORD PTR [ESP],EBX
          mov ESI,EAX
          call _fclose
L_4224bb:
          add ESP,20
          mov EAX,ESI
          pop EBX
          pop ESI
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
FUN_4224d0:
          push EBX
          sub ESP,40
          mov EBX,DWORD PTR [ESP+48]
          test EBX,EBX
          je L_422521
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+12],2
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP+8],0
          call FUN_448af0
          mov DWORD PTR [ESP],EBX
          call FUN_448ff0
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+24],EAX
          mov DWORD PTR [ESP+28],EDX
          call FUN_4490a8
          mov EAX,DWORD PTR [ESP+24]
          mov EDX,DWORD PTR [ESP+28]
          add ESP,40
          pop EBX
          ret 
L_422521:
          add ESP,40
          xor EAX,EAX
          xor EDX,EDX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_422530:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_457af4
          mov DWORD PTR [ESP],EAX
          call _fopen
          test EAX,EAX
          je L_422590
          mov EBX,EAX
          mov DWORD PTR [ESP+12],2
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP],EAX
          call FUN_448af0
          mov DWORD PTR [ESP],EBX
          call FUN_448ff0
          mov DWORD PTR [ESP],EBX
          mov ESI,EAX
          mov EDI,EDX
          call _fclose
          add ESP,16
          mov EAX,ESI
          mov EDX,EDI
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
L_422590:
          add ESP,16
          xor ESI,ESI
          xor EDI,EDI
          mov EAX,ESI
          mov EDX,EDI
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
FUN_4225a0:
          sub ESP,28
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_457af4
          mov DWORD PTR [ESP],EAX
          call _fopen
          xor EDX,EDX
          test EAX,EAX
          je L_4225ca
          mov DWORD PTR [ESP],EAX
          call _fclose
          mov EDX,1
L_4225ca:
          mov EAX,EDX
          add ESP,28
          ret 
FUN_4225d0:
          push EBX
          sub ESP,1048
          mov EAX,DWORD PTR [ESP+1056]
          lea EBX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_449080
          mov EDX,EBX
L_4225f0:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_4225f0
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,DWORD PTR [ESP+1060]
          sbb EDX,3
          sub EDX,EBX
          mov BYTE PTR [EBX+EDX*1],47
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [EBX+EDX*1+1]
          mov DWORD PTR [ESP],EAX
          call FUN_449080
          mov DWORD PTR [ESP+4],OFFSET L_457af4
          mov DWORD PTR [ESP],EBX
          call _fopen
          mov EDX,EAX
          xor EAX,EAX
          test EDX,EDX
          je L_422662
          mov DWORD PTR [ESP],EDX
          call _fclose
          mov EAX,1
L_422662:
          add ESP,1048
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_422670:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EAX,DWORD PTR [ESP+48]
          mov EDI,DWORD PTR [ESP+52]
          test EAX,EAX
          je L_422730
          mov DWORD PTR [ESP+4],OFFSET L_457af4
          mov DWORD PTR [ESP],EAX
          call _fopen
          test EAX,EAX
          mov EBX,EAX
          je L_422705
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EAX
          call FUN_449138
          mov DWORD PTR [ESP],EBX
          call FUN_449128
          mov DWORD PTR [ESP],EBX
          mov ESI,EAX
          call FUN_4490a8
          mov DWORD PTR [ESP],ESI
          call _malloc
          test EAX,EAX
          mov EBP,EAX
          je L_422710
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call FUN_449148
L_4226ed:
          mov DWORD PTR [ESP],EBX
          call _fclose
L_4226f5:
          test EDI,EDI
          je L_4226fb
          mov DWORD PTR [EDI],ESI
L_4226fb:
          add ESP,28
          mov EAX,EBP
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_422705:
          xor ESI,ESI
          xor EBP,EBP
          jmp L_4226f5
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_422710:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_457af8
          xor ESI,ESI
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_4226ed
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_422730:
          xor EBP,EBP
          jmp L_4226fb
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_422740:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov ESI,DWORD PTR [ESP+52]
          mov EBX,DWORD PTR [ESP+56]
          test ESI,ESI
          setne DL
          test EBX,EBX
          setne AL
          test DL,AL
          je L_4227d1
          mov EAX,DWORD PTR [ESP+48]
          test EAX,EAX
          je L_4227d1
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],OFFSET L_457af4
          mov DWORD PTR [ESP],EAX
          call _fopen
          test EAX,EAX
          mov EDI,EAX
          je L_4227d1
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EAX
          call FUN_449138
          mov DWORD PTR [ESP],EDI
          call FUN_449128
          mov DWORD PTR [ESP],EDI
          mov EBP,EAX
          call FUN_4490a8
          cmp EBX,EBP
          ja L_4227d1
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call FUN_449148
          mov DWORD PTR [ESP],EDI
          call _fclose
          mov EAX,EBX
          jmp L_4227d3
L_4227d1:
          xor EAX,EAX
L_4227d3:
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
L_4227e0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1052
          mov EAX,DWORD PTR [ESP+1076]
          mov ESI,DWORD PTR [ESP+1080]
          mov EDX,DWORD PTR [ESP+1072]
          test EAX,EAX
          setne BL
          test ESI,ESI
          setne CL
          test BL,CL
          je L_422838
          test EDX,EDX
          je L_422838
          lea EDI,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],OFFSET L_457b26
          mov DWORD PTR [ESP],EDI
          call _sprintf
          mov EBX,DWORD PTR [ESP+1084]
          test EBX,EBX
          jne L_422850
L_422838:
          xor EBX,EBX
L_42283a:
          add ESP,1052
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_422850:
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],OFFSET L_457af4
          call _fopen
          test EAX,EAX
          mov EDI,EAX
          je L_422838
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EAX
          call FUN_449138
          mov DWORD PTR [ESP],EDI
          call FUN_449128
          mov DWORD PTR [ESP],EDI
          mov EBP,EAX
          call FUN_4490a8
          cmp EBX,EBP
          ja L_422838
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call FUN_449148
          mov DWORD PTR [ESP],EDI
          call _fclose
          jmp L_42283a
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4228c0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1068
          mov EAX,DWORD PTR [ESP+1088]
          mov EDX,DWORD PTR [ESP+1092]
          mov EBX,DWORD PTR [ESP+1100]
          test EAX,EAX
          je L_4229a0
          test EDX,EDX
          je L_4229a0
          lea EBP,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_457b26
          xor EDI,EDI
          mov DWORD PTR [ESP],EBP
          call _sprintf
          mov DWORD PTR [ESP+4],OFFSET L_457af4
          mov DWORD PTR [ESP],EBP
          call _fopen
          test EAX,EAX
          mov ESI,EAX
          je L_42294d
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EAX
          call FUN_449138
          mov DWORD PTR [ESP],ESI
          call FUN_449128
          mov DWORD PTR [ESP],ESI
          mov EDI,EAX
          call _fclose
L_42294d:
          test EBX,EBX
          mov ESI,EDI
          jne L_422992
L_422953:
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],ESI
          call _calloc
          test EAX,EAX
          mov EBX,EAX
          je L_422a30
          test EDI,EDI
          jne L_4229b0
L_422971:
          mov EAX,DWORD PTR [ESP+1096]
          test EAX,EAX
          je L_422985
          mov EAX,DWORD PTR [ESP+1096]
          mov DWORD PTR [EAX],ESI
L_422985:
          add ESP,1068
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_422992:
          lea ESI,DWORD PTR [EDI+EBX*1-1]
          neg EBX
          and ESI,EBX
          jmp L_422953
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4229a0:
          add ESP,1068
          xor EBX,EBX
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_4229b0:
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+4],OFFSET L_457af4
          call _fopen
          test EAX,EAX
          mov EBP,EAX
          je L_4229fa
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EAX
          call FUN_449138
          mov DWORD PTR [ESP],EBP
          call FUN_449128
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+28],EAX
          call FUN_4490a8
          mov EAX,DWORD PTR [ESP+28]
          cmp EAX,EDI
          jae L_422a71
L_4229fa:
          mov EDX,DWORD PTR [ESP+1096]
          test EDX,EDX
          je L_422a12
          mov EAX,DWORD PTR [ESP+1096]
          mov DWORD PTR [EAX],0
L_422a12:
          mov DWORD PTR [ESP],EBX
          xor EBX,EBX
          call _free
          add ESP,1068
          mov EAX,EBX
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
L_422a30:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_457af8
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov ECX,DWORD PTR [ESP+1096]
          test ECX,ECX
          je L_422985
          mov EAX,DWORD PTR [ESP+1096]
          mov DWORD PTR [EAX],0
          add ESP,1068
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_422a71:
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          call FUN_449148
          mov DWORD PTR [ESP],EBP
          call _fclose
          jmp L_422971
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_422aa0:
          push EBX
          mov EBX,DWORD PTR [ESP+8]
          xor EDX,EDX
          lea EAX,DWORD PTR [EBX+16]
          add EBX,268
L_422ab0:
          movzx ECX,BYTE PTR [EAX]
          add EAX,1
          add EDX,ECX
          cmp EBX,EAX
          jne L_422ab0
          not EDX
          movzx EAX,DX
          mov EDX,EAX
          shl EAX,24
          shl EDX,8
          and EDX,16711680
          add EAX,EDX
          pop EBX
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
FUN_422ae0:
          push EBX
          mov EBX,DWORD PTR [ESP+12]
          test EBX,EBX
          je L_422aff
          mov EDX,DWORD PTR [ESP+8]
          xor EAX,EAX
          add EBX,EDX
L_422af1:
          movzx ECX,BYTE PTR [EDX]
          add EDX,1
          add EAX,ECX
          cmp EBX,EDX
          jne L_422af1
          pop EBX
          ret 
L_422aff:
          xor EAX,EAX
          pop EBX
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
FUN_422b10:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EBP,DWORD PTR [ESP+80]
          mov EBX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+4],OFFSET L_457b2c
          mov DWORD PTR [ESP],1
          movzx EDX,BP
          mov EAX,EBP
          mov ESI,EBP
          mov DWORD PTR [ESP+24],EDX
          movzx EDX,WORD PTR [ESP+84]
          shr EAX,16
          movzx EDI,AL
          shr ESI,24
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+20],EDI
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [ESP+44],EAX
          mov DWORD PTR [ESP+8],EDX
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_457b66
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_457b78
          mov DWORD PTR [ESP],1
          call FUN_433690
          test EBX,EBX
          je L_422e41
          cmp ESI,1
          mov BYTE PTR [EBX+7],255
          mov BYTE PTR [EBX+6],255
          mov BYTE PTR [EBX+5],255
          mov BYTE PTR [EBX+4],255
          mov BYTE PTR [EBX+3],255
          mov BYTE PTR [EBX+2],255
          mov BYTE PTR [EBX+1],255
          mov BYTE PTR [EBX],192
          je L_422e00
          jb L_422e20
          cmp ESI,2
          je L_422de0
          cmp ESI,3
          je L_422da0
L_422bd0:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_457bc8
          mov DWORD PTR [ESP],1
          call FUN_433690
L_422be8:
          cmp BYTE PTR [ESP+44],0
          jne L_422c50
          test BP,BP
          jne L_422c50
          mov DWORD PTR [ESP+4],OFFSET L_457c08
          mov DWORD PTR [ESP],1
          call FUN_433690
L_422c08:
          test EBX,EBX
          je L_422c42
          mov EAX,DWORD PTR [ESP+92]
          test EAX,EAX
          je L_422c42
          mov BYTE PTR [EBX+15],15
          mov BYTE PTR [EBX+14],15
          mov BYTE PTR [EBX+13],15
          mov BYTE PTR [EBX+12],15
          mov BYTE PTR [EBX+11],15
          mov BYTE PTR [EBX+10],15
          mov BYTE PTR [EBX+9],15
          mov BYTE PTR [EBX+8],15
          mov DWORD PTR [EBX+16],0
          mov DWORD PTR [EBX+20],0
L_422c42:
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
L_422c50:
          mov ECX,16
          mov EAX,15
          xor EDX,EDX
          sub ECX,EDI
          xor ESI,ESI
          mov DWORD PTR [ESP+4],OFFSET L_457c28
          shl ECX,2
          mov DWORD PTR [ESP],1
          shld EDX,EAX,CL
          shl EAX,CL
          test CL,32
          cmovne EDX,EAX
          cmovne EAX,ESI
          xor ESI,ESI
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+12],EDX
          xor EDI,EDI
          call FUN_433690
          test EBP,1
          jne L_422ec0
          test EBP,2
          jne L_422eff
L_422ca9:
          test EBP,4
          jne L_422f40
L_422cb5:
          test EBP,8
          jne L_422f81
L_422cc1:
          test EBP,16
          jne L_422fc2
L_422ccd:
          test EBP,32
          jne L_423001
L_422cd9:
          test EBP,64
          jne L_423040
L_422ce5:
          test EBP,128
          jne L_42307e
L_422cf1:
          test EBP,256
          jne L_4230bd
L_422cfd:
          test EBP,512
          jne L_4230ff
L_422d09:
          test EBP,1024
          jne L_423141
L_422d15:
          test EBP,2048
          jne L_423183
L_422d21:
          test EBP,4096
          jne L_4231c5
L_422d2d:
          test EBP,8192
          jne L_423204
L_422d39:
          test EBP,16384
          jne L_423243
L_422d45:
          test BP,BP
          js L_422e80
L_422d4e:
          test EBX,EBX
          je L_422c42
          mov EAX,ESI
          mov EDX,EDI
          mov BYTE PTR [EBX+23],AL
          mov EAX,ESI
          mov BYTE PTR [EBX+19],DL
          shrd EAX,EDI,8
          mov BYTE PTR [EBX+22],AL
          mov EAX,ESI
          shrd EAX,EDI,16
          mov BYTE PTR [EBX+21],AL
          mov EAX,ESI
          shrd EAX,EDI,24
          mov BYTE PTR [EBX+20],AL
          mov EAX,EDI
          shr EAX,8
          mov BYTE PTR [EBX+18],AL
          mov EAX,EDI
          shr EAX,16
          mov BYTE PTR [EBX+17],AL
          mov EAX,EDI
          shr EAX,24
          mov BYTE PTR [EBX+16],AL
          jmp L_422c08
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_422da0:
          mov DWORD PTR [ESP+4],OFFSET L_457b98
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov BYTE PTR [EBX+15],240
L_422db8:
          mov BYTE PTR [EBX+14],240
L_422dbc:
          mov BYTE PTR [EBX+13],15
          mov BYTE PTR [EBX+12],15
          mov BYTE PTR [EBX+11],15
          mov BYTE PTR [EBX+10],15
          mov BYTE PTR [EBX+9],15
          mov BYTE PTR [EBX+8],15
          jmp L_422be8
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_422de0:
          mov DWORD PTR [ESP+4],OFFSET L_457cc4
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov BYTE PTR [EBX+15],15
          jmp L_422db8
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_422e00:
          mov DWORD PTR [ESP+4],OFFSET L_457c9c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov BYTE PTR [EBX+15],240
          mov BYTE PTR [EBX+14],15
          jmp L_422dbc
          .byte 0x66
          .byte 0x90
L_422e20:
          mov DWORD PTR [ESP+4],OFFSET L_457c74
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov BYTE PTR [EBX+15],15
          mov BYTE PTR [EBX+14],15
          jmp L_422dbc
L_422e41:
          cmp ESI,1
          je L_4232c0
          jb L_4232a0
          cmp ESI,2
          je L_423280
          cmp ESI,3
          jne L_422bd0
          mov DWORD PTR [ESP+4],OFFSET L_457b98
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_422be8
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_422e80:
          mov DWORD PTR [ESP+16],16
          mov DWORD PTR [ESP+8],15
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EDX,ESI
          or EDX,15
          mov ESI,EDX
          jmp L_422d4e
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_422ec0:
          mov DWORD PTR [ESP+16],1
          mov DWORD PTR [ESP+8],0
          xor ESI,ESI
          mov DWORD PTR [ESP+12],4026531840
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov EDI,4026531840
          mov DWORD PTR [ESP],1
          call FUN_433690
          test EBP,2
          je L_422ca9
L_422eff:
          mov DWORD PTR [ESP+16],2
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+12],251658240
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,EDI
          or EAX,251658240
          test EBP,4
          mov EDI,EAX
          je L_422cb5
L_422f40:
          mov DWORD PTR [ESP+16],3
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+12],15728640
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,EDI
          or EAX,15728640
          test EBP,8
          mov EDI,EAX
          je L_422cc1
L_422f81:
          mov DWORD PTR [ESP+16],4
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+12],983040
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,EDI
          or EAX,983040
          test EBP,16
          mov EDI,EAX
          je L_422ccd
L_422fc2:
          mov DWORD PTR [ESP+16],5
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+12],61440
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,EDI
          or AH,240
          test EBP,32
          mov EDI,EAX
          je L_422cd9
L_423001:
          mov DWORD PTR [ESP+16],6
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+12],3840
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,EDI
          or AH,15
          test EBP,64
          mov EDI,EAX
          je L_422ce5
L_423040:
          mov DWORD PTR [ESP+16],7
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+12],240
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,EDI
          or AL,240
          test EBP,128
          mov EDI,EAX
          je L_422cf1
L_42307e:
          mov DWORD PTR [ESP+16],8
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+12],15
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,EDI
          or EAX,15
          test EBP,256
          mov EDI,EAX
          je L_422cfd
L_4230bd:
          mov DWORD PTR [ESP+16],9
          mov DWORD PTR [ESP+8],4026531840
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EDX,ESI
          or EDX,4026531840
          test EBP,512
          mov ESI,EDX
          je L_422d09
L_4230ff:
          mov DWORD PTR [ESP+16],10
          mov DWORD PTR [ESP+8],251658240
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EDX,ESI
          or EDX,251658240
          test EBP,1024
          mov ESI,EDX
          je L_422d15
L_423141:
          mov DWORD PTR [ESP+16],11
          mov DWORD PTR [ESP+8],15728640
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EDX,ESI
          or EDX,15728640
          test EBP,2048
          mov ESI,EDX
          je L_422d21
L_423183:
          mov DWORD PTR [ESP+16],12
          mov DWORD PTR [ESP+8],983040
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EDX,ESI
          or EDX,983040
          test EBP,4096
          mov ESI,EDX
          je L_422d2d
L_4231c5:
          mov DWORD PTR [ESP+16],13
          mov DWORD PTR [ESP+8],61440
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EDX,ESI
          or DH,240
          test EBP,8192
          mov ESI,EDX
          je L_422d39
L_423204:
          mov DWORD PTR [ESP+16],14
          mov DWORD PTR [ESP+8],3840
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EDX,ESI
          or DH,15
          test EBP,16384
          mov ESI,EDX
          je L_422d45
L_423243:
          mov DWORD PTR [ESP+16],15
          mov DWORD PTR [ESP+8],240
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],OFFSET L_457c4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EDX,ESI
          or DL,240
          mov ESI,EDX
          jmp L_422d45
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_423280:
          mov DWORD PTR [ESP+4],OFFSET L_457cc4
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_422be8
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4232a0:
          mov DWORD PTR [ESP+4],OFFSET L_457c74
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_422be8
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4232c0:
          mov DWORD PTR [ESP+4],OFFSET L_457c9c
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_422be8
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_4232e0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EAX,DWORD PTR [ESP+52]
          mov ESI,DWORD PTR [ESP+48]
          mov EDI,DWORD PTR [ESP+56]
          test EAX,EAX
          je L_423303
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],ESI
          call FUN_433690
L_423303:
          xor EBP,EBP
          xor EBX,EBX
          jmp L_423330
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_423310:
          movzx EAX,BYTE PTR [EDI+EBX*1]
          mov DWORD PTR [ESP+4],OFFSET L_457adf
          add EBX,1
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          cmp EBX,96
          je L_423350
L_423330:
          test BL,7
          jne L_423310
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_457ced
          add EBP,1
          mov DWORD PTR [ESP],ESI
          call FUN_433690
          jmp L_423310
          .byte 0x66
          .byte 0x90
L_423350:
          mov DWORD PTR [ESP+48],ESI
          mov DWORD PTR [ESP+52],OFFSET L_457a80
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp FUN_433690
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_423370:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EBX,DWORD PTR [ESP+36]
          mov EDI,DWORD PTR [ESP+32]
          test EBX,EBX
          je L_4233a3
          lea ESI,DWORD PTR [EBX+16]
L_423385:
          movzx EAX,BYTE PTR [EBX]
          mov DWORD PTR [ESP+4],OFFSET L_457adf
          add EBX,1
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          cmp EBX,ESI
          jne L_423385
L_4233a3:
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_4233b0:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EDI,DWORD PTR [ESP+36]
          mov ESI,DWORD PTR [ESP+32]
          movzx EAX,BYTE PTR [EDI]
          lea EBX,DWORD PTR [EDI+1]
          mov DWORD PTR [ESP+4],OFFSET L_457cfe
          mov DWORD PTR [ESP],ESI
          add EDI,6
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_4233e0:
          mov DWORD PTR [ESP+4],OFFSET L_457d03
          mov DWORD PTR [ESP],ESI
          add EBX,1
          call FUN_433690
          movzx EAX,BYTE PTR [EBX-1]
          mov DWORD PTR [ESP+4],OFFSET L_457cfe
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          cmp EDI,EBX
          jne L_4233e0
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_423420:
          push EBP
          push EDI
          push ESI
          push EBX
          xor EBX,EBX
          sub ESP,28
          mov EBP,DWORD PTR [ESP+52]
          mov ESI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EBP
          call _strlen
          test EAX,EAX
          mov EDI,EAX
          jle L_423480
          nop
L_423440:
          movsx EAX,BYTE PTR [EBP+EBX*1]
          mov DWORD PTR [ESP+4],OFFSET L_457d05
          add EBX,1
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          cmp EDI,EBX
          je L_423480
          test BL,1
          jne L_423440
          mov DWORD PTR [ESP+4],OFFSET L_457d03
          mov DWORD PTR [ESP],ESI
          call FUN_433690
          jmp L_423440
L_423477:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_423480:
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
FUN_423490:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1132
          mov EBX,DWORD PTR [ESP+1152]
          cmp BYTE PTR [EBX],0
          je L_423600
L_4234aa:
          mov DWORD PTR [ESP+4],OFFSET L_457aaf
          mov DWORD PTR [ESP],EBX
          call _fopen
          test EAX,EAX
          mov DWORD PTR [ESP+44],EAX
          je L_423631
          mov EBP,DWORD PTR [ESP+1160]
          lea EBX,DWORD PTR [ESP+48]
          lea ESI,DWORD PTR [ESP+96]
          mov BYTE PTR [ESP+96],0
          lea EDI,DWORD PTR [EBP+20]
L_4234dd:
          movzx EAX,BYTE PTR [EBP+4]
          add EBP,5
          mov DWORD PTR [ESP+24],EAX
          movzx EAX,BYTE PTR [EBP-2]
          mov DWORD PTR [ESP+20],EAX
          movzx EAX,BYTE PTR [EBP-3]
          mov DWORD PTR [ESP+16],EAX
          movzx EAX,BYTE PTR [EBP-4]
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [EBP-5]
          mov DWORD PTR [ESP+4],OFFSET L_457d08
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call _sprintf
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call FUN_449088
          cmp EDI,EBP
          jne L_4234dd
          mov EDX,ESI
L_42352a:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_42352a
          mov ECX,EAX
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP],ESI
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,DWORD PTR [ESP+44]
          sbb EDX,3
          sub EDX,ESI
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP+12],EAX
          call FUN_449118
          mov EAX,DWORD PTR [ESP+1156]
          mov DWORD PTR [ESP+4],OFFSET L_457d1d
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call _sprintf
          mov EDX,ESI
L_423595:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_423595
          mov ECX,EAX
          mov EDI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+8],1
          shr ECX,16
          test EAX,32896
          mov DWORD PTR [ESP],ESI
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          mov DWORD PTR [ESP+12],EDI
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          sub EDX,ESI
          mov DWORD PTR [ESP+4],EDX
          call FUN_449118
          mov DWORD PTR [ESP],EDI
          call _fclose
L_4235eb:
          add ESP,1132
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_423600:
          mov EAX,DWORD PTR [ESP+1156]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_449080
          mov DWORD PTR [ESP],EBX
          call _strlen
          mov EDX,49
          add EAX,EBX
          mov DWORD PTR [EAX],1634235182
          mov WORD PTR [EAX+4],DX
          jmp L_4234aa
L_423631:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_457d24
          mov DWORD PTR [ESP],0
          call FUN_433690
          jmp L_4235eb
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_423650:
          push EBX
          sub ESP,24
          mov EBX,DWORD PTR [ESP+32]
          test EBX,EBX
          je L_423668
          mov DWORD PTR [ESP],EBX
          call FUN_4491f0
          test EAX,EAX
          jne L_423672
L_423668:
          add ESP,24
          mov EAX,1
          pop EBX
          ret 
L_423672:
          call DWORD PTR [_errno]
          mov EAX,DWORD PTR [EAX]
          cmp EAX,17
          je L_4236a2
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_457d84
          mov DWORD PTR [ESP],0
          call FUN_433690
          add ESP,24
          xor EAX,EAX
          pop EBX
          ret 
L_4236a2:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_457d60
          mov DWORD PTR [ESP],0
          call FUN_433690
          jmp L_423668
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4236c0:
          mov EAX,DWORD PTR [ESP+8]
          sub EAX,DWORD PTR [ESP+4]
          mov ECX,DWORD PTR [ESP+12]
          and EAX,67108860
          mov EDX,EAX
          or EAX,1207959553
          or EDX,1207959552
          test ECX,ECX
          cmove EAX,EDX
          ret 
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

.data
.p2align 5
L_44a6e0:
          .long L_457db1
          .long L_457db9
          .long L_457dbf
          .long L_457dc6
          .long L_457dcd
          .long L_457dd4
          .long L_457ddc
          .long L_457de3

.section .rdata,"dr"
.p2align 4
L_457a80:
          .string "\n"
L_457a82:
          .string "\n  "
L_457a86:
          .string " %02X"
L_457a8c:
          .string "dump buffer: n:'%s' b:0x%x s:0x%x\n"
L_457aaf:
          .string "wb"
L_457ab2:
          .string "fopen ERROR\n"
L_457abf:
          .string "dump buffer arg error\n"
L_457ad6:
          .string "dump OK\n"
L_457adf:
          .string "%02X"
L_457ae4:
          .string "\nfuseset %02d: "
L_457af4:
          .string "rb"
          .zero 1
L_457af8:
          .string "unable to allocate file buffer of 0x%x size!\n"
L_457b26:
          .string "%s%s"
          .zero 1
L_457b2c:
          .string "CB %d seq 0x%08x type: 0x%02x cseq: 0x%02x allow: 0x%04x\n"
L_457b66:
          .string "\texpected fuses:\n"
L_457b78:
          .string "\tfuseset 00: C0FFFFFFFFFFFFFF\n"
          .zero 1
L_457b98:
          .string "\tfuseset 01: 0F0F0F0F0F0FF0F0 (retail slim)\n"
          .zero 3
L_457bc8:
          .string "\tfuseset 01: ???????????????? never seen console type 0x%02x\n"
          .zero 2
L_457c08:
          .string "\tfuseset 02: 0000000000000000\n"
          .zero 1
L_457c28:
          .string "\tfuseset 02: %016llX (sequence)\n"
          .zero 3
L_457c4c:
          .string "\tfuseset 02: %016llX (allow cseq %d)\n"
          .zero 2
L_457c74:
          .string "\tfuseset 01: 0F0F0F0F0F0F0F0F (devkit)\n"
L_457c9c:
          .string "\tfuseset 01: 0F0F0F0F0F0F0FF0 (retail)\n"
L_457cc4:
          .string "\tfuseset 01: 0F0F0F0F0F0FF00F (testkit)\n"
L_457ced:
          .string "\n\tfuseset %02d: "
L_457cfe:
          .string "%02x"
L_457d03:
          .string ":"
L_457d05:
          .string "%c"
L_457d08:
          .string "%02x%02x%02x%02x%02x"
L_457d1d:
          .string " *%s\n"
          .zero 1
L_457d24:
          .string "\n\n***** ERROR: could not open %s to write SHA-1! Skipping!"
          .zero 1
L_457d60:
          .string "***** WARNING: reusing folder %s!\n"
          .zero 1
L_457d84:
          .string "\n\n***** ERROR: cannot create %s! (error %d)\n"
L_457db1:
          .string "Unknown"
L_457db9:
          .string "Xenon"
L_457dbf:
          .string "Zephyr"
L_457dc6:
          .string "Falcon"
L_457dcd:
          .string "Jasper"
L_457dd4:
          .string "Trinity"
L_457ddc:
          .string "Corona"
L_457de3:
          .string "Winchester"
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
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_420a90 - .
          .byte 0x18
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
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_420ab0 - .
          .byte 0x13
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
          .byte 0x0
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_420ad0 - .
          .byte 0x9
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
          .byte 0x0
          .byte 0x58
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_420ae0 - .
          .byte 0xe
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
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_420af0 - .
          .byte 0x7
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
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_420b00 - .
          .byte 0x14
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
          .byte 0x0
          .byte 0x94
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_420b20 - .
          .byte 0x23
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_420b50 - .
          .byte 0x51
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
          .byte 0x2
          .byte 0x4b
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
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_420bb0 - .
          .byte 0x78
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
          .byte 0x30
          .byte 0x2
          .byte 0x66
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
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_420c30 - .
          .byte 0xc6
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
          .byte 0x30
          .byte 0x2
          .byte 0x65
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
          .byte 0x45
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4c
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_420d00 - .
          .byte 0x7a
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
          .byte 0x20
          .byte 0x2
          .byte 0x63
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x45
          .byte 0xe
          .byte 0xc
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x84
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_420d80 - .
          .byte 0xb6
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
          .byte 0x46
          .byte 0xe
          .byte 0xa0
          .byte 0x8
          .byte 0x2
          .byte 0x54
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x45
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
          .byte 0x2
          .byte 0x4b
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
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xcc
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_420e40 - .
          .byte 0xc1
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
          .byte 0x46
          .byte 0xe
          .byte 0xa0
          .byte 0x8
          .byte 0x2
          .byte 0xa3
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x46
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
          .byte 0x46
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
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_420f10 - .
          .byte 0xe8
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
          .byte 0xb0
          .byte 0x8
          .byte 0x2
          .byte 0xaa
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
          .byte 0x46
          .byte 0xb
          .byte 0x5e
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
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x68
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_421000 - .
          .byte 0xa4
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
          .byte 0x2c
          .byte 0x2
          .byte 0x7e
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
          .byte 0x4f
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
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xbc
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_4210b0 - .
          .byte 0xbf
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
          .byte 0x2c
          .byte 0x2
          .byte 0xb1
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
          .byte 0xf8
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_421170 - .
          .byte 0x8a
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
          .byte 0x1c
          .byte 0x2
          .byte 0x6b
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
          .byte 0x45
          .byte 0xb
          .byte 0x43
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
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4c
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_421200 - .
          .byte 0xca
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
          .byte 0xa7
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
          .byte 0x43
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
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa0
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long L_4212d0 - .
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x24
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_421300 - .
          .byte 0x7c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x7b
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x5e
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x42
          .byte 0xb
          .byte 0x5b
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x24
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xdc
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_421380 - .
          .byte 0xb7
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x3
          .byte 0x6d
          .byte 0x3
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x42
          .byte 0xb
          .byte 0x7c
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_421840 - .
          .byte 0x11
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_421860 - .
          .byte 0x79
          .byte 0x5
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
          .byte 0x4d
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
          .byte 0x46
          .byte 0xb
          .byte 0x47
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_421de0 - .
          .byte 0x64
          .byte 0x5
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
          .byte 0xec
          .byte 0x3
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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb0
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_422350 - .
          .byte 0x53
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x7a
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x4a
          .byte 0xe
          .byte 0x8
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xdc
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_4223b0 - .
          .byte 0x36
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf0
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_4223f0 - .
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x65
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_422420 - .
          .byte 0x41
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
          .byte 0x45
          .byte 0xe
          .byte 0x20
          .byte 0x75
          .byte 0xe
          .byte 0xc
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long L_422470 - .
          .byte 0x53
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
          .byte 0x45
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x47
          .byte 0xe
          .byte 0xc
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x64
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_4224d0 - .
          .byte 0x5a
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x2
          .byte 0x4b
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x43
          .byte 0xe
          .byte 0x8
          .byte 0x45
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x90
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long L_422530 - .
          .byte 0x6f
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
          .byte 0x20
          .byte 0x2
          .byte 0x51
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x45
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
          .byte 0x42
          .byte 0xb
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x49
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
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd8
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_4225a0 - .
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x6c
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf0
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_4225d0 - .
          .byte 0x9a
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0xa0
          .byte 0x8
          .byte 0x2
          .byte 0x91
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long FUN_422670 - .
          .byte 0xc4
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
          .byte 0x30
          .byte 0x2
          .byte 0x87
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
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long L_422740 - .
          .byte 0x9b
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
          .byte 0x30
          .byte 0x2
          .byte 0x8f
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
          .byte 0x90
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long L_4227e0 - .
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
          .byte 0xb0
          .byte 0x8
          .byte 0x2
          .byte 0x56
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
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd0
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long L_4228c0 - .
          .byte 0xd6
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
          .byte 0xc0
          .byte 0x8
          .byte 0x2
          .byte 0xc1
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
          .byte 0x54
          .byte 0xa
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
          .byte 0x42
          .byte 0xb
          .byte 0x2
          .byte 0x72
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
          .byte 0x7a
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
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long FUN_422aa0 - .
          .byte 0x33
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x71
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long FUN_422ae0 - .
          .byte 0x23
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x5d
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x94
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long FUN_422b10 - .
          .byte 0xc9
          .byte 0x7
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
          .byte 0x2e
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
          .byte 0x47
          .byte 0xb
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd4
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long FUN_4232e0 - .
          .byte 0x88
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
          .byte 0x30
          .byte 0x2
          .byte 0x78
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
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long FUN_423370 - .
          .byte 0x3a
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
          .byte 0x20
          .byte 0x70
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
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long FUN_4233b0 - .
          .byte 0x66
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
          .byte 0x20
          .byte 0x2
          .byte 0x5c
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
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long FUN_423420 - .
          .byte 0x68
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
          .byte 0x30
          .byte 0x2
          .byte 0x5a
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
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long FUN_423490 - .
          .byte 0xbb
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
          .byte 0x80
          .byte 0x9
          .byte 0x3
          .byte 0x57
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf8
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long FUN_423650 - .
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x57
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x6c
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .long L_4236c0 - .
          .byte 0x24
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
