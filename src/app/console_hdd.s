# app/console_hdd.s -- manifest + avatar/kinect data to console HDD, remote dirs
#
# original placement:
#   .bss           004795a0-004796a0
#   .eh_frame      0046af40-0046b300
#   .rdata         0045bdb4-0045c654
#   .rdata$zzz     00463b40-00463b6c
#   .text          00431c20-00433570

.intel_syntax noprefix
.globl FUN_432b10
.globl FUN_432e50
.globl FUN_433440
.globl L_432aa0

.text
.p2align 4
FUN_431c20:
          push EDI
          push ESI
          push EBX
          xor EBX,EBX
          sub ESP,288
          mov EAX,DWORD PTR [L_4795a0]
          lea ESI,DWORD PTR [ESP+28]
          test EAX,EAX
          jne L_431c63
          .byte 0xe9; .long L_431cc0-.-4   # jmp L_431cc0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_431c40:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_45bdf0
          add EBX,1
          mov DWORD PTR [ESP],1
          call _log_printf
          cmp EBX,DWORD PTR [L_4795a0]
          jae L_431cc0
L_431c63:
          mov EAX,DWORD PTR [EBX*4+L_4795c0]
          mov DWORD PTR [ESP+8],OFFSET L_45bdb4
          mov DWORD PTR [ESP+4],OFFSET L_45bdb9
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+12],EAX
          call _sprintf
          mov DWORD PTR [ESP],ESI
          call FUN_420710
          test EAX,EAX
          jne L_431c40
L_431c92:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_45bdc4
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,288
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_431cc0:
          mov EBX,OFFSET L_45c644
          mov EDI,OFFSET L_45c644+16
L_431cca:
          mov DWORD PTR [ESP+8],OFFSET L_45bdb4
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call _sprintf
          mov DWORD PTR [ESP],ESI
          call FUN_420710
          test EAX,EAX
          je L_431c92
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_45bdf0
          add EBX,4
          mov DWORD PTR [ESP],1
          call _log_printf
          cmp EDI,EBX
          jne L_431cca
          add ESP,288
          mov EAX,1
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
L_431d20:
          mov EDX,DWORD PTR [L_4795a0]
          mov ECX,DWORD PTR [ESP+4]
          test EDX,EDX
          je L_431d62
          xor EAX,EAX
          cmp ECX,DWORD PTR [L_4795c0]
          jne L_431d49
          jmp L_431d69
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_431d40:
          cmp DWORD PTR [EAX*4+L_4795c0],ECX
          je L_431d60
L_431d49:
          add EAX,1
          cmp EAX,EDX
          jne L_431d40
          lea EAX,DWORD PTR [EDX+1]
L_431d53:
          mov DWORD PTR [EDX*4+L_4795c0],ECX
          mov DWORD PTR [L_4795a0],EAX
          ret 
L_431d60:
          repz ret 
L_431d62:
          mov EAX,1
          jmp L_431d53
L_431d69:
          repz ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_431d70:
          push ESI
          push EBX
          sub ESP,68
          mov EBX,DWORD PTR [ESP+80]
          mov EAX,DWORD PTR [EBX+328]
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          cmp EAX,3
          jne L_431e32
          mov EAX,DWORD PTR [EBX+312]
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          cmp EAX,2020833645
          je L_431de6
          cmp EAX,2020568685
          jne L_431f00
L_431de6:
          mov EAX,DWORD PTR [EBX]
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          cmp EAX,1481461328
          je L_431e50
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45be4c
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
L_431e2c:
          add ESP,68
          pop EBX
          pop ESI
          ret 
L_431e32:
          mov DWORD PTR [ESP+4],OFFSET L_45be01
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,68
          xor EAX,EAX
          pop EBX
          pop ESI
          ret 
          .byte 0x66   # nop
          nop
L_431e50:
          mov EAX,DWORD PTR [EBX+316]
          lea ESI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+24],ESI
          mov DWORD PTR [ESP+12],0
          mov EDX,EAX
          mov ECX,EAX
          mov DWORD PTR [ESP+8],0
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [EBX+312]
          add EBX,36
          mov DWORD PTR [ESP],EAX
          call _XeCryptSha
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call _memcmp
          mov EDX,EAX
          mov EAX,1
          test EDX,EDX
          je L_431e2c
          mov DWORD PTR [ESP+4],OFFSET L_45be72
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
          jmp L_431e2c
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_431f00:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45be18
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,68
          xor EAX,EAX
          pop EBX
          pop ESI
          ret 
L_431f20:
          push ESI
          push EBX
          sub ESP,20
          mov ESI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],ESI
          call _getBeU16
          test AX,AX
          jne L_431f54
          mov DWORD PTR [ESP+4],OFFSET L_45be8d
          mov DWORD PTR [ESP],1
          xor EBX,EBX
          call _log_printf
          add ESP,20
          mov EAX,EBX
          pop EBX
          pop ESI
          ret 
L_431f54:
          movzx EBX,AX
          mov EAX,DWORD PTR [ESP+36]
          add ESI,2
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+36]
          mov BYTE PTR [EAX+EBX*1],0
          add ESP,20
          mov EAX,EBX
          pop EBX
          pop ESI
          ret 
          .byte 0x66
          .byte 0x90
FUN_431f80:
          push ESI
          push EBX
          sub ESP,68
          mov ESI,DWORD PTR [ESP+84]
          test ESI,ESI
          je L_432065
          lea EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP],EAX
          call _FileToBuffer
          test EAX,EAX
          mov EBX,EAX
          je L_432096
          mov EAX,DWORD PTR [ESP+40]
          cmp EAX,ESI
          jne L_432030
          lea ESI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+24],ESI
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP],EBX
          call _XeCryptSha
          mov EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call _memcmp
          test EAX,EAX
          jne L_432080
          mov DWORD PTR [ESP+4],OFFSET L_45be9b
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,68
          mov EAX,EBX
          pop EBX
          pop ESI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_432030:
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45bec8
          mov DWORD PTR [ESP],1
          call _log_printf
L_43204c:
          mov DWORD PTR [ESP],EBX
          call _free
L_432054:
          xor EBX,EBX
          add DWORD PTR [L_479684],1
          add ESP,68
          mov EAX,EBX
          pop EBX
          pop ESI
          ret 
L_432065:
          mov DWORD PTR [ESP+4],OFFSET L_45bf01
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_432054
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_432080:
          mov DWORD PTR [ESP+4],OFFSET L_45bea4
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_43204c
L_432096:
          mov DWORD PTR [ESP+4],OFFSET L_45beeb
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_432054
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4320b0:
          push ESI
          push EBX
          sub ESP,68
          mov ESI,DWORD PTR [ESP+84]
          test ESI,ESI
          je L_432170
          lea EBX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EBX
          call _stfsInit
          mov EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+20],EAX
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],EAX
          call _stfsLoad
          test EAX,EAX
          je L_43214c
          cmp DWORD PTR [ESP+52],ESI
          jne L_432130
          mov DWORD PTR [ESP+4],OFFSET L_45bf1a
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+44]
          add ESP,68
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_432130:
          mov DWORD PTR [ESP+4],OFFSET L_45bf21
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],EBX
          call _stfsFree
L_43214c:
          mov DWORD PTR [ESP+4],OFFSET L_45bf21
          mov DWORD PTR [ESP],1
          call _log_printf
L_432160:
          add DWORD PTR [L_479684],1
          add ESP,68
          xor EAX,EAX
          pop EBX
          pop ESI
          ret 
          .byte 0x90
L_432170:
          mov DWORD PTR [ESP+4],OFFSET L_45bf2d
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_432160
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_432190:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1628
          mov EBP,DWORD PTR [ESP+1652]
          mov EAX,DWORD PTR [EBP+44]
          mov DWORD PTR [ESP+4],OFFSET L_45bf4c
          mov DWORD PTR [ESP],1
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [EBP+44]
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EDX,EAX
          je L_43233d
          cmp DWORD PTR [L_4ce068],255
          jg L_43233d
          lea EBX,DWORD PTR [EBP+104]
          mov DWORD PTR [ESP+36],0
          jmp L_432285
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_432230:
          mov EAX,DWORD PTR [EBX-56]
          test EAX,EAX
          jne L_4322d0
L_43223b:
          mov EAX,DWORD PTR [EBP+44]
          add DWORD PTR [ESP+36],1
          mov EDI,DWORD PTR [ESP+36]
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          cmp EAX,EDI
          jbe L_43233d
          add EBX,96
          cmp DWORD PTR [L_4ce068],255
          jg L_43233d
L_432285:
          mov EAX,DWORD PTR [EBX-44]
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EDX,EAX
          mov DWORD PTR [ESP+40],EDX
          je L_432230
          mov EAX,EDX
          add EAX,EBP
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          mov DWORD PTR [ESP+40],EAX
          mov EAX,DWORD PTR [EBX-56]
          test EAX,EAX
          je L_43223b
L_4322d0:
          mov ESI,EAX
          mov EDX,EAX
          shl ESI,24
          shr EDX,24
          add EDX,ESI
          mov ESI,EAX
          shr EAX,8
          shl ESI,8
          and EAX,65280
          and ESI,16711680
          add ESI,EDX
          add EAX,ESI
          lea ESI,DWORD PTR [EBP+EAX*1]
          mov DWORD PTR [ESP],ESI
          call _getBeU16
          test AX,AX
          jne L_432350
          mov DWORD PTR [ESP+4],OFFSET L_45be8d
          mov DWORD PTR [ESP],1
          mov EDI,OFFSET L_45bf73
          call _log_printf
          lea EAX,DWORD PTR [ESP+80]
          mov ECX,6
          mov DWORD PTR [ESP+44],EAX
          mov ESI,EAX
          repe cmpsb BYTE PTR [ESI],BYTE PTR ES:[EDI]
          jne L_432385
L_432330:
          mov EAX,DWORD PTR [L_479684]
          test EAX,EAX
          je L_43223b
L_43233d:
          add ESP,1628
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
L_432350:
          movzx EDI,AX
          lea EAX,DWORD PTR [ESP+80]
          add ESI,2
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+44],EAX
          call _memcpy
          mov ESI,DWORD PTR [ESP+44]
          mov BYTE PTR [ESP+EDI*1+80],0
          mov ECX,6
          mov EDI,OFFSET L_45bf73
          repe cmpsb BYTE PTR [ESI],BYTE PTR ES:[EDI]
          je L_432330
L_432385:
          mov EAX,DWORD PTR [ESP+1648]
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+592]
          mov DWORD PTR [ESP],EAX
          call _strcpy
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+592]
          mov DWORD PTR [ESP],EAX
          call _strcat
          lea EAX,DWORD PTR [ESP+592]
          mov DWORD PTR [ESP+4],OFFSET L_45bf79
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [L_4ce068]
          add EAX,1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov ECX,DWORD PTR [EBX-24]
          mov EAX,ECX
          mov EDX,ECX
          mov ESI,ECX
          shl EAX,24
          shr EDX,24
          shl ESI,8
          add EDX,EAX
          and ESI,16711680
          shr ECX,8
          lea EAX,DWORD PTR [EDX+ESI*1]
          and ECX,65280
          lea ESI,DWORD PTR [EAX+ECX*1]
          add ESI,EBP
          mov DWORD PTR [ESP],ESI
          call _getBeU16
          test AX,AX
          jne L_432580
          mov DWORD PTR [ESP+4],OFFSET L_45be8d
          mov DWORD PTR [ESP],1
          call _log_printf
L_432431:
          mov EAX,DWORD PTR [EBX-32]
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          cmp EAX,2
          je L_4325a4
          cmp EAX,3
          jne L_432330
          mov EAX,DWORD PTR [EBX-48]
          mov DWORD PTR [ESP+8],EBX
          mov ESI,DWORD PTR [L_4ce068]
          mov ECX,EAX
          mov EDX,EAX
          shr EDX,24
          shl ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+592]
          imul ESI,ESI,1032
          mov DWORD PTR [ESP],EAX
          call FUN_431f80
          imul EDI,DWORD PTR [L_4ce068],1032
          mov DWORD PTR [ESI+L_4ce06c],EAX
          mov EDX,DWORD PTR [EDI+L_4ce06c]
          test EDX,EDX
          je L_432330
          mov EAX,DWORD PTR [EBX-48]
          mov ESI,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+8],OFFSET L_45bdb4
          mov DWORD PTR [ESP+4],OFFSET L_45bfb0
          mov ECX,EAX
          mov EDX,EAX
          mov DWORD PTR [ESP+12],ESI
          shr EDX,24
          shl ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EDX,EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [EDI+L_4ce06c+4],EDX
          add EDI,OFFSET L_4ce074
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+16],EAX
          call _sprintf
          cmp ESI,DWORD PTR [ESP+1660]
          je L_432574
          mov EDX,DWORD PTR [L_4795a0]
          test EDX,EDX
          je L_432789
          cmp ESI,DWORD PTR [L_4795c0]
          je L_432574
          xor EAX,EAX
          mov ECX,DWORD PTR [ESP+40]
          jmp L_43255a
L_432551:
          cmp ECX,DWORD PTR [EAX*4+L_4795c0]
          je L_432574
L_43255a:
          add EAX,1
          cmp EDX,EAX
          jne L_432551
          lea EAX,DWORD PTR [EDX+1]
L_432564:
          mov EDI,DWORD PTR [ESP+40]
          mov DWORD PTR [L_4795a0],EAX
          mov DWORD PTR [EDX*4+L_4795c0],EDI
L_432574:
          add DWORD PTR [L_4ce068],1
          jmp L_432330
L_432580:
          movzx EDI,AX
          mov EAX,DWORD PTR [ESP+44]
          add ESI,2
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov BYTE PTR [ESP+EDI*1+80],0
          jmp L_432431
L_4325a4:
          mov EAX,DWORD PTR [EBX-48]
          mov EDI,DWORD PTR [L_4ce068]
          lea ESI,DWORD PTR [EBX-20]
          mov ECX,EAX
          mov EDX,EAX
          shr EDX,24
          shl ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EDX,EAX
          mov DWORD PTR [ESP+40],EDX
          je L_432773
          lea EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],EAX
          call _stfsInit
          lea EAX,DWORD PTR [ESP+592]
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],ESI
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP],EAX
          call _stfsLoad
          test EAX,EAX
          je L_432751
          mov EDX,DWORD PTR [ESP+40]
          cmp EDX,DWORD PTR [ESP+68]
          jne L_432731
          mov DWORD PTR [ESP+4],OFFSET L_45bf1a
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDX,DWORD PTR [ESP+60]
L_432652:
          imul EAX,EDI,1032
          imul EDI,DWORD PTR [L_4ce068],1032
          mov DWORD PTR [EAX+L_4ce06c],EDX
          mov ECX,DWORD PTR [EDI+L_4ce06c]
          test ECX,ECX
          je L_432330
          mov EAX,DWORD PTR [EBX-48]
          mov ESI,DWORD PTR [ESP+44]
          mov ECX,EAX
          mov EDX,EAX
          shr EDX,24
          shl ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EDX,EAX
          mov EAX,DWORD PTR [EBX+24]
          mov DWORD PTR [EDI+L_4ce06c+4],EDX
          mov EDX,DWORD PTR [EBX+20]
          add EDI,OFFSET L_4ce074
          mov DWORD PTR [ESP+24],ESI
          mov DWORD PTR [ESP+12],OFFSET L_45bf83
          mov DWORD PTR [ESP+8],OFFSET L_45bdb4
          mov DWORD PTR [ESP+4],OFFSET L_45bf9d
          mov ESI,EDX
          mov ECX,EDX
          mov DWORD PTR [ESP],EDI
          shr ECX,24
          shl ESI,24
          add ESI,ECX
          mov ECX,EDX
          shr EDX,8
          shl ECX,8
          and EDX,65280
          and ECX,16711680
          add ECX,ESI
          add ECX,EDX
          mov EDX,EAX
          mov DWORD PTR [ESP+20],ECX
          mov ECX,EAX
          shr EDX,24
          shl ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          mov DWORD PTR [ESP+16],EAX
          call _sprintf
          add DWORD PTR [L_4ce068],1
          jmp L_432330
L_432731:
          mov DWORD PTR [ESP+4],OFFSET L_45bf21
          mov DWORD PTR [ESP],1
          call _log_printf
          lea EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],EAX
          call _stfsFree
L_432751:
          mov DWORD PTR [ESP+4],OFFSET L_45bf21
          mov DWORD PTR [ESP],1
          call _log_printf
L_432765:
          add DWORD PTR [L_479684],1
          xor EDX,EDX
          jmp L_432652
L_432773:
          mov DWORD PTR [ESP+4],OFFSET L_45bf2d
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_432765
L_432789:
          mov EAX,1
          jmp L_432564
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
FUN_4327a0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EBX,DWORD PTR [ESP+104]
          mov ESI,DWORD PTR [ESP+100]
          lea EAX,DWORD PTR [EBX-356]
          cmp EAX,65180
          ja L_4328a5
          mov EAX,DWORD PTR [ESI+328]
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          cmp EAX,3
          jne L_432873
          mov EAX,DWORD PTR [ESI+312]
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          cmp EAX,2020833645
          je L_43282d
          cmp EAX,2020568685
          jne L_4329f0
L_43282d:
          mov EAX,DWORD PTR [ESI]
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          cmp EAX,1481461328
          je L_4328d0
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45be4c
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_432887
L_432873:
          mov DWORD PTR [ESP+4],OFFSET L_45be01
          mov DWORD PTR [ESP],1
          call _log_printf
L_432887:
          mov DWORD PTR [ESP+4],OFFSET L_45c088
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
L_43289d:
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4328a5:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45bfbc
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,76
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4328c7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4328d0:
          mov EAX,DWORD PTR [ESI+316]
          lea EBP,DWORD PTR [ESP+44]
          lea EDI,DWORD PTR [ESI+312]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+24],EBP
          mov DWORD PTR [ESP+16],0
          mov EDX,EAX
          mov ECX,EAX
          mov DWORD PTR [ESP+12],0
          shl EDX,24
          shr ECX,24
          mov DWORD PTR [ESP+8],0
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          mov DWORD PTR [ESP],EDI
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          mov DWORD PTR [ESP+4],EAX
          call _XeCryptSha
          lea EAX,DWORD PTR [ESI+36]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+4],EAX
          call _memcmp
          test EAX,EAX
          jne L_432a80
          mov EAX,DWORD PTR [ESI+332]
          mov DWORD PTR [ESP+4],OFFSET L_45c0a8
          mov DWORD PTR [ESP],1
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          mov EDX,EAX
          mov DWORD PTR [L_479680],EAX
          and EDX,15
          mov DWORD PTR [ESP+20],EDX
          mov EDX,EAX
          shr EDX,8
          movzx EDX,DX
          mov DWORD PTR [ESP+16],EDX
          mov EDX,EAX
          shr EAX,28
          shr EDX,24
          mov DWORD PTR [ESP+8],EAX
          and EDX,15
          mov DWORD PTR [ESP+12],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+108]
          cmp DWORD PTR [L_479680],EAX
          je L_432a10
          mov DWORD PTR [ESP+4],OFFSET L_45bfdc
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,76
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_4329f0:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45be18
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_432887
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_432a10:
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+96]
          sub EBX,312
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          call FUN_432190
          mov EAX,DWORD PTR [L_479684]
          test EAX,EAX
          je L_432a52
          mov DWORD PTR [ESP+4],OFFSET L_45c024
          mov DWORD PTR [ESP],0
          call _log_printf
          xor EAX,EAX
          jmp L_43289d
L_432a52:
          mov EAX,DWORD PTR [L_4ce068]
          mov DWORD PTR [ESP+4],OFFSET L_45c064
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,1
          jmp L_43289d
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_432a80:
          mov DWORD PTR [ESP+4],OFFSET L_45be72
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_432887
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_432aa0:
          push ESI
          push EBX
          sub ESP,20
          mov EAX,DWORD PTR [L_4cdc60]
          test EAX,EAX
          je L_432ab6
          mov DWORD PTR [ESP],EAX
          call _free
L_432ab6:
          mov EDX,DWORD PTR [L_4ce068]
          test EDX,EDX
          jle L_432afe
          mov EBX,OFFSET L_4ce06c
          xor ESI,ESI
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_432ad0:
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_432ae4
          mov DWORD PTR [ESP],EAX
          call _free
          mov EDX,DWORD PTR [L_4ce068]
L_432ae4:
          add ESI,1
          mov DWORD PTR [EBX],0
          mov DWORD PTR [EBX+4],0
          add EBX,1032
          cmp EDX,ESI
          jg L_432ad0
L_432afe:
          add ESP,20
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
          .byte 0xbf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_432b10:
          push EDI
          push ESI
          push EBX
          sub ESP,2064
          mov EAX,DWORD PTR [ESP+2080]
          lea EBX,DWORD PTR [ESP+1040]
          lea ESI,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _strcpy
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call _strcpy
          mov EDX,EBX
L_432b45:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_432b45
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          mov DWORD PTR [EDX],1953724787
          mov DWORD PTR [EDX+4],1831759205
          mov DWORD PTR [EDX+8],1718185569
          mov DWORD PTR [EDX+12],7631717
          mov DWORD PTR [ESP+8],265228
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4cdc60
          call _memset
          mov DWORD PTR [ESP],EBX
          call _FileExists
          test EAX,EAX
          je L_432c20
L_432bb8:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45c12c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_4ce064
          mov DWORD PTR [ESP],EBX
          call _FileToBuffer
          test EAX,EAX
          mov DWORD PTR [L_4cdc60],EAX
          je L_432bf6
          mov EAX,DWORD PTR [L_4ce064]
          test EAX,EAX
          jne L_432d10
L_432bf6:
          mov DWORD PTR [ESP+4],OFFSET L_45c144
          mov DWORD PTR [ESP],0
          xor EDI,EDI
          call _log_printf
L_432c0c:
          add ESP,2064
          mov EAX,EDI
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
L_432c20:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45c0d8
          mov EDI,ESI
          mov DWORD PTR [ESP],1
          call _log_printf
L_432c3a:
          mov EDX,DWORD PTR [EDI]
          add EDI,4
          lea EAX,DWORD PTR [EDX-16843009]
          not EDX
          and EAX,EDX
          and EAX,2155905152
          je L_432c3a
          mov EDX,EAX
          shr EDX,16
          test EAX,32896
          cmove EAX,EDX
          lea EDX,DWORD PTR [EDI+2]
          mov ECX,EAX
          cmove EDI,EDX
          add CL,AL
          mov EDX,12133
          sbb EDI,3
          sub EDI,ESI
          lea EAX,DWORD PTR [ESI+EDI*1]
          mov WORD PTR [EAX+12],DX
          mov DWORD PTR [EAX],1937330980
          mov DWORD PTR [EAX+4],1433232756
          mov DWORD PTR [EAX+8],1952539760
          mov BYTE PTR [EAX+14],0
          lea EAX,DWORD PTR [EDI+15]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call _memcpy
          lea EAX,DWORD PTR [EBX+EDI*1+14]
          mov DWORD PTR [EAX],1953724787
          mov DWORD PTR [EAX+4],1831759205
          mov DWORD PTR [EAX+8],1718185569
          mov DWORD PTR [EAX+12],7631717
          mov DWORD PTR [ESP],EBX
          call _FileExists
          test EAX,EAX
          mov EDI,EAX
          jne L_432bb8
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45c0d8
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_45c0f4
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,2064
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_432d10:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45c17c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+2084]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [L_4ce064]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [L_4cdc60]
          mov DWORD PTR [ESP+4],EAX
          call FUN_4327a0
          mov DWORD PTR [ESP+8],OFFSET L_45bdb4
          mov EDI,EAX
          mov DWORD PTR [ESP+4],OFFSET L_45c1a0
          mov DWORD PTR [ESP],OFFSET L_4cdc64
          call _sprintf
          test EDI,EDI
          jne L_432c0c
          mov EAX,DWORD PTR [L_4cdc60]
          test EAX,EAX
          je L_432d84
          mov DWORD PTR [ESP],EAX
          call _free
L_432d84:
          mov EDX,DWORD PTR [L_4ce068]
          test EDX,EDX
          jle L_432c0c
          mov EBX,OFFSET L_4ce06c
          xor ESI,ESI
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_432da0:
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_432db4
          mov DWORD PTR [ESP],EAX
          call _free
          mov EDX,DWORD PTR [L_4ce068]
L_432db4:
          add ESI,1
          mov DWORD PTR [EBX],0
          mov DWORD PTR [EBX+4],0
          add EBX,1032
          cmp ESI,EDX
          jl L_432da0
          add ESP,2064
          mov EAX,EDI
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
L_432de0:
          sub ESP,28
          call FUN_4205d0
          test EAX,EAX
          je L_432e10
          mov DWORD PTR [ESP+4],OFFSET L_45c1b4
          mov DWORD PTR [ESP],OFFSET L_45bdb4
          call FUN_41faf0
          test EAX,EAX
          je L_432e30
          add ESP,28
          jmp FUN_431c20
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_432e10:
          mov DWORD PTR [ESP+4],OFFSET L_45c1e8
          mov DWORD PTR [ESP],0
          call _log_printf
          xor EAX,EAX
          add ESP,28
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_432e30:
          mov DWORD PTR [ESP+4],OFFSET L_45c1bc
          mov DWORD PTR [ESP],0
          call _log_printf
          xor EAX,EAX
          add ESP,28
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_432e50:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          call FUN_41ed50
          mov DWORD PTR [ESP+4],OFFSET L_45c212
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EDX,DWORD PTR [ESP+68]
          mov ECX,DWORD PTR [L_4795a0]
          and EDX,4294967280
          test ECX,ECX
          je L_433122
          xor EAX,EAX
          cmp EDX,DWORD PTR [L_4795c0]
          jne L_432e9a
          jmp L_432eb0
L_432e91:
          cmp EDX,DWORD PTR [EAX*4+L_4795c0]
          je L_432eb0
L_432e9a:
          add EAX,1
          cmp EAX,ECX
          jne L_432e91
          lea EAX,DWORD PTR [ECX+1]
L_432ea4:
          mov DWORD PTR [ECX*4+L_4795c0],EDX
          mov DWORD PTR [L_4795a0],EAX
L_432eb0:
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EAX
          call FUN_432b10
          test EAX,EAX
          je L_432f70
          mov DWORD PTR [ESP+4],OFFSET L_45c22c
          mov DWORD PTR [ESP],0
          call _log_printf
          call FUN_4205d0
          test EAX,EAX
          jne L_432f93
          mov DWORD PTR [ESP+4],OFFSET L_45c1e8
          mov DWORD PTR [ESP],0
          mov EDI,1
          call _log_printf
L_432f02:
          mov DWORD PTR [ESP],OFFSET L_45bdb4
          call FUN_41fc30
          mov EAX,DWORD PTR [L_4cdc60]
          test EAX,EAX
          je L_432f1f
          mov DWORD PTR [ESP],EAX
          call _free
L_432f1f:
          mov EDX,DWORD PTR [L_4ce068]
          test EDX,EDX
          jle L_432f89
          mov EBX,OFFSET L_4ce06c
          xor ESI,ESI
L_432f30:
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_432f44
          mov DWORD PTR [ESP],EAX
          call _free
          mov EDX,DWORD PTR [L_4ce068]
L_432f44:
          add ESI,1
          mov DWORD PTR [EBX],0
          mov DWORD PTR [EBX+4],0
          add EBX,1032
          cmp EDX,ESI
          jg L_432f30
          add ESP,44
          mov EAX,EDI
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
L_432f70:
          mov DWORD PTR [ESP+4],OFFSET L_45c354
          mov DWORD PTR [ESP],0
          mov EDI,1
          call _log_printf
L_432f89:
          add ESP,44
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_432f93:
          mov DWORD PTR [ESP+4],OFFSET L_45c1b4
          mov DWORD PTR [ESP],OFFSET L_45bdb4
          call FUN_41faf0
          test EAX,EAX
          je L_4330e1
          call FUN_431c20
          test EAX,EAX
          je L_4330ba
          mov DWORD PTR [ESP+4],OFFSET L_45c254
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_4ce068]
          mov DWORD PTR [ESP+4],OFFSET L_45c287
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [L_4ce068]
          test EAX,EAX
          jle L_433063
          xor EBP,EBP
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_433000:
          imul EBX,EBP,1032
          add EBP,1
          mov DWORD PTR [ESP+4],OFFSET L_45c2bc
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP],1
          mov EAX,DWORD PTR [EBX+L_4ce06c+4]
          lea ESI,DWORD PTR [EBX+L_4ce074]
          mov DWORD PTR [ESP+20],ESI
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          mov EAX,DWORD PTR [EBX+L_4ce06c+4]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [EBX+L_4ce06c]
          mov DWORD PTR [ESP+4],EAX
          call FUN_420470
          test EAX,EAX
          mov EDI,EAX
          je L_4330c4
          cmp EBP,DWORD PTR [L_4ce068]
          jl L_433000
L_433063:
          mov DWORD PTR [ESP+8],OFFSET L_4cdc64
          mov DWORD PTR [ESP+4],OFFSET L_45c2a1
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_4ce064]
          mov DWORD PTR [ESP],OFFSET L_4cdc64
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [L_4cdc60]
          mov DWORD PTR [ESP+4],EAX
          call FUN_420470
          test EAX,EAX
          je L_4330ff
          mov DWORD PTR [ESP+4],OFFSET L_45c318
          mov DWORD PTR [ESP],0
          call _log_printf
          call FUN_41ed70
L_4330ba:
          mov EDI,1
          jmp L_432f02
L_4330c4:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_45c2e4
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_432f02
L_4330e1:
          mov DWORD PTR [ESP+4],OFFSET L_45c1bc
          mov DWORD PTR [ESP],0
          mov EDI,1
          call _log_printf
          jmp L_432f02
L_4330ff:
          mov DWORD PTR [ESP+8],OFFSET L_4cdc64
          mov DWORD PTR [ESP+4],OFFSET L_45c2e4
          xor EDI,EDI
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_432f02
L_433122:
          mov EAX,1
          jmp L_432ea4
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_433130:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,2396
          mov EAX,DWORD PTR [ESP+2416]
          lea EBX,DWORD PTR [ESP+336]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _strcpy
          mov EDX,EBX
L_433156:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_433156
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,12079
          sbb EDX,3
          mov WORD PTR [EDX],AX
          mov BYTE PTR [EDX+2],0
          mov DWORD PTR [ESP],EBX
          call FUN_4481c0
          test EAX,EAX
          mov DWORD PTR [ESP+28],EAX
          je L_4333fc
          lea EBX,DWORD PTR [ESP+76]
          lea EDI,DWORD PTR [ESP+1360]
L_4331b1:
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_448360
          test EAX,EAX
          mov ESI,EAX
          je L_4333c0
          mov EAX,DWORD PTR [ESP+2420]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _strcpy
          mov EDX,EBX
L_4331dc:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_4331dc
          mov ECX,EAX
          lea EBP,DWORD PTR [ESI+8]
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          sub EDX,EBX
          lea EAX,DWORD PTR [EBX+EDX*1+1]
          mov BYTE PTR [EBX+EDX*1],92
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          call _strcpy
          mov EAX,DWORD PTR [ESP+2416]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call _strcpy
          mov EDX,EDI
L_43323a:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_43323a
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          sub EDX,EDI
          lea EAX,DWORD PTR [EDI+EDX*1+1]
          mov BYTE PTR [EDI+EDX*1],92
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          call _strcpy
          lea EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call FUN_448820
          test EAX,EAX
          js L_4331b1
          movzx EAX,WORD PTR [ESP+46]
          test AH,64
          je L_433300
          cmp BYTE PTR [ESI+8],46
          je L_4331b1
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45c38e
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],EBX
          call FUN_420710
          test EAX,EAX
          je L_4333dc
          mov DWORD PTR [ESP+4],OFFSET L_45c3b0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EDI
          call FUN_433130
          jmp L_4331b1
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_433300:
          test AX,AX
          jns L_4331b1
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_45c3ba
          mov DWORD PTR [ESP],1
          call _log_printf
          lea EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call _FileToBuffer
          test EAX,EAX
          mov ESI,EAX
          je L_4331b1
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_45c3d2
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45c3ed
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_420470
          test EAX,EAX
          je L_433409
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45c420
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov DWORD PTR [ESP],ESI
          call _free
          jmp L_4331b1
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4333c0:
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_448470
          add ESP,2396
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4333dc:
          mov DWORD PTR [ESP+4],OFFSET L_45c3a7
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_448470
L_4333fc:
          xor EAX,EAX
L_4333fe:
          add ESP,2396
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_433409:
          mov DWORD PTR [ESP],ESI
          call _free
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45c405
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_448470
          xor EAX,EAX
          jmp L_4333fe
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_433440:
          push EBX
          sub ESP,24
          mov EBX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_45c444
          mov DWORD PTR [ESP],EBX
          call _FileExistsIn
          test EAX,EAX
          je L_4334f5
          mov DWORD PTR [ESP+4],OFFSET L_45c44c
          mov DWORD PTR [ESP],0
          call _log_printf
          call FUN_420670
          test EAX,EAX
          je L_433512
          mov DWORD PTR [ESP+4],OFFSET L_45c3b0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_45c474
          mov DWORD PTR [ESP],OFFSET L_45c496
          call FUN_41faf0
          test EAX,EAX
          .byte 0x0f,0x84; .long L_433530-.-4   # je L_433530
          mov DWORD PTR [ESP+4],OFFSET L_45c49b
          mov DWORD PTR [ESP],EBX
          call FUN_433130
          test EAX,EAX
          je L_433550
          mov DWORD PTR [ESP+4],OFFSET L_45c4a1
          mov DWORD PTR [ESP],0
          mov EBX,1
          call _log_printf
L_4334e2:
          mov DWORD PTR [ESP],OFFSET L_45c496
          call FUN_41fc30
          add ESP,24
          mov EAX,EBX
          pop EBX
          ret 
L_4334f5:
          mov DWORD PTR [ESP+4],OFFSET L_45c57c
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call _log_printf
          add ESP,24
          mov EAX,EBX
          pop EBX
          ret 
L_433512:
          mov DWORD PTR [ESP+4],OFFSET L_45c540
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call _log_printf
          add ESP,24
          mov EAX,EBX
          pop EBX
          ret 
          .byte 0x90
L_433530:
          mov DWORD PTR [ESP+4],OFFSET L_45c504
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call _log_printf
          add ESP,24
          mov EAX,EBX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_433550:
          mov DWORD PTR [ESP+4],OFFSET L_45c4c0
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call _log_printf
          jmp L_4334e2
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.section .rdata,"dr"
.p2align 2
L_45bdb4:
          .string "SSEP"
L_45bdb9:
          .string "%s:\\%08X"
          .zero 2
L_45bdc4:
          .string "ERROR: could not create dir %s on console!\n"
L_45bdf0:
          .string "created dir: %s\n"
L_45be01:
          .string "manifest schema != 3!\n"
L_45be18:
          .string "manifest revision 0x%08x != 0x786F6E6D|0x7873796D!\n"
L_45be4c:
          .string "manifest magic 0x%08x != 0x584D4E50!\n"
L_45be72:
          .string "manifest checksum failed!\n"
L_45be8d:
          .string "err len = 0!\n"
L_45be9b:
          .string "- OK\n"
          .zero 3
L_45bea4:
          .string "file corrupt, hash check FAILED!!\n"
          .zero 1
L_45bec8:
          .string "file size FAIL! 0x%x is not 0x%x!\n"
L_45beeb:
          .string "could not read file!\n"
L_45bf01:
          .string "FAILED! Input len is 0!\n"
L_45bf1a:
          .string " - OK\n"
L_45bf21:
          .string " - FAILED!\n"
L_45bf2d:
          .string " - FAILED! input len is 0!\n"
          .zero 3
L_45bf4c:
          .string "parsing %d entries in system.manifest\n"
L_45bf73:
          .string "flash"
L_45bf79:
          .string "%03d: %s "
L_45bf83:
          .string "Content\\0000000000000000\\"
L_45bf9d:
          .string "%s:\\%s%08X\\%08X\\%s"
L_45bfb0:
          .string "%s:\\%08X\\%s"
L_45bfbc:
          .string "manifest size error! len 0x%x\n"
          .zero 1
L_45bfdc:
          .string "\n\n***** ERROR: this system extended data is not the correct version!\n"
          .zero 2
L_45c024:
          .string "\n\n***** ERROR: loading manifest content encountered problems!\n"
          .zero 1
L_45c064:
          .string "found %d items to send to xbox!\n"
          .zero 3
L_45c088:
          .string "manifest header check failed!\n"
          .zero 1
L_45c0a8:
          .string "header ok!\nManifest flash version: %d.%d.%d.%d\n"
L_45c0d8:
          .string "manifest not found at %s\n"
          .zero 2
L_45c0f4:
          .string "***** WARNING: could not find manifest data for sysex!\n"
L_45c12c:
          .string "loading manifest %s\n"
          .zero 3
L_45c144:
          .string "***** WARNING: could not read manifest data for sysex!\n"
L_45c17c:
          .string "loaded system.manifest, 0x%x bytes\n"
L_45c1a0:
          .string "%s:\\system.manifest"
L_45c1b4:
          .string "\\SEP"
          .zero 3
L_45c1bc:
          .string "ERROR: unable to mount sysex partition!\n"
          .zero 3
L_45c1e8:
          .string "ERROR: unable to format sysex partition!\n"
L_45c212:
          .string "loading avatar data...\n"
          .zero 2
L_45c22c:
          .string "success!\nFormatting HDD partition...\n"
          .zero 2
L_45c254:
          .string "success!\nSending avatar files to HDD partition...\n"
L_45c287:
          .string "sending %d items to xbox\n"
L_45c2a1:
          .string "sending manifest to %s\n"
          .zero 3
L_45c2bc:
          .string "sending %03d: 0x%08x (%d) bytes, %s\n"
          .zero 3
L_45c2e4:
          .string "aborting sending avatar data, failed to send %s\n"
          .zero 3
L_45c318:
          .string "success! Avatar data is successfully sent to the console!\n"
          .zero 1
L_45c354:
          .string "***** WARNING: avatar data skipped, unable to load data!\n"
L_45c38e:
          .string "creating directory %s..."
L_45c3a7:
          .string "FAILED!\n"
L_45c3b0:
          .string "success!\n"
L_45c3ba:
          .string "reading file from %s..."
L_45c3d2:
          .string "OK! read 0x%x (%d) bytes!\n"
L_45c3ed:
          .string "    sending file %s...\n"
L_45c405:
          .string "FAILED sending file %s!\n"
          .zero 2
L_45c420:
          .string "    sent 0x%x bytes to file %s OK!\n"
L_45c444:
          .string "index"
          .zero 2
L_45c44c:
          .string "formatting compatibility partition..."
          .zero 2
L_45c474:
          .string "\\Device\\Harddisk0\\SystemPartition"
L_45c496:
          .string "XCOM"
L_45c49b:
          .string "XCOM:"
L_45c4a1:
          .string "sent files to partition OK!\n"
          .zero 2
L_45c4c0:
          .string "\n\n***** ERROR: Sending files to compatibility partition failed!\n"
          .zero 3
L_45c504:
          .string "\n\n***** ERROR: unable to mount compatibility partition!\n"
          .zero 3
L_45c540:
          .string "\n\n***** ERROR: unable to format compatibility partition!\n"
          .zero 2
L_45c57c:
          .string "\n\n***** WARNING: compatibility data skipped, unable to find index!\n"
L_45c5c0:
          .string "%s:\\Content"
L_45c5cc:
          .string "%s:\\Content\\0000000000000000"
          .zero 3
L_45c5ec:
          .string "%s:\\Content\\0000000000000000\\FFFE07DF"
          .zero 2
L_45c614:
          .string "%s:\\Content\\0000000000000000\\FFFE07DF\\00008000"
          .zero 1
L_45c644:
          .long L_45c5c0
          .long L_45c5cc
          .long L_45c5ec
          .long L_45c614

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
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_431c20 - .
          .byte 0xfa
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
          .byte 0x48
          .byte 0xe
          .byte 0xb0
          .byte 0x2
          .byte 0x2
          .byte 0x85
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
          .byte 0x4b
          .byte 0xb
          .byte 0x2
          .byte 0x51
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
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x64
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_431d20 - .
          .byte 0x4b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_431d70 - .
          .byte 0xb0
          .byte 0x1
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
          .byte 0xba
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
          .byte 0x57
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
          .byte 0x43
          .byte 0xb
          .byte 0x2
          .byte 0xcb
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
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_431f20 - .
          .byte 0x5e
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
          .byte 0x6a
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
          .byte 0x41
          .byte 0xb
          .byte 0x65
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
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_431f80 - .
          .byte 0x2c
          .byte 0x1
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
          .byte 0xa1
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
          .byte 0x46
          .byte 0xb
          .byte 0x70
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
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_4320b0 - .
          .byte 0xd6
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
          .byte 0x75
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
          .byte 0x44
          .byte 0xb
          .byte 0x7a
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
          .byte 0x42
          .byte 0xb
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_432190 - .
          .byte 0x3
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
          .byte 0x46
          .byte 0xe
          .byte 0xf0
          .byte 0xc
          .byte 0x3
          .byte 0xa9
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
          .byte 0x49
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_4327a0 - .
          .byte 0xf9
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
          .byte 0x2
          .byte 0xf9
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
          .byte 0x5b
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
          .byte 0x3
          .byte 0x17
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
          .byte 0x43
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x24
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_432aa0 - .
          .byte 0x64
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
          .byte 0x5c
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
          .byte 0x0
          .byte 0x0
          .byte 0x58
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_432b10 - .
          .byte 0xca
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
          .byte 0x10
          .byte 0x2
          .byte 0xf9
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
          .byte 0x2
          .byte 0xe6
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
          .byte 0x2
          .byte 0xc4
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
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xac
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_432de0 - .
          .byte 0x6a
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x64
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x49
          .byte 0xb
          .byte 0x59
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x47
          .byte 0xb
          .byte 0x59
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_432e50 - .
          .byte 0xdc
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
          .byte 0xa
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
          .byte 0x49
          .byte 0xb
          .byte 0x5c
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
          .byte 0x28
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_433130 - .
          .byte 0x9
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
          .byte 0x46
          .byte 0xe
          .byte 0xf0
          .byte 0x12
          .byte 0x3
          .byte 0x98
          .byte 0x2
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
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_433440 - .
          .byte 0x2b
          .byte 0x1
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
          .byte 0x2
          .byte 0xad
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x59
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x59
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x42
          .byte 0xb
          .byte 0x59
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x0
          .byte 0x0

.bss
.p2align 5
L_4795a0:
          .zero 32
L_4795c0:
          .zero 192
L_479680:
          .zero 4
L_479684:
          .zero 28
