# attempt 21: do-while for the block loop and/or the FS loop: no ch2 guard `blocks != 0`, so the FS exit should keep one predecessor at sccp (blocks is always >= 1 in the code anyway).
# `IWB=build/iw/a21/na.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw279.py -n 30 -t 4`
B0 = '	for (b = 0; b < blocks; b++) {\n		small ='
B1 = '''				}
			}
		}
	}
#undef BLK'''
F0 = '		for (i = 0; i < blocks; i++) {\n'
F1 = '''				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			}
		}
'''
BL = [
 ('', []),
 ('bd', [(B0, '	b = 0;\n	do {\n		small ='), (B1, '''				}
			}
		}
	} while (++b < blocks);
#undef BLK''')]),
 ('bd2', [(B0, '	b = 0;\n	do {\n		small ='), (B1, '''				}
			}
		}
		b++;
	} while (b < blocks);
#undef BLK''')]),
 ('bd3', [(B0, '	b = 0;\n	do {\n		small ='), (B1, '''				}
			}
		}
	} while (++b != blocks);
#undef BLK''')]),
]
FL = [
 ('', []),
 ('fd', [(F0, '		i = 0;\n		do {\n'), (F1, F1[:-4] + '		} while (++i < blocks);\n')]),
 ('fd2', [(F0, '		i = 0;\n		do {\n'), (F1, F1[:-4] + '			i++;\n		} while (i < blocks);\n')]),
 ('fd3', [(F0, '		i = 0;\n		do {\n'), (F1, F1[:-4] + '		} while (++i != blocks);\n')]),
]
AXES = [BL, FL]
