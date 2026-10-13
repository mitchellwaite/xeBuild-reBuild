# Source inside WSL to put the user-local ddisasm install on PATH.
R=~/ddisasm-root/usr
export PATH=$R/bin:$PATH LD_LIBRARY_PATH=$R/lib:$R/lib/x86_64-linux-gnu
