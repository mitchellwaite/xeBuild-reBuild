"""mode_client attempt 15: mc14rmk.add extended to k = 8 extra vrp1 blocks.  k7 adds the
split of wbArgs' first test (`j == argc || !a` / `*a == '-'`), k8 also the -w arm's
(`i + 1 == argc || !a` / `*a == '-'`); both measured +1 and IDENTICAL on 48 in place of
one help split (build/mc/w15/k7.py)."""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc14rmk

Q = "'-'"
WB1 = ("\tif (j == argc || !a || *a == " + Q + ")\n\t\tclient_usage(3, argv[i]);\n\tj++;",
       "\tif (j == argc || !a)\n\t\tclient_usage(3, argv[i]);\n\tif (*a == " + Q + ")\n\t\tclient_usage(3, argv[i]);\n\tj++;")
W1 = ("\t\t\tif (i + 1 == argc || !a || *a == " + Q + ")\n\t\t\t\tclient_usage(3, argv[i]);\n\t\t\tif (mode) { client_usage(5",
      "\t\t\tif (i + 1 == argc || !a)\n\t\t\t\tclient_usage(3, argv[i]);\n\t\t\tif (*a == " + Q + ")\n\t\t\t\tclient_usage(3, argv[i]);\n\t\t\tif (mode) { client_usage(5")


def add(t, k):
    if k <= 6:
        return mc14rmk.add(t, k)
    if k > 8:
        return None
    t = mc14rmk.add(t, 6)
    if t is None:
        return None
    for old, new in [WB1, W1][:k - 6]:
        if old not in t:
            return None
        t = t.replace(old, new, 1)
    return t
