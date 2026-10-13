# runtime/libmingwex/fseeko64.s -- byte match
#
# original placement:
#   .eh_frame      0046ea74-0046ec0c
#   .rdata         004635a0-00463720
#   .rdata$zzz     0046466c-00464698
#   .text          00448a20-00448ff0

.intel_syntax noprefix
.globl _fseeko64

.text
.p2align 4
FUN_448a20:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EBX,DWORD PTR [ESP+64]
          mov EAX,DWORD PTR [EBX+12]
          mov EDX,EAX
          and EDX,3
          cmp EDX,2
          mov EDX,DWORD PTR [EBX+8]
          je L_448a50
L_448a3b:
          xor EAX,EAX
L_448a3d:
          mov DWORD PTR [EBX],EDX
          mov DWORD PTR [EBX+4],0
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_448a50:
          test EAX,264
          je L_448a3b
          mov EBP,DWORD PTR [EBX]
          sub EBP,EDX
          mov EDI,EBP
          sar EDI,31
          cmp EDI,0
          jl L_448a3b
          jle L_448ac0
L_448a67:
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+28],EDX
          call FUN_449238
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDX
          call FUN_4491b8
          mov ECX,EAX
          xor EBP,EAX
          mov EAX,EDI
          sar ECX,31
          xor EAX,ECX
          or EAX,EBP
          jne L_448ad0
          mov EDX,DWORD PTR [EBX+12]
          mov EAX,EDX
          and EAX,128
          jne L_448ab0
          mov EDX,DWORD PTR [EBX+8]
          jmp L_448a3d
L_448aa7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_448ab0:
          and EDX,4294967293
          xor EAX,EAX
          mov DWORD PTR [EBX+12],EDX
          mov EDX,DWORD PTR [EBX+8]
          jmp L_448a3d
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_448ac0:
          cmp EBP,0
          jbe L_448a3b
          jmp L_448a67
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_448ad0:
          or DWORD PTR [EBX+12],32
          mov EDX,DWORD PTR [EBX+8]
          mov EAX,4294967295
          jmp L_448a3d
L_448ae1:
          jmp _fseeko64
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
_fseeko64:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EDX,DWORD PTR [ESP+76]
          mov EBX,DWORD PTR [ESP+64]
          mov ESI,DWORD PTR [ESP+68]
          mov EDI,DWORD PTR [ESP+72]
          cmp EDX,1
          je L_448b35
          cmp EDX,2
          je L_448b53
          test EDX,EDX
          jne L_448b80
          lea EBP,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+24],ESI
          mov DWORD PTR [ESP+28],EDI
L_448b21:
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBX
          call FUN_449130
L_448b2d:
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_448b35:
          lea EBP,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EBP
          call FUN_449170
          test EAX,EAX
          jne L_448b92
          add DWORD PTR [ESP+24],ESI
          adc DWORD PTR [ESP+28],EDI
          jmp L_448b21
L_448b53:
          mov DWORD PTR [ESP],EBX
          lea EBP,DWORD PTR [ESP+24]
          call FUN_449180
          mov DWORD PTR [ESP],EBX
          call FUN_449238
          mov DWORD PTR [ESP],EAX
          call FUN_449240
          add ESI,EAX
          adc EDI,EDX
          mov DWORD PTR [ESP+24],ESI
          mov DWORD PTR [ESP+28],EDI
          jmp L_448b21
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_448b80:
          call FUN_449250
          mov DWORD PTR [EAX],22
          mov EAX,4294967295
          jmp L_448b2d
L_448b92:
          mov EAX,4294967295
          jmp L_448b2d
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_448ba0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EBX,DWORD PTR [ESP+64]
          call FUN_449250
          mov DWORD PTR [EAX],0
          mov DWORD PTR [ESP],EBX
          call FUN_449238
          mov DWORD PTR [ESP+24],EAX
          mov EAX,DWORD PTR [EBX+4]
          test EAX,EAX
          js L_448d20
L_448bcd:
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+12],1
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP],EAX
          call FUN_4491f8
          test EDX,EDX
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+20],EDX
          js L_448d61
          mov EAX,DWORD PTR [EBX+12]
          test EAX,264
          je L_448d00
          mov ECX,DWORD PTR [EBX]
          mov EDX,DWORD PTR [EBX+8]
          mov EDI,ECX
          sub EDI,EDX
          test AL,3
          mov DWORD PTR [ESP+28],EDI
          .byte 0x0f,0x85; .long L_448ca0-.-4   # jne L_448ca0
          test AL,128
          je L_448e40
L_448c2c:
          mov ESI,DWORD PTR [ESP+28]
L_448c30:
          mov EBP,DWORD PTR [ESP+20]
          mov EDI,DWORD PTR [ESP+16]
          mov ECX,EBP
          or ECX,EDI
          je L_448d30
          test AL,1
          je L_448d40
          mov ECX,DWORD PTR [EBX+4]
          test ECX,ECX
          je L_448d54
          mov EDI,DWORD PTR [ESP+28]
          add EDI,ECX
          mov ECX,DWORD PTR [ESP+24]
          mov EAX,ECX
          sar EAX,5
          mov EDX,EAX
          mov EBP,EAX
          mov EAX,ECX
          and EAX,31
          lea EAX,DWORD PTR [EAX+EAX*4]
          lea ECX,DWORD PTR [EAX*8]
          mov EAX,DWORD PTR [__pioinfo]
          mov EAX,DWORD PTR [EAX+EDX*4]
          cmp BYTE PTR [EAX+ECX*1+4],0
          js L_448d70
L_448c8a:
          mov ECX,EDI
          xor EBX,EBX
          mov EAX,ESI
          xor EDX,EDX
L_448c92:
          sub DWORD PTR [ESP+16],ECX
          sbb DWORD PTR [ESP+20],EBX
          jmp L_448d44
          .byte 0x90
L_448ca0:
          mov EBP,DWORD PTR [ESP+24]
          mov ESI,EBP
          sar ESI,5
          mov EDI,ESI
          mov ESI,EBP
          mov EBP,DWORD PTR [__pioinfo]
          and ESI,31
          lea ESI,DWORD PTR [ESI+ESI*4]
          shl ESI,3
          add ESI,DWORD PTR [EBP+EDI*4]
          mov EDI,ESI
          mov ESI,DWORD PTR [ESP+28]
          cmp BYTE PTR [EDI+4],0
          jns L_448c30
          cmp ECX,EDX
          jbe L_448c2c
          mov EBP,DWORD PTR [ESP+24]
          mov EDI,ECX
          .byte 0x66   # nop
          nop
L_448ce0:
          xor ECX,ECX
          cmp BYTE PTR [EDX],10
          sete CL
          add EDX,1
          add ESI,ECX
          cmp EDI,EDX
          jne L_448ce0
          mov DWORD PTR [ESP+24],EBP
          jmp L_448c30
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_448d00:
          mov EAX,DWORD PTR [EBX+4]
          mov EDI,DWORD PTR [ESP+16]
          mov EBP,DWORD PTR [ESP+20]
          cdq 
          sub EDI,EAX
          sbb EBP,EDX
          mov EAX,EDI
          mov EDX,EBP
L_448d14:
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_448d20:
          mov DWORD PTR [EBX+4],0
          jmp L_448bcd
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_448d30:
          add ESP,44
          mov EAX,ESI
          xor EDX,EDX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_448d40:
          mov EAX,ESI
          xor EDX,EDX
L_448d44:
          add EAX,DWORD PTR [ESP+16]
          adc EDX,DWORD PTR [ESP+20]
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_448d54:
          xor EAX,EAX
          xor EDX,EDX
          xor ECX,ECX
          xor EBX,EBX
          jmp L_448c92
L_448d61:
          mov EAX,4294967295
          mov EDX,4294967295
          jmp L_448d14
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_448d70:
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+12],2
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+28],ECX
          mov DWORD PTR [ESP],EAX
          call FUN_4491f8
          xor EAX,DWORD PTR [ESP+16]
          xor EDX,DWORD PTR [ESP+20]
          mov ECX,DWORD PTR [ESP+28]
          or EDX,EAX
          jne L_448ddb
          mov EAX,DWORD PTR [EBX+8]
          lea ECX,DWORD PTR [EAX+EDI*1]
          cmp EAX,ECX
          jae L_448dc3
L_448db2:
          xor EDX,EDX
          cmp BYTE PTR [EAX],10
          sete DL
          add EAX,1
          add EDI,EDX
          cmp ECX,EAX
          jne L_448db2
L_448dc3:
          test BYTE PTR [EBX+13],32
          je L_448c8a
          lea ECX,DWORD PTR [EDI+1]
          xor EBX,EBX
          mov EAX,ESI
          xor EDX,EDX
          jmp L_448c92
L_448ddb:
          mov EAX,DWORD PTR [ESP+16]
          mov EDX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+28],ECX
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP],EAX
          call FUN_4491f8
          cmp EDI,512
          mov ECX,DWORD PTR [ESP+28]
          ja L_448e21
          mov EAX,DWORD PTR [EBX+12]
          mov EDX,512
          and EAX,1032
          cmp EAX,8
          je L_448e24
L_448e21:
          mov EDX,DWORD PTR [EBX+24]
L_448e24:
          mov EAX,DWORD PTR [__pioinfo]
          mov EAX,DWORD PTR [EAX+EBP*4]
          test BYTE PTR [EAX+ECX*1+4],4
          jne L_448e5a
          mov ECX,EDX
          xor EBX,EBX
          mov EAX,ESI
          xor EDX,EDX
          jmp L_448c92
L_448e40:
          call FUN_449250
          mov EDX,4294967295
          mov DWORD PTR [EAX],22
          mov EAX,4294967295
          jmp L_448d14
L_448e5a:
          lea ECX,DWORD PTR [EDX+1]
          xor EBX,EBX
          mov EAX,ESI
          xor EDX,EDX
          jmp L_448c92
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_448e70:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EBX,DWORD PTR [ESP+48]
          mov ESI,DWORD PTR [ESP+52]
          mov EDI,DWORD PTR [ESP+56]
          mov EBP,DWORD PTR [ESP+60]
          call FUN_449250
          test EBX,EBX
          mov DWORD PTR [EAX],0
          je L_448f33
          cmp EBP,2
          ja L_448f33
          and DWORD PTR [EBX+12],4294967279
          cmp EBP,1
          je L_448f20
L_448eac:
          mov DWORD PTR [ESP],EBX
          call FUN_448a20
          mov EAX,DWORD PTR [EBX+12]
          test AL,128
          jne L_448f00
          mov EDX,EAX
          and EDX,9
          cmp EDX,9
          je L_448f10
L_448ec5:
          mov DWORD PTR [ESP],EBX
          call FUN_449238
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP],EAX
          call FUN_4491f8
          and EAX,EDX
          cmp EAX,-1
          sete AL
          movzx EAX,AL
          neg EAX
L_448eee:
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
L_448f00:
          and EAX,4294967292
          mov DWORD PTR [EBX+12],EAX
          jmp L_448ec5
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_448f10:
          test AH,4
          jne L_448ec5
          mov DWORD PTR [EBX+24],512
          jmp L_448ec5
          .byte 0x66
          .byte 0x90
L_448f20:
          mov DWORD PTR [ESP],EBX
          call FUN_448ba0
          add ESI,EAX
          adc EDI,EDX
          xor EBP,EBP
          .byte 0xe9; .long L_448eac-.-4   # jmp L_448eac
L_448f33:
          call FUN_449250
          mov DWORD PTR [EAX],22
          mov EAX,4294967295
          jmp L_448eee
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
L_448f50:
          push ESI
          push EBX
          xor EBX,EBX
          sub ESP,4
          mov ESI,DWORD PTR [ESP+16]
          call FUN_449288
          mov DWORD PTR [EAX],ESI
          mov EAX,1
          jmp L_448f84
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_448f70:
          add EBX,1
          cmp DWORD PTR [EBX*8+L_4635a4],-1
          je L_448fa0
          mov EAX,DWORD PTR [EBX*8+L_4635a0]
L_448f84:
          cmp ESI,EAX
          jne L_448f70
          call FUN_449250
          mov EDX,DWORD PTR [EBX*8+L_4635a4]
          mov DWORD PTR [EAX],EDX
          add ESP,4
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_448fa0:
          lea EAX,DWORD PTR [ESI-19]
          cmp EAX,17
          jbe L_448fd5
          sub ESI,188
          cmp ESI,14
          jbe L_448fc4
          call FUN_449250
          mov DWORD PTR [EAX],22
          add ESP,4
          pop EBX
          pop ESI
          ret 
L_448fc4:
          call FUN_449250
          mov DWORD PTR [EAX],8
          add ESP,4
          pop EBX
          pop ESI
          ret 
L_448fd5:
          call FUN_449250
          mov DWORD PTR [EAX],13
          add ESP,4
          pop EBX
          pop ESI
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

.section .rdata,"dr"
.p2align 5
L_4635a0:
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4635a4:
          .byte 0x16
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x16
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x16
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x11
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x12
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x12
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x21
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x35
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x11
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x52
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x53
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x57
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x16
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x59
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x72
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x16
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x81
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x82
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x83
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x16
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x84
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x91
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x29
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x11
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xce
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
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
          .long FUN_448a20 - .
          .byte 0xc1
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
          .byte 0x62
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _fseeko64 - .
          .byte 0xa9
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
          .byte 0x79
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
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_448ba0 - .
          .byte 0xc8
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
          .byte 0x70
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
          .byte 0x45
          .byte 0xb
          .byte 0x53
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
          .byte 0x45
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
          .byte 0x41
          .byte 0xb
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_448e70 - .
          .byte 0xd5
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
          .byte 0x7a
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
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_448f50 - .
          .byte 0x96
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
          .byte 0x10
          .byte 0x2
          .byte 0x42
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x45
          .byte 0xb
          .byte 0x61
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x4e
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x4e
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
