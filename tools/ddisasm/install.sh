#!/bin/bash
# Install ddisasm + gtirb-pprinter into ~/ddisasm-root without root.  Run inside WSL:
#   wsl -d Ubuntu -- bash tools/ddisasm/install.sh
# GrammaTech only publishes Ubuntu 20.04 (focal) packages, so the focal Boost,
# protobuf and libgomp they link against come from archive.ubuntu.com too.
# Unpacks with Python because dpkg-deb -x fails under WSL1.
set -e
LIST=$(cd "$(dirname "$0")" && pwd)/debs.txt
mkdir -p ~/ddisasm-debs; cd ~/ddisasm-debs
tr -d '\r' < "$LIST" | while read -r url sha; do
  f=$(basename "$url"); [ -f "$f" ] || curl -sfLO "$url"
  echo "$sha  $f"
done | sha256sum -c
rm -rf ~/ddisasm-root; mkdir -p ~/ddisasm-root
for f in *.deb; do
  dpkg-deb --fsys-tarfile "$f" | python3 -c '
import tarfile, sys, os
root = sys.argv[1]
t = tarfile.open(fileobj=sys.stdin.buffer, mode="r|")
for m in t:
    p = os.path.join(root, m.name)
    if m.isdir():
        os.makedirs(p, exist_ok=True)
    elif m.issym():
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if os.path.lexists(p): os.remove(p)
        os.symlink(m.linkname, p)
    elif m.isfile():
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as o: o.write(t.extractfile(m).read())
        os.chmod(p, m.mode)
' ~/ddisasm-root
done
. "$(dirname "$LIST")/env.sh"
ddisasm --version; gtirb-pprinter --version
