import sys
import re
from util import *
from error import errors, warnings, infos
import substitution
Substitution = substitution.Substitution

class ParameterList:
	def __init__(self, parameters, length):
		self.parameters = parameters
		self.length = length

def getPayload(dirsearch, line, parameter_count):
	pos = dirsearch.end(2)+1

	# search to the end of the parameter list
	if parameter_count != 0:
		while True:
			if pos>=len(line):
				return ""

			c = line[pos]

			if c == ')':
				pos += 1
				break

			pos += 1

	# take the reminder of the line and strip out newlines & whitespace
	return line[pos:].strip()

# returns a macro definition parameter list
def getParameterList(group, line):
	trimmed = stripComments(line)
	def_len = len(group)
	parameters = trimmed[def_len:]

	# find each parameter name separated by a comma 
	pos = def_len
	comma_separation = re.compile(r"\(([^()]*)\)")
	reslut = comma_separation.search(line, pos)
	
	parameters = []
	paramList = ParameterList(parameters, def_len)

	# the macro parameter list needs to start right after the macro identifier
	if trimmed[pos] != '(':
		return paramList

	if reslut == None:
		# no parameters --> just a flag
		pass
	else:
		# split string to words and strip leading and trailing whitespace
		paramList.parameters = [word.strip() for word in reslut.group(1).split(",")]
		#print("params: " + str(parameters))

	return paramList

class Macro:
	def __init__(self, dirsearch, line):
		self.name = ""
		self.parameters = []
		self.payload = ""
		self.nameregex = None
		self.flag = False 	# if this macro is just a flag, not a substitution

		if dirsearch == None:
			return

		directive = dirsearch.group(1)
		identifier = dirsearch.group(2)

		if directive == "" or identifier == "":
			#error(row, "Invalid macro directive")
			return None

		self.name = identifier
		self.nameregex = re.compile(r"(\W|^)+(?P<name>" + self.name + r")(\W|$)+")
		self.parameters = getParameterList(dirsearch.group(0), line).parameters
		self.payload = getPayload(dirsearch, line, len(self.parameters))

	def __str__(self):
		return "{" + str(self.name) + ", " + str(self.parameters) + ", '" + str(self.payload) + "'}"

	def __repr__(self):
		return str(self)

	def expand(self, match):
		# first we try to find the given arguments from the matched line, if needed
		# after that we find StringPositions from the payload
		# then we substitute each parameter match in the payload (not inside strings)
		start = match.start('name')
		end = match.end('name')
		identifier = match.group('name')

		#print("MATCH1: " + match.group(1))

		subs = Substitution(match.group('name'), start, end) 
		subs.string = ""
		subs.start = start
						
		if self.parameters:
			c = readchar(match.string, end)

			if not c or c != '(' and self.flag == False:
				errors.add(None, "No parameters for " + self.name)
				return False

			args = parseArgumentList(end, match.string)
			subs.end = end + args.length 

			#print("namematch: " + str(args.arr))

			replacement = self.payload
			strings = scanForStrings(replacement)

			if len(args.arr) != len(self.parameters):
				errors.add(None, "Invalid parameters")
				return None

			for i, p in enumerate(self.parameters):
				reg = re.compile(r"(\W|^)+(?P<name>" + p + r")(\W|$)+")

				while True:
					hits = 0
					namematch = reg.finditer(replacement)

					for n in namematch:
						if checkIfInsideString(n.start('name'), strings):
							continue

						replacement = n.string[:n.start('name')] + args.arr[i] + n.string[n.end('name'):]
						hits += 1
						break
					
					if hits == 0:
						break

			subs.string = replacement

		else:
			subs.string = self.payload

		return subs

