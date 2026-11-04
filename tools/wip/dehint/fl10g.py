"""fl10g.py: does a third exit folded after IPA inlining, but not by IPA-CP, give the reference?  Never-written static flag (a dead test: verifies the model, not a candidate)."""
import fllib as L, fl10lib as F
FLAG = F.KF_NONE.replace("if (*q != 0)", "if (iniFlag)\n\t\t\t\t\treturn i + len;\n\t\t\t\tif (*q != 0)")
FLAG1 = F.KF_NONE.replace("if (*q != 0)", "if (iniFlag)\n\t\t\t\t\treturn -1;\n\t\t\t\tif (*q != 0)")
F.run({'flag': F.fk(FLAG, 'static int iniFlag;\n'), 'flag-1': F.fk(FLAG1, 'static int iniFlag;\n')}, 'g')
