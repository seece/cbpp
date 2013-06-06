import re
from util import *
from operation import Operation, OperationResult

class Replacement:
	def __init__(self, regex, substitution):
		self.regex = regex
		self.substitution = substitution

class MinifyOperation(Operation):
	def __init__(self):
		self.inMultilineComment = False
		pass

	def apply(self, line, state):
		result = OperationResult(line, False)

		if not state.args.minify:
			return result	

		l = stripComments(line)
		strings = scanForStrings(l)
		commentStart = len(l)

		stringRegex = r'(("[^"]+")|(|[^"]*?)([^\s]*?))?'
		comments = r'(?P<comment>(|(\'|//)*$))'

		def string(s):
			if not s:
				return ""
			return s
		
		def replace(m, group):
			if checkIfInsideString(m.start(group), strings):
				return string(m.group(0)) 
			return string(m.group(1)) + string(m.group(group))
		
		ops = []
		ops.append(Replacement(re.compile(r'' + stringRegex + '\s*(?P<op>[=+\-*/\><,\^]{1,2})\s*'), lambda m: replace(m, "op")))
		ops.append(Replacement(re.compile(r'' + stringRegex + r'(?<=\D)(0)(?P<digit>\.\d+)'), lambda m: replace(m, "digit") ))

		#l = l.lstrip("\t")

		for o in ops:
			l = o.regex.sub(o.substitution, l)
				
		l = l.rstrip("\r\n")
		result.line = strInsert(result.line, 0, commentStart-1, l)

		return result

