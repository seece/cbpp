import re
from util import *
from operation import Operation, OperationResult

class CullOperation(Operation):
	def __init__(self):
		self.inMultilineComment = False
		pass

	def apply(self, line, state):
		result = OperationResult(line, False)

		if not state.args.cull:
			return result

		trimmedLine = line.strip()
		words = trimmedLine.split()
		if (len(words) > 0):
			if (words[0].upper() == "REMSTART" or words[0].upper() == "REMEND"):
				self.inMultilineComment = not self.inMultilineComment
				result.discard = True
				return result

		if self.inMultilineComment:
			result.discard = True
			return result
				

		result.line = stripComments(line)
		stripped = result.line.strip()

		if stripped == "" or stripped == "\n" or stripped == "\r\n":
			result.discard = True

		if state.lastline:
			result.line = result.line.rstrip("\r\n")

		return result
			


