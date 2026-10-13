# app/xboxrom.s -- XBOX_ROM_B/4/3 names
#
# original placement:
#   .data          0044a540-0044a580
#   .eh_frame      00466a88-00466be0
#   .rdata$zzz     00463930-0046395c
#   .text          0040e520-0040e950

.intel_syntax noprefix
.globl FUN_40e520
.globl FUN_40e5a0
.globl FUN_40e620
.globl FUN_40e690
.globl FUN_40e7b0
.globl FUN_40e8a0

.text
.p2align 4
FUN_40e520:
          push ESI
          push EBX
          sub ESP,84
          mov EBX,DWORD PTR [ESP+96]
          lea ESI,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+36],20
          mov DWORD PTR [ESP+28],8456
          mov DWORD PTR [ESP+20],7416
          mov DWORD PTR [ESP+32],ESI
          mov DWORD PTR [ESP+12],212
          lea EAX,DWORD PTR [EBX+7928]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+24],EAX
          lea EAX,DWORD PTR [EBX+256]
          mov DWORD PTR [ESP+16],EAX
          lea EAX,DWORD PTR [EBX+28]
          add EBX,7672
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP],EAX
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call _XeKeysPkcs1Verify
          add ESP,84
          pop EBX
          pop ESI
          ret 
FUN_40e5a0:
          push ESI
          push EBX
          sub ESP,68
          mov EBX,DWORD PTR [ESP+80]
          lea ESI,DWORD PTR [ESP+44]
          lea EAX,DWORD PTR [EBX+12]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          add EAX,15
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [ESP],EBX
          and EAX,4294967280
          mov DWORD PTR [ESP+20],20
          mov DWORD PTR [ESP+4],16
          sub EAX,320
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [EBX+320]
          add EBX,64
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptRotSumSha
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],OFFSET L_44a558
          mov DWORD PTR [ESP+12],EAX
          call _XeCryptBnQwBeSigVerify
          add ESP,68
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
FUN_40e620:
          push ESI
          push EBX
          sub ESP,68
          mov EAX,DWORD PTR [ESP+84]
          mov EBX,DWORD PTR [ESP+80]
          lea ESI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+20],20
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+16],ESI
          sub EAX,288
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [EBX+288]
          add EBX,32
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptRotSumSha
          mov EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+92]
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptBnQwBeSigVerify
          add ESP,68
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
FUN_40e690:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,348
          mov EBX,DWORD PTR [ESP+384]
          mov DWORD PTR [ESP+52],0
          lea EBP,DWORD PTR [ESP+60]
          mov EDI,DWORD PTR [ESP+368]
          mov DWORD PTR [ESP+56],0
          lea ESI,DWORD PTR [ESP+80]
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP+44],EAX
          mov EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP+48],EAX
          movzx EAX,WORD PTR [EBX+8]
          mov DWORD PTR [ESP+20],20
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],EDI
          mov WORD PTR [ESP+52],AX
          mov EAX,DWORD PTR [ESP+372]
          sub EAX,288
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [EDI+288]
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptRotSumSha
          mov EAX,DWORD PTR [ESP+380]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+12],EAX
          call _XeCryptBnQwBeSigCreate
          test EAX,EAX
          jne L_40e740
L_40e72b:
          xor EAX,EAX
L_40e72d:
          add ESP,348
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
L_40e740:
          mov EAX,DWORD PTR [ESP+380]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptBnQwNeRsaPrvCrypt
          test EAX,EAX
          je L_40e72b
          mov EAX,DWORD PTR [ESP+376]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+12],EAX
          call _XeCryptBnQwBeSigVerify
          test EAX,EAX
          je L_40e72b
          mov EAX,DWORD PTR [ESI]
          lea ECX,DWORD PTR [EDI+32]
          add EDI,36
          mov DWORD PTR [EDI-4],EAX
          mov EAX,DWORD PTR [ESI+252]
          mov DWORD PTR [EDI+248],EAX
          and EDI,4294967292
          mov EAX,1
          sub ECX,EDI
          sub ESI,ECX
          add ECX,256
          shr ECX,2
          rep movsd 
          jmp L_40e72d
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_40e7b0:
          push EBX
          sub ESP,72
          mov EAX,DWORD PTR [ESP+84]
          mov EDX,DWORD PTR [ESP+80]
          lea EBX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+20],20
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+16],EBX
          sub EAX,32
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [EDX+32]
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptRotSumSha
          mov EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP],EAX
          call _memcmp
          test EAX,EAX
          sete AL
          add ESP,72
          movzx EAX,AL
          pop EBX
          ret 
          .byte 0x90
L_40e810:
          push ESI
          push EBX
          sub ESP,68
          mov EAX,DWORD PTR [ESP+84]
          mov EDX,DWORD PTR [ESP+80]
          lea ESI,DWORD PTR [ESP+44]
          mov EBX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+20],20
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [ESP+4],16
          sub EAX,32
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [EDX+32]
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptRotSumSha
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call _memcmp
          test EAX,EAX
          je L_40e88e
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [EBX+4],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [EBX+8],EAX
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [EBX+12],EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [EBX+16],EAX
          mov EAX,1
L_40e88e:
          add ESP,68
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
FUN_40e8a0:
          push ESI
          push EBX
          sub ESP,68
          lea EAX,DWORD PTR [ESP+44]
          mov EDX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+20],20
          mov DWORD PTR [ESP+4],16
          mov EBX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP],EDX
          mov ESI,DWORD PTR [ESP+88]
          sub EAX,32
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [EDX+32]
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptRotSumSha
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [EBX+4],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [EBX+8],EAX
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [EBX+12],EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [EBX+16],EAX
          mov DWORD PTR [ESP],ESI
          call _getBeU16
          mov EDX,OFFSET L_44a540
          cmp AX,21316
          mov EAX,OFFSET L_44a54c
          cmove EAX,EDX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+92]
          mov DWORD PTR [ESP+4],EAX
          call FUN_40e690
          add ESP,68
          pop EBX
          pop ESI
          ret 
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          nop
          nop
          nop
          nop

.data
.p2align 5
L_44a540:
          .string "XBOX_ROM_4"
          .zero 1
L_44a54c:
          .string "XBOX_ROM_3"
          .zero 1
L_44a558:
          .string "XBOX_ROM_B"
          .zero 29

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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40e520 - .
          .byte 0x80
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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40e5a0 - .
          .byte 0x72
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
          .byte 0x6a
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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x74
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40e620 - .
          .byte 0x65
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
          .byte 0x5d
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40e690 - .
          .byte 0x1a
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
          .byte 0xf0
          .byte 0x2
          .byte 0x2
          .byte 0x99
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
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40e7b0 - .
          .byte 0x5f
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
          .byte 0x50
          .byte 0x2
          .byte 0x56
          .byte 0xe
          .byte 0x8
          .byte 0x44
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_40e810 - .
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
          .byte 0x43
          .byte 0xe
          .byte 0x50
          .byte 0x2
          .byte 0x7c
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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_40e8a0 - .
          .byte 0xa8
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
          .byte 0xa0
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
