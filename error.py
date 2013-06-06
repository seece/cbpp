import sys

class Message:
	def __init__(self, row, message):
		self.row = row
		self.message = message

	def toString(self):
		if (self.row):
			return str(self.row) + ": " + self.message
		else:
			return self.message

class ErrorLog:
	def __init__(self):
		self.log = []
		self.emit = True # print to console on add 
		self.halt = False # quit when add is called

	def add(self, row, message):
		msg = Message(row, message)
		self.log.append(msg)
		if self.emit:
			print(msg.toString())
			
		if self.halt:
			sys.exit(msg.message)
	
	def getLog(self):
		return self.log
	
	def count(self):
		return len(self.log)

	def __iter__(self):
		return iter(self.log)

infos = ErrorLog()
errors = ErrorLog()
warnings = ErrorLog()




