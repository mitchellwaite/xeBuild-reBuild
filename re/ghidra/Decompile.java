// Headless: print Ghidra's decompilation of the functions at the given
// addresses (hex, script args), or of the entry point when none are given.
//
// Ghidra lives outside the repo (C:\Users\Win11VM\ghidra; headless.bat sets
// its JDK). The project build/ghidra/proj is made once with -import:
//
//   headless.bat <abs>/build/ghidra/proj xeBuild -process xeBuild.exe
//       -noanalysis -readOnly -scriptPath <abs>/re/ghidra
//       -postScript Decompile.java 401000 ...
//@category xeBuild
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;

public class Decompile extends GhidraScript {
	@Override
	public void run() throws Exception {
		DecompInterface ifc = new DecompInterface();
		ifc.openProgram(currentProgram);
		String[] args = getScriptArgs();
		if (args.length == 0) {
			Address ep = currentProgram.getSymbolTable()
					.getExternalEntryPointIterator().next();
			args = new String[] { ep.toString() };
		}
		for (String a : args) {
			Address addr = toAddr(Long.parseLong(a.replaceFirst("^0x", ""), 16));
			Function f = getFunctionContaining(addr);
			if (f == null) {
				println("no function at " + addr);
				continue;
			}
			DecompileResults r = ifc.decompileFunction(f, 60, monitor);
			if (!r.decompileCompleted()) {
				println(f.getName() + ": " + r.getErrorMessage());
				continue;
			}
			println("// " + f.getName() + " @ " + f.getEntryPoint());
			println(r.getDecompiledFunction().getC());
		}
		ifc.dispose();
	}
}
