# runtime/libmingw32/pesect.s -- byte match
#
# original placement:
#   .eh_frame      0046e448-0046e5f0
#   .rdata$zzz     004644e0-0046450c
#   .text          00447880-00447c00

.intel_syntax noprefix
.globl FUN_447990
.globl FUN_447a00
.globl FUN_447aa0

.text
.p2align 4
FUN_447880:
          add EAX,DWORD PTR [EAX+60]
          cmp DWORD PTR [EAX],17744
          je L_447891
          xor EAX,EAX
          movzx EAX,AL
          ret 
L_447891:
          cmp WORD PTR [EAX+24],267
          sete AL
          movzx EAX,AL
          ret 
          .byte 0x66
          .byte 0x90
L_4478a0:
          mov EAX,DWORD PTR [ESP+4]
          cmp WORD PTR [EAX],23117
          je L_4478b0
          xor EAX,EAX
          ret 
          .byte 0x66
          .byte 0x90
L_4478b0:
          jmp FUN_447880
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
L_4478c0:
          push ESI
          push EBX
          mov EDX,DWORD PTR [ESP+12]
          mov EBX,DWORD PTR [ESP+16]
          add EDX,DWORD PTR [EDX+60]
          movzx ESI,WORD PTR [EDX+6]
          movzx EAX,WORD PTR [EDX+20]
          test ESI,ESI
          lea EAX,DWORD PTR [EDX+EAX*1+24]
          je L_4478f8
          xor ECX,ECX
          nop
L_4478e0:
          mov EDX,DWORD PTR [EAX+12]
          cmp EDX,EBX
          ja L_4478ee
          add EDX,DWORD PTR [EAX+8]
          cmp EBX,EDX
          jb L_4478fa
L_4478ee:
          add ECX,1
          add EAX,40
          cmp ECX,ESI
          jne L_4478e0
L_4478f8:
          xor EAX,EAX
L_4478fa:
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_447900:
          push EBP
          push EDI
          push ESI
          push EBX
          xor EBX,EBX
          sub ESP,28
          mov EDI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EDI
          call _strlen
          cmp EAX,8
          ja L_447925
          cmp WORD PTR [__image_base__],23117
          je L_447930
L_447925:
          add ESP,28
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_447930:
          mov EAX,OFFSET __image_base__
          call FUN_447880
          test EAX,EAX
          je L_447925
          mov EAX,DWORD PTR [__image_base__+60]
          movzx EDX,WORD PTR [EAX+__image_base__+20]
          add EAX,OFFSET __image_base__
          movzx EBP,WORD PTR [EAX+6]
          lea EBX,DWORD PTR [EAX+EDX*1+24]
          test EBP,EBP
          je L_447982
          xor ESI,ESI
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_447960:
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          call FUN_449068
          test EAX,EAX
          je L_447925
          add ESI,1
          add EBX,40
          cmp ESI,EBP
          jne L_447960
L_447982:
          add ESP,28
          xor EBX,EBX
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
FUN_447990:
          xor EDX,EDX
          cmp WORD PTR [__image_base__],23117
          je L_4479a0
          mov EAX,EDX
          ret 
L_4479a0:
          push ESI
          push EBX
          mov EAX,OFFSET __image_base__
          call FUN_447880
          test EAX,EAX
          je L_4479fa
          mov EAX,DWORD PTR [__image_base__+60]
          mov EBX,DWORD PTR [ESP+12]
          movzx EDX,WORD PTR [EAX+__image_base__+20]
          add EAX,OFFSET __image_base__
          sub EBX,OFFSET __image_base__
          movzx ESI,WORD PTR [EAX+6]
          lea EDX,DWORD PTR [EAX+EDX*1+24]
          test ESI,ESI
          je L_4479f8
          xor ECX,ECX
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_4479e0:
          mov EAX,DWORD PTR [EDX+12]
          cmp EBX,EAX
          jb L_4479ee
          add EAX,DWORD PTR [EDX+8]
          cmp EBX,EAX
          jb L_4479fa
L_4479ee:
          add ECX,1
          add EDX,40
          cmp ECX,ESI
          jne L_4479e0
L_4479f8:
          xor EDX,EDX
L_4479fa:
          mov EAX,EDX
          pop EBX
          pop ESI
          ret 
          .byte 0x90
FUN_447a00:
          xor EDX,EDX
          cmp WORD PTR [__image_base__],23117
          je L_447a10
L_447a0d:
          mov EAX,EDX
          ret 
L_447a10:
          mov EAX,OFFSET __image_base__
          call FUN_447880
          test EAX,EAX
          je L_447a0d
          mov EAX,DWORD PTR [__image_base__+60]
          movzx EDX,WORD PTR [EAX+__image_base__+6]
          mov EAX,EDX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_447a30:
          xor EDX,EDX
          cmp WORD PTR [__image_base__],23117
          push EBX
          mov ECX,DWORD PTR [ESP+8]
          je L_447a50
L_447a42:
          mov EAX,EDX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_447a50:
          mov EAX,OFFSET __image_base__
          call FUN_447880
          test EAX,EAX
          je L_447a42
          mov EAX,DWORD PTR [__image_base__+60]
          movzx EDX,WORD PTR [EAX+__image_base__+20]
          add EAX,OFFSET __image_base__
          movzx EBX,WORD PTR [EAX+6]
          lea EDX,DWORD PTR [EAX+EDX*1+24]
          test EBX,EBX
          je L_447a97
          xor EAX,EAX
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_447a80:
          test BYTE PTR [EDX+39],32
          je L_447a8d
          test ECX,ECX
          je L_447a42
          sub ECX,1
L_447a8d:
          add EAX,1
          add EDX,40
          cmp EAX,EBX
          jne L_447a80
L_447a97:
          xor EDX,EDX
          mov EAX,EDX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
FUN_447aa0:
          xor EDX,EDX
          cmp WORD PTR [__image_base__],23117
          je L_447ab0
          mov EAX,EDX
          ret 
L_447ab0:
          mov EAX,OFFSET __image_base__
          call FUN_447880
          test EAX,EAX
          mov EAX,OFFSET __image_base__
          cmovne EDX,EAX
          mov EAX,EDX
          ret 
L_447ac7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_447ad0:
          xor EAX,EAX
          cmp WORD PTR [__image_base__],23117
          je L_447ae0
          ret 
          .byte 0x66
          .byte 0x90
L_447ae0:
          push ESI
          push EBX
          mov EAX,OFFSET __image_base__
          call FUN_447880
          test EAX,EAX
          je L_447b3a
          mov EAX,DWORD PTR [__image_base__+60]
          mov EBX,DWORD PTR [ESP+12]
          lea EDX,DWORD PTR [EAX+__image_base__]
          movzx EAX,WORD PTR [EAX+__image_base__+20]
          sub EBX,OFFSET __image_base__
          movzx ESI,WORD PTR [EDX+6]
          lea EAX,DWORD PTR [EDX+EAX*1+24]
          test ESI,ESI
          je L_447b38
          xor ECX,ECX
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_447b20:
          mov EDX,DWORD PTR [EAX+12]
          cmp EBX,EDX
          jb L_447b2e
          add EDX,DWORD PTR [EAX+8]
          cmp EBX,EDX
          jb L_447b40
L_447b2e:
          add ECX,1
          add EAX,40
          cmp ECX,ESI
          jne L_447b20
L_447b38:
          xor EAX,EAX
L_447b3a:
          pop EBX
          pop ESI
L_447b3c:
          repz ret 
          .byte 0x66
          .byte 0x90
L_447b40:
          mov EAX,DWORD PTR [EAX+36]
          pop EBX
          pop ESI
          not EAX
          shr EAX,31
          jmp L_447b3c
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_447b50:
          push EDI
          push ESI
          xor ESI,ESI
          cmp WORD PTR [__image_base__],23117
          push EBX
          mov EBX,DWORD PTR [ESP+16]
          je L_447b70
L_447b64:
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
L_447b70:
          mov EAX,OFFSET __image_base__
          call FUN_447880
          test EAX,EAX
          je L_447b64
          mov EAX,DWORD PTR [__image_base__+60]
          lea ECX,DWORD PTR [EAX+__image_base__]
          mov EAX,DWORD PTR [EAX+__image_base__+128]
          test EAX,EAX
          je L_447b64
          movzx EDI,WORD PTR [ECX+6]
          movzx EDX,WORD PTR [ECX+20]
          test EDI,EDI
          lea EDX,DWORD PTR [ECX+EDX*1+24]
          je L_447b64
L_447ba3:
          mov ECX,DWORD PTR [EDX+12]
          cmp EAX,ECX
          jb L_447bb1
          add ECX,DWORD PTR [EDX+8]
          cmp EAX,ECX
          jb L_447bc3
L_447bb1:
          add ESI,1
          add EDX,40
          cmp ESI,EDI
          jne L_447ba3
L_447bbb:
          xor ESI,ESI
          mov EAX,ESI
          pop EBX
          pop ESI
          pop EDI
          ret 
L_447bc3:
          add EAX,OFFSET __image_base__
          jne L_447bd6
          jmp L_447bbb
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_447bd0:
          sub EBX,1
          add EAX,20
L_447bd6:
          mov ECX,DWORD PTR [EAX+4]
          test ECX,ECX
          jne L_447be4
          mov EDX,DWORD PTR [EAX+12]
          test EDX,EDX
          je L_447bbb
L_447be4:
          test EBX,EBX
          jg L_447bd0
          mov ESI,DWORD PTR [EAX+12]
          pop EBX
          add ESI,OFFSET __image_base__
          mov EAX,ESI
          pop ESI
          pop EDI
          ret 
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop

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
          .long FUN_447880 - .
          .byte 0x1e
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
          .long L_4478a0 - .
          .byte 0x12
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
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_4478c0 - .
          .byte 0x3d
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
          .byte 0x79
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_447900 - .
          .byte 0x8e
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
          .byte 0x5f
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
          .byte 0x42
          .byte 0xb
          .byte 0x2
          .byte 0x55
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
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xbc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_447990 - .
          .byte 0x6f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x51
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x2
          .byte 0x5b
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_447a00 - .
          .byte 0x2d
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
          .byte 0xf4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_447a30 - .
          .byte 0x6d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4c
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x49
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x4b
          .byte 0xb
          .byte 0x2
          .byte 0x4c
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_447aa0 - .
          .byte 0x27
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
          .byte 0x2c
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_447ad0 - .
          .byte 0x7c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x51
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x2
          .byte 0x59
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x86
          .byte 0x2
          .byte 0x44
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_447b50 - .
          .byte 0xa7
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
          .byte 0x4c
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x49
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
          .byte 0x47
          .byte 0xb
          .byte 0x2
          .byte 0x50
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
          .byte 0x69
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x49
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x0
