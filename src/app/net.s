# app/net.s -- winsock: beacon, send/recv
#
# original placement:
#   .bss           00479574-0047957c
#   .data          0044a6c0-0044a6e0
#   .eh_frame      00468bd0-00469410
#   .rdata         004574b0-00457a80
#   .rdata$zzz     00463a64-00463a90
#   .text          0041e800-00420a90

.intel_syntax noprefix
.globl FUN_41ea70
.globl FUN_41ed50
.globl FUN_41ed70
.globl FUN_41f700
.globl FUN_41fa40
.globl FUN_41faf0
.globl FUN_41fc30
.globl FUN_41fd60
.globl FUN_41fe10
.globl FUN_41fe20
.globl FUN_41ff90
.globl FUN_41ffe0
.globl FUN_420140
.globl FUN_420200
.globl FUN_420320
.globl FUN_420420
.globl FUN_420470
.globl FUN_4205d0
.globl FUN_420670
.globl FUN_420710
.globl FUN_420840
.globl FUN_420910

.text
.p2align 4
FUN_41e800:
          push EBP
          push EDI
          mov EDX,EAX
          push ESI
          push EBX
          sub ESP,332
          mov DWORD PTR [ESP+44],EAX
          mov EAX,DWORD PTR [L_44a6c0]
          lea EBP,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+52],15
          mov DWORD PTR [ESP+56],0
          mov DWORD PTR [ESP+60],1
          mov DWORD PTR [EDX],0
          mov DWORD PTR [ESP+64],EAX
          lea EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [select]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+36],EAX
          call EAX
          add EAX,1
          sub ESP,20
          cmp EAX,1
          jbe L_41ea10
          mov EAX,DWORD PTR [L_44a6c0]
          lea EBX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],4
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          mov EAX,DWORD PTR [recv]
          mov DWORD PTR [ESP+40],EAX
          call EAX
          add EAX,1
          sub ESP,16
          cmp EAX,1
          jbe L_41ea35
          mov DWORD PTR [ESP],EBX
          call FUN_420ad0
          cmp EAX,-1
          mov EBX,EAX
          je L_41e99b
          test EAX,EAX
          jne L_41e8e5
          mov EAX,DWORD PTR [ESP+44]
          mov ESI,OFFSET L_479578
          mov DWORD PTR [EAX],0
L_41e8d8:
          add ESP,332
          mov EAX,ESI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_41e8e5:
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          xor EDI,EDI
          call _calloc
          test EBX,EBX
          mov ESI,EAX
          jg L_41e93b
          jmp L_41e9e2
L_41e902:
          mov EAX,EBX
          mov DWORD PTR [ESP+12],0
          sub EAX,EDI
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESI+EDI*1]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [ESP+40]
          sub ESP,16
          cmp EAX,-1
          .byte 0x0f,0x84; .long L_41e9b0-.-4   # je L_41e9b0
          add EDI,EAX
          cmp EBX,EDI
          jle L_41e9e0
L_41e93b:
          lea EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+16],EAX
          call DWORD PTR [ESP+36]
          add EAX,1
          sub ESP,20
          cmp EAX,1
          ja L_41e902
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_4574f4
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp ESI,OFFSET L_479578
          je L_41e99b
L_41e993:
          mov DWORD PTR [ESP],ESI
          call _free
L_41e99b:
          xor ESI,ESI
L_41e99d:
          add ESP,332
          mov EAX,ESI
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
L_41e9b0:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_457518
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp ESI,OFFSET L_479578
          jne L_41e993
          xor ESI,ESI
          jmp L_41e99d
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_41e9e0:
          je L_41ea5a
L_41e9e2:
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_457544
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp ESI,OFFSET L_479578
          jne L_41e993
          xor ESI,ESI
          jmp L_41e99d
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_41ea10:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_4574b0
          mov DWORD PTR [ESP+8],EAX
          xor ESI,ESI
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41e8d8
L_41ea35:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_4574d0
          mov DWORD PTR [ESP+8],EAX
          xor ESI,ESI
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41e8d8
L_41ea5a:
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [EAX],EBX
          jmp L_41e8d8
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
FUN_41ea70:
          mov EAX,DWORD PTR [ESP+4]
          cmp EAX,OFFSET L_479578
          je L_41ea84
          test EAX,EAX
          je L_41ea84
          jmp _free
L_41ea84:
          repz ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_41ea90:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,364
          mov DWORD PTR [ESP+36],1
          mov DWORD PTR [ESP+8],17
          mov DWORD PTR [ESP+4],2
          mov DWORD PTR [ESP],2
          call DWORD PTR [socket]
          sub ESP,12
          cmp EAX,-1
          mov DWORD PTR [ESP+32],0
          je L_41ec92
          mov ESI,EAX
          lea EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+16],4
          mov DWORD PTR [ESP+8],32
          mov DWORD PTR [ESP+4],65535
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP],ESI
          call DWORD PTR [setsockopt]
          sub ESP,20
          cmp EAX,-1
          je L_41ed20
          lea EBX,DWORD PTR [ESP+60]
          mov EAX,2
          mov DWORD PTR [ESP+60],0
          mov DWORD PTR [ESP+64],0
          mov DWORD PTR [ESP+68],0
          mov DWORD PTR [ESP+72],0
          mov WORD PTR [ESP+60],AX
          mov DWORD PTR [ESP],48
          call DWORD PTR [htons]
          sub ESP,4
          mov WORD PTR [ESP+62],AX
          mov DWORD PTR [ESP+64],0
          mov DWORD PTR [ESP+8],16
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call DWORD PTR [bind]
          sub ESP,12
          cmp EAX,-1
          je L_41ed37
          lea EBX,DWORD PTR [ESP+52]
          lea EBP,DWORD PTR [ESP+44]
          lea EDI,DWORD PTR [ESP+92]
          jmp L_41ebf7
L_41eb84:
          test EAX,EAX
          je L_41ecc0
          lea EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+20],EAX
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+16],EAX
          call DWORD PTR [recvfrom]
          sub ESP,24
          mov DWORD PTR [ESP],EBX
          call FUN_420ad0
          cmp EAX,1314092658
          je L_41ecf0
          mov DWORD PTR [ESP],EBX
          call FUN_420ad0
          mov DWORD PTR [ESP+12],1314092658
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_457608
          mov DWORD PTR [ESP],0
          call _log_printf
L_41ebf7:
          mov DWORD PTR [EBX],0
          mov DWORD PTR [EBX+4],0
          mov DWORD PTR [ESP+40],16
          mov DWORD PTR [ESP+96],ESI
          mov DWORD PTR [ESP+92],1
          mov DWORD PTR [ESP+44],30
          mov DWORD PTR [ESP+48],0
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],0
          call DWORD PTR [select]
          sub ESP,20
          cmp EAX,-1
          jne L_41eb84
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_4575e1
          mov DWORD PTR [ESP+8],EAX
L_41ec6b:
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP],ESI
          call DWORD PTR [closesocket]
          sub ESP,4
          mov EAX,DWORD PTR [ESP+32]
          add ESP,364
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_41ec92:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_457568
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+32]
          add ESP,364
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_41ecc0:
          mov DWORD PTR [ESP+4],OFFSET L_4575f3
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP],ESI
          call DWORD PTR [closesocket]
          sub ESP,4
          mov EAX,DWORD PTR [ESP+32]
          add ESP,364
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_41ecf0:
          lea EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],EAX
          call FUN_420af0
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+32],EAX
          call DWORD PTR [closesocket]
          sub ESP,4
          mov EAX,DWORD PTR [ESP+32]
          add ESP,364
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
L_41ed20:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_45758c
          mov DWORD PTR [ESP+8],EAX
          jmp L_41ec6b
L_41ed37:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_4575bc
          mov DWORD PTR [ESP+8],EAX
          jmp L_41ec6b
          .byte 0x66
          .byte 0x90
FUN_41ed50:
          sub ESP,28
          mov DWORD PTR [ESP],OFFSET L_4cd844
          call __time32
          add ESP,28
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
FUN_41ed70:
          sub ESP,44
          lea EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call __time32
          mov EAX,DWORD PTR [L_4cd844]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_448190
          fstp QWORD PTR [ESP+8]
          mov DWORD PTR [ESP+4],OFFSET L_45763e
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,44
          ret 
L_41edb0:
          sub ESP,44
          lea EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call __time32
          mov EAX,DWORD PTR [L_4cd844]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_448190
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
L_41ede0:
          push ESI
          push EBX
          sub ESP,20
          mov ESI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],ESI
          call _strlen
          mov EBX,EAX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EBX,EAX
          sete AL
          add ESP,20
          movzx EAX,AL
          pop EBX
          pop ESI
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
FUN_41ee30:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,332
          mov EAX,DWORD PTR [L_44a6c0]
          lea EBP,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+52],15
          mov DWORD PTR [ESP+56],0
          mov DWORD PTR [ESP+60],1
          mov DWORD PTR [ESP+64],EAX
          mov EAX,DWORD PTR [ESP+352]
          mov DWORD PTR [EAX],0
          lea EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [select]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+40],EAX
          call EAX
          add EAX,1
          sub ESP,20
          cmp EAX,1
          jbe L_41f140
          mov EAX,DWORD PTR [L_44a6c0]
          lea EBX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],4
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          mov EAX,DWORD PTR [recv]
          mov DWORD PTR [ESP+44],EAX
          call EAX
          add EAX,1
          sub ESP,16
          cmp EAX,1
          jbe L_41f165
          mov DWORD PTR [ESP],EBX
          call FUN_420ad0
          cmp EAX,-1
          mov ESI,EAX
          je L_41efe9
          test EAX,EAX
          jne L_41ef20
          mov EAX,DWORD PTR [ESP+352]
          mov EDI,OFFSET L_479578
          mov DWORD PTR [EAX],0
L_41ef0c:
          add ESP,332
          mov EAX,EDI
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
L_41ef20:
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call _calloc
          mov EDI,EAX
          mov EAX,DWORD PTR [ESP+356]
          test EAX,EAX
          jne L_41f000
          xor EBX,EBX
          test ESI,ESI
          jg L_41ef89
          jmp L_41f0fc
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_41ef50:
          mov EAX,ESI
          mov DWORD PTR [ESP+12],0
          sub EAX,EBX
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [EDI+EBX*1]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [ESP+44]
          sub ESP,16
          cmp EAX,-1
          je L_41f0ac
          add EBX,EAX
          cmp ESI,EBX
          jle L_41f130
L_41ef89:
          lea EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+4],EAX
          call DWORD PTR [ESP+40]
          add EAX,1
          sub ESP,20
          cmp EAX,1
          ja L_41ef50
L_41efbb:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_4574f4
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp EDI,OFFSET L_479578
          je L_41efe9
L_41efe1:
          mov DWORD PTR [ESP],EDI
          call _free
L_41efe9:
          xor EDI,EDI
L_41efeb:
          add ESP,332
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
L_41f000:
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],OFFSET L_457652
          xor EBX,EBX
          call _printf
          test ESI,ESI
          jg L_41f065
          jmp L_41f18a
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_41f020:
          mov EAX,ESI
          mov DWORD PTR [ESP+12],0
          sub EAX,EBX
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [EDI+EBX*1]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [ESP+44]
          sub ESP,16
          cmp EAX,-1
          je L_41f0a0
          add EBX,EAX
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],OFFSET L_45766a
          mov DWORD PTR [ESP+4],EBX
          call _printf
          cmp ESI,EBX
          jle L_41f0e0
L_41f065:
          lea EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+4],EAX
          call DWORD PTR [ESP+40]
          add EAX,1
          sub ESP,20
          cmp EAX,1
          ja L_41f020
          jmp L_41efbb
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_41f0a0:
          mov DWORD PTR [ESP],10
          call _putchar
L_41f0ac:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_457518
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp EDI,OFFSET L_479578
          jne L_41efe1
          xor EDI,EDI
          jmp L_41efeb
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_41f0e0:
          mov DWORD PTR [ESP],10
          call _putchar
          cmp ESI,EBX
          je L_41f132
L_41f0f0:
          mov DWORD PTR [ESP],10
          call _putchar
L_41f0fc:
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_457544
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp EDI,OFFSET L_479578
          jne L_41efe1
          xor EDI,EDI
          jmp L_41efeb
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_41f130:
          jne L_41f0fc
L_41f132:
          mov EAX,DWORD PTR [ESP+352]
          mov DWORD PTR [EAX],EBX
          jmp L_41ef0c
L_41f140:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_4574b0
          mov DWORD PTR [ESP+8],EAX
          xor EDI,EDI
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41ef0c
L_41f165:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_4574d0
          mov DWORD PTR [ESP+8],EAX
          xor EDI,EDI
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41ef0c
L_41f18a:
          mov DWORD PTR [ESP],10
          call _putchar
          jmp L_41f0f0
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_41f1a0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov ESI,DWORD PTR [ESP+68]
          lea EBX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call FUN_420b20
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],4
          mov DWORD PTR [ESP+4],EBX
          mov EDI,DWORD PTR [send]
          mov DWORD PTR [ESP],EAX
          call EDI
          sub ESP,16
          cmp EAX,-1
          je L_41f300
          test ESI,ESI
          je L_41f2df
          mov EAX,DWORD PTR [ESP+72]
          xor EBX,EBX
          mov EBP,1452
          test EAX,EAX
          je L_41f21a
          jmp L_41f29a
L_41f207:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_41f210:
          add EBX,EAX
          cmp ESI,EBX
          jbe L_41f2f3
L_41f21a:
          mov EAX,ESI
          mov DWORD PTR [ESP+12],0
          sub EAX,EBX
          cmp EAX,1451
          cmovbe EBP,EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+8],EBP
          add EAX,EBX
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP],EAX
          call EDI
          sub ESP,16
          cmp EAX,-1
          jne L_41f210
L_41f24e:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_4576ac
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          xor EAX,EAX
L_41f26e:
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_41f280:
          add EBX,EAX
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],OFFSET L_4576cf
          mov DWORD PTR [ESP+4],EBX
          call _printf
          cmp ESI,EBX
          jbe L_41f2e7
L_41f29a:
          mov EAX,ESI
          mov DWORD PTR [ESP+12],0
          sub EAX,EBX
          cmp EAX,1451
          cmovbe EBP,EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+8],EBP
          add EAX,EBX
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP],EAX
          call EDI
          sub ESP,16
          cmp EAX,-1
          jne L_41f280
          mov DWORD PTR [ESP],10
          call _putchar
          jmp L_41f24e
L_41f2df:
          mov EDX,DWORD PTR [ESP+72]
          test EDX,EDX
          je L_41f2f3
L_41f2e7:
          mov DWORD PTR [ESP],10
          call _putchar
L_41f2f3:
          add ESP,44
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_41f300:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_457688
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          xor EAX,EAX
          jmp L_41f26e
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
L_41f330:
          push ESI
          push EBX
          sub ESP,36
          lea EAX,DWORD PTR [ESP+28]
          call FUN_41e800
          test EAX,EAX
          je L_41f380
          xor ESI,ESI
          cmp DWORD PTR [ESP+28],2
          mov EBX,EAX
          je L_41f365
L_41f34d:
          cmp EBX,OFFSET L_479578
          je L_41f35d
          mov DWORD PTR [ESP],EBX
          call _free
L_41f35d:
          add ESP,36
          mov EAX,ESI
          pop EBX
          pop ESI
          ret 
L_41f365:
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          cmp AX,20299
          sete AL
          movzx EAX,AL
          mov ESI,EAX
          jmp L_41f34d
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_41f380:
          xor ESI,ESI
          add ESP,36
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
L_41f390:
          sub ESP,44
          mov DWORD PTR [ESP+8],6
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],2
          call DWORD PTR [socket]
          sub ESP,12
          cmp EAX,-1
          mov DWORD PTR [L_44a6c0],EAX
          je L_41f414
          mov EAX,2
          mov DWORD PTR [ESP],49
          mov WORD PTR [ESP+16],AX
          call DWORD PTR [htons]
          sub ESP,4
          mov WORD PTR [ESP+18],AX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+8],16
          mov DWORD PTR [ESP+20],EAX
          lea EAX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [connect]
          sub ESP,12
          test EAX,EAX
          mov EDX,1
          js L_41f440
          mov EAX,EDX
          add ESP,44
          ret 
L_41f414:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_4576e8
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          xor EDX,EDX
          add ESP,44
          mov EAX,EDX
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_41f440:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_457712
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          xor EDX,EDX
          add ESP,44
          mov EAX,EDX
          ret 
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_41f470:
          push EBX
          sub ESP,56
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_457736
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EAX,5
          je L_41f4c0
L_41f4a2:
          mov DWORD PTR [ESP+4],OFFSET L_4577bb
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,56
          xor EAX,EAX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_41f4c0:
          lea EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+44],0
          call FUN_41e800
          test EAX,EAX
          je L_41f4a2
          cmp DWORD PTR [ESP+44],1183
          jbe L_41f4a2
          mov EDX,DWORD PTR [EAX]
          mov DWORD PTR [EAX+280],0
          mov DWORD PTR [EAX+284],0
          mov DWORD PTR [L_479574],EAX
          mov ECX,EDX
          mov EBX,EDX
          shl ECX,24
          shr EBX,24
          add EBX,ECX
          mov ECX,EDX
          shr EDX,8
          shl ECX,8
          and EDX,65280
          and ECX,16711680
          add ECX,EBX
          add EDX,ECX
          mov DWORD PTR [EAX],EDX
          mov EDX,DWORD PTR [EAX+4]
          mov ECX,EDX
          mov EBX,EDX
          shl ECX,24
          shr EBX,24
          add EBX,ECX
          mov ECX,EDX
          shr EDX,8
          shl ECX,8
          and EDX,65280
          and ECX,16711680
          add ECX,EBX
          add EDX,ECX
          mov DWORD PTR [EAX+4],EDX
          mov EDX,DWORD PTR [EAX+8]
          mov ECX,EDX
          mov EBX,EDX
          shl ECX,24
          shr EBX,24
          add EBX,ECX
          mov ECX,EDX
          shr EDX,8
          shl ECX,8
          and EDX,65280
          and ECX,16711680
          add ECX,EBX
          add EDX,ECX
          mov DWORD PTR [EAX+8],EDX
          mov EDX,DWORD PTR [EAX+12]
          mov ECX,EDX
          mov EBX,EDX
          shl ECX,24
          shr EBX,24
          add EBX,ECX
          mov ECX,EDX
          shl ECX,8
          and ECX,16711680
          add ECX,EBX
          shr EDX,8
          and EDX,65280
          add EDX,ECX
          mov DWORD PTR [EAX+12],EDX
          mov EDX,DWORD PTR [EAX+16]
          mov ECX,EDX
          mov EBX,EDX
          shl ECX,24
          shr EBX,24
          add EBX,ECX
          mov ECX,EDX
          shr EDX,8
          shl ECX,8
          and EDX,65280
          and ECX,16711680
          add ECX,EBX
          add EDX,ECX
          mov DWORD PTR [EAX+16],EDX
          mov EDX,DWORD PTR [EAX+20]
          mov ECX,EDX
          mov EBX,EDX
          shl ECX,24
          shr EBX,24
          add EBX,ECX
          mov ECX,EDX
          shr EDX,8
          shl ECX,8
          and EDX,65280
          and ECX,16711680
          add ECX,EBX
          add EDX,ECX
          mov DWORD PTR [EAX+20],EDX
          mov EDX,DWORD PTR [EAX+24]
          mov ECX,EDX
          mov EBX,EDX
          shl ECX,24
          shr EBX,24
          add EBX,ECX
          mov ECX,EDX
          shr EDX,8
          shl ECX,8
          and EDX,65280
          and ECX,16711680
          add ECX,EBX
          add EDX,ECX
          mov DWORD PTR [EAX+24],EDX
          mov EDX,DWORD PTR [EAX+28]
          mov ECX,EDX
          mov EBX,EDX
          shl ECX,24
          shr EBX,24
          add EBX,ECX
          mov ECX,EDX
          shr EDX,8
          shl ECX,8
          and EDX,65280
          and ECX,16711680
          add ECX,EBX
          mov EBX,OFFSET L_457732
          add EDX,ECX
          mov DWORD PTR [EAX+28],EDX
          mov DWORD PTR [ESP+4],OFFSET L_45773c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_479574]
          mov EAX,DWORD PTR [EAX+16]
          shr EAX,28
          add EAX,1
          mov DWORD PTR [ESP],EAX
          call FUN_420a90
          mov DWORD PTR [ESP+4],OFFSET L_457746
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479574]
          mov EAX,DWORD PTR [EAX]
          mov DWORD PTR [ESP+4],OFFSET L_457758
          mov DWORD PTR [ESP],0
          movzx EDX,AL
          shr EAX,8
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov ECX,DWORD PTR [L_479574]
          mov EAX,OFFSET L_45772f
          mov EDX,DWORD PTR [ECX+20]
          cmp EDX,50331648
          cmovne EAX,EBX
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ECX+24]
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],OFFSET L_457784
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          add ESP,56
          mov EAX,1
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_41f700:
          push EBX
          sub ESP,488
          lea EAX,DWORD PTR [ESP+80]
          mov EBX,DWORD PTR [ESP+496]
          mov DWORD PTR [ESP],514
          mov DWORD PTR [ESP+4],EAX
          call DWORD PTR [WSAStartup]
          sub ESP,8
          test EAX,EAX
          jne L_41f884
          test EBX,EBX
          je L_41f8c4
          lea EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+44],16
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],2
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+16],EAX
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+12],EAX
          call DWORD PTR [WSAStringToAddressA]
          sub ESP,20
          test EAX,EAX
          jne L_41f860
          movzx EAX,BYTE PTR [ESP+55]
          mov DWORD PTR [ESP+4],OFFSET L_45784c
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+20],EAX
          movzx EAX,BYTE PTR [ESP+54]
          mov DWORD PTR [ESP+16],EAX
          movzx EAX,BYTE PTR [ESP+53]
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [ESP+52]
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EBX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+8],6
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],2
          call DWORD PTR [socket]
          sub ESP,12
          cmp EAX,-1
          mov DWORD PTR [L_44a6c0],EAX
          je L_41f9c0
          mov EAX,2
          mov DWORD PTR [ESP],49
          mov WORD PTR [ESP+64],AX
          call DWORD PTR [htons]
          sub ESP,4
          mov WORD PTR [ESP+66],AX
          lea EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+68],EBX
          mov DWORD PTR [ESP+8],16
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [connect]
          sub ESP,12
          test EAX,EAX
          .byte 0x0f,0x88; .long L_41f8a4-.-4   # js L_41f8a4
          mov DWORD PTR [ESP+4],OFFSET L_45773c
          mov DWORD PTR [ESP],0
L_41f837:
          call _log_printf
          call FUN_41f470
          mov EDX,EAX
          mov EAX,1
          test EDX,EDX
          jne L_41f852
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_41f850:
          xor EAX,EAX
L_41f852:
          add ESP,488
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_41f860:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45787c
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41f850
L_41f884:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_4578b5
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41f850
L_41f8a4:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_457712
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41f850
L_41f8c4:
          mov DWORD PTR [ESP+4],OFFSET L_4577c4
          mov DWORD PTR [ESP],0
          call _log_printf
          call FUN_41ea90
          test EAX,EAX
          mov EBX,EAX
          je L_41f9e3
          shr EAX,24
          mov DWORD PTR [ESP+4],OFFSET L_4577ec
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+20],EAX
          mov EAX,EBX
          shr EAX,16
          movzx EAX,AL
          mov DWORD PTR [ESP+16],EAX
          movzx EAX,BH
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BL
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_457817
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+8],6
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],2
          call DWORD PTR [socket]
          sub ESP,12
          cmp EAX,-1
          mov DWORD PTR [L_44a6c0],EAX
          je L_41f9c0
          mov EDX,2
          mov DWORD PTR [ESP],49
          mov WORD PTR [ESP+64],DX
          call DWORD PTR [htons]
          sub ESP,4
          mov WORD PTR [ESP+66],AX
          lea EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+68],EBX
          mov DWORD PTR [ESP+8],16
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [connect]
          sub ESP,12
          test EAX,EAX
          js L_41f8a4
          mov DWORD PTR [ESP+4],OFFSET L_4578d4
          mov DWORD PTR [ESP],1
          jmp L_41f837
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_41f9c0:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_4576e8
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41f850
L_41f9e3:
          mov DWORD PTR [ESP+4],OFFSET L_457830
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41f850
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_41fa00:
          sub ESP,28
          mov EAX,DWORD PTR [L_479574]
          test EAX,EAX
          je L_41fa1b
          cmp EAX,OFFSET L_479578
          je L_41fa1b
          mov DWORD PTR [ESP],EAX
          call _free
L_41fa1b:
          mov EAX,DWORD PTR [L_44a6c0]
          cmp EAX,-1
          je L_41fa31
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [closesocket]
          sub ESP,4
L_41fa31:
          add ESP,28
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
FUN_41fa40:
          sub ESP,28
          mov DWORD PTR [ESP+4],OFFSET L_4578f5
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_457913
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EAX,5
          je L_41fad0
          mov DWORD PTR [ESP+4],OFFSET L_45791d
          mov DWORD PTR [ESP],0
          call _log_printf
L_41fa99:
          mov EAX,DWORD PTR [L_479574]
          cmp EAX,OFFSET L_479578
          je L_41fab1
          test EAX,EAX
          je L_41fab1
          mov DWORD PTR [ESP],EAX
          call _free
L_41fab1:
          mov EAX,DWORD PTR [L_44a6c0]
          cmp EAX,-1
          je L_41fac7
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [closesocket]
          sub ESP,4
L_41fac7:
          add ESP,28
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_41fad0:
          mov DWORD PTR [ESP+4],OFFSET L_457919
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41fa99
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_41faf0:
          push EDI
          push ESI
          push EBX
          sub ESP,288
          mov EBX,DWORD PTR [ESP+308]
          mov EDI,DWORD PTR [ESP+304]
          lea ESI,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],OFFSET L_457925
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EDI
          call _sprintf
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+12],EDI
          mov EBX,ESI
          mov DWORD PTR [ESP+4],OFFSET L_457931
          mov DWORD PTR [ESP],1
          call _log_printf
L_41fb41:
          mov EDX,DWORD PTR [EBX]
          add EBX,4
          lea EAX,DWORD PTR [EDX-16843009]
          not EDX
          and EAX,EDX
          and EAX,2155905152
          je L_41fb41
          mov EDX,EAX
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],ESI
          shr EDX,16
          test EAX,32896
          cmove EAX,EDX
          lea EDX,DWORD PTR [EBX+2]
          mov ECX,EAX
          cmove EBX,EDX
          add CL,AL
          mov EAX,DWORD PTR [L_44a6c0]
          sbb EBX,3
          sub EBX,ESI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EBX,EAX
          je L_41fbc0
L_41fb98:
          mov DWORD PTR [ESP+4],OFFSET L_4577bb
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,288
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          ret 
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_41fbc0:
          lea EAX,DWORD PTR [ESP+24]
          call FUN_41e800
          test EAX,EAX
          mov EBX,EAX
          je L_41fb98
          cmp DWORD PTR [ESP+24],2
          je L_41fc10
          xor ESI,ESI
          cmp EBX,OFFSET L_479578
          je L_41fb98
L_41fbe0:
          mov DWORD PTR [ESP],EBX
          call _free
L_41fbe8:
          test ESI,ESI
          je L_41fb98
          mov DWORD PTR [ESP+4],OFFSET L_45773c
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,288
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
L_41fc10:
          mov DWORD PTR [ESP],EBX
          call FUN_420ab0
          cmp AX,20299
          sete AL
          cmp EBX,OFFSET L_479578
          movzx EAX,AL
          mov ESI,EAX
          jne L_41fbe0
          jmp L_41fbe8
          .byte 0x66
          .byte 0x90
FUN_41fc30:
          push ESI
          push EBX
          sub ESP,292
          mov EBX,DWORD PTR [ESP+304]
          lea ESI,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],OFFSET L_457947
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EBX
          call _sprintf
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_457950
          mov EBX,ESI
          mov DWORD PTR [ESP],1
          call _log_printf
L_41fc71:
          mov EDX,DWORD PTR [EBX]
          add EBX,4
          lea EAX,DWORD PTR [EDX-16843009]
          not EDX
          and EAX,EDX
          and EAX,2155905152
          je L_41fc71
          mov EDX,EAX
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],ESI
          shr EDX,16
          test EAX,32896
          cmove EAX,EDX
          lea EDX,DWORD PTR [EBX+2]
          mov ECX,EAX
          cmove EBX,EDX
          add CL,AL
          mov EAX,DWORD PTR [L_44a6c0]
          sbb EBX,3
          sub EBX,ESI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EBX,EAX
          je L_41fcf0
L_41fcc8:
          mov DWORD PTR [ESP+4],OFFSET L_4577bb
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,292
          xor EAX,EAX
          pop EBX
          pop ESI
          ret 
L_41fce7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_41fcf0:
          lea EAX,DWORD PTR [ESP+24]
          call FUN_41e800
          test EAX,EAX
          mov EBX,EAX
          je L_41fcc8
          cmp DWORD PTR [ESP+24],2
          je L_41fd40
          xor ESI,ESI
          cmp EBX,OFFSET L_479578
          je L_41fcc8
L_41fd10:
          mov DWORD PTR [ESP],EBX
          call _free
L_41fd18:
          test ESI,ESI
          je L_41fcc8
          mov DWORD PTR [ESP+4],OFFSET L_45773c
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,292
          mov EAX,1
          pop EBX
          pop ESI
          ret 
          .byte 0x66
          .byte 0x90
L_41fd40:
          mov DWORD PTR [ESP],EBX
          call FUN_420ab0
          cmp AX,20299
          sete AL
          cmp EBX,OFFSET L_479578
          movzx EAX,AL
          mov ESI,EAX
          jne L_41fd10
          jmp L_41fd18
          .byte 0x66
          .byte 0x90
FUN_41fd60:
          push ESI
          push EBX
          sub ESP,292
          mov EAX,DWORD PTR [ESP+304]
          lea ESI,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],OFFSET L_457962
          mov DWORD PTR [ESP],ESI
          mov EBX,ESI
          mov DWORD PTR [ESP+8],EAX
          call _sprintf
L_41fd89:
          mov EDX,DWORD PTR [EBX]
          add EBX,4
          lea EAX,DWORD PTR [EDX-16843009]
          not EDX
          and EAX,EDX
          and EAX,2155905152
          je L_41fd89
          mov EDX,EAX
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],ESI
          shr EDX,16
          test EAX,32896
          cmove EAX,EDX
          lea EDX,DWORD PTR [EBX+2]
          mov ECX,EAX
          cmove EBX,EDX
          add CL,AL
          mov EAX,DWORD PTR [L_44a6c0]
          sbb EBX,3
          sub EBX,ESI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EBX,EAX
          je L_41fdf0
          add ESP,292
          xor EAX,EAX
          pop EBX
          pop ESI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_41fdf0:
          mov EAX,DWORD PTR [ESP+308]
          call FUN_41e800
          add ESP,292
          pop EBX
          pop ESI
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
FUN_41fe10:
          mov EAX,DWORD PTR [L_479574]
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_41fe20:
          push EBX
          sub ESP,56
          mov DWORD PTR [ESP],OFFSET L_4cd844
          call __time32
          mov DWORD PTR [ESP+4],OFFSET L_45796c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_457990
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EAX,5
          je L_41fe90
L_41fe72:
          mov DWORD PTR [ESP+4],OFFSET L_4577bb
          mov DWORD PTR [ESP],0
          call _log_printf
          xor EAX,EAX
L_41fe88:
          add ESP,56
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_41fe90:
          call _log_get_verbose
          test EAX,EAX
          setne AL
          movzx EAX,AL
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EAX
          call FUN_41ee30
          test EAX,EAX
          mov EBX,EAX
          je L_41fe72
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],OFFSET L_457998
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP],EAX
          call FUN_420d00
          test EAX,EAX
          je L_41ff70
          mov DWORD PTR [ESP+4],OFFSET L_45773c
          mov DWORD PTR [ESP],0
          call _log_printf
L_41ff07:
          lea EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call __time32
          mov EAX,DWORD PTR [L_4cd844]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call FUN_448190
          fstp QWORD PTR [ESP+8]
          mov DWORD PTR [ESP+4],OFFSET L_45763e
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp EBX,OFFSET L_479578
          mov EAX,1
          je L_41fe88
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+28],EAX
          call _free
          mov EAX,DWORD PTR [ESP+28]
          add ESP,56
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_41ff70:
          mov DWORD PTR [ESP+4],OFFSET L_4577bb
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41ff07
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_41ff90:
          push EBX
          sub ESP,24
          mov EAX,DWORD PTR [L_44a6c0]
          mov EBX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_4579cb
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EAX,5
          je L_41ffd0
          add ESP,24
          xor EAX,EAX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_41ffd0:
          add ESP,24
          mov EAX,EBX
          pop EBX
          jmp FUN_41e800
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_41ffe0:
          push ESI
          push EBX
          sub ESP,36
          mov EBX,DWORD PTR [ESP+48]
          test EBX,EBX
          je L_42001b
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_4579d1
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EAX,5
          je L_420023
L_42001b:
          add ESP,36
          xor EAX,EAX
          pop EBX
          pop ESI
          ret 
L_420023:
          call _log_get_verbose
          test EAX,EAX
          mov DWORD PTR [ESP],EBX
          setne AL
          movzx EAX,AL
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+4],EAX
          call FUN_41f1a0
          test EAX,EAX
          je L_4200e0
          lea ESI,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],OFFSET L_4579d8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,ESI
          call FUN_41e800
          test EAX,EAX
          mov EBX,EAX
          je L_42008c
          cmp DWORD PTR [ESP+28],2
          je L_420100
L_42007c:
          cmp EBX,OFFSET L_479578
          je L_42008c
          mov DWORD PTR [ESP],EBX
          call _free
L_42008c:
          mov DWORD PTR [ESP+4],OFFSET L_4577bb
          mov DWORD PTR [ESP],0
          call _log_printf
L_4200a0:
          mov DWORD PTR [ESP],ESI
          call __time32
          mov EAX,DWORD PTR [L_4cd844]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_448190
          fstp QWORD PTR [ESP+8]
          mov DWORD PTR [ESP+4],OFFSET L_45763e
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,36
          mov EAX,1
          pop EBX
          pop ESI
          ret 
L_4200e0:
          mov DWORD PTR [ESP+4],OFFSET L_4577bb
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_42001b
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_420100:
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          cmp AX,20299
          jne L_42007c
          cmp EBX,OFFSET L_479578
          je L_420122
          mov DWORD PTR [ESP],EBX
          call _free
L_420122:
          mov DWORD PTR [ESP+4],OFFSET L_45773c
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4200a0
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_420140:
          push ESI
          push EBX
          sub ESP,52
          movzx EAX,WORD PTR [ESP+72]
          lea ESI,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+4],OFFSET L_4579f9
          mov DWORD PTR [ESP],ESI
          mov EBX,ESI
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,WORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],EAX
          call _sprintf
L_42016d:
          mov EDX,DWORD PTR [EBX]
          add EBX,4
          lea EAX,DWORD PTR [EDX-16843009]
          not EDX
          and EAX,EDX
          and EAX,2155905152
          je L_42016d
          mov EDX,EAX
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],ESI
          shr EDX,16
          test EAX,32896
          cmove EAX,EDX
          lea EDX,DWORD PTR [EBX+2]
          mov ECX,EAX
          cmove EBX,EDX
          add CL,AL
          mov EAX,DWORD PTR [L_44a6c0]
          sbb EBX,3
          sub EBX,ESI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EBX,EAX
          je L_4201d0
          add ESP,52
          xor EAX,EAX
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4201d0:
          call _log_get_verbose
          test EAX,EAX
          setne AL
          movzx EAX,AL
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP],EAX
          call FUN_41ee30
          add ESP,52
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
FUN_420200:
          push ESI
          push EBX
          sub ESP,84
          movzx EAX,WORD PTR [ESP+108]
          lea ESI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],OFFSET L_457a07
          mov DWORD PTR [ESP],ESI
          mov EBX,ESI
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,WORD PTR [ESP+104]
          mov DWORD PTR [ESP+8],EAX
          call _sprintf
L_42022d:
          mov EDX,DWORD PTR [EBX]
          add EBX,4
          lea EAX,DWORD PTR [EDX-16843009]
          not EDX
          and EAX,EDX
          and EAX,2155905152
          je L_42022d
          mov EDX,EAX
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],ESI
          shr EDX,16
          test EAX,32896
          cmove EAX,EDX
          lea EDX,DWORD PTR [EBX+2]
          mov ECX,EAX
          cmove EBX,EDX
          add CL,AL
          mov EAX,DWORD PTR [L_44a6c0]
          sbb EBX,3
          sub EBX,ESI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EBX,EAX
          je L_420290
L_420284:
          xor EAX,EAX
L_420286:
          add ESP,84
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_420290:
          call _log_get_verbose
          test EAX,EAX
          setne AL
          movzx EAX,AL
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP],EAX
          call FUN_41f1a0
          test EAX,EAX
          je L_420284
          lea EAX,DWORD PTR [ESP+44]
          call FUN_41e800
          test EAX,EAX
          mov EBX,EAX
          je L_420284
          cmp DWORD PTR [ESP+44],2
          je L_4202f0
L_4202cf:
          xor EAX,EAX
          cmp EBX,OFFSET L_479578
          je L_420284
L_4202d9:
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+28],EAX
          call _free
          mov EAX,DWORD PTR [ESP+28]
          add ESP,84
          pop EBX
          pop ESI
          ret 
          nop
L_4202f0:
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          cmp AX,20299
          jne L_4202cf
          cmp EBX,OFFSET L_479578
          jne L_420310
          mov EAX,1
          jmp L_420286
L_420310:
          mov EAX,1
          jmp L_4202d9
L_420317:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_420320:
          push ESI
          push EBX
          sub ESP,84
          movzx EAX,WORD PTR [ESP+100]
          lea ESI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],OFFSET L_457a15
          mov DWORD PTR [ESP],ESI
          mov EBX,ESI
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,WORD PTR [ESP+96]
          mov DWORD PTR [ESP+8],EAX
          call _sprintf
L_42034d:
          mov EDX,DWORD PTR [EBX]
          add EBX,4
          lea EAX,DWORD PTR [EDX-16843009]
          not EDX
          and EAX,EDX
          and EAX,2155905152
          je L_42034d
          mov EDX,EAX
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],ESI
          shr EDX,16
          test EAX,32896
          cmove EAX,EDX
          lea EDX,DWORD PTR [EBX+2]
          mov ECX,EAX
          cmove EBX,EDX
          add CL,AL
          mov EAX,DWORD PTR [L_44a6c0]
          sbb EBX,3
          sub EBX,ESI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EBX,EAX
          je L_4203b0
L_4203a4:
          xor EAX,EAX
L_4203a6:
          add ESP,84
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4203b0:
          lea EAX,DWORD PTR [ESP+44]
          call FUN_41e800
          test EAX,EAX
          mov EBX,EAX
          je L_4203a4
          cmp DWORD PTR [ESP+44],2
          je L_4203f0
L_4203c6:
          xor EAX,EAX
          cmp EBX,OFFSET L_479578
          je L_4203a4
L_4203d0:
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+28],EAX
          call _free
          mov EAX,DWORD PTR [ESP+28]
          add ESP,84
          pop EBX
          pop ESI
          ret 
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4203f0:
          mov DWORD PTR [ESP],EBX
          call FUN_420ab0
          cmp AX,20299
          jne L_4203c6
          cmp EBX,OFFSET L_479578
          je L_42040d
          mov EAX,1
          jmp L_4203d0
L_42040d:
          mov EAX,1
          jmp L_4203a6
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
FUN_420420:
          push EBX
          sub ESP,24
          mov EAX,DWORD PTR [L_44a6c0]
          mov EBX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_457a23
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EAX,5
          je L_420460
          add ESP,24
          xor EAX,EAX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_420460:
          add ESP,24
          mov EAX,EBX
          pop EBX
          jmp FUN_41e800
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_420470:
          push EDI
          push EBX
          sub ESP,308
          mov EDX,DWORD PTR [ESP+320]
          test EDX,EDX
          je L_420530
          mov ECX,DWORD PTR [ESP+324]
          test ECX,ECX
          je L_420530
          lea EDI,DWORD PTR [ESP+48]
          xor EAX,EAX
          mov ECX,64
          mov DWORD PTR [ESP+40],1178881619
          mov DWORD PTR [ESP+44],0
          rep stosd DWORD PTR ES:[EDI]
          lea EAX,DWORD PTR [ESP+44]
          lea EDI,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EAX
          call _strcpy
          mov EAX,EDI
L_4204c9:
          mov ECX,DWORD PTR [EAX]
          add EAX,4
          lea EDX,DWORD PTR [ECX-16843009]
          not ECX
          and EDX,ECX
          and EDX,2155905152
          je L_4204c9
          mov ECX,EDX
          shr ECX,16
          test EDX,32896
          cmove EDX,ECX
          lea ECX,DWORD PTR [EAX+2]
          mov EBX,EDX
          cmove EAX,ECX
          add BL,DL
          mov EDX,10
          sbb EAX,3
          sub EAX,EDI
          mov WORD PTR [EDI+EAX*1],DX
          lea EBX,DWORD PTR [EAX+1]
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EBX,EAX
          je L_420540
          .byte 0x66   # nop
          nop
L_420530:
          xor EAX,EAX
L_420532:
          add ESP,308
          pop EBX
          pop EDI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_420540:
          call _log_get_verbose
          test EAX,EAX
          setne AL
          movzx EAX,AL
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+328]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+324]
          mov DWORD PTR [ESP],EAX
          call FUN_41f1a0
          test EAX,EAX
          je L_420530
          lea EAX,DWORD PTR [ESP+36]
          call FUN_41e800
          test EAX,EAX
          mov EBX,EAX
          je L_420530
          cmp DWORD PTR [ESP+36],2
          je L_4205a1
L_420585:
          xor EAX,EAX
          cmp EBX,OFFSET L_479578
          je L_420530
L_42058f:
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+28],EAX
          call _free
          mov EAX,DWORD PTR [ESP+28]
          jmp L_420532
L_4205a1:
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          cmp AX,20299
          jne L_420585
          cmp EBX,OFFSET L_479578
          jne L_4205c1
          mov EAX,1
          jmp L_420532
L_4205c1:
          mov EAX,1
          jmp L_42058f
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_4205d0:
          push EBX
          sub ESP,56
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_457a29
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EAX,5
          je L_420610
L_420602:
          xor EAX,EAX
L_420604:
          add ESP,56
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_420610:
          lea EAX,DWORD PTR [ESP+44]
          call FUN_41e800
          test EAX,EAX
          mov EBX,EAX
          je L_420602
          cmp DWORD PTR [ESP+44],2
          je L_420645
L_420626:
          xor EAX,EAX
          cmp EBX,OFFSET L_479578
          je L_420602
L_420630:
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+28],EAX
          call _free
          mov EAX,DWORD PTR [ESP+28]
          add ESP,56
          pop EBX
          ret 
L_420645:
          mov DWORD PTR [ESP],EBX
          call FUN_420ab0
          cmp AX,20299
          jne L_420626
          cmp EBX,OFFSET L_479578
          je L_420662
          mov EAX,1
          jmp L_420630
L_420662:
          mov EAX,1
          jmp L_420604
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_420670:
          push EBX
          sub ESP,56
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_457a2f
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EAX,5
          je L_4206b0
L_4206a2:
          xor EAX,EAX
L_4206a4:
          add ESP,56
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4206b0:
          lea EAX,DWORD PTR [ESP+44]
          call FUN_41e800
          test EAX,EAX
          mov EBX,EAX
          je L_4206a2
          cmp DWORD PTR [ESP+44],2
          je L_4206e5
L_4206c6:
          xor EAX,EAX
          cmp EBX,OFFSET L_479578
          je L_4206a2
L_4206d0:
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+28],EAX
          call _free
          mov EAX,DWORD PTR [ESP+28]
          add ESP,56
          pop EBX
          ret 
L_4206e5:
          mov DWORD PTR [ESP],EBX
          call FUN_420ab0
          cmp AX,20299
          jne L_4206c6
          cmp EBX,OFFSET L_479578
          je L_420702
          mov EAX,1
          jmp L_4206d0
L_420702:
          mov EAX,1
          jmp L_4206a4
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_420710:
          push EDI
          push EBX
          xor EAX,EAX
          sub ESP,308
          mov EDX,DWORD PTR [ESP+320]
          test EDX,EDX
          je L_4207c1
          lea EDI,DWORD PTR [ESP+48]
          mov ECX,64
          mov DWORD PTR [ESP+40],1380207437
          mov DWORD PTR [ESP+44],0
          rep stosd DWORD PTR ES:[EDI]
          lea EAX,DWORD PTR [ESP+44]
          lea EDI,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EAX
          call _strcpy
          mov EAX,EDI
L_42075a:
          mov ECX,DWORD PTR [EAX]
          add EAX,4
          lea EDX,DWORD PTR [ECX-16843009]
          not ECX
          and EDX,ECX
          and EDX,2155905152
          je L_42075a
          mov ECX,EDX
          shr ECX,16
          test EDX,32896
          cmove EDX,ECX
          lea ECX,DWORD PTR [EAX+2]
          mov EBX,EDX
          cmove EAX,ECX
          add BL,DL
          mov EDX,10
          sbb EAX,3
          sub EAX,EDI
          mov WORD PTR [EDI+EAX*1],DX
          lea EBX,DWORD PTR [EAX+1]
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EBX,EAX
          je L_4207d0
L_4207bf:
          xor EAX,EAX
L_4207c1:
          add ESP,308
          pop EBX
          pop EDI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4207d0:
          lea EAX,DWORD PTR [ESP+36]
          call FUN_41e800
          test EAX,EAX
          mov EBX,EAX
          je L_4207bf
          cmp DWORD PTR [ESP+36],2
          je L_420810
L_4207e6:
          xor EAX,EAX
          cmp EBX,OFFSET L_479578
          je L_4207bf
L_4207f0:
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+28],EAX
          call _free
          mov EAX,DWORD PTR [ESP+28]
          add ESP,308
          pop EBX
          pop EDI
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_420810:
          mov DWORD PTR [ESP],EBX
          call FUN_420ab0
          cmp AX,20299
          jne L_4207e6
          cmp EBX,OFFSET L_479578
          jne L_42082d
          mov EAX,1
          jmp L_4207c1
L_42082d:
          mov EAX,1
          jmp L_4207f0
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
FUN_420840:
          sub ESP,28
          mov EAX,DWORD PTR [ESP+32]
          cmp EAX,1
          je L_4208c0
          cmp EAX,2
          je L_420860
          mov EAX,1
          add ESP,28
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_420860:
          mov DWORD PTR [ESP+4],OFFSET L_457a57
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_457a71
L_42088c:
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [send]
          sub ESP,16
          cmp EAX,5
          je L_4208f0
          mov DWORD PTR [ESP+4],OFFSET L_45791d
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,1
          add ESP,28
          ret 
          .byte 0x90
L_4208c0:
          mov DWORD PTR [ESP+4],OFFSET L_457a35
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_457a51
          jmp L_42088c
          .byte 0x66   # nop
          nop
L_4208f0:
          mov DWORD PTR [ESP+4],OFFSET L_457919
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,1
          add ESP,28
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
FUN_420910:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EAX,DWORD PTR [L_44a6c0]
          mov ESI,DWORD PTR [send]
          mov EBX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_457a77
          mov DWORD PTR [ESP],EAX
          call ESI
          sub ESP,16
          cmp EAX,5
          je L_420955
L_42094b:
          xor EAX,EAX
L_42094d:
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_420955:
          lea EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_420b20
          lea EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],4
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP],EAX
          call ESI
          sub ESP,16
          cmp EAX,-1
          je L_420a40
          xor EBP,EBP
          test EBX,EBX
          mov EDI,1452
          jne L_4209a6
          jmp L_420a00
L_4209a0:
          add EBP,EAX
          cmp EBX,EBP
          jbe L_420a00
L_4209a6:
          mov EAX,EBX
          mov DWORD PTR [ESP+12],0
          sub EAX,EBP
          cmp EAX,1451
          cmovbe EDI,EAX
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+8],EDI
          add EAX,EBP
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_44a6c0]
          mov DWORD PTR [ESP],EAX
          call ESI
          sub ESP,16
          cmp EAX,-1
          jne L_4209a0
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_4576ac
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_42094b
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_420a00:
          lea EAX,DWORD PTR [ESP+44]
          call FUN_41e800
          test EAX,EAX
          mov EBX,EAX
          je L_42094b
          cmp DWORD PTR [ESP+44],2
          je L_420a63
L_420a1a:
          xor EAX,EAX
          cmp EBX,OFFSET L_479578
          je L_42094b
L_420a28:
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+28],EAX
          call _free
          mov EAX,DWORD PTR [ESP+28]
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_420a40:
          call DWORD PTR [WSAGetLastError]
          mov DWORD PTR [ESP+4],OFFSET L_457688
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_42094b
L_420a63:
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          cmp AX,20299
          jne L_420a1a
          cmp EBX,OFFSET L_479578
          jne L_420a83
          mov EAX,1
          jmp L_42094d
L_420a83:
          mov EAX,1
          jmp L_420a28
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.data
.p2align 5
L_44a6c0:
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

.section .rdata,"dr"
.p2align 4
L_4574b0:
          .string "timeout waiting for data, %d\n"
          .zero 2
L_4574d0:
          .string "unable to fetch first 4 bytes, %d\n"
          .zero 1
L_4574f4:
          .string "timeout waiting for data, error %d\n"
L_457518:
          .string "could not receive data on socket, error %d\n"
L_457544:
          .string "received only %x of %x bytes! fail\n"
L_457568:
          .string "unable to open socket, error %d\n"
          .zero 3
L_45758c:
          .string "unable to set bcast socket option, error %d\n"
          .zero 3
L_4575bc:
          .string "unable to set bind socket, error %d\n"
L_4575e1:
          .string "Socket error! %d\n"
L_4575f3:
          .string "UDP wait timeout!\n"
          .zero 2
L_457608:
          .string "Beacon received, but the beacon magic %X was not %X!\n"
L_45763e:
          .string "Completed in %.0fs\n"
L_457652:
          .string "waiting for 0x%x bytes\n"
L_45766a:
          .string "received 0x%08x of 0x%08x\r"
          .zero 3
L_457688:
          .string "socket error sending data size, %d\n"
L_4576ac:
          .string "socket error sending data (1), %d\n"
L_4576cf:
          .string "sent 0x%08x of 0x%08x\r"
          .zero 2
L_4576e8:
          .string "could not create client socket, error %d\n"
L_457712:
          .string "could not connect, error %d\n"
L_45772f:
          .string "No"
L_457732:
          .string "Yes"
L_457736:
          .string "GTIN\n"
L_45773c:
          .string "success!\n"
L_457746:
          .string "connected to %s"
          .zero 2
L_457758:
          .string " with updsvr version %d (peek version %d)\n"
          .zero 1
L_457784:
          .string "NAND image size: 0x%x Block size: 0x%x Spare Data: %s\n"
L_4577bb:
          .string "failed!\n"
L_4577c4:
          .string "started, watching network for xbox..."
          .zero 2
L_4577ec:
          .string "success, found xbox beacon at %u.%u.%u.%u\n"
L_457817:
          .string "attempting to connect..."
L_457830:
          .string "failed to find xbox beacon\n"
L_45784c:
          .string "attempting forced connection to %u.%u.%u.%u..."
          .zero 1
L_45787c:
          .string "attempting to convert %s to an address failed, error %d\n"
L_4578b5:
          .string "WSAStartup failed, error %d\n"
          .zero 2
L_4578d4:
          .string "success!\nGetting console info..."
L_4578f5:
          .string "\ndisconnecting from server..."
L_457913:
          .string "QUIT\n"
L_457919:
          .string "OK\n"
L_45791d:
          .string "failed\n"
L_457925:
          .string "MTPT%s: %s\n"
L_457931:
          .string "mounting %s to %s:..."
L_457947:
          .string "UMPT%s:\n"
L_457950:
          .string "unmounting %s:..."
L_457962:
          .string "GETF%s\n"
          .zero 2
L_45796c:
          .string "reading flash image from console..."
L_457990:
          .string "GTFL\n"
          .zero 2
L_457998:
          .string "received 0x%x bytes data OK, writing to file %s..."
L_4579cb:
          .string "GTBL\n"
L_4579d1:
          .string "WRFL\n"
          .zero 1
L_4579d8:
          .string "file sent OK, awaiting result..."
L_4579f9:
          .string "RBLK%04x%04x\n"
L_457a07:
          .string "WBLK%04x%04x\n"
L_457a15:
          .string "ERBL%04x%04x\n"
L_457a23:
          .string "GTBB\n"
L_457a29:
          .string "FMEX\n"
L_457a2f:
          .string "FMCM\n"
L_457a35:
          .string "sending shutdown command..."
L_457a51:
          .string "SHDN\n"
L_457a57:
          .string "sending reboot command..."
L_457a71:
          .string "REEB\n"
L_457a77:
          .string "WBPT\n"
          .zero 3

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
          .byte 0x74
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_41e800 - .
          .byte 0x65
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
          .byte 0x46
          .byte 0xe
          .byte 0xe0
          .byte 0x2
          .byte 0x2
          .byte 0x5d
          .byte 0xe
          .byte 0xcc
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0xe0
          .byte 0x2
          .byte 0x74
          .byte 0xe
          .byte 0xd0
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0xe0
          .byte 0x2
          .byte 0x75
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
          .byte 0x40
          .byte 0xe
          .byte 0xd0
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0xe0
          .byte 0x2
          .byte 0x7a
          .byte 0xe
          .byte 0xcc
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0xe0
          .byte 0x2
          .byte 0x7b
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
          .byte 0x47
          .byte 0xb
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x94
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_41ea70 - .
          .byte 0x16
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_41ea90 - .
          .byte 0xbe
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
          .byte 0x80
          .byte 0x3
          .byte 0x65
          .byte 0xe
          .byte 0xf4
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x80
          .byte 0x3
          .byte 0x7c
          .byte 0xe
          .byte 0xec
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x80
          .byte 0x3
          .byte 0x2
          .byte 0x44
          .byte 0xe
          .byte 0xfc
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x80
          .byte 0x3
          .byte 0x62
          .byte 0xe
          .byte 0xf4
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x80
          .byte 0x3
          .byte 0x2
          .byte 0x4c
          .byte 0xe
          .byte 0xe8
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x80
          .byte 0x3
          .byte 0x2
          .byte 0x91
          .byte 0xe
          .byte 0xec
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x80
          .byte 0x3
          .byte 0x70
          .byte 0xe
          .byte 0xfc
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x80
          .byte 0x3
          .byte 0x4a
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
          .byte 0x42
          .byte 0xb
          .byte 0x5d
          .byte 0xe
          .byte 0xfc
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x80
          .byte 0x3
          .byte 0x4a
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
          .byte 0x42
          .byte 0xb
          .byte 0x59
          .byte 0xe
          .byte 0xfc
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x80
          .byte 0x3
          .byte 0x4a
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
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x74
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_41ed50 - .
          .byte 0x13
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x4f
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8c
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_41ed70 - .
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x7c
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa4
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_41edb0 - .
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x64
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xbc
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_41ede0 - .
          .byte 0x42
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
          .byte 0x6c
          .byte 0xe
          .byte 0x10
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x48
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
          .byte 0x88
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xec
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_41ee30 - .
          .byte 0x6b
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
          .byte 0xe0
          .byte 0x2
          .byte 0x2
          .byte 0x60
          .byte 0xe
          .byte 0xcc
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0xe0
          .byte 0x2
          .byte 0x74
          .byte 0xe
          .byte 0xd0
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0xe0
          .byte 0x2
          .byte 0x78
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
          .byte 0x53
          .byte 0xe
          .byte 0xd0
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0xe0
          .byte 0x2
          .byte 0x7a
          .byte 0xe
          .byte 0xcc
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0xe0
          .byte 0x2
          .byte 0x7b
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
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0xd0
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0xe0
          .byte 0x2
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0xcc
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0xe0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x64
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_41f1a0 - .
          .byte 0x85
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
          .byte 0x78
          .byte 0xe
          .byte 0x30
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0x64
          .byte 0xe
          .byte 0x30
          .byte 0x43
          .byte 0xe
          .byte 0x40
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
          .byte 0x4b
          .byte 0xb
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0x30
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x6d
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
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_41f330 - .
          .byte 0x5a
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
          .byte 0x6b
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
          .byte 0x60
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
          .byte 0x18
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long L_41f390 - .
          .byte 0xd6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x5d
          .byte 0xe
          .byte 0x24
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x61
          .byte 0xe
          .byte 0x2c
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x6b
          .byte 0xe
          .byte 0x24
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x4e
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x63
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x49
          .byte 0xb
          .byte 0x63
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_41f470 - .
          .byte 0x8a
          .byte 0x2
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
          .byte 0x40
          .byte 0x66
          .byte 0xe
          .byte 0x30
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x5c
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x3
          .byte 0x33
          .byte 0x2
          .byte 0xe
          .byte 0x8
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x64
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x84
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_41f700 - .
          .byte 0xfc
          .byte 0x2
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
          .byte 0xf0
          .byte 0x3
          .byte 0x5c
          .byte 0xe
          .byte 0xe8
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0xf0
          .byte 0x3
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xdc
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0xf0
          .byte 0x3
          .byte 0x2
          .byte 0x61
          .byte 0xe
          .byte 0xe4
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0xf0
          .byte 0x3
          .byte 0x65
          .byte 0xe
          .byte 0xec
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0xf0
          .byte 0x3
          .byte 0x67
          .byte 0xe
          .byte 0xe4
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0xf0
          .byte 0x3
          .byte 0x78
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x47
          .byte 0xb
          .byte 0x2
          .byte 0xed
          .byte 0xe
          .byte 0xe4
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0xf0
          .byte 0x3
          .byte 0x61
          .byte 0xe
          .byte 0xec
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0xf0
          .byte 0x3
          .byte 0x67
          .byte 0xe
          .byte 0xe4
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0xf0
          .byte 0x3
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xec
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long L_41fa00 - .
          .byte 0x35
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x6b
          .byte 0xe
          .byte 0x1c
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x43
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x24
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_41fa40 - .
          .byte 0xa6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x7a
          .byte 0xe
          .byte 0x10
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x44
          .byte 0xe
          .byte 0x1c
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x43
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x46
          .byte 0xb
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_41faf0 - .
          .byte 0x3e
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
          .byte 0x46
          .byte 0xe
          .byte 0xb0
          .byte 0x2
          .byte 0x2
          .byte 0x98
          .byte 0xe
          .byte 0xa0
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0xb0
          .byte 0x2
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
          .byte 0x49
          .byte 0xb
          .byte 0x2
          .byte 0x46
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
          .byte 0x42
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x88
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_41fc30 - .
          .byte 0x2e
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
          .byte 0x46
          .byte 0xe
          .byte 0xb0
          .byte 0x2
          .byte 0x2
          .byte 0x89
          .byte 0xe
          .byte 0xa0
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0xb0
          .byte 0x2
          .byte 0x5e
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
          .byte 0x4a
          .byte 0xb
          .byte 0x2
          .byte 0x46
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x43
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd0
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_41fd60 - .
          .byte 0xa5
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
          .byte 0x46
          .byte 0xe
          .byte 0xb0
          .byte 0x2
          .byte 0x2
          .byte 0x71
          .byte 0xe
          .byte 0xa0
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0xb0
          .byte 0x2
          .byte 0x4a
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
          .byte 0x52
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
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_41fe10 - .
          .byte 0x6
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
          .byte 0x28
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_41fe20 - .
          .byte 0x66
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
          .byte 0x40
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0x30
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x5e
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x2
          .byte 0xd4
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
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
          .byte 0x60
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_41ff90 - .
          .byte 0x4b
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
          .byte 0x6a
          .byte 0xe
          .byte 0x10
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x48
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x43
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x90
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_41ffe0 - .
          .byte 0x5b
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
          .byte 0x30
          .byte 0x6e
          .byte 0xe
          .byte 0x20
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x48
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
          .byte 0x2
          .byte 0xb5
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x46
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
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd4
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_420140 - .
          .byte 0xb3
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
          .byte 0x40
          .byte 0x2
          .byte 0x78
          .byte 0xe
          .byte 0x30
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x47
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
          .byte 0x45
          .byte 0xb
          .byte 0x60
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
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long FUN_420200 - .
          .byte 0x17
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
          .byte 0x60
          .byte 0x2
          .byte 0x78
          .byte 0xe
          .byte 0x50
          .byte 0x43
          .byte 0xe
          .byte 0x60
          .byte 0x49
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
          .byte 0x2
          .byte 0x5c
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
          .byte 0x42
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x58
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long FUN_420320 - .
          .byte 0xf4
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
          .byte 0x60
          .byte 0x2
          .byte 0x78
          .byte 0xe
          .byte 0x50
          .byte 0x43
          .byte 0xe
          .byte 0x60
          .byte 0x49
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
          .byte 0x73
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
          .byte 0x4b
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9c
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long FUN_420420 - .
          .byte 0x4b
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
          .byte 0x6a
          .byte 0xe
          .byte 0x10
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x48
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x43
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xcc
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long FUN_420470 - .
          .byte 0x58
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
          .byte 0x83
          .byte 0x3
          .byte 0x46
          .byte 0xe
          .byte 0xc0
          .byte 0x2
          .byte 0x2
          .byte 0xaf
          .byte 0xe
          .byte 0xb0
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0xc0
          .byte 0x2
          .byte 0x4e
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x46
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long FUN_4205d0 - .
          .byte 0x99
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
          .byte 0x40
          .byte 0x66
          .byte 0xe
          .byte 0x30
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x4a
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x73
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long FUN_420670 - .
          .byte 0x99
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
          .byte 0x40
          .byte 0x66
          .byte 0xe
          .byte 0x30
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x4a
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x73
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long FUN_420710 - .
          .byte 0x24
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
          .byte 0x83
          .byte 0x3
          .byte 0x48
          .byte 0xe
          .byte 0xc0
          .byte 0x2
          .byte 0x2
          .byte 0x9e
          .byte 0xe
          .byte 0xb0
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0xc0
          .byte 0x2
          .byte 0x4c
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x47
          .byte 0xb
          .byte 0x76
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb0
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long FUN_420840 - .
          .byte 0xcd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x56
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x47
          .byte 0xb
          .byte 0x7a
          .byte 0xe
          .byte 0x10
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x61
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x42
          .byte 0xb
          .byte 0x2
          .byte 0x4c
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x64
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xdc
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long FUN_420910 - .
          .byte 0x7a
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
          .byte 0x6c
          .byte 0xe
          .byte 0x40
          .byte 0x43
          .byte 0xe
          .byte 0x50
          .byte 0x4a
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
          .byte 0x72
          .byte 0xe
          .byte 0x40
          .byte 0x43
          .byte 0xe
          .byte 0x50
          .byte 0x2
          .byte 0x48
          .byte 0xe
          .byte 0x40
          .byte 0x43
          .byte 0xe
          .byte 0x50
          .byte 0x2
          .byte 0x66
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

.bss
.p2align 2
L_479574:
          .zero 4
L_479578:
          .zero 4
