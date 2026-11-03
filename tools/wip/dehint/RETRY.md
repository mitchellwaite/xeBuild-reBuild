# Retrying what's left

`sendAvatarData` is done: attempt 6 found a plain `for` loop. `netRecvVerbose` is
settled for now, with a dead test the user chose over the asm; retry it only with a
new idea. Attempts run one at a time and continue from the function's notes.

| Function | Notes | Done means |
|----------|-------|------------|
| `netRecvVerbose` in `src/net.c`, with its clone `netRecv` | `notes/net_netRecvVerbose.md` | The dead `if (!len)` is gone and the full build's SHA256 matches |

## For each attempt

1. Read `../../../CLAUDE.md`, `README.md` here (what counts as a match) and the
   function's notes. Don't repeat what its don't-retry lists rule out.
2. Pick an idea the notes haven't tested and sweep it with a generator. Earlier
   thresholds came from particular shapes, so they can be wrong for a new one;
   check them. Look at what the reference's instructions say the author wrote.
3. Add an "Attempt N" section to the notes as you go, with what moved the numbers,
   the mechanism, and what not to retry.
4. Stop on a match, or when this attempt's ideas with real odds run out. Don't pad
   an attempt with spellings that the notes already predict won't help.

## Rules

- Only `tools/toolchain-4745`. Don't modify `xeBuild.exe` or set up other compilers.
- Don't search the machine for GCC sources. If a question needs source, read that
  one file from the official repo at tag `releases/gcc-6.2.0`, as CLAUDE.md says.
- Don't commit or push; the session running the attempts does that.
- Don't touch other functions' code or `build.sh`. Leave `src/` unchanged unless
  the result is a match, or for `sendAvatarData` strictly more natural with the same bytes.
- Write generators with the Write tool and change source with the Edit tool:
  heredocs mangle backslashes.
- Natural code wins. Live but redundant code that reads naturally lands, flagged for
  the user's review. Code nobody would write is a candidate: save it as
  `drafts/<obj>_<function>_candidate.patch` and leave `src/` alone.
- Behaviour must stay the same. The full build has the last word, because a
  differing `.p2align` may emit no bytes and fncmp ignores jump targets.
- On a match: update the comment above the function, run `sh build.sh`, and confirm
  the SHA256 is `10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c`.
  Leave the top-level README.md alone.
