# s76: NO MATCH (fncmp stays 78 from best78b.c)

Copied s75 tooling (gr2.py, f.sh, ours.sh, sig.py, origs.txt, best78b.c).
Ran 3 parallel gr2.py hill climbs (1800 s each, sideways moves allowed) from best78b.c:
every accepted move was sideways at 78; no improvement (logs w*.log.gz / w*.out.gz).
Conclusion: the existing bcp-goto chain + cold/hot label lever space is exhausted for item a
(cold-group placement after argv traces). Needs a new lever kind attaching each cold group to
its option trace (e.g. per-group asm goto from the option trace's last block, rok fan weights),
designed from bb-reorder connect_traces mechanics; not attempted in this session.
