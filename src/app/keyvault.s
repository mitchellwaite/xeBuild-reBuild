# app/keyvault.s -- keyvault hash check, DVD key, console serial/date formatting
#
# original placement:
#   .bss           004709e0-00474a20
#   .eh_frame      004674ac-004676ac
#   .rdata         00451fb4-004521b8
#   .rdata$zzz     00463988-004639b4
#   .text          00413090-004136a0

.intel_syntax noprefix
.globl FUN_413090
.globl FUN_4130b0
.globl FUN_4131a0
.globl FUN_413370
.globl FUN_4133d0
.globl FUN_4133f0
.globl FUN_413410
.globl FUN_4134f0
.globl FUN_413510
.globl FUN_4135a0

.text
.p2align 4
FUN_413090:
          mov EAX,DWORD PTR [L_4709e4]
          test EAX,EAX
          mov EAX,0
          cmovne EAX,DWORD PTR [L_4709e0]
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d,0xbf,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_4130b0:
          mov EAX,DWORD PTR [L_4709ec]
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4130c0:
          mov EAX,DWORD PTR [L_4709ec]
          test EAX,EAX
          je L_413100
          push EBX
          mov EBX,7672
          sub ESP,24
L_4130d2:
          mov EAX,DWORD PTR [L_4709f0]
          add EAX,EBX
          mov DWORD PTR [ESP],EAX
          call FUN_420ad0
          sub EAX,1
          cmp EAX,-3
          jbe L_413103
          add EBX,4
          cmp EBX,7736
          jne L_4130d2
          xor EAX,EAX
L_4130f6:
          add ESP,24
          pop EBX
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_413100:
          xor EAX,EAX
          ret 
L_413103:
          mov EAX,DWORD PTR [L_47a140]
          test EAX,EAX
          je L_413178
          mov DWORD PTR [ESP+8],OFFSET L_47a11c
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],OFFSET L_470a20
          call FUN_40e520
          test EAX,EAX
          je L_413150
          mov DWORD PTR [ESP+4],OFFSET L_451fe5
          mov DWORD PTR [ESP],1
          mov DWORD PTR [L_4709e0],3
          call _log_printf
          add ESP,24
          mov EAX,1
          pop EBX
          ret 
L_413150:
          mov DWORD PTR [ESP+4],OFFSET L_452000
          mov DWORD PTR [ESP],0
          mov DWORD PTR [L_4709e0],2
          call _log_printf
          add ESP,24
          mov EAX,1
          pop EBX
          ret 
L_413178:
          mov DWORD PTR [ESP+4],OFFSET L_451fb4
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [L_4709e0],1
          mov EAX,1
          jmp L_4130f6
FUN_4131a0:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EBX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],16384
          mov DWORD PTR [ESP],OFFSET L_470a20
          mov DWORD PTR [ESP+4],EBX
          call _memcpy
          mov DWORD PTR [ESP+4],OFFSET L_452068
          mov DWORD PTR [ESP],1
          mov DWORD PTR [L_4709ec],1
          mov DWORD PTR [L_4709f0],OFFSET L_470a20
          call _log_printf
          mov EDX,DWORD PTR [L_4709e8]
          test EDX,EDX
          je L_413262
          cmp DWORD PTR [L_479ea8],1
          je L_4132a0
          mov EAX,DWORD PTR [L_4709f0]
          mov EDI,DWORD PTR [L_4709f4]
          mov ESI,DWORD PTR [L_4709f8]
          mov ECX,DWORD PTR [L_4709fc]
          mov EDX,DWORD PTR [L_470a00]
          mov DWORD PTR [EBX+256],EDI
          mov DWORD PTR [EBX+260],ESI
          mov DWORD PTR [EBX+264],ECX
          mov DWORD PTR [EBX+268],EDX
          mov DWORD PTR [EAX+256],EDI
          mov DWORD PTR [EAX+260],ESI
          mov DWORD PTR [EAX+264],ECX
          mov DWORD PTR [EAX+268],EDX
          mov DWORD PTR [ESP+4],OFFSET L_452098
          mov DWORD PTR [ESP],1
          call _log_printf
L_413262:
          mov EAX,DWORD PTR [L_4709ec]
          mov EBX,7672
          test EAX,EAX
          je L_413292
L_413270:
          mov EAX,DWORD PTR [L_4709f0]
          add EAX,EBX
          mov DWORD PTR [ESP],EAX
          call FUN_420ad0
          sub EAX,1
          cmp EAX,-3
          jbe L_4132c0
          add EBX,4
          cmp EBX,7736
          jne L_413270
L_413292:
          xor EAX,EAX
L_413294:
          mov DWORD PTR [L_4709e4],EAX
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
L_4132a0:
          mov DWORD PTR [ESP+4],OFFSET L_4520b8
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_413262
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4132c0:
          mov EAX,DWORD PTR [L_47a140]
          test EAX,EAX
          je L_413343
          mov DWORD PTR [ESP+8],OFFSET L_47a11c
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],OFFSET L_470a20
          call FUN_40e520
          test EAX,EAX
          je L_413314
          mov DWORD PTR [ESP+4],OFFSET L_451fe5
          mov DWORD PTR [ESP],1
          mov DWORD PTR [L_4709e0],3
          call _log_printf
          mov EAX,1
          mov DWORD PTR [L_4709e4],EAX
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
L_413314:
          mov DWORD PTR [ESP+4],OFFSET L_452000
          mov DWORD PTR [ESP],0
          mov DWORD PTR [L_4709e0],2
          call _log_printf
          mov EAX,1
          mov DWORD PTR [L_4709e4],EAX
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
L_413343:
          mov DWORD PTR [ESP+4],OFFSET L_451fb4
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [L_4709e0],1
          mov EAX,1
          jmp L_413294
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_413370:
          mov EDX,DWORD PTR [L_4709ec]
          xor EAX,EAX
          test EDX,EDX
          je L_4133a1
          mov EAX,DWORD PTR [L_4709f0]
          push EBX
          movzx ECX,WORD PTR [EAX+28]
          mov EDX,ECX
          shl ECX,8
          shr DX,8
          mov EBX,EDX
          add BX,CX
          je L_4133b0
          test BH,3
          mov EAX,2
          je L_4133a3
L_4133a0:
          pop EBX
L_4133a1:
          repz ret 
L_4133a3:
          and EBX,32
          mov EAX,1
          jne L_4133a0
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_4133b0:
          lea EAX,DWORD PTR [ECX+EDX*1]
          pop EBX
          test EAX,288
          setne AL
          movzx EAX,AL
          jmp L_4133a1
L_4133c1:
          jmp FUN_4133d0
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
          nop
          nop
          nop
FUN_4133d0:
          mov EAX,DWORD PTR [L_4709ec]
          test EAX,EAX
          je L_4133e4
          mov EAX,DWORD PTR [L_4709f0]
          add EAX,256
          ret 
L_4133e4:
          xor EAX,EAX
          ret 
L_4133e7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_4133f0:
          mov EAX,DWORD PTR [L_4709ec]
          test EAX,EAX
          je L_413404
          mov EAX,DWORD PTR [L_4709f0]
          add EAX,176
          ret 
L_413404:
          xor EAX,EAX
          ret 
L_413407:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_413410:
          push EDI
          push ESI
          push EBX
          sub ESP,32
          mov EBX,DWORD PTR [L_4709ec]
          mov EDI,DWORD PTR [ESP+48]
          test EBX,EBX
          je L_4134e4
          test EDI,EDI
          je L_4134e4
          mov ESI,DWORD PTR [L_4709f0]
          xor EBX,EBX
          xor EDX,EDX
          movzx ECX,BYTE PTR [ESI+2506]
          movzx EAX,BYTE PTR [ESI+2507]
          shld EBX,ECX,8
          shl ECX,8
          add EAX,ECX
          movzx ECX,BYTE PTR [ESI+2508]
          adc EDX,EBX
          xor EBX,EBX
          shld EDX,EAX,8
          shl EAX,8
          add ECX,EAX
          movzx EAX,BYTE PTR [ESI+2509]
          movzx ESI,BYTE PTR [ESI+2510]
          adc EBX,EDX
          xor EDX,EDX
          shld EBX,ECX,8
          shl ECX,8
          add EAX,ECX
          adc EDX,EBX
          mov EBX,ESI
          shld EDX,EAX,8
          movzx ECX,BL
          shl EAX,8
          xor EBX,EBX
          add EAX,ECX
          mov ECX,ESI
          adc EDX,EBX
          and ECX,15
          xor EBX,EBX
          cmp CL,9
          jbe L_4134b0
          add ESP,32
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
L_4134b0:
          shrd EAX,EDX,4
          movzx ESI,CL
          shr EDX,4
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [ESP+8],EAX
          mov EBX,1
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+4],OFFSET L_4520e1
          call _sprintf
          add ESP,32
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          ret 
L_4134e4:
          add ESP,32
          xor EBX,EBX
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
FUN_4134f0:
          mov EAX,DWORD PTR [L_4709ec]
          test EAX,EAX
          je L_413504
          mov EAX,DWORD PTR [L_4709f0]
          add EAX,192
          ret 
L_413504:
          xor EAX,EAX
          ret 
L_413507:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_413510:
          sub ESP,44
          mov EAX,DWORD PTR [L_4709ec]
          mov EDX,DWORD PTR [ESP+48]
          test EAX,EAX
          je L_413584
          test EDX,EDX
          je L_413584
          mov EAX,DWORD PTR [L_4709f0]
          movzx ECX,BYTE PTR [EAX+2539]
          mov DWORD PTR [ESP+28],ECX
          movzx ECX,BYTE PTR [EAX+2538]
          mov DWORD PTR [ESP+24],ECX
          movzx ECX,BYTE PTR [EAX+2536]
          mov DWORD PTR [ESP+20],ECX
          movzx ECX,BYTE PTR [EAX+2535]
          mov DWORD PTR [ESP+16],ECX
          movzx ECX,BYTE PTR [EAX+2533]
          mov DWORD PTR [ESP+12],ECX
          movzx EAX,BYTE PTR [EAX+2532]
          mov DWORD PTR [ESP+4],OFFSET L_4520ec
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+8],EAX
          call _sprintf
          mov EAX,1
          add ESP,44
          ret 
L_413584:
          xor EAX,EAX
          add ESP,44
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_413590:
          mov EAX,DWORD PTR [L_4709e4]
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_4135a0:
          push ESI
          push EBX
          sub ESP,36
          mov ESI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],ESI
          call _strlen
          cmp EAX,32
          je L_4135e0
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_452158
          mov DWORD PTR [ESP],0
          call _log_printf
          xor EAX,EAX
L_4135d4:
          add ESP,36
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4135e0:
          mov DWORD PTR [ESP],ESI
          call FUN_422350
          test EAX,EAX
          je L_413671
          xor EBX,EBX
L_4135f2:
          mov DWORD PTR [ESP],ESI
          add EBX,1
          add ESI,2
          call FUN_421300
          mov BYTE PTR [EBX+L_4709f3],AL
          cmp EBX,16
          jne L_4135f2
          mov DWORD PTR [ESP+4],OFFSET L_4520fd
          mov DWORD PTR [ESP],1
          xor EBX,EBX
          call _log_printf
L_413621:
          movzx EAX,BYTE PTR [EBX+L_4709f4]
          mov DWORD PTR [ESP+4],OFFSET L_452110
          add EBX,1
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          cmp EBX,16
          jne L_413621
          mov DWORD PTR [ESP+4],OFFSET L_452115
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [L_4709e8],1
          add ESP,36
          mov EAX,1
          pop EBX
          pop ESI
          ret 
L_413671:
          mov DWORD PTR [ESP+4],OFFSET L_452118
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+28],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+28]
          jmp L_4135d4
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
          .byte 0x90

.section .rdata,"dr"
.p2align 2
L_451fb4:
          .string "Master RSA pub not available, not checking hash\n"
L_451fe5:
          .string "Keyvault hash is good!\n"
          .zero 3
L_452000:
          .string "***** WARNING: Keyvault hash is not good! Keyvault may be corrupt or does not belong to this CPU key!\n"
          .zero 1
L_452068:
          .string "decrypted keyvault has been set for reference\n"
          .zero 1
L_452098:
          .string "dvd key patched into keyvault\n"
          .zero 1
L_4520b8:
          .string "retail image, skipping patching dvd key\n"
L_4520e1:
          .string "%011I64u%X"
L_4520ec:
          .string "%c%c/%c%c/20%c%c"
L_4520fd:
          .string "DVD Key set to: 0x"
L_452110:
          .string "%02X"
L_452115:
          .string "\n"
          .zero 1
L_452118:
          .string "\n******* ERROR: invalid or unexpected characters in DVD key!\n"
          .zero 2
L_452158:
          .string "\n***** ERROR: unable to set dvd key to '%s', %d is not the correct length, 32 chars required!\n"
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
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_413090 - .
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
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4130b0 - .
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_4130c0 - .
          .byte 0xe0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4a
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x48
          .byte 0xe
          .byte 0x20
          .byte 0x67
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x49
          .byte 0xe
          .byte 0x20
          .byte 0x83
          .byte 0x2
          .byte 0x2
          .byte 0x46
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x61
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x58
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4131a0 - .
          .byte 0xcb
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
          .byte 0x20
          .byte 0x2
          .byte 0xf6
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
          .byte 0x70
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
          .byte 0x6b
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
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xdc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_413370 - .
          .byte 0x51
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x52
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x5f
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x42
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x51
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_4133d0 - .
          .byte 0x17
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
          .byte 0x14
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_4133f0 - .
          .byte 0x17
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
          .byte 0x28
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_413410 - .
          .byte 0xdf
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
          .byte 0x6e
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
          .byte 0x43
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
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_4134f0 - .
          .byte 0x17
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x94
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_413510 - .
          .byte 0x7a
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x2
          .byte 0x70
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x45
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_413590 - .
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc8
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_4135a0 - .
          .byte 0xf2
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
          .byte 0x72
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
          .byte 0x47
          .byte 0xb
          .byte 0x2
          .byte 0x89
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

.bss
.p2align 5
L_4709e0:
          .zero 4
L_4709e4:
          .zero 4
L_4709e8:
          .zero 4
L_4709ec:
          .zero 4
L_4709f0:
          .zero 3
L_4709f3:
          .zero 1
L_4709f4:
          .zero 4
L_4709f8:
          .zero 4
L_4709fc:
          .zero 4
L_470a00:
          .zero 32
L_470a20:
          .zero 16384
