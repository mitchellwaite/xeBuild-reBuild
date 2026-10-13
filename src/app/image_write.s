# app/image_write.s -- flash layout (CB/CE/SMC/Mobile*.dat), writing image to disk
#
# original placement:
#   .bss           0046f9c0-004709e0
#   .data          0044a580-0044a5c0
#   .eh_frame      00466be0-004674ac
#   .rdata         00451760-00451fb4
#   .rdata$zzz     0046395c-00463988
#   .text          0040e950-00413090

.intel_syntax noprefix
.globl FUN_40f330
.globl FUN_40fb10
.globl FUN_40fbb0
.globl FUN_40fc30
.globl FUN_40fcc0
.globl FUN_40ff40
.globl FUN_410070
.globl FUN_410220
.globl FUN_410240
.globl FUN_410290
.globl FUN_410360
.globl FUN_410460
.globl FUN_410490
.globl FUN_4104d0
.globl FUN_4104e0
.globl FUN_4104f0
.globl FUN_410500
.globl FUN_410bb0
.globl FUN_411030
.globl FUN_4110b0
.globl FUN_4112b0
.globl FUN_4112f0
.globl FUN_411600
.globl FUN_411680
.globl FUN_411800
.globl FUN_411bd0
.globl FUN_412110
.globl FUN_412230
.globl FUN_412260
.globl FUN_4125a0
.globl FUN_412dd0
.globl FUN_412e90
.globl FUN_412f60
.globl FUN_413030
.globl L_470000
.globl L_47006e

.text
.p2align 4
FUN_40e950:
          cmp DWORD PTR [L_479ee8],EDX
          jb L_40ec84
          push EBP
          push EDI
          mov EDI,EDX
          push ESI
          push EBX
          sub ESP,60
          test EDX,EDX
          mov DWORD PTR [ESP+36],ECX
          mov DWORD PTR [ESP+32],EDX
          je L_40eaab
          cmp EDX,16383
          jbe L_40ec26
          shr EDI,14
          mov DWORD PTR [ESP+28],EDI
          mov EDI,EDX
          and EDI,16383
          jne L_40ec22
L_40e996:
          mov EDI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP],EAX
          call _memcpy
L_40e9af:
          mov ESI,512
          xor EBP,EBP
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40e9c0:
          mov EBX,EBP
          mov EDX,EBP
          mov EDI,EBP
          shr EBX,8
          shl EDX,9
          and EBX,15
          nop
L_40e9d0:
          mov EAX,DWORD PTR [L_479ed0]
          add EAX,EDX
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          mov DWORD PTR [EAX+12],0
          mov ECX,DWORD PTR [L_479ef0]
          test ECX,ECX
          je L_40eac0
          movzx ECX,BYTE PTR [EAX+2]
          add EDX,16
          mov BYTE PTR [EAX],255
          and ECX,4294967280
          or ECX,EBX
          cmp EDX,ESI
          mov BYTE PTR [EAX+2],CL
          mov ECX,EDI
          mov BYTE PTR [EAX+1],CL
          jne L_40e9d0
          add EBP,1
          add ESI,512
          cmp EBP,DWORD PTR [ESP+28]
          jne L_40e9c0
L_40ea2a:
          mov EAX,DWORD PTR [ESP+36]
          cmp AX,61937
          je L_40ea98
          mov EDI,EAX
          sub EAX,1
          mov EBX,DWORD PTR [L_479efc]
          rol DI,8
          cmp AX,-3
          jbe L_40eaf7
          mov EDI,DWORD PTR [ESP+28]
          mov EAX,1
          mov ECX,EBX
          sub EAX,EBX
          neg ECX
          shl ECX,8
          lea ESI,DWORD PTR [EAX+EDI*1]
          add CX,256
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40ea70:
          mov EDX,EAX
          shr DX,8
          add EDX,ECX
          add CX,256
          mov WORD PTR [EAX+EAX*1+L_4cb7be],DX
          add EAX,1
          cmp EAX,ESI
          jne L_40ea70
L_40ea8c:
          cmp WORD PTR [ESP+36],-1
          je L_40ec08
L_40ea98:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [L_4cd840],EAX
          add ESP,60
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_40eaab:
          mov DWORD PTR [ESP+28],1
          jmp L_40e996
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40eac0:
          movzx ECX,BYTE PTR [EAX+1]
          add EDX,16
          mov BYTE PTR [EAX+5],255
          and ECX,4294967280
          or ECX,EBX
          cmp EDX,ESI
          mov BYTE PTR [EAX+1],CL
          mov ECX,EDI
          mov BYTE PTR [EAX],CL
          jne L_40e9d0
          add EBP,1
          add ESI,512
          cmp EBP,DWORD PTR [ESP+28]
          jne L_40e9c0
          jmp L_40ea2a
L_40eaf7:
          mov EAX,EBX
          neg EAX
          lea EAX,DWORD PTR [EAX+EAX*1+L_4cb7c0]
          shr EAX,1
          and EAX,1
          cmp EBP,6
          mov ESI,EAX
          ja L_40ec75
          mov ESI,EBP
L_40eb14:
          mov EAX,EBX
          neg EAX
          cmp ESI,1
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],DI
          je L_40ec94
          mov EAX,1
          sub EAX,EBX
          cmp ESI,2
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],DI
          je L_40ec9e
          mov EAX,2
          sub EAX,EBX
          cmp ESI,3
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],DI
          je L_40eca8
          mov EAX,3
          sub EAX,EBX
          cmp ESI,4
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],DI
          je L_40ecb2
          mov EAX,4
          sub EAX,EBX
          cmp ESI,5
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],DI
          je L_40ec8a
          mov EAX,5
          mov ECX,6
          sub EAX,EBX
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],DI
L_40eb9d:
          cmp EBP,ESI
          je L_40ea8c
L_40eba5:
          sub EBP,ESI
          lea EDX,DWORD PTR [EBP-2]
          mov DWORD PTR [ESP+44],EBP
          shr EDX,1
          add EDX,1
          cmp EBP,1
          lea EAX,DWORD PTR [EDX+EDX*1]
          mov DWORD PTR [ESP+40],EAX
          je L_40ebf0
          mov EAX,EDI
          movzx EBP,DI
          shl EAX,16
          or EBP,EAX
          mov EAX,ESI
          sub EAX,EBX
          lea ESI,DWORD PTR [EAX+EAX*1+L_4cb7c0]
          xor EAX,EAX
L_40ebd6:
          mov DWORD PTR [ESI+EAX*4],EBP
          add EAX,1
          cmp EDX,EAX
          ja L_40ebd6
          mov EAX,DWORD PTR [ESP+40]
          add ECX,EAX
          cmp EAX,DWORD PTR [ESP+44]
          je L_40ea8c
L_40ebf0:
          mov EAX,ECX
          sub EAX,EBX
          cmp WORD PTR [ESP+36],-1
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],DI
          jne L_40ea98
L_40ec08:
          mov EAX,EBX
          mov EDX,4294967071
          not EAX
          add EAX,DWORD PTR [ESP+28]
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],DX
          jmp L_40ea98
L_40ec22:
          mov EDI,DWORD PTR [ESP+32]
L_40ec26:
          mov DWORD PTR [ESP+4],EAX
          mov EDX,EDI
          mov EAX,DWORD PTR [L_479ed8]
          shr EDX,14
          mov DWORD PTR [ESP+8],EDI
          lea ESI,DWORD PTR [EDX+1]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+28],ESI
          call _memcpy
          mov EDX,EDI
          lea EAX,DWORD PTR [EDI+16383]
          add EDX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+4],0
          and EAX,4294950912
          sub EAX,EDI
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],EDX
          call _memset
          jmp L_40e9af
L_40ec75:
          test EAX,EAX
          jne L_40eb14
          xor ECX,ECX
          jmp L_40eba5
L_40ec84:
          mov EAX,4294967295
          ret 
L_40ec8a:
          mov ECX,5
          jmp L_40eb9d
L_40ec94:
          mov ECX,1
          jmp L_40eb9d
L_40ec9e:
          mov ECX,2
          jmp L_40eb9d
L_40eca8:
          mov ECX,3
          jmp L_40eb9d
L_40ecb2:
          mov ECX,4
          jmp L_40eb9d
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_40ecc0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,24
          mov DWORD PTR [ESP+16],ECX
          mov ECX,DWORD PTR [L_479ee8]
          cmp ECX,EAX
          jb L_40eed8
          lea ESI,DWORD PTR [EAX+4096]
          cmp ECX,ESI
          mov DWORD PTR [ESP+20],ESI
          jb L_40eed8
          mov ECX,EAX
          mov EDI,EAX
          mov DWORD PTR [ESP+8],1
          and ECX,16383
          shr EDI,14
          test ECX,ECX
          mov DWORD PTR [ESP+12],EDI
          jne L_40ee98
L_40ed0c:
          add EAX,DWORD PTR [L_479ed8]
          mov ECX,DWORD PTR [EDX]
          mov ESI,EDX
          mov DWORD PTR [EAX],ECX
          lea EDI,DWORD PTR [EAX+4]
          mov ECX,DWORD PTR [EDX+4092]
          and EDI,4294967292
          mov DWORD PTR [EAX+4092],ECX
          sub EAX,EDI
          lea ECX,DWORD PTR [EAX+4096]
          sub ESI,EAX
          shr ECX,2
          rep movsd 
          mov EBP,DWORD PTR [ESP+12]
          mov ESI,DWORD PTR [ESP+8]
          mov EAX,EBP
          add ESI,EBP
          shl EAX,9
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          nop
L_40ed50:
          mov EAX,DWORD PTR [ESP]
          mov EBX,EBP
          mov EDI,EBP
          shr EBX,8
          and EBX,15
          lea ESI,DWORD PTR [EAX+128]
          mov EDX,EAX
L_40ed65:
          mov EAX,DWORD PTR [L_479ed0]
          add EAX,EDX
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          mov DWORD PTR [EAX+12],0
          mov ECX,DWORD PTR [L_479ef0]
          test ECX,ECX
          je L_40ee60
          movzx ECX,BYTE PTR [EAX+2]
          add EDX,16
          mov BYTE PTR [EAX],255
          and ECX,4294967280
          or ECX,EBX
          cmp EDX,ESI
          mov BYTE PTR [EAX+2],CL
          mov ECX,EDI
          mov BYTE PTR [EAX+1],CL
          jne L_40ed65
          add EBP,1
          add DWORD PTR [ESP],512
          cmp DWORD PTR [ESP+4],EBP
          jne L_40ed50
L_40edc0:
          mov EDI,DWORD PTR [ESP+16]
          cmp DI,61937
          je L_40ee46
          mov ESI,DWORD PTR [ESP+12]
          mov ECX,DWORD PTR [L_479efc]
          lea EBX,DWORD PTR [EDI-1]
          mov EAX,EDI
          rol AX,8
          mov EDX,ESI
          sub EDX,ECX
          cmp BX,-3
          jbe L_40eeb8
          mov EAX,ESI
          lea ESI,DWORD PTR [EDX+1]
          sub EAX,ECX
          add EAX,1
          mov EBX,ESI
          mov EDI,EAX
          shr BX,8
          shl EDI,8
          add EBX,EDI
          cmp DWORD PTR [ESP+8],2
          mov WORD PTR [EDX+EDX*1+L_4cb7c0],BX
          jne L_40ee29
          add EDX,2
          add EAX,1
          shr DX,8
          shl EAX,8
          add EAX,EDX
          mov WORD PTR [ESI+ESI*1+L_4cb7c0],AX
L_40ee29:
          cmp WORD PTR [ESP+16],-1
          jne L_40ee46
          mov EAX,ECX
          mov EDX,4294967071
          not EAX
          add EAX,DWORD PTR [ESP+4]
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],DX
L_40ee46:
          mov EAX,DWORD PTR [ESP+20]
          mov DWORD PTR [L_4cd840],EAX
          xor EAX,EAX
L_40ee51:
          add ESP,24
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
L_40ee60:
          movzx ECX,BYTE PTR [EAX+1]
          add EDX,16
          mov BYTE PTR [EAX+5],255
          and ECX,4294967280
          or ECX,EBX
          cmp EDX,ESI
          mov BYTE PTR [EAX+1],CL
          mov ECX,EDI
          mov BYTE PTR [EAX],CL
          jne L_40ed65
          add EBP,1
          add DWORD PTR [ESP],512
          cmp DWORD PTR [ESP+4],EBP
          jne L_40ed50
          jmp L_40edc0
L_40ee98:
          mov EBX,16384
          sub EBX,ECX
          mov ECX,EBX
          xor EBX,EBX
          cmp ECX,4096
          setb BL
          add EBX,1
          mov DWORD PTR [ESP+8],EBX
          jmp L_40ed0c
L_40eeb8:
          cmp DWORD PTR [ESP+8],2
          mov WORD PTR [EDX+EDX*1+L_4cb7c0],AX
          jne L_40ee46
          mov WORD PTR [EDX+EDX*1+L_4cb7c2],AX
          jmp L_40ee46
L_40eed8:
          mov EAX,4294967295
          jmp L_40ee51
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
FUN_40eef0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov ESI,DWORD PTR [L_479ee8]
          mov EDI,DWORD PTR [ESP+80]
          cmp ESI,EAX
          mov DWORD PTR [ESP+32],EDI
          jb L_40f289
          lea EDI,DWORD PTR [EAX+ECX*1]
          cmp ESI,EDI
          mov DWORD PTR [ESP+40],EDI
          jb L_40f289
          mov EBX,ECX
          mov EDI,EAX
          mov ECX,EAX
          shr EDI,14
          and ECX,16383
          mov ESI,16384
          sub ESI,ECX
          mov DWORD PTR [ESP+36],EDI
          test ECX,ECX
          mov EDI,0
          cmove ESI,EDI
          cmp EBX,ESI
          jbe L_40f0bb
          mov EDI,EBX
          sub EDI,ESI
          mov ESI,EDI
          and ESI,16383
          cmp EDI,16384
          cmovb ESI,EDI
          shr EDI,14
          test ESI,ESI
          mov DWORD PTR [ESP+28],EDI
          je L_40f1f8
          test ECX,ECX
          lea ESI,DWORD PTR [EDI+1]
          je L_40f2e6
          add EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDX
          add DWORD PTR [ESP+28],2
          mov DWORD PTR [ESP],EAX
          call _memcpy
L_40ef92:
          mov ESI,DWORD PTR [ESP+40]
          mov EDX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+4],0
          mov EAX,ESI
          add EDX,ESI
          add EAX,16383
          mov DWORD PTR [ESP],EDX
          and EAX,4294950912
          sub EAX,ESI
          mov DWORD PTR [ESP+8],EAX
          call _memset
L_40efc0:
          mov EBP,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+24],0
          mov EDX,EBP
          shl EDX,9
L_40efd1:
          mov EBX,EBP
          lea ESI,DWORD PTR [EDX+512]
          mov EDI,EBP
          shr EBX,8
          and EBX,15
L_40efe1:
          mov EAX,DWORD PTR [L_479ed0]
          add EAX,EDX
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          mov DWORD PTR [EAX+12],0
          mov ECX,DWORD PTR [L_479ef0]
          test ECX,ECX
          je L_40f0f0
          movzx ECX,BYTE PTR [EAX+2]
          add EDX,16
          mov BYTE PTR [EAX],255
          and ECX,4294967280
          or ECX,EBX
          cmp EDX,ESI
          mov BYTE PTR [EAX+2],CL
          mov ECX,EDI
          mov BYTE PTR [EAX+1],CL
          jne L_40efe1
L_40f02c:
          add DWORD PTR [ESP+24],1
          add EBP,1
          mov EDX,ESI
          mov EAX,DWORD PTR [ESP+24]
          cmp DWORD PTR [ESP+28],EAX
          ja L_40efd1
          mov EDI,DWORD PTR [ESP+32]
          cmp DI,61937
          je L_40f0a8
          mov ESI,DWORD PTR [ESP+36]
          mov EDX,DWORD PTR [L_479efc]
          lea EBX,DWORD PTR [EDI-1]
          mov ECX,EDI
          rol CX,8
          mov EAX,ESI
          sub EAX,EDX
          cmp BX,-3
          jbe L_40f114
          mov ECX,ESI
          mov ESI,DWORD PTR [ESP+28]
          add EAX,1
          sub ECX,EDX
          add ECX,1
          lea EBX,DWORD PTR [EAX+ESI*1]
          shl ECX,8
L_40f080:
          mov EDX,EAX
          shr DX,8
          add EDX,ECX
          add CX,256
          mov WORD PTR [EAX+EAX*1+L_4cb7be],DX
          add EAX,1
          cmp EAX,EBX
          jne L_40f080
L_40f09c:
          cmp WORD PTR [ESP+32],-1
          je L_40f1d4
L_40f0a8:
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [L_4cd840],EAX
          xor EAX,EAX
L_40f0b3:
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_40f0bb:
          add EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EAX
          call _memcpy
          test EBX,EBX
          mov DWORD PTR [ESP+28],1
          je L_40efc0
          jmp L_40ef92
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40f0f0:
          movzx ECX,BYTE PTR [EAX+1]
          add EDX,16
          mov BYTE PTR [EAX+5],255
          and ECX,4294967280
          or ECX,EBX
          cmp EDX,ESI
          mov BYTE PTR [EAX+1],CL
          mov ECX,EDI
          mov BYTE PTR [EAX],CL
          jne L_40efe1
          jmp L_40f02c
L_40f114:
          lea EDX,DWORD PTR [EAX+EAX*1+L_4cb7c0]
          shr EDX,1
          and EDX,1
          cmp DWORD PTR [ESP+28],6
          ja L_40f234
          mov EDI,DWORD PTR [ESP+28]
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],CX
          cmp EDI,1
          je L_40f2aa
          cmp EDI,2
          mov WORD PTR [EAX+EAX*1+L_4cb7c2],CX
          je L_40f2b9
          cmp EDI,3
          mov WORD PTR [EAX+EAX*1+L_4cb7c4],CX
          je L_40f2c8
          cmp EDI,4
          mov WORD PTR [EAX+EAX*1+L_4cb7c6],CX
          je L_40f2d7
          cmp EDI,5
          mov WORD PTR [EAX+EAX*1+L_4cb7c8],CX
          je L_40f293
          mov ESI,EDI
          mov WORD PTR [EAX+EAX*1+L_4cb7ca],CX
          mov EDI,6
L_40f193:
          mov EBX,DWORD PTR [ESP+28]
          cmp EBX,ESI
          je L_40f09c
          sub EBX,ESI
          lea EDX,DWORD PTR [EBX-2]
          mov DWORD PTR [ESP+44],EBX
          shr EDX,1
          cmp EBX,1
          lea EBP,DWORD PTR [EDX+1]
          lea EDX,DWORD PTR [EBP+EBP*1]
          mov DWORD PTR [ESP+24],EDX
          jne L_40f254
L_40f1be:
          add EAX,EDI
          cmp WORD PTR [ESP+32],-1
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],CX
          jne L_40f0a8
L_40f1d4:
          mov EDX,DWORD PTR [L_479efc]
          mov EAX,DWORD PTR [ESP+36]
          add EAX,DWORD PTR [ESP+28]
          not EDX
          add EAX,EDX
          mov EDX,4294967071
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],DX
          jmp L_40f0a8
L_40f1f8:
          test ECX,ECX
          jne L_40f305
          add EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+28]
          test EAX,EAX
          jne L_40efc0
          cmp WORD PTR [ESP+32],61937
          jne L_40f09c
          jmp L_40f0a8
L_40f234:
          test EDX,EDX
          jne L_40f2a2
          mov ESI,DWORD PTR [ESP+28]
          lea EDX,DWORD PTR [ESI-2]
          mov DWORD PTR [ESP+44],ESI
          xor ESI,ESI
          shr EDX,1
          lea EBP,DWORD PTR [EDX+1]
          lea EDI,DWORD PTR [EBP+EBP*1]
          mov DWORD PTR [ESP+24],EDI
          xor EDI,EDI
L_40f254:
          mov EDX,ECX
          movzx EBX,CX
          shl EDX,16
          or EBX,EDX
          lea EDX,DWORD PTR [EAX+ESI*1]
          lea ESI,DWORD PTR [EDX+EDX*1+L_4cb7c0]
          xor EDX,EDX
L_40f26a:
          mov DWORD PTR [ESI+EDX*4],EBX
          add EDX,1
          cmp EDX,EBP
          jb L_40f26a
          mov ESI,DWORD PTR [ESP+24]
          add EDI,ESI
          cmp ESI,DWORD PTR [ESP+44]
          jne L_40f1be
          jmp L_40f09c
L_40f289:
          mov EAX,4294967295
          jmp L_40f0b3
L_40f293:
          mov ESI,5
          mov EDI,5
          jmp L_40f193
L_40f2a2:
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],CX
L_40f2aa:
          mov ESI,1
          mov EDI,1
          jmp L_40f193
L_40f2b9:
          mov ESI,2
          mov EDI,2
          jmp L_40f193
L_40f2c8:
          mov ESI,3
          mov EDI,3
          jmp L_40f193
L_40f2d7:
          mov ESI,4
          mov EDI,4
          jmp L_40f193
L_40f2e6:
          add EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov DWORD PTR [ESP+28],ESI
          jmp L_40ef92
L_40f305:
          add EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDX
          add DWORD PTR [ESP+28],1
          mov DWORD PTR [ESP],EAX
          call _memcpy
          jmp L_40efc0
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
FUN_40f330:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          cmp DWORD PTR [L_479ea8],1
          je L_40fa60
L_40f344:
          mov EAX,DWORD PTR [L_479ea4]
          test EAX,1073741824
          je L_40f3c5
          test EAX,536870912
          mov DWORD PTR [L_479ee4],4096
          mov DWORD PTR [L_479eec],62783488
          mov DWORD PTR [L_479ef0],1
          mov BYTE PTR [L_479ecc],4
          mov BYTE PTR [L_479ece],16
          je L_40f630
          mov DWORD PTR [L_479efc],736
          mov DWORD PTR [L_479ef8],3808
          mov ESI,67108864
          mov BYTE PTR [L_479ecd],96
          mov DWORD PTR [L_479ec8],92
          mov EDI,2097152
          mov DWORD PTR [ESP+28],1
          mov EAX,69206016
          jmp L_40f420
L_40f3c5:
          mov ESI,DWORD PTR [L_479ea8]
          lea EDX,DWORD PTR [ESI-6]
          and EDX,4294967293
          jne L_40f5d0
          mov DWORD PTR [L_479ee4],4096
          mov DWORD PTR [L_479eec],64995328
          mov ESI,67108864
          mov DWORD PTR [L_479ef0],0
          mov DWORD PTR [L_479efc],0
          mov EDI,2097152
          mov DWORD PTR [L_479ef8],3964
          mov DWORD PTR [ESP+28],0
          mov EAX,69206016
L_40f420:
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [L_479ee8],EAX
          mov DWORD PTR [L_479ed4],EDI
          call _malloc
          mov DWORD PTR [ESP],ESI
          mov EBX,EAX
          mov DWORD PTR [L_479ed0],EAX
          mov DWORD PTR [L_479edc],ESI
          call _malloc
          test EAX,EAX
          mov EBP,EAX
          mov DWORD PTR [L_479ed8],EAX
          je L_40fae0
          test EBX,EBX
          je L_40fae0
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],255
          mov DWORD PTR [ESP],EBX
          call _memset
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],255
          mov DWORD PTR [ESP],EBP
          call _memset
          mov EDX,OFFSET L_4c97c0
          xor EAX,EAX
          mov ECX,2048
          mov EDI,EDX
          mov EDX,OFFSET L_4cd7c0
          rep stosd DWORD PTR ES:[EDI]
          mov EDI,OFFSET L_4cb7c4
          mov ECX,OFFSET L_4cd7c0
          mov DWORD PTR [L_4cb7c0],0
          and EDI,4294967292
          mov DWORD PTR [L_4cd7bc],0
          sub ECX,EDI
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          mov EDI,EDX
          mov ECX,32
          mov EDX,OFFSET L_4c9164
          rep stosd DWORD PTR ES:[EDI]
          mov ECX,128
          mov EDI,EDX
          mov DWORD PTR [L_4cd7c0],1611091967
          rep stosd DWORD PTR ES:[EDI]
          mov EAX,DWORD PTR [L_479ea8]
          cmp EAX,2
          je L_40f784
          sub EAX,8
          mov DWORD PTR [ESP],9
          cmp EAX,2
          sbb EAX,EAX
          and EAX,OFFSET __ImageBase
          add EAX,8388608
          mov DWORD PTR [L_4cd7c8],EAX
          call FUN_427650
          mov DWORD PTR [ESP],9
          mov EBX,EAX
          call FUN_427650
          mov DWORD PTR [ESP],9
          mov ESI,EAX
          shl EBX,24
          call FUN_427650
          mov DWORD PTR [ESP],9
          mov EDI,EAX
          shl ESI,8
          call FUN_427650
          shr EAX,24
          mov ECX,DWORD PTR [L_479ea8]
          and ESI,16711680
          lea EDX,DWORD PTR [EBX+EAX*1]
          shr EDI,8
          mov DWORD PTR [L_4cd828],302449152
          and EDI,65280
          mov DWORD PTR [L_4cd82c],OFFSET __ImageBase
          mov DWORD PTR [L_4cd838],3145728
          lea EBX,DWORD PTR [EDX+ESI*1]
          lea EDX,DWORD PTR [ECX-8]
          mov DWORD PTR [L_4cd83c],1048576
          mov DWORD PTR [L_4cd840],32768
          lea EAX,DWORD PTR [EBX+EDI*1]
          cmp EDX,2
          sbb EDX,EDX
          mov DWORD PTR [L_4cd7cc],EAX
          mov DWORD PTR [L_4cd824],EAX
          and EDX,OFFSET __ImageBase
          mov EAX,DWORD PTR [L_479ea4]
          add EDX,OFFSET __ImageBase
          mov DWORD PTR [L_4cd820],EDX
          mov EDX,EAX
          and EDX,7
          jmp DWORD PTR [EDX*4+L_4517d8]
          .byte 0x66   # nop
          nop
L_40f5d0:
          test EAX,268435456
          jne L_40f9f0
          mov DWORD PTR [L_479ee4],1024
          mov DWORD PTR [L_479eec],16236544
          mov ESI,16777216
          mov DWORD PTR [L_479efc],0
          mov DWORD PTR [L_479ef8],988
          mov EDI,524288
          mov EAX,17301504
L_40f612:
          mov DWORD PTR [L_479ef0],0
          mov DWORD PTR [ESP+28],0
          jmp L_40f420
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40f630:
          mov DWORD PTR [L_479efc],2784
          mov DWORD PTR [L_479ef8],3808
          mov ESI,67108864
          mov BYTE PTR [L_479ecd],32
          mov DWORD PTR [L_479ec8],348
          mov EDI,2097152
          mov DWORD PTR [ESP+28],1
          mov EAX,69206016
          jmp L_40f420
L_40f671:
          test EAX,EAX
          js L_40fac0
L_40f679:
          mov EBX,DWORD PTR [L_479ef0]
          test EBX,EBX
          je L_40f68d
          mov DWORD PTR [L_4cd830],512
L_40f68d:
          mov BYTE PTR [L_44a58a],57
L_40f694:
          cmp ECX,5
          jbe L_40f805
          cmp DWORD PTR [L_479ef0],1
          mov EAX,128
          mov BYTE PTR [L_44a589],49
          mov WORD PTR [L_4cd7c4],AX
          mov BYTE PTR [L_44a58a],48
          sbb EAX,EAX
          xor AL,AL
          add EAX,512
          mov DWORD PTR [L_4cd830],EAX
          mov EAX,DWORD PTR [L_44a580]
          mov DWORD PTR [L_4cd7d0],EAX
          mov EAX,DWORD PTR [L_44a584]
          mov DWORD PTR [L_4cd7d4],EAX
          mov EAX,DWORD PTR [L_44a588]
          mov DWORD PTR [L_4cd7d8],EAX
          mov EAX,DWORD PTR [L_44a58c]
          mov DWORD PTR [L_4cd7dc],EAX
          mov EAX,DWORD PTR [L_44a590]
          mov DWORD PTR [L_4cd7e0],EAX
          mov EAX,DWORD PTR [L_44a594]
          mov DWORD PTR [L_4cd7e4],EAX
          mov EAX,DWORD PTR [L_44a598]
          mov DWORD PTR [L_4cd7e8],EAX
          mov EAX,DWORD PTR [L_44a59c]
          mov DWORD PTR [L_4cd7ec],EAX
          mov EAX,DWORD PTR [L_44a5a0]
          mov DWORD PTR [L_4cd7f0],EAX
          mov EAX,DWORD PTR [L_44a5a4]
          mov DWORD PTR [L_4cd7f4],EAX
          mov EAX,DWORD PTR [L_44a5a8]
          mov DWORD PTR [L_4cd7f8],EAX
          mov EAX,DWORD PTR [L_44a5ac]
          mov DWORD PTR [L_4cd7fc],EAX
          mov EAX,DWORD PTR [L_44a5b0]
          mov DWORD PTR [L_4cd800],EAX
          mov EAX,DWORD PTR [L_44a5b4]
          mov DWORD PTR [L_4cd804],EAX
          mov EAX,DWORD PTR [L_44a5b8]
          mov DWORD PTR [L_4cd808],EAX
          mov EAX,DWORD PTR [L_44a5bc]
          mov DWORD PTR [L_4cd80c],EAX
L_40f76b:
          mov EAX,DWORD PTR [L_479ed8]
          mov BYTE PTR [EAX+73],0
          mov BYTE PTR [EAX+74],0
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp L_42e760
L_40f784:
          mov EDX,DWORD PTR [L_479ea4]
          mov DWORD PTR [L_4cd7c8],8388608
          mov DWORD PTR [L_4cd7cc],1792
          mov DWORD PTR [L_4cd820],OFFSET __ImageBase
          mov DWORD PTR [L_4cd824],1792
          mov DWORD PTR [L_4cd828],302449152
          mov EAX,EDX
          mov DWORD PTR [L_4cd82c],OFFSET __ImageBase
          mov DWORD PTR [L_4cd838],3145728
          and EAX,7
          mov DWORD PTR [L_4cd83c],1048576
          mov DWORD PTR [L_4cd840],32768
          cmp EAX,4
          je L_40fa30
          sub EAX,1
          cmp EAX,1
          jbe L_40faa0
          mov BYTE PTR [L_44a58a],55
L_40f805:
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          call _checkZeros
          test EAX,EAX
          je L_40f900
L_40f821:
          mov EAX,DWORD PTR [L_479ea8]
L_40f826:
          mov EDX,DWORD PTR [L_44a580]
          cmp EAX,1
          mov DWORD PTR [L_4cd7d0],EDX
          mov EDX,DWORD PTR [L_44a584]
          mov DWORD PTR [L_4cd7d4],EDX
          mov EDX,DWORD PTR [L_44a588]
          mov DWORD PTR [L_4cd7d8],EDX
          mov EDX,DWORD PTR [L_44a58c]
          mov DWORD PTR [L_4cd7dc],EDX
          mov EDX,DWORD PTR [L_44a590]
          mov DWORD PTR [L_4cd7e0],EDX
          mov EDX,DWORD PTR [L_44a594]
          mov DWORD PTR [L_4cd7e4],EDX
          mov EDX,DWORD PTR [L_44a598]
          mov DWORD PTR [L_4cd7e8],EDX
          mov EDX,DWORD PTR [L_44a59c]
          mov DWORD PTR [L_4cd7ec],EDX
          mov EDX,DWORD PTR [L_44a5a0]
          mov DWORD PTR [L_4cd7f0],EDX
          mov EDX,DWORD PTR [L_44a5a4]
          mov DWORD PTR [L_4cd7f4],EDX
          mov EDX,DWORD PTR [L_44a5a8]
          mov DWORD PTR [L_4cd7f8],EDX
          mov EDX,DWORD PTR [L_44a5ac]
          mov DWORD PTR [L_4cd7fc],EDX
          mov EDX,DWORD PTR [L_44a5b0]
          mov DWORD PTR [L_4cd800],EDX
          mov EDX,DWORD PTR [L_44a5b4]
          mov DWORD PTR [L_4cd804],EDX
          mov EDX,DWORD PTR [L_44a5b8]
          mov DWORD PTR [L_4cd808],EDX
          mov EDX,DWORD PTR [L_44a5bc]
          mov DWORD PTR [L_4cd80c],EDX
          jne L_40f76b
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp L_42e760
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_40f900:
          cmp BYTE PTR [L_479f15],0
          jne L_40f821
          mov DWORD PTR [ESP+4],OFFSET L_451760
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea8]
          cmp EAX,2
          je L_40f944
          mov DWORD PTR [ESP+4],OFFSET L_45179c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea8]
L_40f944:
          mov BYTE PTR [L_479f15],1
          jmp L_40f826
L_40f950:
          mov DWORD PTR [L_479ef4],1
          mov DWORD PTR [L_4cd830],256
          mov BYTE PTR [L_44a589],49
          mov BYTE PTR [L_44a58a],48
          mov DWORD PTR [L_4cd83c],2048
          mov DWORD PTR [L_4cd838],14336
          jmp L_40f694
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_40f990:
          mov DWORD PTR [L_479ef4],1
          mov DWORD PTR [L_4cd830],256
          mov BYTE PTR [L_44a589],49
          mov BYTE PTR [L_44a58a],48
          jmp L_40f694
L_40f9b7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40f9c0:
          mov BYTE PTR [L_44a58a],55
          jmp L_40f694
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_40f9d0:
          mov BYTE PTR [L_44a58a],53
          mov DWORD PTR [L_4cd820],0
          jmp L_40f694
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40f9f0:
          mov DWORD PTR [L_479ee4],3072
          mov DWORD PTR [L_479eec],50315264
          mov ESI,50331648
          mov DWORD PTR [L_479efc],0
          mov DWORD PTR [L_479ef8],3066
          mov EDI,1572864
          mov EAX,51904512
          jmp L_40f612
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_40fa30:
          test EDX,EDX
          js L_40faf0
L_40fa38:
          mov EDX,DWORD PTR [ESP+28]
          test EDX,EDX
          je L_40fa4a
          mov DWORD PTR [L_4cd830],256
L_40fa4a:
          mov BYTE PTR [L_44a58a],56
          jmp L_40f805
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40fa60:
          mov DWORD PTR [ESP],9
          call FUN_4276f0
          mov DWORD PTR [ESP],25
          mov EBX,EAX
          call FUN_4276f0
          imul EAX,EAX,1068
          imul EBX,EBX,1068
          mov EAX,DWORD PTR [EAX+L_4bc150+8]
          mov DWORD PTR [EBX+L_4bc150+8],EAX
          jmp L_40f344
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40faa0:
          mov BYTE PTR [L_44a58a],53
          mov DWORD PTR [L_4cd820],0
          jmp L_40f805
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40fac0:
          mov DWORD PTR [L_479ef4],1
          mov DWORD PTR [L_4cd830],256
          jmp L_40f679
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40fae0:
          add ESP,44
          mov EAX,4294967295
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_40faf0:
          mov DWORD PTR [L_479ef4],1
          mov DWORD PTR [L_4cd830],256
          jmp L_40fa38
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_40fb10:
          sub ESP,28
          mov EAX,DWORD PTR [L_479ed0]
          test EAX,EAX
          je L_40fb24
          mov DWORD PTR [ESP],EAX
          call _free
L_40fb24:
          mov EAX,DWORD PTR [L_479ed8]
          test EAX,EAX
          je L_40fb35
          mov DWORD PTR [ESP],EAX
          call _free
L_40fb35:
          mov EAX,DWORD PTR [L_479ee0]
          test EAX,EAX
          je L_40fb46
          mov DWORD PTR [ESP],EAX
          call _free
L_40fb46:
          mov EAX,DWORD PTR [L_47a080]
          test EAX,EAX
          je L_40fb57
          mov DWORD PTR [ESP],EAX
          call _free
L_40fb57:
          add ESP,28
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_40fb60:
          push EDI
          push ESI
          xor ECX,ECX
          push EBX
          mov EDI,DWORD PTR [ESP+20]
          xor EAX,EAX
          mov EBX,DWORD PTR [ESP+16]
          xor EDX,EDX
L_40fb71:
          test DL,31
          jne L_40fb86
          cmp EDX,4096
          cmove EBX,EDI
          mov ECX,DWORD PTR [EBX]
          add EBX,4
          not ECX
L_40fb86:
          mov ESI,ECX
          shr ECX,1
          and ESI,1
          xor EAX,ESI
          mov ESI,EAX
          xor ESI,110445913
          test AL,1
          cmovne EAX,ESI
          add EDX,1
          shr EAX,1
          cmp EDX,4198
          jne L_40fb71
          pop EBX
          not EAX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
FUN_40fbb0:
          push EDI
          push ESI
          xor ECX,ECX
          push EBX
          mov EBX,DWORD PTR [ESP+20]
          xor EAX,EAX
          mov ESI,DWORD PTR [ESP+16]
          xor EDX,EDX
L_40fbc1:
          test DL,31
          jne L_40fbd6
          cmp EDX,4096
          cmove ESI,EBX
          mov ECX,DWORD PTR [ESI]
          add ESI,4
          not ECX
L_40fbd6:
          mov EDI,ECX
          shr ECX,1
          and EDI,1
          xor EAX,EDI
          mov EDI,EAX
          xor EDI,110445913
          test AL,1
          cmovne EAX,EDI
          add EDX,1
          shr EAX,1
          cmp EDX,4198
          jne L_40fbc1
          movzx EDX,BYTE PTR [EBX+12]
          not EAX
          mov ECX,EAX
          shl ECX,6
          and EDX,63
          add EDX,ECX
          mov BYTE PTR [EBX+12],DL
          mov EDX,EAX
          shr EDX,2
          mov BYTE PTR [EBX+13],DL
          mov EDX,EAX
          shr EAX,18
          shr EDX,10
          mov BYTE PTR [EBX+15],AL
          mov BYTE PTR [EBX+14],DL
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_40fc30:
          push EDI
          push ESI
          xor ECX,ECX
          push EBX
          mov ESI,DWORD PTR [ESP+20]
          xor EAX,EAX
          mov EBX,DWORD PTR [ESP+16]
          xor EDX,EDX
L_40fc41:
          test DL,31
          jne L_40fc56
          cmp EDX,4096
          cmove EBX,ESI
          mov ECX,DWORD PTR [EBX]
          add EBX,4
          not ECX
L_40fc56:
          mov EDI,ECX
          shr ECX,1
          and EDI,1
          xor EAX,EDI
          mov EDI,EAX
          xor EDI,110445913
          test AL,1
          cmovne EAX,EDI
          add EDX,1
          shr EAX,1
          cmp EDX,4198
          jne L_40fc41
          movzx EBX,BYTE PTR [ESI+12]
          not EAX
          mov ECX,EAX
          mov EDX,EAX
          xor EAX,EAX
          shl ECX,6
          movzx ECX,CL
          and EBX,192
          cmp EBX,ECX
          je L_40fc99
L_40fc95:
          pop EBX
          pop ESI
          pop EDI
          ret 
L_40fc99:
          mov ECX,EDX
          shr ECX,2
          cmp BYTE PTR [ESI+13],CL
          jne L_40fc95
          mov ECX,EDX
          shr ECX,10
          cmp BYTE PTR [ESI+14],CL
          jne L_40fc95
          xor EAX,EAX
          shr EDX,18
          cmp BYTE PTR [ESI+15],DL
          sete AL
          jmp L_40fc95
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_40fcc0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,20
          cmp DWORD PTR [ESP+44],1
          mov EDI,DWORD PTR [ESP+40]
          sbb EAX,EAX
          and AL,32
          add EAX,256
          imul EAX,EAX,528
          add EAX,EDI
          mov DWORD PTR [ESP+16],EAX
L_40fce5:
          lea ESI,DWORD PTR [EDI+512]
          xor EAX,EAX
          jmp L_40fcfe
          .byte 0x90
L_40fcf0:
          add EAX,1
          cmp EAX,512
          je L_40fdb0
L_40fcfe:
          cmp BYTE PTR [EDI+EAX*1],255
          je L_40fcf0
L_40fd04:
          movzx EAX,BYTE PTR [EDI+524]
          mov BYTE PTR [ESP],AL
L_40fd0e:
          xor EAX,EAX
          mov EBX,EDI
          xor ECX,ECX
          xor EDX,EDX
          mov EBP,EAX
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_40fd20:
          test DL,31
          jne L_40fd37
          mov EAX,EBX
          cmp EDX,4096
          cmove EAX,ESI
          mov ECX,DWORD PTR [EAX]
          lea EBX,DWORD PTR [EAX+4]
          not ECX
L_40fd37:
          mov EAX,ECX
          shr ECX,1
          and EAX,1
          xor EAX,EBP
          mov EBP,EAX
          xor EBP,110445913
          test AL,1
          cmovne EAX,EBP
          add EDX,1
          shr EAX,1
          cmp EDX,4198
          mov EBP,EAX
          jne L_40fd20
          not EAX
          mov EDX,DWORD PTR [ESP]
          mov ECX,EAX
          shl ECX,6
          and EDX,192
          movzx ECX,CL
          cmp EDX,ECX
          je L_40fd7d
L_40fd73:
          add ESP,20
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_40fd7d:
          mov EDX,EAX
          shr EDX,2
          cmp BYTE PTR [EDI+525],DL
          jne L_40fd73
          mov EDX,EAX
          shr EDX,10
          cmp BYTE PTR [EDI+526],DL
          jne L_40fd73
          shr EAX,18
          cmp BYTE PTR [EDI+527],AL
          jne L_40fd73
          jmp L_40fe86
L_40fda7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40fdb0:
          cmp BYTE PTR [EDI+512],255
          jne L_40fd04
          cmp BYTE PTR [EDI+513],255
          jne L_40fd04
          cmp BYTE PTR [EDI+514],255
          jne L_40fd04
          cmp BYTE PTR [EDI+515],255
          jne L_40fd04
          cmp BYTE PTR [EDI+516],255
          jne L_40fd04
          cmp BYTE PTR [EDI+517],255
          jne L_40fd04
          cmp BYTE PTR [EDI+518],255
          jne L_40fd04
          cmp BYTE PTR [EDI+519],255
          jne L_40fd04
          cmp BYTE PTR [EDI+520],255
          jne L_40fd04
          cmp BYTE PTR [EDI+521],255
          jne L_40fd04
          cmp BYTE PTR [EDI+522],255
          jne L_40fd04
          cmp BYTE PTR [EDI+523],255
          jne L_40fd04
          movzx EAX,BYTE PTR [EDI+524]
          cmp AL,255
          mov BYTE PTR [ESP],AL
          jne L_40fd0e
          cmp BYTE PTR [EDI+525],255
          jne L_40fd0e
          movzx EAX,BYTE PTR [EDI+526]
          cmp AL,255
          mov BYTE PTR [ESP],AL
          jne L_40fea3
          cmp BYTE PTR [EDI+527],255
          jne L_40fd0e
L_40fe86:
          add EDI,528
          cmp DWORD PTR [ESP+16],EDI
          jne L_40fce5
          add ESP,20
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_40fea3:
          mov BYTE PTR [ESP],255
          jmp L_40fd0e
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_40feb0:
          mov EAX,DWORD PTR [ESP+4]
          mov ECX,DWORD PTR [ESP+8]
          lea EDX,DWORD PTR [EAX+512]
          jmp L_40fec7
L_40fec0:
          add EAX,1
          cmp EAX,EDX
          je L_40fed0
L_40fec7:
          cmp BYTE PTR [EAX],255
          je L_40fec0
L_40fecc:
          xor EAX,EAX
          ret 
          .byte 0x90
L_40fed0:
          cmp BYTE PTR [ECX],255
          jne L_40fecc
          cmp BYTE PTR [ECX+1],255
          jne L_40fecc
          cmp BYTE PTR [ECX+2],255
          jne L_40fecc
          cmp BYTE PTR [ECX+3],255
          jne L_40fecc
          cmp BYTE PTR [ECX+4],255
          jne L_40fecc
          cmp BYTE PTR [ECX+5],255
          jne L_40fecc
          cmp BYTE PTR [ECX+6],255
          jne L_40fecc
          cmp BYTE PTR [ECX+7],255
          jne L_40fecc
          cmp BYTE PTR [ECX+8],255
          jne L_40fecc
          cmp BYTE PTR [ECX+9],255
          jne L_40fecc
          cmp BYTE PTR [ECX+10],255
          jne L_40fecc
          cmp BYTE PTR [ECX+11],255
          jne L_40fecc
          cmp BYTE PTR [ECX+12],255
          jne L_40fecc
          cmp BYTE PTR [ECX+13],255
          jne L_40fecc
          cmp BYTE PTR [ECX+14],255
          jne L_40fecc
          xor EAX,EAX
          cmp BYTE PTR [ECX+15],255
          sete AL
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
FUN_40ff40:
          cmp DWORD PTR [ESP+8],1
          mov EAX,DWORD PTR [ESP+4]
          sbb EDX,EDX
          and EDX,4294849024
          lea EDX,DWORD PTR [EDX+EAX*1+135168]
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_40ff60:
          cmp BYTE PTR [EAX],255
          jne L_40ff72
          add EAX,1
          cmp EAX,EDX
          jne L_40ff60
          mov EAX,1
          ret 
L_40ff72:
          xor EAX,EAX
          ret 
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
L_40ff80:
          push EBX
          cmp DWORD PTR [ESP+16],1
          mov ECX,DWORD PTR [ESP+12]
          mov EDX,DWORD PTR [ESP+8]
          sbb EBX,EBX
          and BL,32
          add EBX,256
          shl EBX,4
          add EBX,ECX
          .byte 0x66   # nop
          nop
L_40ffa0:
          xor EAX,EAX
          jmp L_40ffae
L_40ffa4:
          add EAX,1
          cmp EAX,512
          je L_40ffc0
L_40ffae:
          cmp BYTE PTR [EDX+EAX*1],255
          je L_40ffa4
L_40ffb4:
          xor EAX,EAX
          pop EBX
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40ffc0:
          cmp BYTE PTR [ECX],255
          jne L_40ffb4
          cmp BYTE PTR [ECX+1],255
          jne L_40ffb4
          cmp BYTE PTR [ECX+2],255
          jne L_40ffb4
          cmp BYTE PTR [ECX+3],255
          jne L_40ffb4
          cmp BYTE PTR [ECX+4],255
          jne L_40ffb4
          cmp BYTE PTR [ECX+5],255
          jne L_40ffb4
          cmp BYTE PTR [ECX+6],255
          jne L_40ffb4
          cmp BYTE PTR [ECX+7],255
          jne L_40ffb4
          cmp BYTE PTR [ECX+8],255
          jne L_40ffb4
          cmp BYTE PTR [ECX+9],255
          jne L_40ffb4
          cmp BYTE PTR [ECX+10],255
          jne L_40ffb4
          cmp BYTE PTR [ECX+11],255
          jne L_40ffb4
          cmp BYTE PTR [ECX+12],255
          jne L_40ffb4
          cmp BYTE PTR [ECX+13],255
          jne L_40ffb4
          cmp BYTE PTR [ECX+14],255
          jne L_40ffb4
          cmp BYTE PTR [ECX+15],255
          jne L_40ffb4
          add ECX,16
          add EDX,512
          cmp EBX,ECX
          jne L_40ffa0
          mov EAX,1
          pop EBX
          ret 
L_410037:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_410040:
          mov EAX,DWORD PTR [ESP+4]
          lea EDX,DWORD PTR [EAX+16384]
          jmp L_410057
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_410050:
          add EAX,1
          cmp EAX,EDX
          je L_410060
L_410057:
          cmp BYTE PTR [EAX],255
          je L_410050
          xor EAX,EAX
          ret 
          .byte 0x90
L_410060:
          mov EAX,1
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_410070:
          mov ECX,DWORD PTR [ESP+8]
          mov EDX,DWORD PTR [ESP+4]
          test ECX,ECX
          je L_41009d
          cmp BYTE PTR [EDX],255
          jne L_4100a3
          lea EAX,DWORD PTR [EDX+1]
          add EDX,ECX
          jmp L_410099
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_410090:
          add EAX,1
          cmp BYTE PTR [EAX-1],255
          jne L_4100a3
L_410099:
          cmp EAX,EDX
          jne L_410090
L_41009d:
          mov EAX,1
          ret 
L_4100a3:
          xor EAX,EAX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_4100b0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,8
          mov EDI,DWORD PTR [ESP+36]
          mov ECX,DWORD PTR [ESP+28]
          mov EBX,DWORD PTR [ESP+32]
          cmp EDI,1
          lea ESI,DWORD PTR [ECX+512]
          sbb EAX,EAX
          mov EDX,EBX
          mov BYTE PTR [ESP+6],BL
          and AL,32
          shr EDX,8
          add EAX,256
          imul EAX,EAX,528
          lea EAX,DWORD PTR [ECX+EAX*1+512]
          mov DWORD PTR [ESP],EAX
          mov EAX,EDX
          and EAX,15
          mov BYTE PTR [ESP+7],AL
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_410100:
          test EDI,EDI
          mov DWORD PTR [ESI],0
          mov DWORD PTR [ESI+4],0
          mov DWORD PTR [ESI+8],0
          mov DWORD PTR [ESI+12],0
          je L_4101d8
          movzx EAX,BYTE PTR [ESI+2]
          mov BYTE PTR [ESI],255
          and EAX,4294967280
          or AL,BYTE PTR [ESP+7]
          mov BYTE PTR [ESI+2],AL
          movzx EAX,BYTE PTR [ESP+6]
          mov BYTE PTR [ESI+1],AL
L_41013c:
          xor EAX,EAX
          lea EBX,DWORD PTR [ESI-512]
          xor ECX,ECX
          xor EDX,EDX
          mov EBP,EAX
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_410150:
          test DL,31
          jne L_410167
          mov EAX,EBX
          cmp EDX,4096
          cmove EAX,ESI
          mov ECX,DWORD PTR [EAX]
          lea EBX,DWORD PTR [EAX+4]
          not ECX
L_410167:
          mov EAX,ECX
          shr ECX,1
          and EAX,1
          xor EAX,EBP
          mov EBP,EAX
          xor EBP,110445913
          test AL,1
          cmovne EAX,EBP
          add EDX,1
          shr EAX,1
          cmp EDX,4198
          mov EBP,EAX
          jne L_410150
          movzx EDX,BYTE PTR [ESI+12]
          not EAX
          add ESI,528
          mov ECX,EAX
          shl ECX,6
          and EDX,63
          add EDX,ECX
          mov BYTE PTR [ESI-516],DL
          mov EDX,EAX
          shr EDX,2
          mov BYTE PTR [ESI-515],DL
          mov EDX,EAX
          shr EAX,18
          shr EDX,10
          mov BYTE PTR [ESI-513],AL
          mov BYTE PTR [ESI-514],DL
          cmp DWORD PTR [ESP],ESI
          jne L_410100
          add ESP,8
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4101d8:
          mov EAX,DWORD PTR [L_479ef4]
          test EAX,EAX
          je L_410200
          movzx EAX,BYTE PTR [ESI+2]
          mov BYTE PTR [ESI+5],255
          and EAX,4294967280
          or AL,BYTE PTR [ESP+7]
          mov BYTE PTR [ESI+2],AL
          movzx EAX,BYTE PTR [ESP+6]
          mov BYTE PTR [ESI+1],AL
          jmp L_41013c
L_410200:
          movzx EAX,BYTE PTR [ESI+1]
          mov BYTE PTR [ESI+5],255
          and EAX,4294967280
          or AL,BYTE PTR [ESP+7]
          mov BYTE PTR [ESI+1],AL
          movzx EAX,BYTE PTR [ESP+6]
          mov BYTE PTR [ESI],AL
          jmp L_41013c
          .byte 0x66
          .byte 0x90
FUN_410220:
          mov EAX,DWORD PTR [L_4cd840]
          mov ECX,EAX
          lea EDX,DWORD PTR [EAX+16384]
          and ECX,16383
          sub EDX,ECX
          test ECX,ECX
          cmovne EAX,EDX
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_410240:
          sub ESP,28
          mov EDX,DWORD PTR [L_479ed8]
          movzx EAX,WORD PTR [ESP+32]
          rol AX,8
          mov WORD PTR [EDX+2],AX
          mov EDX,EAX
          movzx EAX,AH
          shl EDX,8
          mov DWORD PTR [ESP+4],OFFSET L_4517f8
          mov DWORD PTR [ESP],1
          and EDX,65280
          add EAX,EDX
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          add ESP,28
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
FUN_410290:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EDX,DWORD PTR [ESP+32]
          cmp EDX,14336
          ja L_410320
          mov ESI,16384
          mov ECX,EDX
          mov EAX,EDX
          sub ESI,EDX
          shl ECX,8
          shl EAX,24
          mov EDX,ESI
          and ECX,16711680
          mov EDI,DWORD PTR [L_479ed8]
          shl EDX,8
          add ECX,EAX
          and EDX,16711680
          sub EDX,EAX
          mov EAX,ECX
          mov DWORD PTR [EDI+120],ECX
          shr EAX,8
          shr ECX,24
          mov DWORD PTR [EDI+124],EDX
          and EAX,65280
          mov DWORD PTR [ESP+4],OFFSET L_451850
          mov DWORD PTR [ESP],1
          add ECX,EAX
          mov EAX,EDX
          shr EDX,24
          shr EAX,8
          mov DWORD PTR [ESP+12],ECX
          and EAX,65280
          add EDX,EAX
          mov DWORD PTR [ESP+8],EDX
          call _log_printf
          add ESP,16
          mov EAX,ESI
          pop EBX
          pop ESI
          pop EDI
          ret 
L_410317:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_410320:
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],OFFSET L_451820
          xor ESI,ESI
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,16
          mov EAX,ESI
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
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_410350:
          mov EAX,DWORD PTR [L_479ed8]
          mov EAX,DWORD PTR [EAX+124]
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_410360:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EDX,DWORD PTR [L_479ef0]
          mov EAX,DWORD PTR [L_479ed8]
          mov EBX,DWORD PTR [ESP+32]
          test EBX,EBX
          cmove EBX,DWORD PTR [L_4cd840]
          test EDX,EDX
          je L_410400
          add EBX,131071
          and EBX,4294836224
          cmp DWORD PTR [L_479ea8],1
          je L_410410
L_410397:
          mov EDX,EBX
          mov ECX,EBX
          shl EDX,8
          shr ECX,8
          and ECX,65280
          and EDX,16711680
          or EDX,ECX
          mov ECX,EBX
          shr ECX,24
          add EDX,ECX
          mov DWORD PTR [EAX+100],EDX
          mov DWORD PTR [EAX+12],EDX
          mov ECX,EDX
          mov EAX,EDX
          shl ECX,8
          shl EDX,24
          shr EAX,8
          and ECX,16711680
          mov DWORD PTR [ESP+4],OFFSET L_45187c
          and EAX,65280
          mov DWORD PTR [ESP],1
          or ECX,EAX
          add EDX,ECX
          mov DWORD PTR [ESP+8],EDX
          call _log_printf
          add ESP,16
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
L_410400:
          add EBX,16383
          and EBX,4294950912
          jmp L_410397
          .byte 0x66
          .byte 0x90
L_410410:
          mov EDI,DWORD PTR [EAX+112]
          mov ECX,EDI
          mov ESI,EDI
          mov EDX,EDI
          shl ECX,24
          shr ESI,24
          shl EDX,8
          and EDX,16711680
          add ESI,ECX
          shr EDI,8
          lea ECX,DWORD PTR [ESI+EDX*1]
          and EDI,65280
          lea EDX,DWORD PTR [ECX+EDI*1]
          lea ECX,DWORD PTR [EDX+EDX*1]
          test EDX,EDX
          mov EDX,131072
          cmovne EDX,ECX
          add EDX,EBX
          shr EDX,17
          mov BYTE PTR [L_479ece],DL
          jmp L_410397
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_410460:
          mov EAX,DWORD PTR [L_479ed8]
          mov EDX,DWORD PTR [EAX+100]
          mov EAX,EDX
          mov ECX,EDX
          shl EAX,24
          shr ECX,24
          add ECX,EAX
          mov EAX,EDX
          shr EDX,8
          shl EAX,8
          and EDX,65280
          and EAX,16711680
          add EAX,ECX
          add EAX,EDX
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_410490:
          mov EAX,DWORD PTR [L_479ed8]
          push EBX
          mov EBX,DWORD PTR [EAX+112]
          mov EDX,EBX
          mov ECX,EBX
          mov EAX,EBX
          shl EDX,24
          shr ECX,24
          shl EAX,8
          and EAX,16711680
          add ECX,EDX
          shr EBX,8
          lea EDX,DWORD PTR [ECX+EAX*1]
          and EBX,65280
          mov EAX,EDX
          mov EDX,65536
          add EAX,EBX
          cmove EAX,EDX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_4104d0:
          mov EAX,DWORD PTR [L_4cd840]
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_4104e0:
          mov EAX,DWORD PTR [ESP+4]
          mov DWORD PTR [L_4cd840],EAX
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_4104f0:
          mov EAX,DWORD PTR [L_479ef0]
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_410500:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,124
          mov EAX,DWORD PTR [ESP+160]
          mov ESI,DWORD PTR [ESP+156]
          mov EDI,DWORD PTR [ESP+144]
          mov DWORD PTR [ESP+104],EAX
          mov EAX,ESI
          mov BYTE PTR [ESP+24],AL
          mov EAX,DWORD PTR [L_479ee8]
          cmp EAX,EDI
          jb L_410b29
          mov ECX,DWORD PTR [ESP+152]
          add ECX,EDI
          cmp EAX,ECX
          mov DWORD PTR [ESP+108],ECX
          jb L_410b29
          mov EAX,EDI
          mov EDX,0
          and EAX,16383
          mov ECX,EAX
          mov DWORD PTR [ESP+88],EAX
          mov EAX,EDI
          shr EAX,14
          mov DWORD PTR [ESP+96],EAX
          mov EAX,16384
          sub EAX,ECX
          test ECX,ECX
          cmove EAX,EDX
          cmp EAX,DWORD PTR [ESP+152]
          jae L_4105e2
          mov ECX,DWORD PTR [ESP+152]
          sub ECX,EAX
          cmp ECX,16383
          mov EAX,ECX
          jbe L_410a33
          shr ECX,14
          test EAX,16383
          mov DWORD PTR [ESP+100],ECX
          jne L_410a3b
          mov EAX,DWORD PTR [ESP+88]
          test EAX,EAX
          je L_410a9c
          add DWORD PTR [ESP+100],1
          xor EBX,EBX
L_4105b4:
          mov ECX,DWORD PTR [ESP+152]
          mov EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],ECX
          add EAX,EDI
          mov ECX,DWORD PTR [ESP+148]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ECX
          call _memcpy
          test BL,BL
          je L_410628
          jmp L_410a69
L_4105e2:
          mov ECX,DWORD PTR [ESP+152]
          mov EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],ECX
          mov ECX,DWORD PTR [ESP+148]
          add EAX,EDI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ECX
          call _memcpy
          cmp DWORD PTR [ESP+164],1
          jne L_410620
          mov EAX,DWORD PTR [ESP+152]
          test EAX,EAX
          jne L_410a61
L_410620:
          mov DWORD PTR [ESP+100],1
L_410628:
          mov EAX,ESI
          lea ECX,DWORD PTR [ESI-49]
          test AL,AL
          setne DL
          cmp AL,48
          mov BYTE PTR [ESP+82],CL
          setne AL
          mov ECX,DWORD PTR [ESP+152]
          and EDX,EAX
          cmp DWORD PTR [ESP+152],16383
          mov EAX,DWORD PTR [ESP+152]
          mov EBP,EDX
          lea EDX,DWORD PTR [ECX+512]
          mov EBX,ECX
          setbe BYTE PTR [ESP+28]
          shr EAX,9
          shr EDX,9
          lea ECX,DWORD PTR [EAX+1]
          and EBX,511
          cmove EDX,EAX
          test EBX,EBX
          mov EBX,DWORD PTR [ESP+152]
          cmove ECX,EAX
          mov EAX,32
          and EDI,131071
          sub EAX,ECX
          mov DWORD PTR [ESP+92],EDI
          mov BYTE PTR [ESP+71],AL
          lea EAX,DWORD PTR [ESI-42]
          shr EBX,8
          mov DWORD PTR [ESP+32],EBX
          and EAX,4294967293
          mov BYTE PTR [ESP+70],AL
          lea EAX,DWORD PTR [ECX+4]
          mov EBX,EAX
          mov EAX,DWORD PTR [ESP+96]
          and EBX,4294967292
          mov ESI,EAX
          shl ESI,5
          mov DWORD PTR [ESP+72],ESI
          mov ESI,DWORD PTR [ESP+100]
          add ESI,EAX
          mov EAX,EBP
          and AL,BYTE PTR [ESP+28]
          mov DWORD PTR [ESP+76],ESI
          mov ESI,DWORD PTR [ESP+96]
          mov BYTE PTR [ESP+83],AL
          mov EAX,32
          mov DWORD PTR [ESP+64],ESI
          cmovne EAX,EDX
          mov EDX,EDI
          mov DWORD PTR [ESP+84],EAX
          mov EAX,256
          shr EDX,9
          mov EBP,EAX
          sub EBP,EDX
          test EDI,EDI
          mov EDX,EBP
          cmove EDX,EAX
          movzx EAX,BYTE PTR [ESP+24]
          test CL,3
          cmove EBX,ECX
          sub EDX,EBX
          shr EDX,2
          and EAX,63
          mov DWORD PTR [ESP+48],EDX
          mov BYTE PTR [ESP+28],AL
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_410720:
          cmp BYTE PTR [ESP+83],0
          je L_410940
          xor EDX,EDX
          cmp BYTE PTR [ESP+82],14
          ja L_41074f
L_410734:
          mov ESI,DWORD PTR [L_479ef0]
          mov EDX,DWORD PTR [ESP+88]
          test ESI,ESI
          cmovne EDX,DWORD PTR [ESP+92]
          mov EAX,EDX
          shr EAX,9
          test EDX,EDX
          cmovne EDX,EAX
L_41074f:
          mov EAX,DWORD PTR [ESP+84]
          lea EDI,DWORD PTR [EDX+EAX*1]
          cmp EDX,EDI
          jae L_41086e
L_41075e:
          mov EAX,DWORD PTR [ESP+64]
          mov ESI,EAX
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+72]
          shr ESI,8
          and ESI,15
          lea ECX,DWORD PTR [EAX+EDX*1]
          shl ECX,4
          jmp L_4107e1
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_410780:
          movzx EBX,BYTE PTR [EAX+2]
          mov BYTE PTR [EAX],255
          and EBX,4294967280
          or EBX,ESI
          cmp BYTE PTR [ESP+24],1
          mov BYTE PTR [EAX+2],BL
          mov EBX,EBP
          mov BYTE PTR [EAX+1],BL
          jbe L_4107d3
          movzx EBX,BYTE PTR [EAX+12]
          and EBX,4294967232
          or BL,BYTE PTR [ESP+28]
          cmp BYTE PTR [ESP+70],0
          mov BYTE PTR [EAX+12],BL
          je L_410900
          movzx EBX,BYTE PTR [ESP+48]
          mov BYTE PTR [EAX+5],1
          mov BYTE PTR [EAX+9],BL
          movzx EBX,BYTE PTR [ESP+32]
          mov BYTE PTR [EAX+8],BL
          movzx EBX,BYTE PTR [ESP+152]
          mov BYTE PTR [EAX+7],BL
L_4107d3:
          add EDX,1
          add ECX,16
          cmp EDX,EDI
          jae L_41086e
L_4107e1:
          mov EAX,DWORD PTR [L_479ed0]
          add EAX,ECX
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          mov DWORD PTR [EAX+12],0
          mov EBX,DWORD PTR [L_479ef0]
          test EBX,EBX
          jne L_410780
          movzx EBX,BYTE PTR [EAX+1]
          mov BYTE PTR [EAX+5],255
          and EBX,4294967280
          or EBX,ESI
          cmp BYTE PTR [ESP+24],1
          mov BYTE PTR [EAX+1],BL
          mov EBX,EBP
          mov BYTE PTR [EAX],BL
          jbe L_4107d3
          movzx EBX,BYTE PTR [EAX+12]
          mov BYTE PTR [EAX+2],1
          and EBX,4294967232
          or BL,BYTE PTR [ESP+28]
          cmp BYTE PTR [ESP+24],48
          mov BYTE PTR [EAX+12],BL
          movzx EBX,BYTE PTR [ESP+71]
          mov BYTE PTR [EAX+9],BL
          je L_4107d3
          movzx EBX,BYTE PTR [ESP+32]
          add EDX,1
          add ECX,16
          cmp EDX,EDI
          mov BYTE PTR [EAX+8],BL
          movzx EBX,BYTE PTR [ESP+152]
          mov BYTE PTR [EAX+7],BL
          jb L_4107e1
L_41086e:
          add DWORD PTR [ESP+64],1
          add DWORD PTR [ESP+72],32
          mov EAX,DWORD PTR [ESP+64]
          cmp DWORD PTR [ESP+76],EAX
          jne L_410720
          mov EDI,DWORD PTR [ESP+104]
          cmp DI,61937
          je L_4108eb
          mov ECX,DWORD PTR [ESP+96]
          mov EBP,DWORD PTR [L_479efc]
          lea EDX,DWORD PTR [EDI-1]
          mov ESI,EDI
          rol SI,8
          mov EAX,ECX
          sub EAX,EBP
          cmp DX,-3
          jbe L_410957
          mov EBX,DWORD PTR [ESP+100]
          sub ECX,EBP
          add EAX,1
          add ECX,1
          shl ECX,8
          add EBX,EAX
L_4108c3:
          mov EDX,EAX
          shr DX,8
          add EDX,ECX
          add CX,256
          mov WORD PTR [EAX+EAX*1+L_4cb7be],DX
          add EAX,1
          cmp EBX,EAX
          jne L_4108c3
L_4108df:
          cmp WORD PTR [ESP+104],-1
          je L_410a19
L_4108eb:
          mov EAX,DWORD PTR [ESP+108]
          mov DWORD PTR [L_4cd840],EAX
          xor EAX,EAX
L_4108f6:
          add ESP,124
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_410900:
          cmp BYTE PTR [ESP+24],44
          je L_410930
L_410907:
          movzx EBX,BYTE PTR [L_479ecc]
          mov BYTE PTR [EAX+9],BL
          movzx EBX,BYTE PTR [L_479ecd]
          mov BYTE PTR [EAX+8],BL
          movzx EBX,BYTE PTR [L_479ece]
          mov BYTE PTR [EAX+7],BL
          jmp L_4107d3
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_410930:
          mov BYTE PTR [EAX+5],1
          jmp L_410907
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_410940:
          cmp BYTE PTR [ESP+82],14
          jbe L_410734
          mov EDI,32
          xor EDX,EDX
          jmp L_41075e
L_410957:
          lea EDX,DWORD PTR [EAX+EAX*1+L_4cb7c0]
          shr EDX,1
          and EDX,1
          cmp DWORD PTR [ESP+100],6
          ja L_410ac6
          mov EDI,DWORD PTR [ESP+100]
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],SI
          cmp EDI,1
          je L_410b4a
          cmp EDI,2
          mov WORD PTR [EAX+EAX*1+L_4cb7c2],SI
          je L_410b59
          cmp EDI,3
          mov WORD PTR [EAX+EAX*1+L_4cb7c4],SI
          je L_410b68
          cmp EDI,4
          mov WORD PTR [EAX+EAX*1+L_4cb7c6],SI
          je L_410b77
          cmp EDI,5
          mov WORD PTR [EAX+EAX*1+L_4cb7c8],SI
          je L_410b33
          mov EBX,EDI
          mov WORD PTR [EAX+EAX*1+L_4cb7ca],SI
          mov EDI,6
L_4109d6:
          mov ECX,DWORD PTR [ESP+100]
          cmp ECX,EBX
          je L_4108df
          sub ECX,EBX
          lea EDX,DWORD PTR [ECX-2]
          mov DWORD PTR [ESP+32],ECX
          shr EDX,1
          add EDX,1
          mov DWORD PTR [ESP+28],EDX
          add EDX,EDX
          cmp ECX,1
          mov DWORD PTR [ESP+24],EDX
          jne L_410ae8
L_410a03:
          add EAX,EDI
          cmp WORD PTR [ESP+104],-1
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],SI
          jne L_4108eb
L_410a19:
          mov EAX,EBP
          mov EDX,4294967071
          not EAX
          add EAX,DWORD PTR [ESP+76]
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],DX
          jmp L_4108eb
L_410a33:
          mov DWORD PTR [ESP+100],0
L_410a3b:
          add DWORD PTR [ESP+100],1
          cmp DWORD PTR [ESP+164],1
          mov EBP,DWORD PTR [ESP+88]
          sete BL
          test EBP,EBP
          je L_4105b4
          add DWORD PTR [ESP+100],1
          jmp L_4105b4
L_410a61:
          mov DWORD PTR [ESP+100],1
L_410a69:
          mov ECX,DWORD PTR [ESP+108]
          mov EDX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+4],0
          mov EAX,ECX
          add EDX,ECX
          add EAX,16383
          mov DWORD PTR [ESP],EDX
          and EAX,4294950912
          sub EAX,ECX
          mov DWORD PTR [ESP+8],EAX
          call _memset
          jmp L_410628
L_410a9c:
          mov ECX,DWORD PTR [ESP+152]
          mov EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],ECX
          mov ECX,DWORD PTR [ESP+148]
          add EAX,EDI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ECX
          call _memcpy
          jmp L_410628
L_410ac6:
          test EDX,EDX
          jne L_410b42
          mov EDI,DWORD PTR [ESP+100]
          xor EBX,EBX
          lea EDX,DWORD PTR [EDI-2]
          mov DWORD PTR [ESP+32],EDI
          xor EDI,EDI
          shr EDX,1
          lea ECX,DWORD PTR [EDX+1]
          mov DWORD PTR [ESP+28],ECX
          add ECX,ECX
          mov DWORD PTR [ESP+24],ECX
L_410ae8:
          mov EDX,ESI
          movzx ECX,SI
          mov DWORD PTR [ESP+64],EAX
          shl EDX,16
          or ECX,EDX
          lea EDX,DWORD PTR [EAX+EBX*1]
          mov EAX,DWORD PTR [ESP+28]
          lea EBX,DWORD PTR [EDX+EDX*1+L_4cb7c0]
          xor EDX,EDX
L_410b06:
          mov DWORD PTR [EBX+EDX*4],ECX
          add EDX,1
          cmp EDX,EAX
          jb L_410b06
          mov ECX,DWORD PTR [ESP+24]
          mov EAX,DWORD PTR [ESP+64]
          add EDI,ECX
          cmp ECX,DWORD PTR [ESP+32]
          jne L_410a03
          jmp L_4108df
L_410b29:
          mov EAX,4294967295
          jmp L_4108f6
L_410b33:
          mov EBX,5
          mov EDI,5
          jmp L_4109d6
L_410b42:
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],SI
L_410b4a:
          mov EBX,1
          mov EDI,1
          jmp L_4109d6
L_410b59:
          mov EBX,2
          mov EDI,2
          jmp L_4109d6
L_410b68:
          mov EBX,3
          mov EDI,3
          jmp L_4109d6
L_410b77:
          mov EBX,4
          mov EDI,4
          jmp L_4109d6
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_410b90:
          mov EAX,DWORD PTR [L_479ef8]
          mov EDX,DWORD PTR [ESP+8]
          add EDX,DWORD PTR [ESP+4]
          add EAX,262143
          shl EAX,14
          cmp EAX,EDX
          setae AL
          movzx EAX,AL
          ret 
          .byte 0x66
          .byte 0x90
FUN_410bb0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EBX,DWORD PTR [L_4cd840]
          mov EAX,DWORD PTR [ESP+100]
          mov EDX,DWORD PTR [ESP+96]
          mov EDI,DWORD PTR [ESP+104]
          mov ECX,EBX
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [ESP+108]
          and ECX,16383
          mov ESI,EAX
          mov DWORD PTR [ESP+24],EAX
          lea EAX,DWORD PTR [EBX+16384]
          sub EAX,ECX
          test ECX,ECX
          cmovne EBX,EAX
          mov EAX,ESI
          add EAX,EBX
          mov ESI,EAX
          mov DWORD PTR [ESP+52],EAX
          mov EAX,DWORD PTR [L_479ef8]
          add EAX,262143
          shl EAX,14
          cmp EAX,ESI
          jb L_410e90
          mov EAX,EBX
          mov EBP,DWORD PTR [L_46f9c4]
          mov DWORD PTR [ESP+4],EDX
          shr EAX,14
          mov ECX,EAX
          sub AX,WORD PTR [L_479efc]
          sub CX,WORD PTR [L_479efc]
          mov ESI,EBP
          shl ESI,5
          shr CX,8
          shl EAX,8
          add EAX,ECX
          mov ECX,DWORD PTR [ESP+24]
          mov WORD PTR [ESI+L_4c97d6],AX
          mov EAX,ECX
          shr EAX,8
          mov DWORD PTR [ESP+28],EAX
          mov EAX,ECX
          shl ECX,24
          shr EAX,24
          add ECX,EAX
          mov EAX,DWORD PTR [ESP+24]
          shl EAX,8
          and EAX,16711680
          add EAX,ECX
          mov ECX,DWORD PTR [ESP+28]
          and ECX,65280
          add EAX,ECX
          mov DWORD PTR [ESI+L_4c97d8],EAX
          add ESI,OFFSET L_4c97c0
          mov DWORD PTR [ESP],ESI
          call _strcpy
          mov EDX,DWORD PTR [L_479ef0]
          mov EAX,DWORD PTR [EDI]
          test EDX,EDX
          mov DWORD PTR [ESI+28],EAX
          je L_410eb0
          mov EAX,DWORD PTR [L_479ee8]
          cmp DWORD PTR [ESP+52],EAX
          ja L_410ecc
          cmp EBX,EAX
          ja L_410ecc
          mov EAX,EBX
          mov EDX,EBX
          mov EDI,DWORD PTR [ESP+24]
          shr EAX,14
          and EDX,16383
          mov ECX,0
          mov DWORD PTR [ESP+60],EAX
          mov EAX,16384
          sub EAX,EDX
          test EDX,EDX
          cmove EAX,ECX
          cmp EDI,EAX
          ja L_410edd
          add EBX,DWORD PTR [L_479ed8]
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EBX
          call _memcpy
          test EDI,EDI
          mov DWORD PTR [ESP+56],1
          jne L_410f3d
L_410d06:
          mov EDI,DWORD PTR [ESP+24]
          mov ESI,DWORD PTR [ESP+60]
          mov EBP,32
          lea EDX,DWORD PTR [EDI+512]
          mov EAX,EDI
          mov ECX,EDI
          shr EAX,9
          shr EDX,9
          and ECX,511
          cmove EDX,EAX
          test ECX,ECX
          mov EBX,EDX
          mov DWORD PTR [ESP+48],EDX
          lea EDX,DWORD PTR [EAX+1]
          cmovne EAX,EDX
          mov EDX,32
          sub EDX,EAX
          mov EAX,ESI
          shl EAX,9
          mov BYTE PTR [ESP+32],DL
          mov DWORD PTR [ESP+40],EAX
          mov EAX,ESI
          add ESI,DWORD PTR [ESP+56]
          cmp EDI,16383
          mov DWORD PTR [ESP+36],EAX
          cmovbe EBP,EBX
          mov DWORD PTR [ESP+44],ESI
L_410d65:
          cmp DWORD PTR [ESP+24],16383
          ja L_410d7b
          mov ESI,DWORD PTR [ESP+48]
          test ESI,ESI
          je L_410e09
L_410d7b:
          mov EAX,DWORD PTR [ESP+36]
          mov ECX,DWORD PTR [ESP+40]
          xor EDX,EDX
          mov ESI,EAX
          mov EDI,EAX
          shr ESI,8
          and ESI,15
          nop
L_410d90:
          mov EAX,DWORD PTR [L_479ed0]
          add EAX,ECX
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          mov DWORD PTR [EAX+12],0
          mov EBX,DWORD PTR [L_479ef0]
          test EBX,EBX
          je L_410f70
          movzx EBX,BYTE PTR [EAX+2]
          mov BYTE PTR [EAX],255
          add EDX,1
          add ECX,16
          and EBX,4294967280
          or EBX,ESI
          mov BYTE PTR [EAX+2],BL
          mov EBX,EDI
          mov BYTE PTR [EAX+1],BL
          movzx EBX,BYTE PTR [EAX+12]
          and EBX,4294967232
          or EBX,42
          cmp EBP,EDX
          mov BYTE PTR [EAX+12],BL
          movzx EBX,BYTE PTR [L_479ecc]
          mov BYTE PTR [EAX+9],BL
          movzx EBX,BYTE PTR [L_479ecd]
          mov BYTE PTR [EAX+8],BL
          movzx EBX,BYTE PTR [L_479ece]
          mov BYTE PTR [EAX+7],BL
          ja L_410d90
L_410e09:
          add DWORD PTR [ESP+36],1
          add DWORD PTR [ESP+40],512
          mov EAX,DWORD PTR [ESP+36]
          cmp DWORD PTR [ESP+44],EAX
          jne L_410d65
          mov EDI,DWORD PTR [ESP+60]
          mov ECX,DWORD PTR [L_479efc]
          mov ESI,DWORD PTR [ESP+56]
          mov EAX,EDI
          mov EBX,EDI
          sub EAX,ECX
          sub EBX,ECX
          add EAX,1
          add EBX,1
          shl EBX,8
          add ESI,EAX
L_410e45:
          mov EDX,EAX
          shr DX,8
          add EDX,EBX
          add BX,256
          mov WORD PTR [EAX+EAX*1+L_4cb7be],DX
          add EAX,1
          cmp ESI,EAX
          jne L_410e45
L_410e61:
          mov EAX,DWORD PTR [ESP+44]
          not ECX
          mov EBP,DWORD PTR [L_46f9c4]
          add EAX,ECX
          mov ECX,4294967071
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],CX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [L_4cd840],EAX
          jmp L_410ecc
L_410e87:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_410e90:
          mov DWORD PTR [ESP+104],EDX
          mov DWORD PTR [ESP+100],OFFSET L_4518a0
          mov DWORD PTR [ESP+96],0
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _log_printf
L_410eb0:
          mov ECX,DWORD PTR [ESP+24]
          mov EDX,DWORD PTR [ESP+32]
          mov EAX,EBX
          mov DWORD PTR [ESP],65535
          call FUN_40eef0
          mov EBP,DWORD PTR [L_46f9c4]
L_410ecc:
          add EBP,1
          mov DWORD PTR [L_46f9c4],EBP
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_410edd:
          sub EDI,EAX
          mov ECX,EDI
          mov EAX,EDI
          and ECX,16383
          cmp EDI,16384
          mov ESI,ECX
          cmovb ESI,EDI
          shr EAX,14
          test ESI,ESI
          mov DWORD PTR [ESP+56],EAX
          je L_410fc0
          add EAX,1
          test EDX,EDX
          mov DWORD PTR [ESP+56],EAX
          je L_411005
L_410f12:
          mov EAX,DWORD PTR [ESP+24]
          add EBX,DWORD PTR [L_479ed8]
          add DWORD PTR [ESP+56],1
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          test ESI,ESI
          je L_410d06
L_410f3d:
          mov EDI,DWORD PTR [ESP+52]
          mov EDX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+4],0
          mov EAX,EDI
          add EDX,EDI
          add EAX,16383
          mov DWORD PTR [ESP],EDX
          and EAX,4294950912
          sub EAX,EDI
          mov DWORD PTR [ESP+8],EAX
          call _memset
          jmp L_410d06
L_410f70:
          movzx EBX,BYTE PTR [EAX+1]
          add EDX,1
          add ECX,16
          mov BYTE PTR [EAX+5],255
          mov BYTE PTR [EAX+2],1
          and EBX,4294967280
          or EBX,ESI
          mov BYTE PTR [EAX+1],BL
          mov EBX,EDI
          mov BYTE PTR [EAX],BL
          movzx EBX,BYTE PTR [EAX+12]
          and EBX,4294967232
          or EBX,42
          cmp EDX,EBP
          mov BYTE PTR [EAX+12],BL
          movzx EBX,BYTE PTR [ESP+32]
          mov BYTE PTR [EAX+9],BL
          movzx EBX,BYTE PTR [ESP+28]
          mov BYTE PTR [EAX+8],BL
          movzx EBX,BYTE PTR [ESP+24]
          mov BYTE PTR [EAX+7],BL
          jb L_410d90
          jmp L_410e09
L_410fc0:
          test EDX,EDX
          jne L_410f12
          mov EAX,DWORD PTR [ESP+24]
          add EBX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+56]
          test EAX,EAX
          jne L_410d06
          mov EAX,DWORD PTR [ESP+60]
          mov ECX,DWORD PTR [L_479efc]
          mov DWORD PTR [ESP+44],EAX
          jmp L_410e61
L_411005:
          mov EAX,DWORD PTR [ESP+24]
          add EBX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          jmp L_410f3d
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_411030:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EAX,DWORD PTR [L_4cd840]
          mov EBX,DWORD PTR [ESP+76]
          mov ESI,DWORD PTR [ESP+64]
          mov EDI,DWORD PTR [ESP+68]
          mov EBP,DWORD PTR [ESP+72]
          mov ECX,EAX
          lea EDX,DWORD PTR [EAX+16384]
          mov DWORD PTR [ESP+4],OFFSET L_4518e8
          and ECX,16383
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP+8],ESI
          sub EDX,ECX
          test ECX,ECX
          mov DWORD PTR [ESP],1
          cmovne EAX,EDX
          lea EDX,DWORD PTR [EBX+EAX*1]
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+20],EDX
          call _log_printf
          mov DWORD PTR [ESP+76],EBX
          mov DWORD PTR [ESP+72],EBP
          mov DWORD PTR [ESP+68],EDI
          mov DWORD PTR [ESP+64],ESI
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp FUN_410bb0
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
FUN_4110b0:
          push EDI
          push ESI
          push EBX
          sub ESP,32
          mov EDX,DWORD PTR [L_479ef0]
          mov EBX,DWORD PTR [ESP+52]
          mov EAX,DWORD PTR [ESP+56]
          test EDX,EDX
          je L_4111b3
          mov EDX,DWORD PTR [L_46f9c0]
          test EDX,EDX
          jne L_411280
          mov EDX,DWORD PTR [L_4cd840]
          mov ESI,EDX
          lea ECX,DWORD PTR [EDX+16384]
          and ESI,16383
          sub ECX,ESI
          test ESI,ESI
          cmovne EDX,ECX
          test EDX,131071
          je L_411109
          add EDX,131072
          and EDX,4294836224
L_411109:
          lea ESI,DWORD PTR [EBX+EDX*1]
          mov DWORD PTR [L_46f9c0],EDX
L_411112:
          mov EDI,DWORD PTR [L_479ef8]
          lea ECX,DWORD PTR [EDI+262143]
          shl ECX,14
          cmp ECX,ESI
          jb L_4111ea
          movzx EDI,AL
          mov DWORD PTR [ESP+24],ESI
          mov DWORD PTR [ESP+20],EBX
          lea EAX,DWORD PTR [EDI+17]
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+4],OFFSET L_451978
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],8190
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_46f9c0]
          mov DWORD PTR [ESP],EAX
          call FUN_410500
          mov EAX,DWORD PTR [L_46f9c0]
          add EBX,EAX
          mov EDI,EAX
          lea EAX,DWORD PTR [EBX+2048]
          shr EDI,17
          and EAX,4294965248
          test EBX,2047
          cmovne EBX,EAX
          mov EAX,EDI
          mov DWORD PTR [L_46f9c0],EBX
          add ESP,32
          pop EBX
          pop ESI
          pop EDI
          ret 
L_4111b3:
          mov EDX,DWORD PTR [L_4cd840]
          mov ESI,EDX
          lea ECX,DWORD PTR [EDX+16384]
          and ESI,16383
          sub ECX,ESI
          test ESI,ESI
          mov ESI,DWORD PTR [L_479ef8]
          cmovne EDX,ECX
          lea EDI,DWORD PTR [EBX+EDX*1]
          mov DWORD PTR [L_46f9c0],EDX
          lea ECX,DWORD PTR [ESI+262143]
          shl ECX,14
          cmp ECX,EDI
          jae L_411213
L_4111ea:
          movzx EAX,AL
          mov DWORD PTR [ESP+4],OFFSET L_451924
          mov DWORD PTR [ESP],0
          add EAX,17
          xor EDI,EDI
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          add ESP,32
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          ret 
L_411213:
          movzx ESI,AL
          mov DWORD PTR [ESP+24],EDI
          mov DWORD PTR [ESP+20],EBX
          lea EAX,DWORD PTR [ESI+17]
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+4],OFFSET L_451978
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [L_46f9c0]
          mov DWORD PTR [ESP+8],EBX
          mov EBX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],8190
          mov EDI,EAX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EBX
          shr EDI,14
          call FUN_410500
          add ESP,32
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_411280:
          mov ECX,EDX
          lea ESI,DWORD PTR [EDX+EBX*1]
          and ECX,4294836224
          add ECX,131072
          cmp ECX,ESI
          jae L_411112
          add EDX,131072
          and EDX,4294836224
          jmp L_411109
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_4112b0:
          push EBX
          mov EDX,DWORD PTR [ESP+8]
          shr EDX,14
          test EDX,EDX
          je L_4112eb
          mov ECX,DWORD PTR [L_479efc]
          mov EAX,OFFSET L_4cb7c0
          lea EBX,DWORD PTR [ECX+ECX*1]
          sub EDX,ECX
          lea EDX,DWORD PTR [EDX+EDX*1+L_4cb7c0]
          sub EAX,EBX
L_4112d5:
          cmp WORD PTR [EAX],64287
          je L_4112e4
          mov ECX,4294966047
          mov WORD PTR [EAX],CX
L_4112e4:
          add EAX,2
          cmp EAX,EDX
          jne L_4112d5
L_4112eb:
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
FUN_4112f0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,8
          mov ECX,DWORD PTR [L_479ef8]
          mov EAX,DWORD PTR [ESP+28]
          shr EAX,14
          cmp EAX,ECX
          jae L_41141b
          mov EDI,DWORD PTR [L_479efc]
          mov EBP,EAX
          mov ESI,ECX
          sub ESI,EAX
          sub EBP,EDI
          lea EDX,DWORD PTR [EBP+EBP*1+L_4cb7c0]
          mov EBX,EBP
          mov DWORD PTR [ESP],EBP
          shr EDX,1
          and EDX,1
          cmp ESI,6
          ja L_4115a5
          mov EDX,ESI
L_411336:
          mov EBP,4294966815
          cmp EDX,1
          mov WORD PTR [EBX+EBX*1+L_4cb7c0],BP
          lea EBX,DWORD PTR [EAX+1]
          je L_411560
          sub EBX,EDI
          mov EBP,4294966815
          cmp EDX,2
          mov WORD PTR [EBX+EBX*1+L_4cb7c0],BP
          lea EBX,DWORD PTR [EAX+2]
          je L_411560
          sub EBX,EDI
          mov EBP,4294966815
          cmp EDX,3
          mov WORD PTR [EBX+EBX*1+L_4cb7c0],BP
          lea EBX,DWORD PTR [EAX+3]
          je L_411560
          sub EBX,EDI
          mov EBP,4294966815
          cmp EDX,4
          mov WORD PTR [EBX+EBX*1+L_4cb7c0],BP
          lea EBX,DWORD PTR [EAX+4]
          je L_411560
          sub EBX,EDI
          mov EBP,4294966815
          cmp EDX,6
          mov WORD PTR [EBX+EBX*1+L_4cb7c0],BP
          lea EBX,DWORD PTR [EAX+5]
          jne L_411560
          sub EBX,EDI
          mov EBP,4294966815
          add EAX,6
          mov WORD PTR [EBX+EBX*1+L_4cb7c0],BP
L_4113cd:
          cmp ESI,EDX
          je L_41141b
L_4113d1:
          sub ESI,EDX
          lea EBX,DWORD PTR [ESI-2]
          shr EBX,1
          add EBX,1
          cmp ESI,1
          lea EBP,DWORD PTR [EBX+EBX*1]
          mov DWORD PTR [ESP+4],EBP
          je L_41140c
          add EDX,DWORD PTR [ESP]
          lea EBP,DWORD PTR [EDX+EDX*1+L_4cb7c0]
          xor EDX,EDX
L_4113f3:
          mov DWORD PTR [EBP+EDX*4],4263509535
          add EDX,1
          cmp EBX,EDX
          ja L_4113f3
          mov EBX,DWORD PTR [ESP+4]
          add EAX,EBX
          cmp ESI,EBX
          je L_41141b
L_41140c:
          sub EAX,EDI
          mov EDX,4294966815
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],DX
L_41141b:
          mov EAX,DWORD PTR [L_479ef0]
          test EAX,EAX
          jne L_411570
          mov EAX,DWORD PTR [L_479ea4]
          mov ESI,DWORD PTR [L_479ea8]
          and EAX,268435456
          cmp EAX,1
          sbb EBX,EBX
          and EBX,4294967294
          add EBX,6
          cmp ESI,5
          ja L_411595
L_41144c:
          lea EDX,DWORD PTR [ECX+ECX*1+L_4cb7c0]
          test EBX,EBX
          mov EAX,1
          cmovne EAX,EBX
          shr EDX,1
          and EDX,1
          cmp EAX,6
          ja L_4115b2
          mov EDX,EAX
L_41146d:
          mov EBP,4294966047
          cmp EDX,1
          mov WORD PTR [ECX+ECX*1+L_4cb7c0],BP
          je L_4115e9
          mov EDI,4294966047
          cmp EDX,2
          mov WORD PTR [ECX+ECX*1+L_4cb7c2],DI
          je L_4115df
          mov EBP,4294966047
          cmp EDX,3
          mov WORD PTR [ECX+ECX*1+L_4cb7c4],BP
          je L_4115d5
          mov EDI,4294966047
          cmp EDX,4
          mov WORD PTR [ECX+ECX*1+L_4cb7c6],DI
          je L_4115cb
          mov EBP,4294966047
          cmp EDX,6
          mov WORD PTR [ECX+ECX*1+L_4cb7c8],BP
          jne L_4115c1
          mov EDI,4294966047
          mov WORD PTR [ECX+ECX*1+L_4cb7ca],DI
          mov EDI,6
L_4114ed:
          cmp EAX,EDX
          .byte 0x0f,0x84; .long L_411576-.-4   # je L_411576
L_4114f5:
          sub EAX,EDX
          mov DWORD PTR [ESP],EAX
          sub EAX,2
          shr EAX,1
          add EAX,1
          test EBX,EBX
          lea EBP,DWORD PTR [EAX+EAX*1]
          mov DWORD PTR [ESP+4],EBP
          lea EBP,DWORD PTR [EBX-1]
          mov EBX,0
          cmove EBP,EBX
          cmp EBP,EDX
          je L_41153e
          add EDX,ECX
          lea EBX,DWORD PTR [EDX+EDX*1+L_4cb7c0]
          xor EDX,EDX
L_411525:
          mov DWORD PTR [EBX+EDX*4],4213177119
          add EDX,1
          cmp EAX,EDX
          ja L_411525
          mov EAX,DWORD PTR [ESP+4]
          add EDI,EAX
          cmp DWORD PTR [ESP],EAX
          je L_411576
L_41153e:
          add ECX,EDI
          mov EAX,4294966047
          cmp ESI,2
          mov WORD PTR [ECX+ECX*1+L_4cb7c0],AX
          je L_41157b
L_411552:
          add ESP,8
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
L_411560:
          mov EAX,EBX
          jmp L_4113cd
L_411567:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_411570:
          mov ESI,DWORD PTR [L_479ea8]
L_411576:
          cmp ESI,2
          jne L_411552
L_41157b:
          mov EAX,DWORD PTR [L_479ed0]
          mov BYTE PTR [EAX+26],3
          mov EAX,DWORD PTR [L_479ed0]
          mov BYTE PTR [EAX+27],80
          add ESP,8
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_411595:
          mov EBX,DWORD PTR [L_479ee4]
          sub EBX,ECX
          jne L_41144c
          jmp L_411552
L_4115a5:
          test EDX,EDX
          je L_4113d1
          jmp L_411336
L_4115b2:
          test EDX,EDX
          jne L_41146d
          xor EDI,EDI
          jmp L_4114f5
L_4115c1:
          mov EDI,5
          jmp L_4114ed
L_4115cb:
          mov EDI,4
          jmp L_4114ed
L_4115d5:
          mov EDI,3
          jmp L_4114ed
L_4115df:
          mov EDI,2
          jmp L_4114ed
L_4115e9:
          mov EDI,1
          jmp L_4114ed
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
FUN_411600:
          push EDI
          mov EDX,OFFSET L_46f9e0
          push ESI
          mov EAX,4294967295
          mov EDI,EDX
          mov ECX,1024
          sub ESP,20
          rep stosd DWORD PTR ES:[EDI]
          mov EAX,DWORD PTR [ESP+36]
          mov ESI,DWORD PTR [ESP+32]
          mov EDI,EDX
          mov ECX,256
          rep movsd 
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [L_479eec]
          mov DWORD PTR [ESP+4],OFFSET L_4519c4
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [L_479ef0]
          mov ECX,61937
          test EAX,EAX
          jne L_41165d
          mov ECX,8187
L_41165d:
          mov EAX,DWORD PTR [L_479eec]
          add ESP,20
          mov EDX,OFFSET L_46f9e0
          pop ESI
          pop EDI
          jmp L_40ecc0
L_411671:
          jmp FUN_411680
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
FUN_411680:
          push EDI
          push ESI
          sub ESP,20
          mov EDI,DWORD PTR [L_479ef0]
          test EDI,EDI
          je L_411780
          cmp DWORD PTR [L_479ee8],127
          jbe L_41173c
          mov ECX,DWORD PTR [L_479ed8]
          mov EAX,DWORD PTR [L_4cd7c0]
          mov ESI,OFFSET L_4cd7c0
          mov DWORD PTR [ECX],EAX
          lea EDI,DWORD PTR [ECX+4]
          mov EAX,DWORD PTR [L_4cd83c]
          and EDI,4294967292
          mov DWORD PTR [ECX+124],EAX
          sub ECX,EDI
          sub ESI,ECX
          sub ECX,-128
          shr ECX,2
          rep movsd 
          mov DWORD PTR [ESP+8],16256
          mov DWORD PTR [ESP+4],0
          mov EAX,DWORD PTR [L_479ed8]
          sub EAX,-128
          mov DWORD PTR [ESP],EAX
          call _memset
          xor EDX,EDX
          .byte 0x66   # nop
          nop
L_4116f0:
          mov EAX,DWORD PTR [L_479ed0]
          add EAX,EDX
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          mov DWORD PTR [EAX+12],0
          mov ESI,DWORD PTR [L_479ef0]
          test ESI,ESI
          je L_411760
          add EDX,16
          and BYTE PTR [EAX+2],240
          mov BYTE PTR [EAX],255
          cmp EDX,512
          mov BYTE PTR [EAX+1],0
          jne L_4116f0
L_411732:
          mov DWORD PTR [L_4cd840],128
L_41173c:
          mov ECX,DWORD PTR [L_47a104]
          test ECX,ECX
          je L_411750
          mov EDX,DWORD PTR [L_47a108]
          test EDX,EDX
          jne L_411796
L_411750:
          add ESP,20
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_411760:
          add EDX,16
          and BYTE PTR [EAX+1],240
          mov BYTE PTR [EAX+5],255
          cmp EDX,512
          mov BYTE PTR [EAX],0
          jne L_4116f0
          jmp L_411732
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_411780:
          mov ECX,8187
          mov EDX,128
          mov EAX,OFFSET L_4cd7c0
          call FUN_40e950
          jmp L_41173c
L_411796:
          mov DWORD PTR [ESP+4],OFFSET L_4519f4
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_479ef0]
          test EAX,EAX
          jne L_4117d6
          mov ECX,DWORD PTR [L_47a108]
          mov EDX,DWORD PTR [L_47a104]
          mov EAX,128
          mov DWORD PTR [ESP],8187
          call FUN_40eef0
          add ESP,20
          pop ESI
          pop EDI
          ret 
L_4117d6:
          mov ECX,DWORD PTR [L_47a108]
          mov EDX,DWORD PTR [L_47a104]
          mov EAX,128
          mov DWORD PTR [ESP],61937
          call FUN_40eef0
          add ESP,20
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
FUN_411800:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EDI,DWORD PTR [L_47a080]
          mov EAX,DWORD PTR [EDI+108]
          mov EBP,DWORD PTR [EDI+96]
          mov ECX,EAX
          mov EDX,EAX
          mov ESI,EBP
          shr EDX,24
          shl ECX,24
          shl ESI,24
          lea ECX,DWORD PTR [ECX+EDX*1+15]
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          mov EBX,EBP
          add ECX,ESI
          mov ESI,EBP
          and EDX,16711680
          shr ESI,24
          shl EBX,8
          add ESI,ECX
          and EBX,16711680
          lea ECX,DWORD PTR [ESI+EDX*1]
          lea EDX,DWORD PTR [ECX+EAX*1]
          lea EAX,DWORD PTR [EDX+EBX*1]
          mov EBX,EBP
          shr EBX,8
          and EBX,65280
          add EBX,EAX
          and EBX,4294967280
          add EDI,EBX
          mov EAX,DWORD PTR [EDI+12]
          movzx EBP,WORD PTR [EDI]
          movzx EDX,WORD PTR [EDI+2]
          mov DWORD PTR [ESP+20],EBX
          mov DWORD PTR [ESP+4],OFFSET L_451a20
          mov DWORD PTR [ESP],1
          mov ESI,EAX
          mov ECX,EAX
          shl ESI,24
          shr ECX,24
          rol BP,8
          add ECX,ESI
          mov ESI,EAX
          shr EAX,8
          shl ESI,8
          and EAX,65280
          rol DX,8
          and ESI,16711680
          movzx EDX,DX
          add ECX,ESI
          mov DWORD PTR [ESP+16],EDX
          lea ESI,DWORD PTR [ECX+EAX*1]
          mov EAX,EBP
          movzx EAX,AL
          mov DWORD PTR [ESP+12],EAX
          mov EAX,EBP
          mov DWORD PTR [ESP+24],ESI
          movzx EAX,AH
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,EBP
          and AX,17407
          cmp AX,17218
          jne L_411b13
          lea EBX,DWORD PTR [EBX+ESI*1+15]
          and EBX,4294967280
          test BYTE PTR [EDI+6],8
          jne L_411b22
          test BP,4096
          jne L_411a90
L_4118ff:
          mov EAX,DWORD PTR [L_47a080]
          add EAX,EBX
          movzx EDI,WORD PTR [EAX]
          movzx EDX,WORD PTR [EAX+2]
          mov EAX,DWORD PTR [EAX+12]
          mov DWORD PTR [ESP+20],EBX
          mov DWORD PTR [ESP+4],OFFSET L_451a94
          mov DWORD PTR [ESP],1
          mov ESI,EAX
          mov ECX,EAX
          rol DI,8
          shl ESI,24
          shr ECX,24
          add ECX,ESI
          mov ESI,EAX
          shr EAX,8
          shl ESI,8
          and EAX,65280
          and ESI,16711680
          add ESI,ECX
          add ESI,EAX
          mov EAX,EDX
          rol AX,8
          mov DWORD PTR [ESP+24],ESI
          movzx EAX,AX
          mov DWORD PTR [ESP+16],EAX
          mov EAX,EDI
          movzx EAX,AL
          mov DWORD PTR [ESP+12],EAX
          mov EAX,EDI
          and DI,17407
          movzx EAX,AH
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          cmp DI,17220
          jne L_411b13
          lea ESI,DWORD PTR [EBX+ESI*1+15]
          mov EDI,DWORD PTR [L_47a080]
          and ESI,4294967280
          add EDI,ESI
          mov EAX,DWORD PTR [EDI+12]
          movzx EBX,WORD PTR [EDI]
          movzx ECX,WORD PTR [EDI+2]
          mov DWORD PTR [ESP+20],ESI
          mov DWORD PTR [ESP+4],OFFSET L_451ab8
          mov DWORD PTR [ESP],1
          mov EBP,EAX
          mov EDX,EAX
          shr EDX,24
          shl EBP,24
          rol BX,8
          add EBP,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          rol CX,8
          and EDX,16711680
          movzx ECX,CX
          add EDX,EBP
          mov DWORD PTR [ESP+16],ECX
          add EAX,EDX
          mov DWORD PTR [ESP+24],EAX
          movzx EAX,BL
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BH
          and BX,17407
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          cmp BX,17221
          jne L_411b13
          mov EBX,DWORD PTR [EDI+12]
          mov DWORD PTR [ESP+4],OFFSET L_451adc
          mov DWORD PTR [ESP],1
          mov EAX,EBX
          mov ECX,EBX
          shl EAX,24
          shr ECX,24
          lea EDX,DWORD PTR [ESI+EAX*1+15]
          mov EAX,EBX
          shl EAX,8
          add ECX,EDX
          and EAX,16711680
          lea EDX,DWORD PTR [ECX+EAX*1]
          mov EAX,EBX
          xor EBX,EBX
          shr EAX,8
          and EAX,65280
          add EAX,EDX
          and EAX,4294967280
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [L_47a084],EAX
          call _log_printf
          mov EDX,DWORD PTR [ESP+64]
          test EDX,EDX
          je L_411a7f
          mov EAX,DWORD PTR [L_479ef0]
          test EAX,EAX
          jne L_411bb1
          mov EDX,DWORD PTR [L_47a084]
          mov EAX,DWORD PTR [L_47a080]
          mov ECX,8187
          call FUN_40e950
L_411a7f:
          add ESP,44
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
L_411a90:
          mov EAX,DWORD PTR [L_47a080]
          add EAX,EBX
          movzx EDI,WORD PTR [EAX]
          movzx EDX,WORD PTR [EAX+2]
          mov EAX,DWORD PTR [EAX+12]
          mov DWORD PTR [ESP+20],EBX
          mov DWORD PTR [ESP+4],OFFSET L_451a6c
          mov DWORD PTR [ESP],1
          mov ESI,EAX
          mov ECX,EAX
          rol DI,8
          shl ESI,24
          shr ECX,24
          add ECX,ESI
          mov ESI,EAX
          shr EAX,8
          shl ESI,8
          and EAX,65280
          and ESI,16711680
          add ESI,ECX
          add ESI,EAX
          mov EAX,EDX
          rol AX,8
          mov DWORD PTR [ESP+24],ESI
          movzx EAX,AX
          mov DWORD PTR [ESP+16],EAX
          mov EAX,EDI
          movzx EAX,AL
          mov DWORD PTR [ESP+12],EAX
          mov EAX,EDI
          and DI,17407
          movzx EAX,AH
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          cmp DI,17219
          je L_411ba5
L_411b13:
          add ESP,44
          mov EBX,4294967295
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_411b22:
          mov EAX,DWORD PTR [L_47a080]
          add EAX,EBX
          movzx EDI,WORD PTR [EAX]
          movzx EDX,WORD PTR [EAX+2]
          mov EAX,DWORD PTR [EAX+12]
          mov DWORD PTR [ESP+20],EBX
          mov DWORD PTR [ESP+4],OFFSET L_451a44
          mov DWORD PTR [ESP],1
          mov ESI,EAX
          mov ECX,EAX
          rol DI,8
          shl ESI,24
          shr ECX,24
          add ECX,ESI
          mov ESI,EAX
          shr EAX,8
          shl ESI,8
          and EAX,65280
          and ESI,16711680
          add ESI,ECX
          add ESI,EAX
          mov EAX,EDX
          rol AX,8
          mov DWORD PTR [ESP+24],ESI
          movzx EAX,AX
          mov DWORD PTR [ESP+16],EAX
          mov EAX,EDI
          movzx EAX,AL
          mov DWORD PTR [ESP+12],EAX
          mov EAX,EDI
          and DI,17407
          movzx EAX,AH
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          cmp DI,17218
          jne L_411b13
L_411ba5:
          lea EBX,DWORD PTR [EBX+ESI*1+15]
          and EBX,4294967280
          jmp L_4118ff
L_411bb1:
          mov EDX,DWORD PTR [L_47a084]
          mov EAX,DWORD PTR [L_47a080]
          mov ECX,61937
          call FUN_40e950
          add ESP,44
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
FUN_411bd0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EDI,DWORD PTR [L_479ef0]
          mov EAX,DWORD PTR [ESP+96]
          mov ESI,EAX
          mov DWORD PTR [ESP+28],EAX
          shr ESI,14
          test EDI,EDI
          mov DWORD PTR [ESP+48],ESI
          je L_411bfd
          test EAX,131071
          jne L_411eef
L_411bfd:
          mov EAX,DWORD PTR [ESP+48]
          sub EAX,DWORD PTR [L_479efc]
          mov ESI,4294966559
          mov DWORD PTR [ESP],16384
          mov EBX,OFFSET L_4cb7c0
          mov EBP,OFFSET L_4c97c0
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],SI
          call _malloc
          mov DWORD PTR [ESP+52],EAX
          .byte 0x66   # nop
          nop
L_411c30:
          mov ESI,EBX
          lea EDX,DWORD PTR [EAX+512]
          add EBX,512
          mov EDI,EAX
          mov ECX,128
          add EAX,1024
          rep movsd 
          mov ESI,EBP
          add EBP,512
          cmp EBX,OFFSET L_4cd7c0
          mov ECX,128
          mov EDI,EDX
          rep movsd 
          jne L_411c30
          mov ESI,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],OFFSET L_451b04
          mov DWORD PTR [ESP],1
          mov EAX,ESI
          mov DWORD PTR [ESP+8],ESI
          add EAX,16384
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+56],EAX
          call _log_printf
          mov EBX,DWORD PTR [L_479ef0]
          mov EAX,DWORD PTR [L_479ee8]
          mov ESI,DWORD PTR [ESP+28]
          test EBX,EBX
          jne L_411f60
          cmp ESI,EAX
          ja L_411e03
          cmp DWORD PTR [ESP+56],EAX
          ja L_411e03
          mov EAX,ESI
          mov EDX,ESI
          and EAX,16383
          shr EDX,14
          test EAX,EAX
          mov DWORD PTR [ESP+60],EDX
          mov EAX,ESI
          je L_4120e0
          add EAX,DWORD PTR [L_479ed8]
          mov ESI,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+8],16384
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov DWORD PTR [ESP+40],2
L_411cf9:
          mov EAX,DWORD PTR [ESP+28]
          mov ESI,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+32],0
          and EAX,131071
          mov EDX,EAX
          mov DWORD PTR [ESP+44],EAX
          mov EAX,224
          shr EDX,9
          sub EAX,EDX
          mov EDX,ESI
          shr EAX,2
          shl EDX,9
          mov DWORD PTR [ESP+36],EAX
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_411d30:
          mov EAX,DWORD PTR [ESP+44]
          mov EBP,ESI
          mov EBX,ESI
          shr EBP,8
          lea ECX,DWORD PTR [EDX+512]
          mov BYTE PTR [ESP+28],BL
          and EBP,15
          test EAX,EAX
          jne L_411e7b
L_411d50:
          mov EAX,DWORD PTR [L_479ed0]
          add EAX,EDX
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          mov DWORD PTR [EAX+12],0
          mov EDI,DWORD PTR [L_479ef0]
          test EDI,EDI
          jne L_411f10
          movzx EDI,BYTE PTR [EAX+1]
          add EDX,16
          mov BYTE PTR [EAX+5],255
          mov BYTE PTR [EAX+9],0
          mov BYTE PTR [EAX+2],1
          and EDI,4294967280
          or EDI,EBP
          mov EBX,EDI
          movzx EDI,BYTE PTR [EAX+12]
          mov BYTE PTR [EAX+1],BL
          movzx EBX,BYTE PTR [ESP+28]
          and EDI,4294967232
          or EDI,48
          mov BYTE PTR [EAX],BL
          cmp EDX,ECX
          mov EBX,EDI
          mov BYTE PTR [EAX+12],BL
          jne L_411d50
L_411db7:
          add DWORD PTR [ESP+32],1
          add ESI,1
          mov EDX,ECX
          mov EAX,DWORD PTR [ESP+32]
          cmp DWORD PTR [ESP+40],EAX
          ja L_411d30
          mov EAX,DWORD PTR [ESP+60]
          sub EAX,DWORD PTR [L_479efc]
          mov ECX,4294966559
          cmp DWORD PTR [ESP+40],2
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],CX
          jne L_411dfa
          mov EDX,4294966559
          mov WORD PTR [EAX+EAX*1+L_4cb7c2],DX
L_411dfa:
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [L_4cd840],EAX
L_411e03:
          movzx EAX,WORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],OFFSET L_4c9180
          mov DWORD PTR [ESP],EAX
          call _setBeU16
          mov DWORD PTR [ESP+4],OFFSET L_4c9182
          mov DWORD PTR [ESP],0
          call _setBeU16
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+96],EAX
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _free
L_411e40:
          movzx EDI,BYTE PTR [EAX+1]
          add EDX,16
          mov BYTE PTR [EAX+5],255
          mov BYTE PTR [EAX+9],0
          mov BYTE PTR [EAX+2],1
          and EDI,4294967280
          or EDI,EBP
          mov EBX,EDI
          movzx EDI,BYTE PTR [EAX+12]
          mov BYTE PTR [EAX+1],BL
          movzx EBX,BYTE PTR [ESP+28]
          and EDI,4294967232
          or EDI,48
          mov BYTE PTR [EAX],BL
          cmp EDX,ECX
          mov EBX,EDI
          mov BYTE PTR [EAX+12],BL
          je L_411db7
L_411e7b:
          mov EAX,DWORD PTR [L_479ed0]
          add EAX,EDX
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          mov DWORD PTR [EAX+12],0
          mov EBX,DWORD PTR [L_479ef0]
          test EBX,EBX
          je L_411e40
          movzx EDI,BYTE PTR [EAX+2]
          add EDX,16
          mov BYTE PTR [EAX],255
          mov BYTE PTR [EAX+5],1
          mov BYTE PTR [EAX+8],64
          mov BYTE PTR [EAX+7],0
          and EDI,4294967280
          or EDI,EBP
          mov EBX,EDI
          movzx EDI,BYTE PTR [EAX+12]
          mov BYTE PTR [EAX+2],BL
          movzx EBX,BYTE PTR [ESP+28]
          and EDI,4294967232
          or EDI,48
          mov BYTE PTR [EAX+1],BL
          cmp EDX,ECX
          mov EBX,EDI
          mov BYTE PTR [EAX+12],BL
          movzx EBX,BYTE PTR [ESP+36]
          mov BYTE PTR [EAX+9],BL
          jne L_411e7b
          jmp L_411db7
L_411eef:
          add EAX,131072
          and EAX,4294836224
          mov DWORD PTR [ESP+28],EAX
          shr EAX,14
          mov DWORD PTR [ESP+48],EAX
          jmp L_411bfd
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_411f10:
          movzx EDI,BYTE PTR [EAX+2]
          add EDX,16
          mov BYTE PTR [EAX],255
          mov BYTE PTR [EAX+9],56
          mov BYTE PTR [EAX+5],1
          mov BYTE PTR [EAX+8],64
          mov BYTE PTR [EAX+7],0
          and EDI,4294967280
          or EDI,EBP
          mov EBX,EDI
          movzx EDI,BYTE PTR [EAX+12]
          mov BYTE PTR [EAX+2],BL
          movzx EBX,BYTE PTR [ESP+28]
          and EDI,4294967232
          or EDI,48
          mov BYTE PTR [EAX+1],BL
          cmp EDX,ECX
          mov EBX,EDI
          mov BYTE PTR [EAX+12],BL
          jne L_411d50
          jmp L_411db7
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_411f60:
          cmp ESI,EAX
          ja L_411e03
          cmp DWORD PTR [ESP+56],EAX
          ja L_411e03
          mov EAX,ESI
          mov EDX,ESI
          shr ESI,14
          and EAX,16383
          mov DWORD PTR [ESP+8],16384
          mov DWORD PTR [ESP+32],ESI
          test EAX,EAX
          mov EBP,ESI
          setne AL
          movzx EAX,AL
          add EAX,1
          mov EBX,EAX
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [L_479ed8]
          add EAX,EDX
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDX
          call _memcpy
          mov EDX,ESI
          add ESI,EBX
          shl EDX,9
          mov DWORD PTR [ESP+28],ESI
          nop
L_411fc0:
          mov EBX,EBP
          lea ESI,DWORD PTR [EDX+512]
          mov EDI,EBP
          shr EBX,8
          and EBX,15
L_411fd0:
          mov EAX,DWORD PTR [L_479ed0]
          add EAX,EDX
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          mov DWORD PTR [EAX+12],0
          mov ECX,DWORD PTR [L_479ef0]
          test ECX,ECX
          je L_412090
          movzx ECX,BYTE PTR [EAX+2]
          mov BYTE PTR [EAX],255
          add EDX,16
          mov BYTE PTR [EAX+5],1
          and ECX,4294967280
          or ECX,EBX
          mov BYTE PTR [EAX+2],CL
          mov ECX,EDI
          mov BYTE PTR [EAX+1],CL
          movzx ECX,BYTE PTR [EAX+12]
          and ECX,4294967232
          or ECX,44
          cmp ESI,EDX
          mov BYTE PTR [EAX+12],CL
          movzx ECX,BYTE PTR [L_479ecc]
          mov BYTE PTR [EAX+9],CL
          movzx ECX,BYTE PTR [L_479ecd]
          mov BYTE PTR [EAX+8],CL
          movzx ECX,BYTE PTR [L_479ece]
          mov BYTE PTR [EAX+7],CL
          jne L_411fd0
          add EBP,1
          cmp DWORD PTR [ESP+28],EBP
          mov EDX,ESI
          jne L_411fc0
L_412059:
          mov EAX,DWORD PTR [ESP+32]
          sub EAX,DWORD PTR [L_479efc]
          mov ECX,4294966815
          cmp DWORD PTR [ESP+36],2
          mov WORD PTR [EAX+EAX*1+L_4cb7c0],CX
          jne L_411dfa
          mov EDX,4294966815
          mov WORD PTR [EAX+EAX*1+L_4cb7c2],DX
          jmp L_411dfa
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_412090:
          movzx ECX,BYTE PTR [EAX+1]
          add EDX,16
          mov BYTE PTR [EAX+5],255
          mov BYTE PTR [EAX+9],0
          mov BYTE PTR [EAX+2],1
          mov BYTE PTR [EAX+8],64
          mov BYTE PTR [EAX+7],0
          and ECX,4294967280
          or ECX,EBX
          mov BYTE PTR [EAX+1],CL
          mov ECX,EDI
          mov BYTE PTR [EAX],CL
          movzx ECX,BYTE PTR [EAX+12]
          and ECX,4294967232
          or ECX,44
          cmp ESI,EDX
          mov BYTE PTR [EAX+12],CL
          jne L_411fd0
          add EBP,1
          cmp DWORD PTR [ESP+28],EBP
          mov EDX,ESI
          jne L_411fc0
          jmp L_412059
L_4120e0:
          add EAX,DWORD PTR [L_479ed8]
          mov ESI,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+8],16384
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov DWORD PTR [ESP+40],1
          jmp L_411cf9
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_412110:
          push EDI
          push ESI
          mov ECX,50249728
          push EBX
          mov EDX,50233344
          mov ESI,OFFSET L_4c9164
          sub ESP,16
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_451b2c
          mov DWORD PTR [ESP],1
          cmp EAX,1
          mov DWORD PTR [ESP+8],EAX
          cmovne EDX,ECX
          mov DWORD PTR [ESP+12],EDX
          mov EBX,EDX
          call _log_printf
          mov ECX,DWORD PTR [L_479ed8]
          xor EAX,EAX
          add ECX,EBX
          lea EDI,DWORD PTR [ECX+4]
          mov DWORD PTR [ECX],0
          mov DWORD PTR [ECX+4092],0
          and EDI,4294967292
          sub ECX,EDI
          add ECX,4096
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          add EBX,DWORD PTR [L_479ed8]
          mov EAX,DWORD PTR [L_4c9164]
          lea EDI,DWORD PTR [EBX+4]
          mov DWORD PTR [EBX],EAX
          mov ECX,EBX
          mov EAX,DWORD PTR [L_4c9360]
          and EDI,4294967292
          sub ECX,EDI
          sub ESI,ECX
          add ECX,512
          mov DWORD PTR [EBX+508],EAX
          shr ECX,2
          rep movsd 
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
L_4121b0:
          mov EAX,DWORD PTR [ESP+4]
          cmp BYTE PTR [EAX],255
          jne L_412220
          cmp BYTE PTR [EAX+1],255
          jne L_412220
          cmp BYTE PTR [EAX+2],255
          jne L_412220
          cmp BYTE PTR [EAX+3],255
          jne L_412220
          cmp BYTE PTR [EAX+4],255
          jne L_412220
          cmp BYTE PTR [EAX+5],255
          jne L_412220
          cmp BYTE PTR [EAX+6],255
          jne L_412220
          cmp BYTE PTR [EAX+7],255
          jne L_412220
          cmp BYTE PTR [EAX+8],255
          jne L_412220
          cmp BYTE PTR [EAX+9],255
          jne L_412220
          cmp BYTE PTR [EAX+10],255
          jne L_412220
          cmp BYTE PTR [EAX+11],255
          jne L_412220
          cmp BYTE PTR [EAX+12],255
          jne L_412220
          cmp BYTE PTR [EAX+13],255
          jne L_412220
          cmp BYTE PTR [EAX+14],255
          jne L_412220
          cmp BYTE PTR [EAX+15],255
          setne AL
          movzx EAX,AL
          ret 
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_412220:
          mov EAX,1
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_412230:
          test BYTE PTR [L_479ea7],16
          mov EAX,DWORD PTR [L_479ed8]
          mov ECX,50331648
          jne L_412252
          imul ECX,DWORD PTR [L_479ee4],16896
          mov EAX,DWORD PTR [L_479ee0]
L_412252:
          mov EDX,DWORD PTR [ESP+4]
          mov DWORD PTR [EDX],ECX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_412260:
          push EDI
          push ESI
          push EBX
          sub ESP,160
          mov ESI,DWORD PTR [ESP+176]
          mov DWORD PTR [ESP+4],OFFSET L_451b54
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_451b7a
          mov DWORD PTR [ESP],ESI
          call _fopen
          test EAX,EAX
          je L_412593
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_451b7d
          mov EBX,EAX
          mov DWORD PTR [ESP],1
          call _log_printf
          test BYTE PTR [L_479ea7],16
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],1
          je L_412320
          mov EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+4],50331648
          mov DWORD PTR [ESP],EAX
          call _fwrite
          cmp EAX,1
          jne L_4123d1
          mov EDI,DWORD PTR [L_4c97a8]
          test EDI,EDI
          jne L_4123f3
L_4122f7:
          mov DWORD PTR [ESP+4],OFFSET L_451cdd
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],EBX
          call _fclose
          xor EAX,EAX
L_412315:
          add ESP,160
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
L_412320:
          imul EAX,DWORD PTR [L_479ee4],16896
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_479ee0]
          mov DWORD PTR [ESP],EAX
          call _fwrite
          cmp EAX,1
          jne L_412380
          mov ECX,DWORD PTR [L_4c97a8]
          test ECX,ECX
          jne L_412480
          mov EAX,DWORD PTR [L_479f6c]
          test EAX,EAX
          je L_412364
          test BYTE PTR [L_479f03],16
          jne L_412560
L_412364:
          mov EAX,DWORD PTR [L_479ee0]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [L_479ee0],0
          jmp L_4122f7
L_412380:
          mov DWORD PTR [ESP+4],OFFSET L_451b9a
          mov DWORD PTR [ESP],1
          call _log_printf
          imul EAX,DWORD PTR [L_479ee4],16896
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EAX
L_4123a6:
          mov DWORD PTR [ESP+4],OFFSET L_451ba4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP],EBX
          call _fclose
          add ESP,160
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          ret 
L_4123d1:
          mov DWORD PTR [ESP+4],OFFSET L_451b9a
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],50331648
          jmp L_4123a6
L_4123f3:
          mov DWORD PTR [ESP+4],OFFSET L_451be4
          mov DWORD PTR [ESP],1
          lea EDI,DWORD PTR [ESP+64]
          call _log_printf
          mov EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+24],EDI
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],50331648
          call _XeCryptSha
          mov DWORD PTR [ESP+4],OFFSET L_451c18
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],OFFSET L_4c93a8
          call _writeSha1File
          jmp L_4122f7
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_412480:
          lea EDI,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],OFFSET L_451be4
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],EDI
          call _XeCryptShaInit
          imul EAX,DWORD PTR [L_479ee4],16896
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [L_479ee0]
          mov DWORD PTR [ESP+4],EAX
          call _XeCryptShaUpdate
          mov EDX,DWORD PTR [L_479f6c]
          mov EAX,DWORD PTR [L_4c97a8]
          test EDX,EDX
          je L_412509
          test BYTE PTR [L_479f03],16
          je L_412509
          test EAX,EAX
          je L_412560
          mov DWORD PTR [ESP+4],OFFSET L_451c38
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          call FUN_416840
          mov DWORD PTR [L_479f6c],EAX
          mov EAX,DWORD PTR [L_4c97a8]
L_412509:
          test EAX,EAX
          je L_412364
          lea EAX,DWORD PTR [ESP+64]
          lea EDI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDI
          call _XeCryptShaFinal
          mov DWORD PTR [ESP+4],OFFSET L_451c18
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],OFFSET L_4c93a8
          call _writeSha1File
          jmp L_412364
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_412560:
          mov DWORD PTR [ESP+4],OFFSET L_451c94
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EBX
          call FUN_416840
          mov DWORD PTR [L_479f6c],EAX
          mov EAX,DWORD PTR [L_4c97a8]
          jmp L_412509
L_412593:
          mov EAX,4294967294
          jmp L_412315
          .byte 0x8d
          .byte 0x76
          .byte 0x0
FUN_4125a0:
          push EBP
          push EDI
          xor EAX,EAX
          push ESI
          push EBX
          sub ESP,76
          mov EBX,DWORD PTR [L_479ea4]
          and EBX,268435456
          mov DWORD PTR [ESP+60],EBX
          je L_4125c3
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4125c3:
          mov EAX,DWORD PTR [L_479ee8]
          mov DWORD PTR [ESP],EAX
          call _malloc
          test EAX,EAX
          mov DWORD PTR [ESP+40],EAX
          mov DWORD PTR [L_479ee0],EAX
          je L_4128ca
          mov EDI,DWORD PTR [L_479ef0]
          test EDI,EDI
          jne L_412d46
          mov ESI,DWORD PTR [L_479ef4]
          test ESI,ESI
          jne L_412be3
L_4125fd:
          mov DWORD PTR [ESP+4],OFFSET L_451d54
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EBX,DWORD PTR [L_479ee4]
          test EBX,EBX
          je L_412785
          mov EBX,DWORD PTR [ESP+40]
          mov EBP,DWORD PTR [L_479ed0]
          mov EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+56],0
          mov ESI,EBX
L_412638:
          mov EDX,DWORD PTR [ESP+56]
          mov EBX,EDX
          shl EBX,9
          mov DWORD PTR [ESP+44],EBX
          mov EBX,EDX
          lea EDX,DWORD PTR [ESI+16896]
          shl EBX,14
          mov DWORD PTR [ESP+40],EBX
          mov DWORD PTR [ESP+52],EDX
          mov EBX,ESI
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_412660:
          mov EDX,DWORD PTR [ESP+44]
          mov ESI,DWORD PTR [ESP+40]
          xor ECX,ECX
          add EDX,EBP
          add ESI,EAX
          jmp L_41267f
L_412670:
          add ECX,1
          cmp ECX,512
          je L_412812
L_41267f:
          cmp BYTE PTR [ESI+ECX*1],255
          je L_412670
L_412685:
          movzx EAX,BYTE PTR [EDX+12]
          mov BYTE PTR [ESP+48],AL
L_41268d:
          xor EAX,EAX
          xor EDI,EDI
          xor ECX,ECX
          mov EBP,EAX
L_412695:
          test CL,31
          jne L_4126ac
          mov EAX,ESI
          cmp ECX,4096
          cmove EAX,EDX
          mov EDI,DWORD PTR [EAX]
          lea ESI,DWORD PTR [EAX+4]
          not EDI
L_4126ac:
          mov EAX,EDI
          shr EDI,1
          and EAX,1
          xor EAX,EBP
          mov EBP,EAX
          xor EBP,110445913
          test AL,1
          cmovne EAX,EBP
          add ECX,1
          shr EAX,1
          cmp ECX,4198
          mov EBP,EAX
          jne L_412695
          movzx ECX,BYTE PTR [ESP+48]
          not EAX
          mov ESI,EAX
          shl ESI,6
          and ECX,63
          add ECX,ESI
          mov BYTE PTR [EDX+12],CL
          mov ECX,EAX
          shr ECX,2
          mov BYTE PTR [EDX+13],CL
          mov ECX,EAX
          shr EAX,18
          shr ECX,10
          mov BYTE PTR [EDX+15],AL
          mov BYTE PTR [EDX+14],CL
          mov EDX,DWORD PTR [ESP+40]
          mov EAX,DWORD PTR [L_479ed8]
          mov EBP,DWORD PTR [L_479ed0]
          lea ESI,DWORD PTR [EAX+EDX*1]
          mov EDX,DWORD PTR [ESP+44]
          add EDX,EBP
L_412713:
          mov ECX,DWORD PTR [ESI]
          lea EDI,DWORD PTR [EBX+4]
          and EDI,4294967292
          mov DWORD PTR [EBX],ECX
          mov ECX,DWORD PTR [ESI+508]
          mov DWORD PTR [EBX+508],ECX
          mov ECX,EBX
          add EBX,528
          sub ECX,EDI
          sub ESI,ECX
          add ECX,512
          shr ECX,2
          rep movsd 
          mov EDI,DWORD PTR [EDX]
          mov ESI,DWORD PTR [EDX+4]
          mov ECX,DWORD PTR [EDX+8]
          mov EDX,DWORD PTR [EDX+12]
          add DWORD PTR [ESP+44],16
          add DWORD PTR [ESP+40],512
          mov DWORD PTR [EBX-16],EDI
          mov DWORD PTR [EBX-12],ESI
          mov DWORD PTR [EBX-8],ECX
          mov DWORD PTR [EBX-4],EDX
          cmp EBX,DWORD PTR [ESP+52]
          jne L_412660
          add DWORD PTR [ESP+56],1
          mov ESI,EBX
          mov EBX,DWORD PTR [ESP+56]
          cmp DWORD PTR [L_479ee4],EBX
          ja L_412638
L_412785:
          mov DWORD PTR [ESP+4],OFFSET L_451cdd
          mov DWORD PTR [ESP],1
          call _log_printf
          mov ECX,DWORD PTR [L_479f6c]
          test ECX,ECX
          je L_4127b0
          test BYTE PTR [L_479f03],16
          jne L_412ae3
L_4127b0:
          mov EAX,DWORD PTR [L_479f74]
          lea EDX,DWORD PTR [EAX-1]
          cmp EDX,31
          ja L_4127f4
          mov EBX,DWORD PTR [L_479f60]
          cmp DWORD PTR [L_479ef0],EBX
          je L_4128d7
          cmp DWORD PTR [L_479ea0],2
          je L_4128d7
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_451ec0
          mov DWORD PTR [ESP],1
          call _log_printf
L_4127f4:
          mov DWORD PTR [ESP+4],OFFSET L_451f37
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,76
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_412812:
          cmp BYTE PTR [EDX],255
          jne L_412685
          cmp BYTE PTR [EDX+1],255
          jne L_412685
          cmp BYTE PTR [EDX+2],255
          jne L_412685
          cmp BYTE PTR [EDX+3],255
          jne L_412685
          cmp BYTE PTR [EDX+4],255
          jne L_412685
          cmp BYTE PTR [EDX+5],255
          jne L_412685
          cmp BYTE PTR [EDX+6],255
          jne L_412685
          cmp BYTE PTR [EDX+7],255
          jne L_412685
          cmp BYTE PTR [EDX+8],255
          jne L_412685
          cmp BYTE PTR [EDX+9],255
          jne L_412685
          cmp BYTE PTR [EDX+10],255
          jne L_412685
          cmp BYTE PTR [EDX+11],255
          jne L_412685
          movzx ECX,BYTE PTR [EDX+12]
          cmp CL,255
          mov BYTE PTR [ESP+48],CL
          jne L_41268d
          cmp BYTE PTR [EDX+13],255
          jne L_41268d
          movzx ECX,BYTE PTR [EDX+14]
          cmp CL,255
          mov BYTE PTR [ESP+48],CL
          jne L_4128c0
          cmp BYTE PTR [EDX+15],255
          je L_412713
          jmp L_41268d
L_4128c0:
          mov BYTE PTR [ESP+48],255
          jmp L_41268d
L_4128ca:
          add ESP,76
          mov EAX,4294967295
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4128d7:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_451dca
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDX,DWORD PTR [L_479ef0]
          test EDX,EDX
          jne L_412ac7
          mov EAX,DWORD PTR [L_479ea8]
          mov EBX,16896
          mov DWORD PTR [ESP+40],16896
          sub EAX,6
          and EAX,4294967293
          cmp EAX,1
          sbb EBP,EBP
          and EBP,3072
          add EBP,1024
          mov EDI,EBP
L_412928:
          mov EAX,DWORD PTR [L_479f74]
          test EAX,EAX
          je L_4127f4
          mov DWORD PTR [ESP+48],EDI
          mov EDI,DWORD PTR [ESP+60]
          jmp L_412973
          .byte 0x90
L_412940:
          mov ESI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_451e28
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+16],ESI
          call _log_printf
L_412964:
          add EDI,1
          cmp DWORD PTR [L_479f74],EDI
          jbe L_4127f4
L_412973:
          mov EAX,DWORD PTR [EDI*4+L_479f78]
          mov EDX,DWORD PTR [EDI*4+L_479ff8]
          cmp EAX,EBP
          jae L_412989
          cmp EDX,EBP
          jb L_4129dc
L_412989:
          cmp EDX,-5
          jne L_412940
          mov ESI,EAX
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_451e84
          mov DWORD PTR [ESP],1
          call _log_printf
          imul ESI,EBX
          mov EAX,DWORD PTR [L_479ee0]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],0
          add EAX,ESI
          mov DWORD PTR [ESP],EAX
          call _memset
L_4129c6:
          mov DWORD PTR [ESP+4],OFFSET L_451cdd
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_412964
L_4129dc:
          mov ESI,EAX
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+40]
          imul ESI,EBX
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP+4],OFFSET L_451de0
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+44],ESI
          mov ESI,EDX
          imul ESI,EBX
          call _log_printf
          mov EAX,DWORD PTR [L_479ee0]
          mov DWORD PTR [ESP+8],EBX
          lea EDX,DWORD PTR [EAX+ESI*1]
          add EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          mov DWORD PTR [ESP+4],OFFSET L_451e14
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+44]
          add EAX,DWORD PTR [L_479ee0]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EAX
          call _memset
          cmp DWORD PTR [L_479ef0],1
          mov EAX,DWORD PTR [L_479ee0]
          lea EDX,DWORD PTR [EAX+ESI*1]
          sbb ECX,ECX
          and ECX,4294849024
          lea ECX,DWORD PTR [ESI+ECX*1+135168]
          add EAX,ECX
L_412a7c:
          cmp BYTE PTR [EDX],255
          jne L_4129c6
          add EDX,1
          cmp EDX,EAX
          jne L_412a7c
          mov DWORD PTR [ESP+4],OFFSET L_451f48
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_479ef0]
          add ESI,DWORD PTR [L_479ee0]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [EDI*4+L_479f78]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call FUN_4100b0
          jmp L_4129c6
L_412ac7:
          mov EBX,135168
          mov EBP,512
          mov EDI,512
          mov DWORD PTR [ESP+40],135168
          jmp L_412928
L_412ae3:
          mov DWORD PTR [ESP+4],OFFSET L_451d88
          mov DWORD PTR [ESP],1
          call _log_printf
          movzx EAX,BYTE PTR [L_479ece]
          mov EBX,DWORD PTR [L_479ee0]
          imul EDX,EAX,135168
          mov DWORD PTR [ESP+44],EAX
          add EBX,EDX
          mov EDX,EAX
          shl EAX,17
          mov DWORD PTR [ESP+52],EAX
          mov EAX,EDX
          shl EAX,12
          cmp DWORD PTR [L_479ec8],EDX
          mov DWORD PTR [ESP+48],EAX
          jbe L_412bca
L_412b2e:
          lea EAX,DWORD PTR [EBX+135168]
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+40],EAX
          mov EAX,DWORD PTR [ESP+48]
L_412b40:
          mov ESI,DWORD PTR [L_479f4c]
          lea EDI,DWORD PTR [EBX+4]
          and EDI,4294967292
          add ESI,EDX
          add EDX,512
          mov ECX,DWORD PTR [ESI]
          mov DWORD PTR [EBX],ECX
          mov ECX,DWORD PTR [ESI+508]
          mov DWORD PTR [EBX+508],ECX
          mov ECX,EBX
          add EBX,528
          sub ECX,EDI
          sub ESI,ECX
          add ECX,512
          shr ECX,2
          rep movsd 
          mov ECX,DWORD PTR [L_479f50]
          mov EBP,DWORD PTR [ECX+EAX*1]
          mov EDI,DWORD PTR [ECX+EAX*1+4]
          mov ESI,DWORD PTR [ECX+EAX*1+8]
          mov ECX,DWORD PTR [ECX+EAX*1+12]
          add EAX,16
          mov DWORD PTR [EBX-16],EBP
          mov DWORD PTR [EBX-12],EDI
          mov DWORD PTR [EBX-8],ESI
          mov DWORD PTR [EBX-4],ECX
          cmp EBX,DWORD PTR [ESP+40]
          jne L_412b40
          add DWORD PTR [ESP+44],1
          add DWORD PTR [ESP+52],131072
          mov EAX,DWORD PTR [ESP+44]
          add DWORD PTR [ESP+48],4096
          cmp DWORD PTR [L_479ec8],EAX
          ja L_412b2e
L_412bca:
          mov DWORD PTR [ESP+4],OFFSET L_451cdd
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4127b0
L_412be3:
          mov DWORD PTR [ESP+4],OFFSET L_451d10
          mov DWORD PTR [ESP],1
          call _log_printf
          mov ESI,DWORD PTR [L_479ee4]
          mov EAX,ESI
          shl EAX,5
          test EAX,EAX
          je L_412d2d
          xor EBP,EBP
          mov EDX,2
          jmp L_412cd5
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_412c20:
          cmp BYTE PTR [EBX+EDX*1-1],255
          lea EAX,DWORD PTR [EDX-1]
          movzx ECX,BYTE PTR [EBX+EDX*1]
          jne L_412cfa
          cmp CL,255
          jne L_412cfa
          cmp BYTE PTR [EBX+EDX*1+1],255
          jne L_412cfa
          cmp BYTE PTR [EBX+EDX*1+2],255
          jne L_412dc5
          movzx ECX,BYTE PTR [EBX+EDX*1+3]
          cmp CL,255
          jne L_412dc5
          cmp BYTE PTR [EBX+EDX*1+4],255
          jne L_412cfa
          cmp BYTE PTR [EBX+EDX*1+5],255
          jne L_412dc5
          movzx ECX,BYTE PTR [EBX+EDX*1+6]
          cmp CL,255
          jne L_412dc5
          cmp BYTE PTR [EBX+EDX*1+7],255
          jne L_412cfa
          cmp BYTE PTR [EBX+EDX*1+8],255
          jne L_412dc5
          movzx ECX,BYTE PTR [EBX+EDX*1+9]
          cmp CL,255
          jne L_412dc5
          cmp BYTE PTR [EBX+EDX*1+10],255
          jne L_412cfa
          cmp BYTE PTR [EBX+EDX*1+11],255
          jne L_412cfa
          movzx ECX,BYTE PTR [EBX+EDX*1+12]
          cmp CL,255
          jne L_412dc5
          cmp BYTE PTR [EBX+EDX*1+13],255
          jne L_412cfa
          mov EAX,ESI
          add EBP,1
          add EDX,16
          shl EAX,5
          cmp EAX,EBP
          jbe L_412d2d
L_412cd5:
          mov EBX,DWORD PTR [L_479ed0]
          mov EAX,EBP
          shl EAX,4
          add EAX,EBX
          movzx EDI,BYTE PTR [EAX]
          mov DWORD PTR [ESP+44],EAX
          mov EAX,EDI
          cmp AL,255
          je L_412c20
          movzx ECX,BYTE PTR [EBX+EDX*1]
          lea EAX,DWORD PTR [EDX-1]
L_412cfa:
          mov EBX,DWORD PTR [ESP+44]
          add EBP,1
          mov BYTE PTR [EBX],CL
          mov EBX,DWORD PTR [L_479ed0]
          movzx ECX,BYTE PTR [EBX+EAX*1]
          mov BYTE PTR [EBX+EDX*1],CL
          mov ECX,DWORD PTR [L_479ed0]
          mov EBX,EDI
          add EDX,16
          mov BYTE PTR [ECX+EAX*1],BL
          mov ESI,DWORD PTR [L_479ee4]
          mov EAX,ESI
          shl EAX,5
          cmp EAX,EBP
          ja L_412cd5
L_412d2d:
          mov DWORD PTR [ESP+4],OFFSET L_451cdd
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4125fd
L_412d46:
          mov DWORD PTR [ESP+4],OFFSET L_451ce4
          mov DWORD PTR [ESP],1
          xor EBX,EBX
          call _log_printf
          mov EDI,DWORD PTR [L_479ee4]
          mov EAX,DWORD PTR [L_479ed0]
          shr EDI,3
          lea ECX,DWORD PTR [EAX+4096]
          test EDI,EDI
          je L_412d2d
L_412d74:
          mov ESI,EBX
          lea EAX,DWORD PTR [ECX-4096]
          shr ESI,8
          and ESI,15
          jmp L_412d9a
L_412d84:
          movzx EDX,BYTE PTR [EAX+2]
          mov BYTE PTR [EAX+1],BL
          add EAX,16
          and EDX,4294967280
          or EDX,ESI
          mov BYTE PTR [EAX-14],DL
          cmp ECX,EAX
          je L_412db3
L_412d9a:
          movzx EDX,BYTE PTR [EAX+2]
          and EDX,15
          cmp DL,15
          jne L_412d84
          cmp BYTE PTR [EAX+1],255
          jne L_412d84
          add EAX,16
          cmp ECX,EAX
          jne L_412d9a
L_412db3:
          add EBX,1
          add ECX,4096
          cmp EDI,EBX
          jne L_412d74
          jmp L_412d2d
L_412dc5:
          mov ECX,4294967295
          jmp L_412cfa
          .byte 0x90
FUN_412dd0:
          mov EAX,DWORD PTR [L_479efc]
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_412de0:
          push ESI
          push EBX
          mov EBX,DWORD PTR [ESP+20]
          mov ECX,DWORD PTR [ESP+24]
          mov EDX,DWORD PTR [ESP+28]
          mov EAX,DWORD PTR [ESP+32]
          test EBX,EBX
          je L_412e20
          lea EBX,DWORD PTR [EAX+3071]
          mov EAX,EBX
          shl EAX,14
          test ECX,ECX
          je L_412e0c
L_412e05:
          mov ESI,EBX
          shl ESI,9
          mov DWORD PTR [ECX],ESI
L_412e0c:
          test EDX,EDX
          je L_412e15
          shl EBX,5
          mov DWORD PTR [EDX],EBX
L_412e15:
          pop EBX
          pop ESI
          ret 
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_412e20:
          mov ESI,DWORD PTR [ESP+12]
          test ESI,ESI
          je L_412e50
          lea EBX,DWORD PTR [EAX+479]
          mov EAX,EBX
          shl EAX,17
          test ECX,ECX
          je L_412e3e
          mov ESI,EBX
          shl ESI,12
          mov DWORD PTR [ECX],ESI
L_412e3e:
          test EDX,EDX
          je L_412e15
          shl EBX,11
          mov DWORD PTR [EDX],EBX
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_412e50:
          mov EBX,DWORD PTR [ESP+16]
          test EBX,EBX
          je L_412e70
          lea EBX,DWORD PTR [EAX+3967]
          mov EAX,EBX
          shl EAX,14
          test ECX,ECX
          jne L_412e05
          jmp L_412e0c
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_412e70:
          lea EBX,DWORD PTR [EAX+991]
          mov EAX,EBX
          shl EAX,14
          test ECX,ECX
          jne L_412e05
          jmp L_412e0c
          jmp FUN_412e90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          nop
          nop
          nop
          nop
          nop
          nop
          nop
FUN_412e90:
          mov ECX,DWORD PTR [ESP+12]
          mov EDX,DWORD PTR [ESP+16]
          mov EAX,DWORD PTR [ESP+20]
          test ECX,ECX
          je L_412ec0
          test EDX,EDX
          je L_412eaa
          mov DWORD PTR [EDX],1571840
L_412eaa:
          test EAX,EAX
          je L_412f20
          mov DWORD PTR [EAX],98240
          mov EAX,50298880
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_412ec0:
          mov ECX,DWORD PTR [ESP+4]
          test ECX,ECX
          je L_412ee2
          test EDX,EDX
          je L_412ed2
          mov DWORD PTR [EDX],1957888
L_412ed2:
          test EAX,EAX
          je L_412f30
          mov DWORD PTR [EAX],978944
          mov EAX,62652416
          ret 
L_412ee2:
          mov ECX,DWORD PTR [ESP+8]
          test ECX,ECX
          je L_412f04
          test EDX,EDX
          je L_412ef4
          mov DWORD PTR [EDX],2030592
L_412ef4:
          test EAX,EAX
          je L_412f40
          mov DWORD PTR [EAX],126912
          mov EAX,64978944
          ret 
L_412f04:
          test EDX,EDX
          je L_412f0e
          mov DWORD PTR [EDX],506880
L_412f0e:
          test EAX,EAX
          je L_412f50
          mov DWORD PTR [EAX],31680
          mov EAX,16220160
          ret 
          .byte 0x66
          .byte 0x90
L_412f20:
          mov EAX,50298880
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_412f30:
          mov EAX,62652416
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_412f40:
          mov EAX,64978944
          ret 
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_412f50:
          mov EAX,16220160
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_412f60:
          mov ECX,DWORD PTR [ESP+12]
          mov EDX,DWORD PTR [ESP+16]
          mov EAX,DWORD PTR [ESP+20]
          test ECX,ECX
          je L_412f90
          test EDX,EDX
          je L_412f7a
          mov DWORD PTR [EDX],1571328
L_412f7a:
          test EAX,EAX
          je L_412ff0
          mov DWORD PTR [EAX],98208
          mov EAX,50282496
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_412f90:
          mov ECX,DWORD PTR [ESP+4]
          test ECX,ECX
          je L_412fb2
          test EDX,EDX
          je L_412fa2
          mov DWORD PTR [EDX],1953792
L_412fa2:
          test EAX,EAX
          je L_413000
          mov DWORD PTR [EAX],976896
          mov EAX,62521344
          ret 
L_412fb2:
          mov ECX,DWORD PTR [ESP+8]
          test ECX,ECX
          je L_412fd4
          test EDX,EDX
          je L_412fc4
          mov DWORD PTR [EDX],2030080
L_412fc4:
          test EAX,EAX
          je L_413010
          mov DWORD PTR [EAX],126880
          mov EAX,64962560
          ret 
L_412fd4:
          test EDX,EDX
          je L_412fde
          mov DWORD PTR [EDX],506368
L_412fde:
          test EAX,EAX
          je L_413020
          mov DWORD PTR [EAX],31648
          mov EAX,16203776
          ret 
          .byte 0x66
          .byte 0x90
L_412ff0:
          mov EAX,50282496
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_413000:
          mov EAX,62521344
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_413010:
          mov EAX,64962560
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_413020:
          mov EAX,16203776
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_413030:
          push ESI
          push EBX
          sub ESP,36
          mov EAX,DWORD PTR [ESP+56]
          mov EBX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],OFFSET L_451f80
          mov DWORD PTR [ESP],1
          mov ESI,DWORD PTR [ESP+52]
          lea EDX,DWORD PTR [EBX+EAX*1]
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+20],EDX
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [L_479ef0]
          mov ECX,61937
          test EAX,EAX
          jne L_41307f
          mov ECX,8187
L_41307f:
          add ESP,36
          mov EDX,ESI
          mov EAX,EBX
          pop EBX
          pop ESI
          jmp L_40ecc0
          .byte 0x90
          .byte 0x90
          .byte 0x90

.data
.p2align 5
L_44a580:
          .byte 0xa9
          .byte 0x20
          .byte 0x32
          .byte 0x30
L_44a584:
          .ascii "04-2"
L_44a588:
          .ascii "0"
L_44a589:
          .ascii "0"
L_44a58a:
          .zero 1
          .ascii " "
L_44a58c:
          .ascii "Micr"
L_44a590:
          .ascii "osof"
L_44a594:
          .ascii "t Co"
L_44a598:
          .ascii "rpor"
L_44a59c:
          .ascii "atio"
L_44a5a0:
          .ascii "n. A"
L_44a5a4:
          .ascii "ll r"
L_44a5a8:
          .ascii "ight"
L_44a5ac:
          .ascii "s re"
L_44a5b0:
          .ascii "serv"
L_44a5b4:
          .string "ed."
L_44a5b8:
          .zero 4
L_44a5bc:
          .zero 4

.section .rdata,"dr"
.p2align 2
L_451760:
          .string "***** WARNING: cfldv was not set anywhere, setting it to 1\n"
L_45179c:
          .string "      please set it in ini or on command line and rebuild!\n"
L_4517d8:
          .long L_40f694
          .long L_40f9d0
          .long L_40f9d0
          .long L_40f9c0
          .long L_40f671
          .long L_40f990
          .long L_40f950
          .long L_40f950
L_4517f8:
          .string "flash header build version set to v.%d\n"
L_451820:
          .string "\n***** ERROR: SMC size 0x%x not supported!!!\n\n"
          .zero 1
L_451850:
          .string "reset smc load address to 0x%x size 0x%x\n"
          .zero 2
L_45187c:
          .string "patch slot offset reset to: 0x%x\n"
          .zero 2
L_4518a0:
          .string "\n******* ERROR: adding %s will exceed available flash space! Skipped!\n\n"
L_4518e8:
          .string "\tadding as %s at raw offset 0x%x len 0x%08x (end 0x%08x)\n"
          .zero 2
L_451924:
          .string "\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\n\n"
          .zero 2
L_451978:
          .string "\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\n"
          .zero 2
L_4519c4:
          .string "adding smc config to offset 0x%08x, len 0x%x\n"
          .zero 2
L_4519f4:
          .string "Inserting netKd data from dump into header\n"
L_451a20:
          .string "%c%c v%d at 0x%x size 0x%x (CB)\n"
          .zero 3
L_451a44:
          .string "%c%c v%d at 0x%x size 0x%x (dual CB)\n"
          .zero 2
L_451a6c:
          .string "%c%c v%d at 0x%x size 0x%x (devkit CC)\n"
L_451a94:
          .string "%c%c v%d at 0x%x size 0x%x (CD)\n"
          .zero 3
L_451ab8:
          .string "%c%c v%d at 0x%x size 0x%x (CE)\n"
          .zero 3
L_451adc:
          .string "final truncated bootloader size 0x%x\n"
          .zero 2
L_451b04:
          .string "offset 0x%x len 0x4000 (end 0x%x)..."
          .zero 3
L_451b2c:
          .string "copying anchor block %d to offset 0x%x\n"
L_451b54:
          .string "\n------ writing image to disk ------\n"
L_451b7a:
          .string "wb"
L_451b7d:
          .string "writing file '%s' to disk..."
L_451b9a:
          .string "failed!\n"
          .zero 1
L_451ba4:
          .string "\n***** ERROR: was not able to write %d bytes to the file %s!\n"
          .zero 2
L_451be4:
          .string "done!\ncreating SHA-1 hash from system area data..."
          .zero 1
L_451c18:
          .string "done!\nwriting SHA-1 to file..."
          .zero 1
L_451c38:
          .string "done!\nchecking and copying > 64M NAND data from dump file if present and updating SHA-1...\n"
L_451c94:
          .string "done!\nchecking and copying > 64M NAND data from dump file if present...\n"
L_451cdd:
          .string "done!\n"
L_451ce4:
          .string "fixing up big block LBA numbers in spare..."
L_451d10:
          .string "fixing up big block controller on small block NAND LBA numbers..."
          .zero 2
L_451d54:
          .string "calculating ECD bytes and assembling raw image..."
          .zero 2
L_451d88:
          .string "attempting to restore NAND MU data to big block unit from dump..."
L_451dca:
          .string "remapping %d blocks\n"
          .zero 1
L_451de0:
          .string "    copying 0x%x bytes of LBA 0x%x to block 0x%x..."
L_451e14:
          .string "zero fill origin..."
L_451e28:
          .string "\n\n***** ERROR: Remapping block 0x%x to block 0x%x is not sane on a NAND with 0x%x blocks!\n"
          .zero 1
L_451e84:
          .string "    Remapping block 0x%x is not required, zerofilling..."
          .zero 3
L_451ec0:
          .string "\n\n***** ERROR: if you had given the same small/big block style NAND donor image I'd be remapping %d bad blocks now...\n"
L_451f37:
          .string "done remapping!\n"
L_451f48:
          .string "\n        dest block is empty, fixing up LBA and ECD..."
          .zero 1
L_451f80:
          .string "\tadding %s at raw offset 0x%x len 0x%x (end 0x%x)\n"
          .zero 1

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
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40e950 - .
          .byte 0x6c
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4d
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
          .byte 0x50
          .byte 0x3
          .byte 0x3f
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
          .byte 0x3
          .byte 0xd9
          .byte 0x1
          .byte 0xe
          .byte 0x4
          .byte 0xc3
          .byte 0xc5
          .byte 0xc6
          .byte 0xc7
          .byte 0x46
          .byte 0xe
          .byte 0x50
          .byte 0x83
          .byte 0x5
          .byte 0x85
          .byte 0x2
          .byte 0x86
          .byte 0x4
          .byte 0x87
          .byte 0x3
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_40ecc0 - .
          .byte 0x22
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
          .byte 0x2c
          .byte 0x3
          .byte 0x8d
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
          .byte 0x48
          .byte 0xb
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40eef0 - .
          .byte 0x35
          .byte 0x4
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
          .byte 0x41
          .byte 0xb
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40f330 - .
          .byte 0xd9
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
          .byte 0x40
          .byte 0x3
          .byte 0x44
          .byte 0x4
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
          .byte 0x3
          .byte 0x6e
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
          .byte 0x4a
          .byte 0xb
          .byte 0x3
          .byte 0xe3
          .byte 0x1
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
          .byte 0x44
          .byte 0xb
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_40fb10 - .
          .byte 0x4b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x47
          .byte 0xe
          .byte 0x4
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_40fb60 - .
          .byte 0x4f
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
          .byte 0x2
          .byte 0x45
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa8
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_40fbb0 - .
          .byte 0x76
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
          .byte 0x2
          .byte 0x6e
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
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd8
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_40fc30 - .
          .byte 0x8a
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
          .byte 0x2
          .byte 0x61
          .byte 0xa
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_40fcc0 - .
          .byte 0xec
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
          .byte 0x28
          .byte 0x2
          .byte 0xaf
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
          .byte 0x1c
          .byte 0x1
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
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_40feb0 - .
          .byte 0x83
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
          .byte 0x74
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_40ff40 - .
          .byte 0x35
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x88
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_40ff80 - .
          .byte 0xb7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x76
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x49
          .byte 0xb
          .byte 0x2
          .byte 0x76
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xac
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_410040 - .
          .byte 0x26
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
          .byte 0xc0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_410070 - .
          .byte 0x36
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
          .byte 0xd4
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_4100b0 - .
          .byte 0x6e
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
          .byte 0x1c
          .byte 0x3
          .byte 0x1c
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
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_410220 - .
          .byte 0x1b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_410240 - .
          .byte 0x42
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x7e
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_410290 - .
          .byte 0xb3
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
          .byte 0x7b
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
          .byte 0x4a
          .byte 0xb
          .byte 0x5d
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
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x88
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long L_410350 - .
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9c
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_410360 - .
          .byte 0xf6
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
          .byte 0x8d
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
          .byte 0x48
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd4
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_410460 - .
          .byte 0x2c
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
          .byte 0xe8
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_410490 - .
          .byte 0x39
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x46
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x72
          .byte 0xc3
          .byte 0xe
          .byte 0x4
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
          .long FUN_4104d0 - .
          .byte 0x6
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
          .byte 0x18
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_4104e0 - .
          .byte 0xa
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
          .byte 0x2c
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_4104f0 - .
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_410500 - .
          .byte 0x86
          .byte 0x6
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
          .byte 0x3
          .byte 0xf2
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
          .byte 0x43
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x84
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long L_410b90 - .
          .byte 0x1e
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
          .byte 0x98
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_410bb0 - .
          .byte 0x78
          .byte 0x4
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
          .byte 0xf0
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
          .byte 0x45
          .byte 0xb
          .byte 0x68
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
          .byte 0xf0
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_411030 - .
          .byte 0x74
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
          .byte 0x64
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
          .byte 0x58
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_4110b0 - .
          .byte 0xfa
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
          .byte 0x30
          .byte 0x2
          .byte 0xf9
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
          .byte 0x2
          .byte 0x5a
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
          .byte 0x2
          .byte 0x63
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
          .byte 0x45
          .byte 0xb
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x88
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_4112b0 - .
          .byte 0x3d
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
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa4
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_4112f0 - .
          .byte 0x3
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
          .byte 0x1c
          .byte 0x3
          .byte 0x5e
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
          .byte 0x47
          .byte 0xb
          .byte 0x70
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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xfc
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_411600 - .
          .byte 0x71
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x87
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0xc
          .byte 0x86
          .byte 0x3
          .byte 0x4f
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x4f
          .byte 0xe
          .byte 0xc
          .byte 0x46
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long FUN_411680 - .
          .byte 0x79
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
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0xce
          .byte 0xa
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
          .byte 0x4b
          .byte 0xb
          .byte 0x2
          .byte 0x73
          .byte 0xa
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
          .byte 0x60
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
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long FUN_411800 - .
          .byte 0xd0
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
          .byte 0x40
          .byte 0x3
          .byte 0x7b
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
          .byte 0x48
          .byte 0xb
          .byte 0x2
          .byte 0x86
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x48
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
          .byte 0x2
          .byte 0xa7
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xdc
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long FUN_411bd0 - .
          .byte 0x3b
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
          .byte 0x60
          .byte 0x3
          .byte 0x60
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
          .byte 0x45
          .byte 0xb
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long FUN_412110 - .
          .byte 0xa0
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
          .byte 0x46
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x4d
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x87
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
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long L_4121b0 - .
          .byte 0x76
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
          .byte 0x64
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long FUN_412230 - .
          .byte 0x29
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long FUN_412260 - .
          .byte 0x3d
          .byte 0x3
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
          .byte 0xb0
          .byte 0x1
          .byte 0x2
          .byte 0xb2
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
          .byte 0x42
          .byte 0xb
          .byte 0x2
          .byte 0xa8
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
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc4
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long FUN_4125a0 - .
          .byte 0x2f
          .byte 0x8
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
          .byte 0x60
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
          .byte 0x3
          .byte 0x48
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
          .byte 0x41
          .byte 0xb
          .byte 0x2
          .byte 0xbb
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
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long FUN_412dd0 - .
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long L_412de0 - .
          .byte 0xa1
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
          .byte 0x74
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x49
          .byte 0xb
          .byte 0x68
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x47
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7c
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long FUN_412e90 - .
          .byte 0xc6
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
          .byte 0x90
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long FUN_412f60 - .
          .byte 0xc6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa4
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long FUN_413030 - .
          .byte 0x5d
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
          .byte 0x30
          .byte 0x2
          .byte 0x4d
          .byte 0xe
          .byte 0xc
          .byte 0x45
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0

.bss
.p2align 5
L_46f9c0:
          .zero 4
L_46f9c4:
          .zero 28
L_46f9e0:
          .zero 1568
L_470000:
          .zero 110
L_47006e:
          .zero 2418
