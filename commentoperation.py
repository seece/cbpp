
import re
from util import *
from operation import Operation, OperationResult
from regex import regex


class CommentOperation(Operation):
	def __init__(self):
		self.strings = []

	def replaceAll(self, line, regex, substitution, matchgroup):
		quit = False
		output = line

		while (not quit):
			startmatch = regex.finditer(output)
			quit = True

			for m in startmatch:
				if checkIfInsideString(m.start(matchgroup), self.strings):
					continue
				# todo COMMENT CHECK

				output = output[:m.start(matchgroup)] + substitution + output[m.end(matchgroup):]
				quit = False
				break 
		
		return output


	def apply(self, line, state):
		result = OperationResult(line, False)

		#trimmed = stripComments(line)
		output = line

		self.strings = scanForStrings(line)

		output = self.replaceAll(output, regex['comment_start'], 'REMSTART', 'comment_start')
		output = self.replaceAll(output, regex['comment_end'], 'REMEND', 'comment_end')

		result.line = output

		return result
