
import argparse
from util import *
import processor

def getParser():
	parser = argparse.ArgumentParser()

	parser.add_argument("input", help="path to the input source file")
	parser.add_argument("output", help="path to the output source file")

	parser.add_argument("--show-report", help="show a detailed report after processing", 
		action="store_true")
	parser.add_argument("-v", "--verbose", help="print additional debug data",
		action="store_true")
	parser.add_argument("--wait-on-error", help="halts and waits for keypress if an error is encountered",
			action="store_true")

	parser.add_argument("--dumb-debug", help="adds setwindow commands before each line to help with debugging",
			action="store_true")
	parser.add_argument("--flags", help="a list of semicolon separated values to use as flag macros")
	parser.add_argument("--cull", help="removes empty rows and comments after processing", action="store_true")
	parser.add_argument("--minify", help="removes unnecessary whitespace", action="store_true")
	parser.add_argument("--anticrap", help="remove the \ and . idiocy", action="store_true")
	parser.add_argument("--nomacros", help="do not expand any macros", action="store_true")
	parser.add_argument("-d", "--filedir", help="file directory")
	return parser

parser = getParser()
args = parser.parse_args()

proc = processor.Processor(args)
proc.process()

