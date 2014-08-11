
import sys
import ntpath

import re
from util import *
import substitution
import macro
import stack
from operation import Operation, OperationResult
from ifdef import IfdefOperation
from macrooperation import MacroOperation
from debugoperation import DebugOperation 
from culloperation import CullOperation
from minifyoperation import MinifyOperation
from dotoperation import DotOperation
from commentoperation import CommentOperation
from multilineoperation import MultilineMacroOperation
from error import infos, errors, warnings
from regex import regex

Macro = macro.Macro
Substitution = substitution.Substitution
Stack = stack.Stack

class ParserState:
	def __init__(self):
		self.depth = 0
		self.instring = False
		self.args = None
		self.row = 0
		self.lastline = False	# are we currently on the last line of the file
		self.filename = ""
		self.macros = {}
		self.filestack = Stack()
		pass

def createFlagsFromList(state, args):
	if args.flags == "" or args.flags == None:
		return

	flaglist = args.flags.split(";")
	macrolist = []

	for f in flaglist:
		m = Macro(None, None)
		m.name = f
		m.flag = True
		state.macros[m.name] = m

class Processor:
	def __init__(self, args, logger=False):
		self.config = {}
		self.regex = {}
		self.args = args
		self.state = ParserState()
		createFlagsFromList(self.state, self.args)
	
	def process(self):
		args = self.args
		self.state.args = args
		state = self.state

		path = args.input

		inputfile = open(path)
		nextline = inputfile.readline()
		line = ""

		state.filename = ntpath.basename(path)
		state.row = 0
		out = [] # the actual contents of the output file

		operations = []
		operations.append(IfdefOperation())
		operations.append(DebugOperation())
		operations.append(CommentOperation())
		operations.append(MacroOperation())
		""" TODO: #include handling might clash with DECORATE definitions """
		operations.append(MultilineMacroOperation())
		operations.append(DotOperation())
		operations.append(MinifyOperation())
		operations.append(CullOperation())

		while True:
			state.depth = 0 	# paren depth
			state.instring = False
			discard = False

			line = nextline
			nextline = inputfile.readline()

			if not nextline:
				state.lastline = True

			if not line:
				break

			current_line = line
			state.row += 1

			for o in operations:
				result = o.apply(current_line, state)

				if result.error != None:
					errors.add(state.row, result.error)

				if result.discard:
					discard = True
					break
				current_line = result.line
				
			if not discard:
				out.append(current_line)
		inputfile.close()

		outputfile = open(args.output, 'w')
		for r in out:
			print(r, file=outputfile, end='')

		outputfile.close()
			
		if args.show_report:
			print ("Found the following macros: ")
			for m in state.macros:
				print(str(state.macros[m]))

			print("")
		if args.wait_on_error:
			error_count = len(errors.getLog())
			print(str(error_count) + " errors: ")

			for m in errors:
				print("  " + m.toString())

			if error_count > 0:
				waitForEnter()



