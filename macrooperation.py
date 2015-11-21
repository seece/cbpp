
import re
from macro import Macro
from macro import ParameterList, getParameterList
from util import *
from stack import Stack
from operation import Operation, OperationResult
from error import errors, warnings, infos
from regex import regex

# TODO move this somewhere else
def handlePragma(identifier, args):
	if identifier == "dumb_debug":
		args.dumb_debug = True
	elif identifier == "anticrap":
		args.anticrap = True
	elif identifier == "nomacros":
		args.nomacros = True
	else:
		errors.add("Invalid #pragma identifier")	
	return args



class MacroOperation(Operation):
	def __init__(self):
		self.strings = []
		# self.macros = {}

	def handleInclude(self, state, line, filedir):
		line=line.strip()
		words = re.split('[\s"]+', line)
		filepath = words[1]
		#line = re.split('[\s"]+',string.strip(line))
		print("filedir: " + filedir)
		print("filepath: " + filepath)
		inputfile = open(filedir + filepath)

		nextline = inputfile.readline()
		while True:
			line = nextline
			nextline = inputfile.readline()

			if not nextline:
				state.lastline = True

			if not line:
				break

			self.apply(line, state)
			if not nextline:
				break

		inputfile.close()


	def apply(self, line, state):
		result = OperationResult(line, False)
		# strings = [] # string start and end positions as StringPos instances

		trimmed = stripComments(line)
		output = line
		expanded_line = line

		# find the directive
		dirsearch = regex['directive'].search(trimmed)
		if dirsearch:
			directive = dirsearch.group(1)
			identifier = dirsearch.group(2)

			origline = output
			output = commentLine(line)

			if directive == "#define":
				macro = Macro(dirsearch, trimmed)
				if macro != None:
					state.macros[macro.name] = macro
			elif directive == "#undef":
				temp_macro = Macro(dirsearch, trimmed)
				if temp_macro.name in state.macros:
					del state.macros[temp_macro.name]
				else:
					warnings.add(state.row, "Trying to undefine a nonexistent macro " + temp_macro.name)					
			elif directive == "#pragma":
				if state.args.verbose: print("pragma: " + identifier)
				state.args = handlePragma(identifier, state.args)
			elif directive == "#include":
				if state.args.filedir:
					self.handleInclude(state, trimmed, state.args.filedir)
			else:
				# we'll leave #ifdef, #ifndef and #else to the other operators
				output = origline

		else:
			if state.args.nomacros:
				return result

			visited = Stack()

			#for name in self.macros:
			output = expandAll(line, state.macros, visited, state)

		result.line = output
		return result

# returns a regex string that matches this identifier name
def nameRegex(name):
	return "(\W|^)+(?P<name>" + name + r")(\W|$)+"

lineNameRegex = re.compile(nameRegex("__LINE__"))
fileNameRegex = re.compile(nameRegex("__FILE__"))
concatNameRegex = re.compile(r"(?P<name>" + " ## " + r")")
	
# applies some additional macros to the macro array
# and the returns the keyset
def getMacroKeys(macrodict, state):
	macrokeys = list(macrodict.keys())
	linenum = Macro(None, "")
	linenum.name = "__LINE__" 
	linenum.payload = str(state.row)
	linenum.nameregex = lineNameRegex

	filename= Macro(None, "")
	filename.name = "__FILE__" 
	filename.payload = str('"' + state.filename + '"')
	filename.nameregex = fileNameRegex

	# temporary concatenation macro, must run LAST
	concat = Macro(None, "")
	concat.name = " ## " 
	concat.payload = ""
	concat.nameregex = concatNameRegex

	macrodict[linenum.name] = linenum
	macrodict[filename.name] = filename
	macrodict[concat.name] = concat
	macrokeys = list(macrodict.keys())
	macrokeys.append(linenum.name)
	macrokeys.append(filename.name)
	macrokeys.append(concat.name)
	
	return macrokeys

# returns the length of one macro invocation
# useful when replacing parts of the line with expanded versions
def getInvocationLength(match, macro):
	start = match.start('name')
	end = match.end('name')
	identifier = match.group('name')
	
	c = readchar(match.string, end)
	
	if macro.flag == True:
		return len(match.group('name'))

	if not c or c != '(' and macro.parameters:
		errors.add(None, "No parameters for " + macro.name)
		return False
		
	args = parseArgumentList(match.end('name'), match.string)
	
	if not args:
		return False
		
	return args.length + len(identifier)
				
def expandAll(string, macros, visited, state):
	macrokeys = getMacroKeys(macros, state)
	expanded = string
	line = string
	strings = []
	
	for name in macrokeys:
		m = macros[name]

		if m.flag:
			continue
			
		if visited.contains(name):
			warnings.add(state.row, "Skipping recursive macro call " + name)
			continue

		try_match = True
		while (try_match):
			try_match = False
			strings = scanForStrings(expanded)
			namematch = m.nameregex.finditer(expanded)

			for n in namematch:
				if checkIfInsideString(n.start('name'), strings):
					continue

				if checkIfInsideComment(line, n.start('name')):
					continue

				if state.args.verbose: infos.add(state.row, "\tfound " + name)

				visited.push(name)
				length = getInvocationLength(n, m)
				
				subs = m.expand(n)
				visited.pop()
				
				if not subs:
					errors.add(state.row, "Invalid macro call " + name)
					return expanded

				final = expandAll(subs.string, macros, visited, state)
				expanded = strInsert(expanded, subs.start, subs.end, final)
				
				if state.args.verbose == True: infos.add(state.row, "Expand " + name + ": " + final)
				try_match = True
				break
				
	return expanded
	
	
	
