import re
from stack import Stack
from operation import Operation, OperationResult
from regex import regex
from util import *

def handleCulledLine(line):
	#return commentLine(line)
	if "\n" in line:
		return "\n"
	else:
		return "" # no extra newline to the last line of the file

class ConditionalState:
	parent = ""
	def __init__(self, state):
		self.state = state

class IfdefOperation(Operation):
	stack = None

	def __init__(self):
		self.stack = Stack()
		pass

	def apply(self, line, state):
		result = OperationResult(line, False)
		skip = False

		if not self.stack.isEmpty():
			#print(str(state.row) + " : " + str(self.stack.arr))
			if self.stack.contains(False):
				skip = True

		dirsearch = regex['directive'].search(line)
		if dirsearch:
			directive = dirsearch.group(1)
			identifier = dirsearch.group(2)

			if directive == "#ifdef" or directive == "#ifndef" and not skip:
				result.line = commentLine(result.line)

				if identifier == "":
					result.error = "Invalid " + directive
					return result

				if not identifier in state.macros:
					self.stack.push(directive == "#ifndef")
					result.line = handleCulledLine(result.line)
					return result

				self.stack.push(directive != "#ifndef")

			elif directive == "#else":
				result.line = commentLine(result.line)

				if self.stack.isEmpty():
					result.error = "Unexpected #else"
					return result
				
				if self.stack.top() == True:
					self.stack.pop()	
					self.stack.push(False)
				else:
					self.stack.pop()
					self.stack.push(True)

			elif directive == "#endif":
				result.line = commentLine(result.line)

				if self.stack.isEmpty():
					result.error = "Unexpected #endif"
					return result

				self.stack.pop()

		if skip:
			result.line = handleCulledLine(result.line)

		return result

