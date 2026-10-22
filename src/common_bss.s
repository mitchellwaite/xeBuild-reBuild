# common_bss.s -- COMMON globals, laid out by ld in hash order
#
# original placement:
#   .bss           00479e84-0050eca8

.intel_syntax noprefix
.globl L_479ea4
.globl L_479ea7
.globl L_479eac
.globl L_479eb0
.globl L_479eb4
.globl L_479eb8
.globl L_479ebc
.globl L_479ec0
.globl L_479ec4
.globl L_479ec8
.globl L_479ecc
.globl L_479ecd
.globl L_479ece
.globl L_479ed0
.globl L_479ed8
.globl L_479edc
.globl L_479ee0
.globl L_479ee4
.globl L_479ee8
.globl L_479ef0
.globl L_479ef4
.globl L_479ef8
.globl L_479efc
.globl L_479f00
.globl L_479f02
.globl L_479f03
.globl L_479f04
.globl L_479f06
.globl L_479f07
.globl L_479f08
.globl L_479f0c
.globl L_479f10
.globl L_479f14
.globl L_479f15
.globl L_479f18
.globl L_479f1c
.globl L_479f20
.globl L_479f24
.globl L_479f28
.globl L_479f2c
.globl L_479f30
.globl L_479f34
.globl L_479f38
.globl L_479f3c
.globl L_479f40
.globl L_479f43
.globl L_479f44
.globl L_479f45
.globl L_479f46
.globl L_479f47
.globl L_479f48
.globl L_479f49
.globl L_479f50
.globl L_479f54
.globl L_479f58
.globl L_479f5c
.globl L_479f60
.globl L_479f64
.globl L_479f68
.globl L_479f6c
.globl L_479f70
.globl L_479f74
.globl L_479f78
.globl L_479ff8
.globl L_47a078
.globl L_47a07c
.globl L_47a084
.globl L_47a088
.globl L_47a08c
.globl L_47a0d4
.globl L_47a0dc
.globl L_47a0e0
.globl L_47a0e4
.globl L_47a0e8
.globl L_47a0ec
.globl L_47a0f4
.globl L_47a0f8
.globl L_47a0fc
.globl L_47a100
.globl L_47a104
.globl L_47a10b
.globl L_47a110
.globl L_47a114
.globl L_47a118
.globl L_47a11b
.globl L_47a120
.globl L_47a124
.globl L_47a128
.globl L_47a130
.globl L_47a134
.globl L_47a138
.globl L_47a148
.globl L_47a14c
.globl L_47a14d
.globl L_47a54c
.globl L_47a550
.globl L_47a552
.globl L_47a94c
.globl L_47ad4c
.globl L_47ad4e
.globl L_47ad4f
.globl L_47b14c
.globl L_47b150
.globl L_47b54c
.globl L_47b550
.globl L_47b554
.globl L_47b94c
.globl L_480000
.globl L_490000
.globl L_4a0000
.globl L_4b0000
.globl L_4bb94c
.globl L_4bbd4c
.globl L_4bbd50
.globl L_4bc150
.globl L_4bc174
.globl L_4bc17c
.globl L_4bc580
.globl L_4bc588
.globl L_4bc590
.globl L_4bce00
.globl L_4c0000
.globl L_4c0020
.globl L_4c0c94
.globl L_4c10a4
.globl L_4c4f54
.globl L_4c4f55
.globl L_4c4f94
.globl L_4c4f98
.globl L_4c4f9c
.globl L_4c4fa0
.globl L_4c8fe0
.globl L_4c8fe8
.globl L_4c8ffa
.globl L_4c8ffe
.globl L_4c9010
.globl L_4c9014
.globl L_4c9018
.globl L_4c901c
.globl L_4c9026
.globl L_4c902a
.globl L_4c902e
.globl L_4c903c
.globl L_4c9040
.globl L_4c9044
.globl L_4c9052
.globl L_4c9068
.globl L_4c907e
.globl L_4c9094
.globl L_4c90aa
.globl L_4c90c0
.globl L_4c90e8
.globl L_4c90ec
.globl L_4c90f0
.globl L_4c90f4
.globl L_4c90f8
.globl L_4c90fc
.globl L_4c9100
.globl L_4c9104
.globl L_4c9108
.globl L_4c910c
.globl L_4c9110
.globl L_4c9114
.globl L_4c9118
.globl L_4c911c
.globl L_4c9120
.globl L_4c9124
.globl L_4c9128
.globl L_4c912c
.globl L_4c9130
.globl L_4c9134
.globl L_4c9138
.globl L_4c917f
.globl L_4c9180
.globl L_4c9182
.globl L_4c9184
.globl L_4c9186
.globl L_4c9364
.globl L_4c93a8
.globl L_4c97a8
.globl L_4c97d6
.globl L_4c97d8
.globl L_4cb7be
.globl L_4cb7c2
.globl L_4cb7c4
.globl L_4cb7c6
.globl L_4cb7c8
.globl L_4cb7ca
.globl L_4cdc64
.globl L_4ce064
.globl L_4ce068
.globl L_4ce06c
.globl L_4ce074
.globl L_4d0000
.globl L_4e0000
.globl L_4f0000
.globl L_500000
.globl L_50000a
.globl L_50ec88
.globl L_50ec8c
.globl L_50ec90
.globl L_50ec94
.globl _XeCryptRandomState
.globl _blOrder
.globl _buildMode
.globl _cpuKey
.globl _flashFiles
.globl _fsFiles
.globl _fsTable
.globl _g479ea8
.globl _g479f4c
.globl _g47a080
.globl _hdrTemplate
.globl _imgEnd
.globl _iniBuf
.globl _iniSize
.globl _key1bl
.globl _key28c
.globl _manifest
.globl _masterPub
.globl _mmcAnchor
.globl _netStartTime
.globl _pub1bl
.globl _pub2a4
.globl _xb

.bss
.p2align 2
_blOrder:
          .zero 28
_xb:
          .zero 4
L_479ea4:
          .zero 3
L_479ea7:
          .zero 1
_g479ea8:
          .zero 4
L_479eac:
          .zero 4
L_479eb0:
          .zero 4
L_479eb4:
          .zero 4
L_479eb8:
          .zero 4
L_479ebc:
          .zero 4
L_479ec0:
          .zero 4
L_479ec4:
          .zero 4
L_479ec8:
          .zero 4
L_479ecc:
          .zero 1
L_479ecd:
          .zero 1
L_479ece:
          .zero 2
L_479ed0:
          .zero 4
L_479ed4:
          .zero 4
L_479ed8:
          .zero 4
L_479edc:
          .zero 4
L_479ee0:
          .zero 4
L_479ee4:
          .zero 4
L_479ee8:
          .zero 4
L_479eec:
          .zero 4
L_479ef0:
          .zero 4
L_479ef4:
          .zero 4
L_479ef8:
          .zero 4
L_479efc:
          .zero 4
L_479f00:
          .zero 2
L_479f02:
          .zero 1
L_479f03:
          .zero 1
L_479f04:
          .zero 2
L_479f06:
          .zero 1
L_479f07:
          .zero 1
L_479f08:
          .zero 4
L_479f0c:
          .zero 4
L_479f10:
          .zero 4
L_479f14:
          .zero 1
L_479f15:
          .zero 3
L_479f18:
          .zero 4
L_479f1c:
          .zero 4
L_479f20:
          .zero 4
L_479f24:
          .zero 4
L_479f28:
          .zero 4
L_479f2c:
          .zero 4
L_479f30:
          .zero 4
L_479f34:
          .zero 4
L_479f38:
          .zero 4
L_479f3c:
          .zero 4
L_479f40:
          .zero 3
L_479f43:
          .zero 1
L_479f44:
          .zero 1
L_479f45:
          .zero 1
L_479f46:
          .zero 1
L_479f47:
          .zero 1
L_479f48:
          .zero 1
L_479f49:
          .zero 3
_g479f4c:
          .zero 4
L_479f50:
          .zero 4
L_479f54:
          .zero 4
L_479f58:
          .zero 4
L_479f5c:
          .zero 4
L_479f60:
          .zero 4
L_479f64:
          .zero 4
L_479f68:
          .zero 4
L_479f6c:
          .zero 4
L_479f70:
          .zero 4
L_479f74:
          .zero 4
L_479f78:
          .zero 128
L_479ff8:
          .zero 128
L_47a078:
          .zero 4
L_47a07c:
          .zero 4
_g47a080:
          .zero 4
L_47a084:
          .zero 4
L_47a088:
          .zero 4
L_47a08c:
          .zero 72
L_47a0d4:
          .zero 4
L_47a0d8:
          .zero 4
L_47a0dc:
          .zero 4
L_47a0e0:
          .zero 4
L_47a0e4:
          .zero 4
L_47a0e8:
          .zero 4
L_47a0ec:
          .zero 8
L_47a0f4:
          .zero 4
L_47a0f8:
          .zero 4
L_47a0fc:
          .zero 4
L_47a100:
          .zero 4
L_47a104:
          .zero 4
L_47a108:
          .zero 3
L_47a10b:
          .zero 1
_key1bl:
          .zero 4
L_47a110:
          .zero 4
L_47a114:
          .zero 4
L_47a118:
          .zero 3
L_47a11b:
          .zero 1
_cpuKey:
          .zero 4
L_47a120:
          .zero 4
L_47a124:
          .zero 4
L_47a128:
          .zero 4
_key28c:
          .zero 4
L_47a130:
          .zero 4
L_47a134:
          .zero 4
L_47a138:
          .zero 4
_pub1bl:
          .zero 4
_masterPub:
          .zero 4
_pub2a4:
          .zero 4
L_47a148:
          .zero 4
L_47a14c:
          .zero 1
L_47a14d:
          .zero 1023
L_47a54c:
          .zero 4
L_47a550:
          .zero 2
L_47a552:
          .zero 1017
L_47a94b:
          .zero 1
L_47a94c:
          .zero 3
L_47a94f:
          .zero 1
L_47a950:
          .zero 2
L_47a952:
          .zero 2
L_47a954:
          .zero 4
L_47a958:
          .zero 1012
L_47ad4c:
          .zero 2
L_47ad4e:
          .zero 1
L_47ad4f:
          .zero 1021
L_47b14c:
          .zero 4
L_47b150:
          .zero 1020
L_47b54c:
          .zero 4
L_47b550:
          .zero 4
L_47b554:
          .zero 1016
L_47b94c:
          .zero 18100
L_480000:
          .zero 65536
L_490000:
          .zero 65536
L_4a0000:
          .zero 65536
L_4b0000:
          .zero 47436
L_4bb94c:
          .zero 1024
L_4bbd4c:
          .zero 4
L_4bbd50:
          .zero 1024
L_4bc150:
          .zero 36
L_4bc174:
          .zero 8
L_4bc17c:
          .zero 1028
L_4bc580:
          .zero 8
L_4bc588:
          .zero 8
L_4bc590:
          .zero 2160
L_4bce00:
          .zero 12800
L_4c0000:
          .zero 32
L_4c0020:
          .zero 3188
L_4c0c94:
          .zero 1040
L_4c10a4:
          .zero 16048
L_4c4f54:
          .zero 1
L_4c4f55:
          .zero 63
L_4c4f94:
          .zero 4
L_4c4f98:
          .zero 4
L_4c4f9c:
          .zero 4
L_4c4fa0:
          .zero 1024
L_4c53a0:
          .zero 15424
L_4c8fe0:
          .zero 4
_flashFiles:
          .zero 4
L_4c8fe8:
          .zero 18
L_4c8ffa:
          .zero 4
L_4c8ffe:
          .zero 18
L_4c9010:
          .zero 4
L_4c9014:
          .zero 4
L_4c9018:
          .zero 4
L_4c901c:
          .zero 10
L_4c9026:
          .zero 4
L_4c902a:
          .zero 4
L_4c902e:
          .zero 14
L_4c903c:
          .zero 4
L_4c9040:
          .zero 4
L_4c9044:
          .zero 14
L_4c9052:
          .zero 22
L_4c9068:
          .zero 22
L_4c907e:
          .zero 22
L_4c9094:
          .zero 22
L_4c90aa:
          .zero 22
L_4c90c0:
          .zero 40
L_4c90e8:
          .zero 4
L_4c90ec:
          .zero 4
L_4c90f0:
          .zero 4
L_4c90f4:
          .zero 4
L_4c90f8:
          .zero 4
L_4c90fc:
          .zero 4
L_4c9100:
          .zero 4
L_4c9104:
          .zero 4
L_4c9108:
          .zero 4
L_4c910c:
          .zero 4
L_4c9110:
          .zero 4
L_4c9114:
          .zero 4
L_4c9118:
          .zero 4
L_4c911c:
          .zero 4
L_4c9120:
          .zero 4
L_4c9124:
          .zero 4
L_4c9128:
          .zero 4
L_4c912c:
          .zero 4
L_4c9130:
          .zero 4
L_4c9134:
          .zero 4
L_4c9138:
          .zero 40
_buildMode:
          .zero 4
_mmcAnchor:
          .zero 27
L_4c917f:
          .zero 1
L_4c9180:
          .zero 2
L_4c9182:
          .zero 2
L_4c9184:
          .zero 2
L_4c9186:
          .zero 474
L_4c9360:
          .zero 4
L_4c9364:
          .zero 64
_iniBuf:
          .zero 4
L_4c93a8:
          .zero 1024
L_4c97a8:
          .zero 4
_iniSize:
          .zero 20
_fsFiles:
          .zero 22
L_4c97d6:
          .zero 2
L_4c97d8:
          .zero 8166
L_4cb7be:
          .zero 2
_fsTable:
          .zero 2
L_4cb7c2:
          .zero 2
L_4cb7c4:
          .zero 2
L_4cb7c6:
          .zero 2
L_4cb7c8:
          .zero 2
L_4cb7ca:
          .zero 8178
L_4cd7bc:
          .zero 4
_hdrTemplate:
          .zero 4
L_4cd7c4:
          .zero 4
L_4cd7c8:
          .zero 4
L_4cd7cc:
          .zero 4
L_4cd7d0:
          .zero 4
L_4cd7d4:
          .zero 4
L_4cd7d8:
          .zero 4
L_4cd7dc:
          .zero 4
L_4cd7e0:
          .zero 4
L_4cd7e4:
          .zero 4
L_4cd7e8:
          .zero 4
L_4cd7ec:
          .zero 4
L_4cd7f0:
          .zero 4
L_4cd7f4:
          .zero 4
L_4cd7f8:
          .zero 4
L_4cd7fc:
          .zero 4
L_4cd800:
          .zero 4
L_4cd804:
          .zero 4
L_4cd808:
          .zero 4
L_4cd80c:
          .zero 20
L_4cd820:
          .zero 4
L_4cd824:
          .zero 4
L_4cd828:
          .zero 4
L_4cd82c:
          .zero 4
L_4cd830:
          .zero 8
L_4cd838:
          .zero 4
L_4cd83c:
          .zero 4
_imgEnd:
          .zero 4
_netStartTime:
          .zero 1052
_manifest:
          .zero 4
L_4cdc64:
          .zero 1024
L_4ce064:
          .zero 4
L_4ce068:
          .zero 4
L_4ce06c:
          .zero 8
L_4ce074:
          .zero 8076
L_4d0000:
          .zero 65536
L_4e0000:
          .zero 65536
L_4f0000:
          .zero 65536
L_500000:
          .zero 10
L_50000a:
          .zero 59510
_XeCryptRandomState:
          .zero 1032
L_50ec88:
          .zero 4
L_50ec8c:
          .zero 4
L_50ec90:
          .zero 4
L_50ec94:
          .zero 20
