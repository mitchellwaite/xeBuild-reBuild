# runtime/libmingw32/tlsthrd.s -- byte match
#
# original placement:
#   .bss           00479e50-00479e74
#   .eh_frame      0046e31c-0046e448
#   .rdata$zzz     004644b4-004644e0
#   .text          00447600-00447880

.intel_syntax noprefix
.globl FUN_4477a0

.text
.p2align 4
FUN_447600:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov DWORD PTR [ESP],OFFSET L_479e58
          call DWORD PTR [EnterCriticalSection]
          mov EBX,DWORD PTR [L_479e50]
          sub ESP,4
          mov EBP,DWORD PTR [TlsGetValue]
          mov EDI,DWORD PTR [GetLastError]
          test EBX,EBX
          je L_447655
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_447630:
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP],EAX
          call EBP
          sub ESP,4
          mov ESI,EAX
          call EDI
          test EAX,EAX
          jne L_44764e
          test ESI,ESI
          je L_44764e
          mov EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP],ESI
          call EAX
L_44764e:
          mov EBX,DWORD PTR [EBX+8]
          test EBX,EBX
          jne L_447630
L_447655:
          mov DWORD PTR [ESP],OFFSET L_479e58
          call DWORD PTR [LeaveCriticalSection]
          sub ESP,4
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_447670:
          push ESI
          push EBX
          xor ESI,ESI
          sub ESP,20
          mov EAX,DWORD PTR [L_479e54]
          test EAX,EAX
          jne L_447690
L_447680:
          add ESP,20
          mov EAX,ESI
          pop EBX
          pop ESI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_447690:
          mov DWORD PTR [ESP+4],12
          mov DWORD PTR [ESP],1
          call _calloc
          test EAX,EAX
          mov EBX,EAX
          je L_4476ed
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],OFFSET L_479e58
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [EBX+4],EAX
          call DWORD PTR [EnterCriticalSection]
          mov EAX,DWORD PTR [L_479e50]
          sub ESP,4
          mov DWORD PTR [L_479e50],EBX
          mov DWORD PTR [ESP],OFFSET L_479e58
          mov DWORD PTR [EBX+8],EAX
          call DWORD PTR [LeaveCriticalSection]
          sub ESP,4
          mov EAX,ESI
          add ESP,20
          pop EBX
          pop ESI
          ret 
L_4476ed:
          mov ESI,4294967295
          jmp L_447680
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
L_447700:
          push EBX
          sub ESP,24
          mov EAX,DWORD PTR [L_479e54]
          mov EBX,DWORD PTR [ESP+32]
          test EAX,EAX
          jne L_447720
          add ESP,24
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
L_447720:
          mov DWORD PTR [ESP],OFFSET L_479e58
          call DWORD PTR [EnterCriticalSection]
          mov EDX,DWORD PTR [L_479e50]
          sub ESP,4
          test EDX,EDX
          je L_447751
          mov EAX,DWORD PTR [EDX]
          cmp EBX,EAX
          jne L_44774a
          jmp L_447790
L_447742:
          mov ECX,DWORD PTR [EAX]
          cmp ECX,EBX
          je L_447770
          mov EDX,EAX
L_44774a:
          mov EAX,DWORD PTR [EDX+8]
          test EAX,EAX
          jne L_447742
L_447751:
          mov DWORD PTR [ESP],OFFSET L_479e58
          call DWORD PTR [LeaveCriticalSection]
          sub ESP,4
L_447761:
          add ESP,24
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
L_447770:
          mov ECX,DWORD PTR [EAX+8]
          mov DWORD PTR [EDX+8],ECX
L_447776:
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP],OFFSET L_479e58
          call DWORD PTR [LeaveCriticalSection]
          sub ESP,4
          jmp L_447761
L_447790:
          mov EAX,DWORD PTR [EDX+8]
          mov DWORD PTR [L_479e50],EAX
          mov EAX,EDX
          jmp L_447776
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_4477a0:
          push EBX
          sub ESP,24
          mov EAX,DWORD PTR [ESP+36]
          cmp EAX,1
          je L_447840
          jb L_4477e0
          cmp EAX,2
          je L_4477d0
          cmp EAX,3
          jne L_4477d5
          mov EAX,DWORD PTR [L_479e54]
          test EAX,EAX
          je L_4477d5
          call FUN_447600
          jmp L_4477d5
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4477d0:
          call FUN_446fb0
L_4477d5:
          add ESP,24
          mov EAX,1
          pop EBX
          ret 
          .byte 0x90
L_4477e0:
          mov EAX,DWORD PTR [L_479e54]
          test EAX,EAX
          jne L_447872
L_4477ed:
          mov EAX,DWORD PTR [L_479e54]
          cmp EAX,1
          jne L_4477d5
          mov EAX,DWORD PTR [L_479e50]
          test EAX,EAX
          je L_447811
L_447800:
          mov EBX,DWORD PTR [EAX+8]
          mov DWORD PTR [ESP],EAX
          call _free
          test EBX,EBX
          mov EAX,EBX
          jne L_447800
L_447811:
          mov DWORD PTR [L_479e50],0
          mov DWORD PTR [L_479e54],0
          mov DWORD PTR [ESP],OFFSET L_479e58
          call DWORD PTR [DeleteCriticalSection]
          sub ESP,4
          jmp L_4477d5
L_447837:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_447840:
          mov EAX,DWORD PTR [L_479e54]
          test EAX,EAX
          je L_447860
L_447849:
          mov DWORD PTR [L_479e54],1
          add ESP,24
          mov EAX,1
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_447860:
          mov DWORD PTR [ESP],OFFSET L_479e58
          call DWORD PTR [InitializeCriticalSection]
          sub ESP,4
          jmp L_447849
L_447872:
          call FUN_447600
          jmp L_4477ed
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

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
          .byte 0x4c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_447600 - .
          .byte 0x6d
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
          .byte 0x4d
          .byte 0xe
          .byte 0x2c
          .byte 0x49
          .byte 0xe
          .byte 0x30
          .byte 0x5a
          .byte 0xe
          .byte 0x2c
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x68
          .byte 0xe
          .byte 0x2c
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x43
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
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_447670 - .
          .byte 0x84
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
          .byte 0x4c
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
          .byte 0x49
          .byte 0xb
          .byte 0x74
          .byte 0xe
          .byte 0x1c
          .byte 0x48
          .byte 0xe
          .byte 0x20
          .byte 0x56
          .byte 0xe
          .byte 0x1c
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x45
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
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_447700 - .
          .byte 0x9c
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
          .byte 0x50
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x49
          .byte 0xb
          .byte 0x4d
          .byte 0xe
          .byte 0x1c
          .byte 0x49
          .byte 0xe
          .byte 0x20
          .byte 0x68
          .byte 0xe
          .byte 0x1c
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x43
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x49
          .byte 0xb
          .byte 0x5b
          .byte 0xe
          .byte 0x1c
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4477a0 - .
          .byte 0xdc
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
          .byte 0x74
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x42
          .byte 0xb
          .byte 0x2
          .byte 0x52
          .byte 0xe
          .byte 0x1c
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x61
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x4d
          .byte 0xe
          .byte 0x1c
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x0
          .byte 0x0

.bss
.p2align 2
L_479e50:
          .zero 4
L_479e54:
          .zero 4
L_479e58:
          .zero 28
