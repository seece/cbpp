import sys
import inspect
from tests.testcase import *
from processor import *

class noMacroExpansionInComments(Test):
	def setup(self):
		self.name = "no macro expansion in comments"
		self.sourcefile = "tests/cb/comments.cb"

class simpleSubstitution(Test):
	def setup(self):
		#self.name = "no macro expansion in comments"
		self.sourcefile = "tests/cb/substitution.cb"

class singleParameterSubstitution(Test):
	def setup(self):
		self.sourcefile = "tests/cb/substitution_single.cb"

class twoParameterSubstitution(Test):
	def setup(self):
		self.sourcefile = "tests/cb/substitution_two.cb"

class multipleSubstitution(Test):
	def setup(self):
		self.sourcefile = "tests/cb/substitution_multiple.cb"

class stringsAsParameters(Test):
	def setup(self):
		self.sourcefile = "tests/cb/strings.cb"

class noParens(Test):
	def setup(self):
		self.sourcefile = "tests/cb/no_parens.cb"

	def apply(self):
		args = self.getDefaultArgs()
		#args.show_report = True
		return self.compareExpected(args)

testlist = []

for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
	if obj.__module__ == __name__:
		testlist.append(obj)
