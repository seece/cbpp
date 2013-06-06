class ArgumentList:
	#length = 0  # the length of the original argument list in characters
	#arr = [] 	# array of argument strings
	def __init__(self, length, arr):
		self.length = length
		self.arr = arr 

class StringPos:
	start = 0
	end = 0
	
	def __init__(self, pstart, pend):
		self.start = pstart
		self.end = pend
	
	def isInside(self, pos):
		if pos >= self.start and pos <= self.end:
			return True
		return False

	def __str__(self):
		return toString(self)

	def toString(self):
		return "StringPos{"+str(self.start)+", "+str(self.end)+"}"

def readchar(string, i):
	if i >= len(string) or i < 0:
		return False

	return string[i]

def stripComments(line):
	length = len(line)
	lastchar = ""
	instring = False

	# iterate line from right to left
	for i, c in enumerate(reversed(line)):
		if instring and c!='"':
			continue

		if c=='"':
			instring = not instring # negation
			continue	

		# if we hit a comment character outside a string
		if (lastchar == "/" and c == "/") or c == "'":
			return line[:(length-i-1)]	+ "\n"
		 
		lastchar = c
	
	return line

# the comment starting position in characters from the beginning of the string
# returns None if no comments are found
def getCommentStart(line):
	stripped = stripComments(line)

	if len(stripped) == len(line):
		return None

	return len(stripped)

def checkIfInsideComment(line, pos):
	start = getCommentStart(line)

	if start == None:
		return False

	if pos >= start:
		return True

	return False


# returns an ArgumentList object, on error None
# start_pos should be the position of the first paren
def parseArgumentList(start_pos, line):
	trimmed = stripComments(line)
	#def_len = len(dirsearch.group(0))
	#parameters = trimmed[def_len:]

	args = ArgumentList(-1, [])

	# find each argument separated by a comma 
	pos = start_pos 
	paren_depth = 0
	current_phrase = ""

	while True:
		c = trimmed[pos]
		paren = False

		if c == '(':
			paren_depth += 1
			paren = True
		if c == ')':
			paren_depth -= 1
			paren = True

		if c == ',' and paren_depth == 1:
			args.arr.append(current_phrase)
			current_phrase = ""
		else:
			# only add the character to the string if it't not the closing paren of the macro call
			if pos != start_pos and not (paren and paren_depth == 0):
				current_phrase += c
		
		if paren_depth == 0:
			args.arr.append(current_phrase)
			break

		pos += 1

		if pos >= len(trimmed):
			#error(-1, "Invalid macro parameters") # TODO fix line number (global state?)
			return False

	args.length = pos - start_pos + 1
	#print("MMAKRO: " + parameters + "\n")
	return args

def checkIfInsideString(string_start, strings):
	for s in strings:
		if s.isInside(string_start):
			return True
	return False

def scanForStrings(line):
	strings = []
	string_start_pos = 0
	instring = False

	for i, c in enumerate(line):
		if c == '"':
			if instring:
				sp = StringPos(string_start_pos, i)
				strings.append(sp)			
				instring = False
			else:
				instring = True
				string_start_pos = i

	return strings

def waitForEnter():
	input("Press Enter to continue...")
	return

def commentLine(line):
	return "// " + line

'''Inserts a string in the middle of another string'''	
def strInsert(line, start, end, substitution):
	return line[:start] + substitution + line[end:]


