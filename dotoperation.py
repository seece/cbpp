
import re
from util import *
from operation import Operation, OperationResult
from regex import regex


class DotOperation(Operation):
	def __init__(self):
		self.strings = []

	def apply(self, line, state):
		result = OperationResult(line, False)

		if not state.args.anticrap:
			return result

		#trimmed = stripComments(line)
		output = line

		self.strings = scanForStrings(line)
		slashmatch = regex['backslash'].finditer(line)
		dotmatch = regex['typedot'].finditer(line)

		for m in slashmatch:
			if checkIfInsideString(m.start('backslash'), self.strings):
				continue

			substitution = "."
			output = output[:m.start('backslash')] + substitution + output[m.end('backslash'):]

		for m in dotmatch:
			if checkIfInsideString(m.start('dot'), self.strings):
				continue

			substitution = "\\"
			output = output[:m.start('dot')] + substitution + output[m.end('dot'):]

		result.line = output

		return result
