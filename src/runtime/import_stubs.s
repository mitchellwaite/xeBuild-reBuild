# runtime/import_stubs.s -- dlltool `jmp [__imp_x]` stubs, no unwind info
#
# original placement:
#   .text          00449038-004492a0

.intel_syntax noprefix
.globl FUN_449040
.globl FUN_449048
.globl FUN_449068
.globl FUN_4490c8
.globl FUN_449120
.globl FUN_449130
.globl FUN_449170
.globl FUN_4491b0
.globl FUN_4491b8
.globl FUN_4491c8
.globl FUN_4491e0
.globl FUN_4491e8
.globl FUN_4491f8
.globl FUN_449208
.globl FUN_449210
.globl FUN_449218
.globl FUN_449220
.globl FUN_449228
.globl FUN_449230
.globl FUN_449238
.globl FUN_449240
.globl FUN_449248
.globl FUN_449250
.globl FUN_449260
.globl FUN_449268
.globl FUN_449278
.globl FUN_449280
.globl FUN_449288
.globl FUN_449290
.globl L_4491c0
.globl L_449270
.globl __chdir
.globl __gmtime32
.globl __lrotl
.globl __mkdir
.globl __mktime32
.globl __time32
.globl _atoi
.globl _calloc
.globl _exit
.globl _fclose
.globl _feof
.globl _fflush
.globl _fgetc
.globl _fgets
.globl _fopen
.globl _fprintf
.globl _fputc
.globl _fread
.globl _free
.globl _fseek
.globl _ftell
.globl _fwrite
.globl _malloc
.globl _memcmp
.globl _memcpy
.globl _memset
.globl _printf
.globl _putchar
.globl _puts
.globl _rand
.globl _remove
.globl _rename
.globl _rewind
.globl _signal
.globl _sprintf
.globl _srand
.globl _strcat
.globl _strcpy
.globl _stricmp
.globl _strlen
.globl _strncat
.globl _strncpy
.globl _strnicmp
.globl _strrchr

.text
.p2align 3
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
FUN_449040:
          jmp DWORD PTR [wcscpy]
          .byte 0x90
          .byte 0x90
FUN_449048:
          jmp DWORD PTR [vfprintf]
          .byte 0x90
          .byte 0x90
__time32:
          jmp DWORD PTR [time]
          .byte 0x90
          .byte 0x90
_strrchr:
          jmp DWORD PTR [strrchr]
          .byte 0x90
          .byte 0x90
_strncpy:
          jmp DWORD PTR [strncpy]
          .byte 0x90
          .byte 0x90
FUN_449068:
          jmp DWORD PTR [strncmp]
          .byte 0x90
          .byte 0x90
_strncat:
          jmp DWORD PTR [strncat]
          .byte 0x90
          .byte 0x90
_strlen:
          jmp DWORD PTR [strlen]
          .byte 0x90
          nop
_strcpy:
          jmp DWORD PTR [strcpy]
          .byte 0x90
          .byte 0x90
_strcat:
          jmp DWORD PTR [strcat]
          .byte 0x90
          .byte 0x90
_srand:
          jmp DWORD PTR [srand]
          .byte 0x90
          .byte 0x90
_sprintf:
          jmp DWORD PTR [sprintf]
          .byte 0x90
          .byte 0x90
_signal:
          jmp DWORD PTR [signal]
          .byte 0x90
          .byte 0x90
_rewind:
          jmp DWORD PTR [rewind]
          .byte 0x90
          .byte 0x90
_rename:
          jmp DWORD PTR [rename]
          .byte 0x90
          .byte 0x90
_remove:
          jmp DWORD PTR [remove]
          .byte 0x90
          .byte 0x90
_rand:
          jmp DWORD PTR [rand]
          .byte 0x90
          .byte 0x90
FUN_4490c8:
          jmp DWORD PTR [raise]
          .byte 0x90
          .byte 0x90
_puts:
          jmp DWORD PTR [puts]
          .byte 0x90
          .byte 0x90
_putchar:
          jmp DWORD PTR [putchar]
          .byte 0x90
          .byte 0x90
_printf:
          jmp DWORD PTR [printf]
          .byte 0x90
          .byte 0x90
__mktime32:
          jmp DWORD PTR [mktime]
          .byte 0x90
          .byte 0x90
_memset:
          jmp DWORD PTR [memset]
          .byte 0x90
          .byte 0x90
_memcpy:
          jmp DWORD PTR [memcpy]
          .byte 0x90
          .byte 0x90
_memcmp:
          jmp DWORD PTR [memcmp]
          .byte 0x90
          .byte 0x90
_malloc:
          jmp DWORD PTR [malloc]
          .byte 0x90
          .byte 0x90
__gmtime32:
          jmp DWORD PTR [gmtime]
          .byte 0x90
          .byte 0x90
_fwrite:
          jmp DWORD PTR [fwrite]
          .byte 0x90
          .byte 0x90
FUN_449120:
          jmp DWORD PTR [fwprintf]
          .byte 0x90
          .byte 0x90
_ftell:
          jmp DWORD PTR [ftell]
          .byte 0x90
          .byte 0x90
FUN_449130:
          jmp DWORD PTR [fsetpos]
          .byte 0x90
          .byte 0x90
_fseek:
          jmp DWORD PTR [fseek]
          .byte 0x90
          .byte 0x90
_free:
          jmp DWORD PTR [free]
          .byte 0x90
          nop
_fread:
          jmp DWORD PTR [fread]
          .byte 0x90
          nop
_fputc:
          jmp DWORD PTR [fputc]
          .byte 0x90
          nop
_fprintf:
          jmp DWORD PTR [fprintf]
          .byte 0x90
          nop
_fopen:
          jmp DWORD PTR [fopen]
          .byte 0x90
          .byte 0x90
_fgets:
          jmp DWORD PTR [fgets]
          .byte 0x90
          .byte 0x90
FUN_449170:
          jmp DWORD PTR [fgetpos]
          .byte 0x90
          .byte 0x90
_fgetc:
          jmp DWORD PTR [fgetc]
          .byte 0x90
          .byte 0x90
_fflush:
          jmp DWORD PTR [fflush]
          .byte 0x90
          .byte 0x90
_feof:
          jmp DWORD PTR [feof]
          .byte 0x90
          .byte 0x90
_fclose:
          jmp DWORD PTR [fclose]
          .byte 0x90
          .byte 0x90
_exit:
          jmp DWORD PTR [exit]
          .byte 0x90
          .byte 0x90
_calloc:
          jmp DWORD PTR [calloc]
          .byte 0x90
          .byte 0x90
_atoi:
          jmp DWORD PTR [atoi]
          .byte 0x90
          .byte 0x90
FUN_4491b0:
          jmp DWORD PTR [abort]
          .byte 0x90
          .byte 0x90
FUN_4491b8:
          jmp DWORD PTR [_write]
          .byte 0x90
          .byte 0x90
L_4491c0:
          jmp DWORD PTR [_vsnprintf]
          .byte 0x90
          .byte 0x90
FUN_4491c8:
          jmp DWORD PTR [_unlock]
          .byte 0x90
          .byte 0x90
_strnicmp:
          jmp DWORD PTR [__imp___strnicmp]
          .byte 0x90
          .byte 0x90
_stricmp:
          jmp DWORD PTR [__imp___stricmp]
          .byte 0x90
          .byte 0x90
FUN_4491e0:
          jmp DWORD PTR [_stat]
          .byte 0x90
          .byte 0x90
FUN_4491e8:
          jmp DWORD PTR [_snwprintf]
          .byte 0x90
          .byte 0x90
__mkdir:
          jmp DWORD PTR [_mkdir]
          .byte 0x90
          .byte 0x90
FUN_4491f8:
          jmp DWORD PTR [_lseeki64]
          .byte 0x90
          .byte 0x90
__lrotl:
          jmp DWORD PTR [_lrotl]
          .byte 0x90
          .byte 0x90
FUN_449208:
          jmp DWORD PTR [_lock]
          .byte 0x90
          .byte 0x90
FUN_449210:
          jmp DWORD PTR [_initterm]
          .byte 0x90
          .byte 0x90
FUN_449218:
          jmp DWORD PTR [_fullpath]
          .byte 0x90
          .byte 0x90
FUN_449220:
          jmp DWORD PTR [_findnext]
          .byte 0x90
          .byte 0x90
FUN_449228:
          jmp DWORD PTR [_findfirst]
          .byte 0x90
          .byte 0x90
FUN_449230:
          jmp DWORD PTR [_findclose]
          .byte 0x90
          .byte 0x90
FUN_449238:
          jmp DWORD PTR [_fileno]
          .byte 0x90
          .byte 0x90
FUN_449240:
          jmp DWORD PTR [_filelengthi64]
          .byte 0x90
          .byte 0x90
FUN_449248:
          jmp DWORD PTR [__imp___exit]
          .byte 0x90
          .byte 0x90
FUN_449250:
          jmp DWORD PTR [_errno]
          nop
          nop
__chdir:
          jmp DWORD PTR [_chdir]
          .byte 0x90
          .byte 0x90
FUN_449260:
          jmp DWORD PTR [_cexit]
          .byte 0x90
          .byte 0x90
FUN_449268:
          jmp DWORD PTR [_amsg_exit]
          .byte 0x90
          .byte 0x90
L_449270:
          jmp DWORD PTR [__setusermatherr]
          .byte 0x90
          .byte 0x90
FUN_449278:
          jmp DWORD PTR [__set_app_type]
          .byte 0x90
          .byte 0x90
FUN_449280:
          jmp DWORD PTR [__getmainargs]
          .byte 0x90
          .byte 0x90
FUN_449288:
          jmp DWORD PTR [__doserrno]
          .byte 0x90
          .byte 0x90
FUN_449290:
          jmp DWORD PTR [__dllonexit]
          .byte 0x90
          .byte 0x90
          .byte 0x66
          .byte 0x90
          .byte 0x66
          .byte 0x90
          .byte 0x66
          .byte 0x90
          .byte 0x66
          .byte 0x90
