import re
from macro import Macro
from util import *
from stack import Stack
from operation import Operation, OperationResult
from error import errors, warnings, infos
from regex import regex

def isEmptyLine(line):
	if line == "" or line == "\n" or line == "\r\n":
		return True
	return False

class DebugOperation(Operation):
	def __init__(self):
		self.macrostring = 'SetWindow "line: " + __LINE__ '

	def apply(self, line, state):
		result = OperationResult(line, False)

		if not state.args.dumb_debug:
			return result

		trimmed = stripComments(line)  
		addition = ": "

		if isEmptyLine(trimmed):
			addition = ""

		if trimmed is not line: # there's a comment on this line
			#print("left: " + line[len(trimmed)-1:])

			if isEmptyLine(trimmed): 
				trimmed = line[:len(trimmed)-1] + self.macrostring + addition + line[len(trimmed)-1:]
			else:
				trimmed = self.macrostring + addition + line
		else:
			trimmed = self.macrostring + addition + line
		result.line = trimmed

		return result
