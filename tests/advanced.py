
import sys
import inspect
from tests.testcase import *
from processor import *

class basicIfdef(Test):
	def setup(self):
		self.name = "test normal #ifdef feature"
		self.sourcefile = "tests/cb/ifdef.cb"

class negationIfdef(Test):
	def setup(self):
		self.name = "test #ifndef feature"
		self.sourcefile = "tests/cb/ifndef.cb"

class undef(Test):
	def setup(self):
		self.name = "test #undef feature"
		self.sourcefile = "tests/cb/undef.cb"

class basicConcatenation(Test):
	def setup(self):
		self.sourcefile = "tests/cb/concat.cb"

class lineMacro(Test):
	def setup(self):
		self.sourcefile = "tests/cb/line.cb"

class fileMacro(Test):
	def setup(self):
		self.sourcefile = "tests/cb/filemacro.cb"

class macroOverlap(Test):
	def setup(self):
		self.sourcefile = "tests/cb/substitution_overlap.cb"

class onlyMacroOnLine(Test):
	def setup(self):
		self.sourcefile = "tests/cb/linestart.cb"

class parensInArguments(Test):
	def setup(self):
		self.sourcefile = "tests/cb/parens.cb"

class dumbDebug(Test):
	def setup(self):
		self.sourcefile = "tests/cb/pragma.cb"
		
class recursion(Test):
	def setup(self):
		self.sourcefile = "tests/cb/recursion.cb"

"""
class namespaceBasic(Test):
	def setup(self):
		self.sourcefile = "tests/cb/namespace_basic.cb"

class namespaceNested(Test):
	def setup(self):
		self.sourcefile = "tests/cb/namespace_nested.cb"
"""

class culling(Test):
	def setup(self):
		self.sourcefile = "tests/cb/cull.cb"

	def getDefaultArgs(self):
		args = super().getDefaultArgs()
		args.cull = True
		return args

class minify(Test):
	def setup(self):
		self.sourcefile = "tests/cb/minify.cb"

	def getDefaultArgs(self):
		args = super().getDefaultArgs()
		args.minify= True
		return args

class minifyWithCulling(Test):
	def setup(self):
		self.sourcefile = "tests/cb/minify_and_cull.cb"

	def getDefaultArgs(self):
		args = super().getDefaultArgs()
		args.cull = True
		args.minify= True
		return args

class stringify(Test):
	def setup(self):
		self.name = "stringify macro parameters"
		self.sourcefile = "tests/cb/stringify.cb"
		
class multilineParse(Test):
	def setup(self):
		self.name = "multiline macro parsing"
		self.sourcefile = "tests/decorate/multiline_parse.txt"

class multilineExpand(Test):
	def setup(self):
		self.name = "basic multiline macro expansion"
		self.sourcefile = "tests/decorate/multiline_expand_basic.txt"

class multilineExpandNoParams(Test):
	def setup(self):
		self.name = "multiline macro with no parameters"
		self.sourcefile = "tests/decorate/multiline_expand_noparams.txt"

class multilineExpandMultiple(Test):
	def setup(self):
		self.name = "multiple multiline macros"
		self.sourcefile = "tests/decorate/multiline_expand_multiple.txt"

class multilineExpandLambda(Test):
	def setup(self):
		self.name = "basic multiline lambda expansion"
		self.sourcefile = "tests/decorate/multiline_expand_lambda.txt"
		
testlist = []

for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
	if obj.__module__ == __name__:
		testlist.append(obj)
