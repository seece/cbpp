from macrooperation import MacroOperation, expandAll
from operation import Operation, OperationResult
from util import stripComments, commentLine
from regex import regex
from stack import Stack
from macro import Macro
import re

class MultilineMacroOperation(MacroOperation):
	def __init__(self):
		self.strings = []
		self.macro = None
		self.payload = ""
		self.multimacros = {}

	def apply(self, line, state):
		result = OperationResult(line, False)

		trimmed = stripComments(line)
		output = line
		expanded_line = line

		# find the directive
		dirsearch = regex['directive'].search(trimmed)
		if dirsearch:
			directive = dirsearch.group(1)
			identifier = dirsearch.group(2)

			output = commentLine(line)

			if directive == "#macro":
				if self.macro:
					warnings.add("Trying to define multiline macro %s inside other macro %s" % (identifier, self.macro.name))					
					return result

				self.macro = Macro(dirsearch, trimmed)
				self.payload = ""
			elif directive == "#endmacro":
				#print ("macro %s ends") % (self.macro.name)
				self.macro.payload = self.macro.payload.rstrip('\n')
				self.multimacros[self.macro.name] = self.macro
				self.macro = None
				
			# TODO this is basically duplicate of the above functionality, clean it up
			elif directive == "#lambda":
				if self.macro:
					warnings.add("Trying to define multiline lambda %s inside other macro %s" % (identifier, self.macro.name))					
					return result

				self.macro = Macro(dirsearch, trimmed)
				self.macro.oneliner = True
				self.payload = ""
				
			elif directive == "#endlambda":
				#print ("macro %s ends") % (self.macro.name)
				self.macro.payload = self.macro.payload.rstrip('\n')
				self.macro.payload = re.sub("\n+", r':', self.macro.payload)
				self.multimacros[self.macro.name] = self.macro
				self.macro = None
			elif directive == "#undef":
				temp_macro = Macro(dirsearch, trimmed)
				if temp_macro.name in self.multimacros:
					del self.multimacros[temp_macro.name]	

			else:
				output = output

		else:
			if state.args.nomacros:
				return result

			# Expand collected macros only if not inside a multiline macro.
			if self.macro:
				line_trimmed = line
				
				if self.macro.oneliner:
					line_trimmed = line.lstrip(" ").lstrip("\t")
				
				self.macro.payload += line_trimmed
				output = commentLine(output)
			else:
				output = expandAll(line, self.multimacros, Stack(), state)

		result.line = output
		return result
