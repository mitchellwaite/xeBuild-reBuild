B=$1; P=$2
N='"erasing block 0x%x...", block);
			if (netEraseBlockU32(block, 1))'
sh r.sh ${P}1 $B "$N" '"erasing block 0x%x...", block);
			if (__builtin_expect(netEraseBlockU32(block, 1), 1))'
sh r.sh ${P}2 $B "$N" '"erasing block 0x%x...", block);
			if (__builtin_expect(!!netEraseBlockU32(block, 1), 0))'
sh r.sh ${P}3 $B '
		if (block < cinfo->nandSize / cinfo->blockSize) {

			eerase:' '
		if (__builtin_expect(block < cinfo->nandSize / cinfo->blockSize, 1)) {

			eerase:'
sh r.sh ${P}4 $B 'myatoh32(sblock, -1);



	if (block != -1) {' 'myatoh32(sblock, -1);



	if (__builtin_expect(block != -1, 1)) {'
