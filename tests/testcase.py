import sys
from processor import *
import abc

class Test(object):

	def __init__(self):
		self.__metaclass__ = abc.ABCMeta
		self.name = self.__class__.__name__
		self.sourcefile = ""
		self.setup()

	@abc.abstractmethod
	def apply(self):
		args = self.getDefaultArgs()
		return self.compareExpected(args)

	@abc.abstractmethod
	def setup(self):
		"""Setup the the test, called once on creation"""
		return

	def getDefaultArgs(self):
		args = Argument
		args.input = self.sourcefile
		args.output = args.input + ".out"
		args.verbose = True
		args.wait_on_error = False
		args.dumb_debug = False
		args.cull = False
		args.minify = False
		args.nomacros = False
		args.anticrap = False
		args.flags = ""
		return args

	def compareExpected(self, args):
		proc = Processor(args)

		expected_path = args.input + ".expected"

		proc.process()
		
		f = open(args.output, mode='r')
		e = open(expected_path, mode='r')

		while (True):
			line1 = f.readline()
			line2 = e.readline()

			if line1 != line2:
				sys.stdout.write("  in %s:\n  Expected:\t%s" % (expected_path, line2))
				sys.stdout.write("  Got:\t\t" + line1)
				return False

			# each line has \n, so EOF is ''
			if line1 == '':
				break

		e.close()
		f.close()

		return True

class Argument(object):
	show_report = False
	def __init__(self):
		self.show_report = False


