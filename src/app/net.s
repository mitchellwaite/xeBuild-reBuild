# app/net.s -- winsock: beacon, send/recv
#
# mixed: `#@C name` lines are functions from net.c (re/splice.py)
#
# original placement:
#   .bss           00479574-0047957c
#   .data          0044a6c0-0044a6e0
#   .eh_frame      00468bd0-00469410
#   .rdata         004574b0-00457a80
#   .rdata$zzz     00463a64-00463a90
#   .text          0041e800-00420a90

.intel_syntax noprefix
.globl _netConnect
.globl _netEmpty
.globl _netInfo
.globl _netRecv
.globl _netRecvVerbose
.globl _netSock
.globl _netWritePatches
.globl _net_457568
.globl _net_45758c
.globl _net_4575bc
.globl _net_4575e1
.globl _net_4575f3
.globl _net_457608
.globl _net_45763e
.globl _net_457688
.globl _net_4576ac
.globl _net_4576cf
.globl _net_4576e8
.globl _net_457712
.globl _net_45772f
.globl _net_457732
.globl _net_457736
.globl _net_45773c
.globl _net_457746
.globl _net_457758
.globl _net_457784
.globl _net_4577bb
.globl _net_4578f5
.globl _net_457913
.globl _net_457919
.globl _net_45791d
.globl _net_457925
.globl _net_457931
.globl _net_457947
.globl _net_457950
.globl _net_457962
.globl _net_45796c
.globl _net_457990
.globl _net_457998
.globl _net_4579cb
.globl _net_4579d1
.globl _net_4579d8
.globl _net_4579f9
.globl _net_457a07
.globl _net_457a15
.globl _net_457a23
.globl _net_457a29
.globl _net_457a2f
.globl _net_457a35
.globl _net_457a51
.globl _net_457a57
.globl _net_457a71

.text
.p2align 4
_netRecv:
          push EBP
          push EDI
          mov EDX,EAX
          push ESI
          push EBX
          sub ESP,332
          mov DWORD PTR [ESP+44],EAX
          mov EAX,DWORD PTR [_netSock]
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
          mov EAX,DWORD PTR [__imp__select@20]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+36],EAX
          call EAX
          add EAX,1
          sub ESP,20
          cmp EAX,1
          jbe L_41ea10
          mov EAX,DWORD PTR [_netSock]
          lea EBX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],4
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          mov EAX,DWORD PTR [__imp__recv@16]
          mov DWORD PTR [ESP+40],EAX
          call EAX
          add EAX,1
          sub ESP,16
          cmp EAX,1
          jbe L_41ea35
          mov DWORD PTR [ESP],EBX
          call _getBeU32
          cmp EAX,-1
          mov EBX,EAX
          je L_41e99b
          test EAX,EAX
          jne L_41e8e5
          mov EAX,DWORD PTR [ESP+44]
          mov ESI,OFFSET _netEmpty
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
          mov EAX,DWORD PTR [_netSock]
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
          call DWORD PTR [__imp__WSAGetLastError@0]
          mov DWORD PTR [ESP+4],OFFSET L_4574f4
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp ESI,OFFSET _netEmpty
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
          call DWORD PTR [__imp__WSAGetLastError@0]
          mov DWORD PTR [ESP+4],OFFSET L_457518
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp ESI,OFFSET _netEmpty
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
          cmp ESI,OFFSET _netEmpty
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
          call DWORD PTR [__imp__WSAGetLastError@0]
          mov DWORD PTR [ESP+4],OFFSET L_4574b0
          mov DWORD PTR [ESP+8],EAX
          xor ESI,ESI
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41e8d8
L_41ea35:
          call DWORD PTR [__imp__WSAGetLastError@0]
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
#@C _netFree
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _netFindBeacon
          .byte 0x66
          .byte 0x90
#@C _netTimerStart
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
#@C _netTimerEnd
#@C _netTimerElapsed
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _netSendStr
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
_netRecvVerbose:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,332
          mov EAX,DWORD PTR [_netSock]
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
          mov EAX,DWORD PTR [__imp__select@20]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+40],EAX
          call EAX
          add EAX,1
          sub ESP,20
          cmp EAX,1
          jbe L_41f140
          mov EAX,DWORD PTR [_netSock]
          lea EBX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],4
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          mov EAX,DWORD PTR [__imp__recv@16]
          mov DWORD PTR [ESP+44],EAX
          call EAX
          add EAX,1
          sub ESP,16
          cmp EAX,1
          jbe L_41f165
          mov DWORD PTR [ESP],EBX
          call _getBeU32
          cmp EAX,-1
          mov ESI,EAX
          je L_41efe9
          test EAX,EAX
          jne L_41ef20
          mov EAX,DWORD PTR [ESP+352]
          mov EDI,OFFSET _netEmpty
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
          mov EAX,DWORD PTR [_netSock]
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
          call DWORD PTR [__imp__WSAGetLastError@0]
          mov DWORD PTR [ESP+4],OFFSET L_4574f4
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp EDI,OFFSET _netEmpty
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
          mov EAX,DWORD PTR [_netSock]
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
          call DWORD PTR [__imp__WSAGetLastError@0]
          mov DWORD PTR [ESP+4],OFFSET L_457518
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp EDI,OFFSET _netEmpty
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
          cmp EDI,OFFSET _netEmpty
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
          call DWORD PTR [__imp__WSAGetLastError@0]
          mov DWORD PTR [ESP+4],OFFSET L_4574b0
          mov DWORD PTR [ESP+8],EAX
          xor EDI,EDI
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41ef0c
L_41f165:
          call DWORD PTR [__imp__WSAGetLastError@0]
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
#@C _netSendData
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
#@C _netCheckOk
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _netOpenSocket
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _netReadInfo
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
_netConnect:
          push EBX
          sub ESP,488
          lea EAX,DWORD PTR [ESP+80]
          mov EBX,DWORD PTR [ESP+496]
          mov DWORD PTR [ESP],514
          mov DWORD PTR [ESP+4],EAX
          call DWORD PTR [__imp__WSAStartup@8]
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
          call DWORD PTR [__imp__WSAStringToAddressA@20]
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
          call DWORD PTR [__imp__socket@12]
          sub ESP,12
          cmp EAX,-1
          mov DWORD PTR [_netSock],EAX
          je L_41f9c0
          mov EAX,2
          mov DWORD PTR [ESP],49
          mov WORD PTR [ESP+64],AX
          call DWORD PTR [__imp__htons@4]
          sub ESP,4
          mov WORD PTR [ESP+66],AX
          lea EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+68],EBX
          mov DWORD PTR [ESP+8],16
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [_netSock]
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [__imp__connect@12]
          sub ESP,12
          test EAX,EAX
          .byte 0x0f,0x88; .long L_41f8a4-.-4   # js L_41f8a4
          mov DWORD PTR [ESP+4],OFFSET _net_45773c
          mov DWORD PTR [ESP],0
L_41f837:
          call _log_printf
          call _netReadInfo
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
          call DWORD PTR [__imp__WSAGetLastError@0]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45787c
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41f850
L_41f884:
          call DWORD PTR [__imp__WSAGetLastError@0]
          mov DWORD PTR [ESP+4],OFFSET L_4578b5
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41f850
L_41f8a4:
          call DWORD PTR [__imp__WSAGetLastError@0]
          mov DWORD PTR [ESP+4],OFFSET _net_457712
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41f850
L_41f8c4:
          mov DWORD PTR [ESP+4],OFFSET L_4577c4
          mov DWORD PTR [ESP],0
          call _log_printf
          call _netFindBeacon
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
          call DWORD PTR [__imp__socket@12]
          sub ESP,12
          cmp EAX,-1
          mov DWORD PTR [_netSock],EAX
          je L_41f9c0
          mov EDX,2
          mov DWORD PTR [ESP],49
          mov WORD PTR [ESP+64],DX
          call DWORD PTR [__imp__htons@4]
          sub ESP,4
          mov WORD PTR [ESP+66],AX
          lea EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+68],EBX
          mov DWORD PTR [ESP+8],16
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [_netSock]
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [__imp__connect@12]
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
          call DWORD PTR [__imp__WSAGetLastError@0]
          mov DWORD PTR [ESP+4],OFFSET _net_4576e8
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
#@C _netClose
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
#@C _netDisconnect
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _netMount
          .byte 0x66
          .byte 0x90
#@C _netUnmount
          .byte 0x66
          .byte 0x90
#@C _netGetFile
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
#@C _netGetInfo
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _netDumpNand
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _netGetBldrs
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _netSendFlash
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _netReadBlocks
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
#@C _netWriteBlocks
L_420317:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _netEraseBlock
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
#@C _netGetBadBlocks
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _netSendFile
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _netFormatSysex
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _netFormatCompat
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _netMkdir
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
#@C _netReboot
          .byte 0x8d
          .byte 0x76
          .byte 0x0
_netWritePatches:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EAX,DWORD PTR [_netSock]
          mov ESI,DWORD PTR [__imp__send@16]
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
          call _setBeU32
          lea EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],4
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [_netSock]
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
          mov EAX,DWORD PTR [_netSock]
          mov DWORD PTR [ESP],EAX
          call ESI
          sub ESP,16
          cmp EAX,-1
          jne L_4209a0
          call DWORD PTR [__imp__WSAGetLastError@0]
          mov DWORD PTR [ESP+4],OFFSET _net_4576ac
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_42094b
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_420a00:
          lea EAX,DWORD PTR [ESP+44]
          call _netRecv
          test EAX,EAX
          mov EBX,EAX
          je L_42094b
          cmp DWORD PTR [ESP+44],2
          je L_420a63
L_420a1a:
          xor EAX,EAX
          cmp EBX,OFFSET _netEmpty
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
          call DWORD PTR [__imp__WSAGetLastError@0]
          mov DWORD PTR [ESP+4],OFFSET _net_457688
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_42094b
L_420a63:
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          cmp AX,20299
          jne L_420a1a
          cmp EBX,OFFSET _netEmpty
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
_netSock:
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
_net_457568:
          .string "unable to open socket, error %d\n"
          .zero 3
_net_45758c:
          .string "unable to set bcast socket option, error %d\n"
          .zero 3
_net_4575bc:
          .string "unable to set bind socket, error %d\n"
_net_4575e1:
          .string "Socket error! %d\n"
_net_4575f3:
          .string "UDP wait timeout!\n"
          .zero 2
_net_457608:
          .string "Beacon received, but the beacon magic %X was not %X!\n"
_net_45763e:
          .string "Completed in %.0fs\n"
L_457652:
          .string "waiting for 0x%x bytes\n"
L_45766a:
          .string "received 0x%08x of 0x%08x\r"
          .zero 3
_net_457688:
          .string "socket error sending data size, %d\n"
_net_4576ac:
          .string "socket error sending data (1), %d\n"
_net_4576cf:
          .string "sent 0x%08x of 0x%08x\r"
          .zero 2
_net_4576e8:
          .string "could not create client socket, error %d\n"
_net_457712:
          .string "could not connect, error %d\n"
_net_45772f:
          .string "No"
_net_457732:
          .string "Yes"
_net_457736:
          .string "GTIN\n"
_net_45773c:
          .string "success!\n"
_net_457746:
          .string "connected to %s"
          .zero 2
_net_457758:
          .string " with updsvr version %d (peek version %d)\n"
          .zero 1
_net_457784:
          .string "NAND image size: 0x%x Block size: 0x%x Spare Data: %s\n"
_net_4577bb:
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
_net_4578f5:
          .string "\ndisconnecting from server..."
_net_457913:
          .string "QUIT\n"
_net_457919:
          .string "OK\n"
_net_45791d:
          .string "failed\n"
_net_457925:
          .string "MTPT%s: %s\n"
_net_457931:
          .string "mounting %s to %s:..."
_net_457947:
          .string "UMPT%s:\n"
_net_457950:
          .string "unmounting %s:..."
_net_457962:
          .string "GETF%s\n"
          .zero 2
_net_45796c:
          .string "reading flash image from console..."
_net_457990:
          .string "GTFL\n"
          .zero 2
_net_457998:
          .string "received 0x%x bytes data OK, writing to file %s..."
_net_4579cb:
          .string "GTBL\n"
_net_4579d1:
          .string "WRFL\n"
          .zero 1
_net_4579d8:
          .string "file sent OK, awaiting result..."
_net_4579f9:
          .string "RBLK%04x%04x\n"
_net_457a07:
          .string "WBLK%04x%04x\n"
_net_457a15:
          .string "ERBL%04x%04x\n"
_net_457a23:
          .string "GTBB\n"
_net_457a29:
          .string "FMEX\n"
_net_457a2f:
          .string "FMCM\n"
_net_457a35:
          .string "sending shutdown command..."
_net_457a51:
          .string "SHDN\n"
_net_457a57:
          .string "sending reboot command..."
_net_457a71:
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
          .long _netRecv - .
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
          .long _netFree - .
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
          .long _netFindBeacon - .
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
          .long _netTimerStart - .
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
          .long _netTimerEnd - .
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
          .long _netTimerElapsed - .
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
          .long _netSendStr - .
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
          .long _netRecvVerbose - .
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
          .long _netSendData - .
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
          .long _netCheckOk - .
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
          .long _netOpenSocket - .
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
          .long _netReadInfo - .
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
          .long _netConnect - .
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
          .long _netClose - .
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
          .long _netDisconnect - .
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
          .long _netMount - .
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
          .long _netUnmount - .
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
          .long _netGetFile - .
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
          .long _netGetInfo - .
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
          .long _netDumpNand - .
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
          .long _netGetBldrs - .
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
          .long _netSendFlash - .
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
          .long _netReadBlocks - .
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
          .long _netWriteBlocks - .
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
          .long _netEraseBlock - .
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
          .long _netGetBadBlocks - .
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
          .long _netSendFile - .
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
          .long _netFormatSysex - .
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
          .long _netFormatCompat - .
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
          .long _netMkdir - .
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
          .long _netReboot - .
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
          .long _netWritePatches - .
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
_netInfo:
          .zero 4
_netEmpty:
          .zero 4
