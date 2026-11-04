# attempt 24, pin_t: the over-long table's size. Its k loop has n + 1 times the arm's frequency at profile_estimate (bb 33 830, k head 2491 for n = 2), so once it's hotter than the page loop's head every frequency in imgAdd is rescaled, including the 900 of the block loop that t's rounding depends on. Base: src minus the pin.
# `IWB=build/iw/a24/np.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw304.py -n 40 -t 4`
A = 'uint32_t used[2] = { (off & 0x1ffff) / 512, 0 };'
K = 'for (k = 0; k < 2; k++)\n								left -= used[k];'
AXES = [[('', [])] + [('n%d' % n, [(A, 'uint32_t used[%d] = { (off & 0x1ffff) / 512 };' % n), (K, ('for (k = 0; k < %d; k++)\n								left -= used[k];' % n))]) for n in range(3, 26)]]
