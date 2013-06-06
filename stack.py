
class Stack:
	def __init__(self):
		self.arr = []

	def push(self, obj):
		self.arr.append(obj)

	def pop(self):
		return self.arr.pop()

	def top(self):
		return self.arr[-1]

	def clear(self):
		self.arr = []

	def size(self):
		return len(self.arr)
		
	def isEmpty(self):
		if len(self.arr) == 0:
			return True
		else:
			return False

	def contains(self, obj):
		for o in self.arr:
			if o == obj:
				return True

		return False
