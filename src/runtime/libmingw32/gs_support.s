# runtime/libmingw32/gs_support.s -- byte match
#
# original placement:
#   .bss           00479ae0-00479e34
#   .data          0044b6cc-0044b6d4
#   .eh_frame      0046e034-0046e0c8
#   .rdata         00463284-00463290
#   .rdata$zzz     00464380-004643ac
#   .text          00446cd0-00446e10

.intel_syntax noprefix
.globl FUN_446cd0
.globl L_46328c
.globl L_479e20
.globl L_479e24
.globl L_479e28
.globl L_479e2c
.globl L_479e30

.text
.p2align 4
FUN_446cd0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EAX,DWORD PTR [L_44b6cc]
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+20],0
          cmp EAX,3141592654
          je L_446d02
          not EAX
          mov DWORD PTR [L_44b6d0],EAX
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_446d02:
          lea EAX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [GetSystemTimeAsFileTime]
          sub ESP,4
          mov EBX,DWORD PTR [ESP+16]
          xor EBX,DWORD PTR [ESP+20]
          call DWORD PTR [GetCurrentProcessId]
          mov EBP,EAX
          call DWORD PTR [GetCurrentThreadId]
          mov EDI,EAX
          call DWORD PTR [GetTickCount]
          mov ESI,EAX
          lea EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [QueryPerformanceCounter]
          sub ESP,4
          mov EAX,DWORD PTR [ESP+24]
          xor EAX,EBX
          xor EAX,DWORD PTR [ESP+28]
          xor EAX,EBP
          xor EAX,EDI
          xor EAX,ESI
          cmp EAX,3141592654
          je L_446d70
          mov EDX,EAX
          not EDX
L_446d5d:
          mov DWORD PTR [L_44b6cc],EAX
          mov DWORD PTR [L_44b6d0],EDX
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_446d70:
          mov EDX,1153374640
          mov EAX,3141592655
          jmp L_446d5d
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_446d80:
          push EBP
          mov EBP,ESP
          sub ESP,40
          mov DWORD PTR [L_479dc0],3221226505
          mov EAX,DWORD PTR [EBP+4]
          lea EDX,DWORD PTR [EBP+4]
          mov DWORD PTR [L_479dc4],1
          mov DWORD PTR [ESP],0
          mov DWORD PTR [L_479ba4],EDX
          mov DWORD PTR [L_479b98],EAX
          mov DWORD PTR [L_479dcc],EAX
          mov EAX,DWORD PTR [EBP+8]
          mov DWORD PTR [L_479b8c],EAX
          mov EAX,DWORD PTR [L_44b6cc]
          mov DWORD PTR [EBP-16],EAX
          mov EAX,DWORD PTR [L_44b6d0]
          mov DWORD PTR [EBP-12],EAX
          call DWORD PTR [SetUnhandledExceptionFilter]
          sub ESP,4
          mov DWORD PTR [ESP],OFFSET L_463284
          call DWORD PTR [UnhandledExceptionFilter]
          sub ESP,4
          call DWORD PTR [GetCurrentProcess]
          mov DWORD PTR [ESP+4],3221226505
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [TerminateProcess]
          sub ESP,8
          call FUN_4491b0
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
.p2align 2
L_44b6cc:
          .byte 0x4e
          .byte 0xe6
          .byte 0x40
          .byte 0xbb
L_44b6d0:
          .byte 0xb1
          .byte 0x19
          .byte 0xbf
          .byte 0x44

.section .rdata,"dr"
.p2align 2
L_463284:
          .long L_479dc0
          .long L_479ae0
L_46328c:
          .long FUN_446e60

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
          .byte 0x5c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_446cd0 - .
          .byte 0xac
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
          .byte 0x4d
          .byte 0xe
          .byte 0x3c
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x6d
          .byte 0xe
          .byte 0x3c
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x69
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
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_446d80 - .
          .byte 0x87
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x42
          .byte 0xd
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0

.bss
.p2align 2
L_479ae0:
          .zero 172
L_479b8c:
          .zero 12
L_479b98:
          .zero 12
L_479ba4:
          .zero 540
L_479dc0:
          .zero 4
L_479dc4:
          .zero 8
L_479dcc:
          .zero 84
L_479e20:
          .zero 4
L_479e24:
          .zero 4
L_479e28:
          .zero 4
L_479e2c:
          .zero 4
L_479e30:
          .zero 4
