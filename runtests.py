import sys
from colorama import init, deinit # a third party library
from colorama import Fore, Back, Style
from error import infos, errors, warnings
import tests.basic
import tests.advanced

class MockStdOut(object):
	def __init__(self, textlist):
		self.textlist = textlist
	def write(self, string):
		self.textlist.append(string);

all_tests = []

all_tests += tests.basic.testlist
all_tests += tests.advanced.testlist

failed = []

passed = 0

init()

for t in all_tests:
	real_stdout = sys.stdout

	infos.log = []
	warnings.log = []
	errors.log = []

	infos.emit = False
	warnings.emit = False
	errors.emit = False
	test = t()

	if test.apply():
		sys.stdout.write(Fore.GREEN + "OK" + Fore.RESET + "\t")
		passed += 1
	else:
		#output the test log only on failure
		for msg in infos.log:
			print(msg.toString())
		for msg in warnings.log:
			print(msg.toString())
		for msg in errors.log:
			print(msg.toString())

		failed.append(test.name)
		sys.stdout.write(Fore.RED + "FAIL" + Fore.RESET + "\t")

	sys.stdout.write(test.name + "\n")

print("Tests passed: " + str(passed) + " / " + str(len(all_tests)))
print("Failed tests: " + str(failed) )

deinit()
