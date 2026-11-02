"""table2.py OUT BASE: s21 table.py with ext.py's extended targets (test blocks 110/113/116/129)."""
import os, sys, runpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ext  # extends search.TGT, sets table.D
import table
sys.argv = ['table.py'] + sys.argv[1:]
src = open(table.__file__).read().split("if __name__ == '__main__':")[1]
exec('if True:' + src, table.__dict__)
