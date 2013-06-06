import re
import abc

class OperationResult:
	def __init__(self, line, discard):
		self.line = line
		self.discard = discard 
		self.error = None

class Operation:
	__metaclass__ = abc.ABCMeta
	def __init__(self):
		pass

	@abc.abstractmethod
	def apply(self, line, state):
		pass

