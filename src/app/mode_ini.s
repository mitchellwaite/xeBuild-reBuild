# app/mode_ini.s -- "Usage: %s ini"
#
# original placement:
#   .bss           00478d60-00479560
#   .eh_frame      00467fd0-00468114
#   .rdata         004541f8-004546bc
#   .rdata$zzz     004639e0-00463a0c
#   .text          00418240-00418a10

.intel_syntax noprefix
.globl FUN_418830

.text
.p2align 4
FUN_418240:
          sub ESP,28
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+8],OFFSET L_4541f8
          mov DWORD PTR [ESP+4],OFFSET L_454200
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_45422b
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+8],OFFSET L_4541f8
          mov DWORD PTR [ESP+4],OFFSET L_454236
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+8],OFFSET L_4541f8
          mov DWORD PTR [ESP+4],OFFSET L_45424c
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+8],OFFSET L_4541f8
          mov DWORD PTR [ESP+4],OFFSET L_454270
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_4542a0
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_4542e8
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_454338
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_454380
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov EAX,DWORD PTR [L_44a524]
          test EAX,EAX
          jne L_418354
L_418348:
          mov DWORD PTR [ESP],1
          call FUN_449198
L_418354:
          mov DWORD PTR [ESP+4],OFFSET L_4543ce
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov EAX,DWORD PTR [_iob]
          mov DWORD PTR [ESP],EAX
          call FUN_449178
          jmp L_418348
L_418377:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_418380:
          sub ESP,28
          mov EAX,DWORD PTR [ESP+32]
          test EAX,EAX
          je L_4183c3
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],OFFSET L_479160
          call FUN_449080
          mov DWORD PTR [ESP],OFFSET L_479160
          call FUN_4490b8
          mov DWORD PTR [ESP+8],OFFSET L_479160
          mov DWORD PTR [ESP+4],OFFSET L_4543e9
          mov DWORD PTR [ESP],0
          call FUN_433690
L_4183c3:
          add ESP,28
          ret 
L_4183c7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_4183d0:
          push ESI
          push EBX
          sub ESP,532
          lea EAX,DWORD PTR [ESP+548]
          lea EBX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+4],512
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+544]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_449030
          mov DWORD PTR [ESP],EBX
          call _printf
          mov DWORD PTR [ESP+4],OFFSET L_454402
          mov DWORD PTR [ESP],OFFSET L_479160
          call _fopen
          test EAX,EAX
          je L_418438
          mov ESI,EAX
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          call FUN_449158
          mov DWORD PTR [ESP],ESI
          call _fclose
L_418438:
          add ESP,532
          pop EBX
          pop ESI
          ret 
L_418441:
          jmp FUN_418450
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
FUN_418450:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,108
          lea ESI,DWORD PTR [ESP+40]
          lea EBX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],OFFSET L_454404
          call FUN_4183d0
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call FUN_40c940
          test EAX,EAX
          je L_418650
          lea EBP,DWORD PTR [ESP+48]
          lea EDI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+40],0
          nop
L_418490:
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call FUN_40c860
          test EAX,EAX
          je L_418570
L_4184a4:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          call FUN_40c7b0
          test EAX,EAX
          je L_418490
          mov DWORD PTR [ESP+8],7
          mov DWORD PTR [ESP+4],OFFSET L_45440f
          mov DWORD PTR [ESP],EBX
          call FUN_4491d0
          test EAX,EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          jne L_418580
          call _crc32
          mov DWORD PTR [ESP+28],EAX
          lea EAX,DWORD PTR [ESP+59]
          mov DWORD PTR [ESP+8],16
          mov DWORD PTR [ESP+4],OFFSET L_454417
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_4185e1
          mov DWORD PTR [ESP],OFFSET L_454428
          call FUN_4183d0
L_418520:
          lea EAX,DWORD PTR [ESP+59]
          mov DWORD PTR [ESP+8],12
          mov DWORD PTR [ESP+4],OFFSET L_4544cc
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_4185a0
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],OFFSET L_4544dc
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+59]
          mov DWORD PTR [ESP+4],EAX
          call FUN_4183d0
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call FUN_40c860
          test EAX,EAX
          jne L_4184a4
L_418570:
          add ESP,108
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_418580:
          call _crc32
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],EAX
L_41858d:
          mov DWORD PTR [ESP],OFFSET L_4544dc
          call FUN_4183d0
          jmp L_418490
          .byte 0x66
          .byte 0x90
L_4185a0:
          lea EAX,DWORD PTR [ESP+59]
          mov DWORD PTR [ESP+8],6
          mov DWORD PTR [ESP+4],OFFSET L_4544fc
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+59]
          mov DWORD PTR [ESP+4],EAX
          je L_41858d
          mov DWORD PTR [ESP],OFFSET L_454503
          call FUN_4183d0
          jmp L_418490
L_4185e1:
          lea EAX,DWORD PTR [ESP+59]
          mov DWORD PTR [ESP+8],17
          mov DWORD PTR [ESP+4],OFFSET L_454454
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_418612
          mov DWORD PTR [ESP],OFFSET L_454468
          call FUN_4183d0
          jmp L_418520
L_418612:
          lea EAX,DWORD PTR [ESP+59]
          mov DWORD PTR [ESP+8],16
          mov DWORD PTR [ESP+4],OFFSET L_454495
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_418520
          mov DWORD PTR [ESP],OFFSET L_4544a4
          call FUN_4183d0
          jmp L_418520
L_418647:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_418650:
          mov DWORD PTR [ESP+4],OFFSET L_45450c
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+28],EAX
          call FUN_433690
          mov EAX,DWORD PTR [ESP+28]
          add ESP,108
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
          .byte 0x8d
          .byte 0xbf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_418680:
          push EDI
          push EBX
          sub ESP,36
          lea EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP],EAX
          call FUN_40c650
          test EAX,EAX
          je L_4187d5
          lea EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP],EAX
          call FUN_40c700
          test EAX,EAX
          je L_418813
          mov EAX,DWORD PTR [ESP+16]
          add EAX,20
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          movzx EBX,AX
          mov EAX,DWORD PTR [ESP+16]
          add EAX,12
          mov DWORD PTR [ESP],EAX
          call FUN_420ad0
          mov DWORD PTR [ESP+24],EAX
          mov EAX,DWORD PTR [ESP+20]
          add EAX,12
          mov DWORD PTR [ESP],EAX
          call FUN_420ad0
          mov EDI,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+28],EAX
          xor EAX,EAX
          mov DWORD PTR [EDI+32],0
          mov DWORD PTR [EDI+556],0
          lea ECX,DWORD PTR [EDI+32]
          add EDI,36
          and EDI,4294967292
          sub ECX,EDI
          add ECX,528
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          mov EDX,DWORD PTR [ESP+20]
          mov DWORD PTR [EDX+16],0
          mov DWORD PTR [EDX+20],0
          mov DWORD PTR [EDX+24],0
          mov DWORD PTR [EDX+28],0
          mov DWORD PTR [ESP+8],OFFSET L_479160
          mov DWORD PTR [ESP+4],OFFSET L_45453c
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_454563
          call FUN_4183d0
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP],EAX
          call _crc32
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],OFFSET L_454577
          call FUN_4183d0
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP],EAX
          call _crc32
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],EAX
          mov EBX,1
          mov DWORD PTR [ESP],OFFSET L_454587
          call FUN_4183d0
          jmp L_4187eb
L_4187d5:
          mov DWORD PTR [ESP+4],OFFSET L_4545c8
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call FUN_433690
L_4187eb:
          mov EAX,DWORD PTR [ESP+16]
          test EAX,EAX
          je L_4187fb
          mov DWORD PTR [ESP],EAX
          call _free
L_4187fb:
          mov EAX,DWORD PTR [ESP+20]
          test EAX,EAX
          je L_41880b
          mov DWORD PTR [ESP],EAX
          call _free
L_41880b:
          add ESP,36
          mov EAX,EBX
          pop EBX
          pop EDI
          ret 
L_418813:
          mov DWORD PTR [ESP+4],OFFSET L_454598
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call FUN_433690
          jmp L_4187eb
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_418830:
          push EDI
          push EBX
          sub ESP,84
          lea EBX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],1
          call FUN_433570
          mov EDI,EBX
          xor EAX,EAX
          mov ECX,10
          rep stosd DWORD PTR ES:[EDI]
          mov DWORD PTR [ESP+8],OFFSET L_4545f5
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EBX
          call FUN_418ee0
          test EAX,EAX
          jne L_4188b0
L_41886c:
          cmp DWORD PTR [ESP+96],1
          jne L_4189fc
          mov EAX,DWORD PTR [ESP+100]
          mov EAX,DWORD PTR [EAX]
          mov DWORD PTR [ESP],EAX
          call FUN_40cc80
          test EAX,EAX
          jne L_4188e0
          mov DWORD PTR [ESP+4],OFFSET L_4546a7
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov EAX,4
L_4188a2:
          add ESP,84
          pop EBX
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
L_4188b0:
          mov DWORD PTR [ESP],EBX
          call FUN_41b740
          test EAX,EAX
          jne L_41886c
          mov DWORD PTR [ESP+4],OFFSET L_454600
          mov DWORD PTR [ESP],0
          call FUN_433690
          add ESP,84
          mov EAX,4
          pop EBX
          pop EDI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4188e0:
          mov DWORD PTR [ESP+4],OFFSET L_454643
          mov DWORD PTR [ESP],0
          call FUN_433690
          call FUN_40c260
          mov DWORD PTR [ESP],OFFSET L_478d60
          mov DWORD PTR [ESP+4],EAX
          call FUN_449080
          mov EDX,OFFSET L_478d60
L_41890e:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_41890e
          mov ECX,EAX
          mov DWORD PTR [ESP+4],OFFSET L_478d60
          mov DWORD PTR [ESP],OFFSET L_479160
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          mov EBX,EAX
          cmove EDX,ECX
          add BL,AL
          sbb EDX,OFFSET L_478d63
          mov DWORD PTR [EDX+L_478d60],777343839
          mov DWORD PTR [EDX+L_478d64],6909545
          add EDX,8
          mov DWORD PTR [ESP+8],EDX
          call _memcpy
          mov DWORD PTR [ESP],OFFSET L_479160
          call FUN_4490b8
          mov DWORD PTR [ESP+8],OFFSET L_479160
          mov DWORD PTR [ESP+4],OFFSET L_4543e9
          mov DWORD PTR [ESP],0
          call FUN_433690
          call FUN_418680
          test EAX,EAX
          je L_4189e0
          call FUN_418450
          mov EDX,EAX
          xor EAX,EAX
          test EDX,EDX
          je L_4188a2
          mov DWORD PTR [ESP+8],OFFSET L_479160
          mov DWORD PTR [ESP+4],OFFSET L_45465c
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+28],EAX
          call FUN_433690
          mov EAX,DWORD PTR [ESP+28]
          jmp L_4188a2
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4189e0:
          mov DWORD PTR [ESP+4],OFFSET L_454678
          mov DWORD PTR [ESP],0
          call FUN_433690
          add ESP,84
          xor EAX,EAX
          pop EBX
          pop EDI
          ret 
L_4189fc:
          call FUN_418240
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
          nop
          nop
          nop
          nop
          nop

.section .rdata,"dr"
.p2align 2
L_4541f8:
          .string "xeBuild"
L_454200:
          .string "Usage   :\n   %s ini [systeUpdateConPath]\n\n"
L_45422b:
          .string "Examples:\n"
L_454236:
          .string "   %s ini ./16547/\n"
          .zero 2
L_45424c:
          .string "   %s ini c:\\16547\\$SystemUpdate\n"
          .zero 2
L_454270:
          .string "   %s ini z:\\someWeirdPath\\su20076000_00000000\n"
L_4542a0:
          .string "      when specifying path, either provide relative path or full path\n"
          .zero 1
L_4542e8:
          .string "      to either the SU container, a folder with $SystemUpdate folder in it,\n"
          .zero 3
L_454338:
          .string "      or a folder with flash update named 'su20076000_00000000' in it.\n"
L_454380:
          .string "      Hash data will be output to the folder with the SU in it named _SU.ini\n"
L_4543ce:
          .string "\npress <enter> to quit...\n"
L_4543e9:
          .string "output set to file '%s'\n"
L_454402:
          .string "a"
L_454404:
          .string "[flashfs]\n"
L_45440f:
          .string "$flash_"
L_454417:
          .string "xenonclatin.xttp"
L_454428:
          .string "xenonclatin.xtt,d5d17ff5; added by xebuild\n"
L_454454:
          .string "xenonjklatin.xttp"
          .zero 2
L_454468:
          .string "xenonjklatin.xtt,dde4a14c; added by xebuild\n"
L_454495:
          .string "ximedic.xexp"
          .zero 2
L_4544a4:
          .string "ximedic.xex,1d992bfb; added by xebuild\n"
L_4544cc:
          .string "systemupdate"
          .zero 3
L_4544dc:
          .string ";%s,%08x; commented by xebuild\n"
L_4544fc:
          .string "oddupd"
L_454503:
          .string "%s,%08x\n"
L_45450c:
          .string "***** ERROR SU seems loaded, but is unparsed!\n"
          .zero 1
L_45453c:
          .string "Attempting to output info to file %s\n\n"
L_454563:
          .string "[version]\n%d\n\n[bl]\n"
L_454577:
          .string "cf_%d.bin,%08x\n"
L_454587:
          .string "cg_%d.bin,%08x\n\n"
L_454598:
          .string "***** ERROR: could not get CG data from SU!\n"
          .zero 3
L_4545c8:
          .string "***** ERROR: could not get CF data from SU!\n"
L_4545f5:
          .string "1blkey.txt"
L_454600:
          .string "\n***** WARNING: 1blkey.txt not found or invalid, cannot proceed.\n\n"
L_454643:
          .string "SU loaded successfully!\n"
L_45465c:
          .string "\nCompleted output to %s\n"
          .zero 3
L_454678:
          .string "***** ERROR unable to get CF/CG data from SU!\n"
L_4546a7:
          .string "Error loading SU!\n"
          .zero 2

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
          .long FUN_418240 - .
          .byte 0x37
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_418380 - .
          .byte 0x47
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x4
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4183d0 - .
          .byte 0x71
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
          .byte 0xa0
          .byte 0x4
          .byte 0x2
          .byte 0x66
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x74
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_418450 - .
          .byte 0x24
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
          .byte 0x80
          .byte 0x1
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
          .byte 0x44
          .byte 0xb
          .byte 0x2
          .byte 0xef
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
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xcc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_418680 - .
          .byte 0xab
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
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x3
          .byte 0x89
          .byte 0x1
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x43
          .byte 0xc3
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
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xfc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_418830 - .
          .byte 0xd1
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
          .byte 0x43
          .byte 0xe
          .byte 0x60
          .byte 0x2
          .byte 0x70
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
          .byte 0x49
          .byte 0xb
          .byte 0x63
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x46
          .byte 0xb
          .byte 0x3
          .byte 0x17
          .byte 0x1
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0

.bss
.p2align 5
L_478d60:
          .zero 3
L_478d63:
          .zero 1
L_478d64:
          .zero 1020
L_479160:
          .zero 1024
