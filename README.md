# cbpp
A CoolBasic preprocessor.

## Features

* C-like macro flags and conditional compilation
* recursive macro expansion
* useless debugging features (```#pragma dumbdebug```)

## Installation
Requires Python 3.x to run, 3.3 recommended.

0. Install Python.
1. Extract (the hacked editor & compilation scripts)[1] to your CoolBasic directory. 
2. Clone this repository to IDE/cbpp, so cbpp.py can be located at IDE/cbpp/cbpp.py.
3. Add your python executable location to IDE/pythonpath (the file needs to be created). The file has to contain just one line: the full name of the python exe, e.g. C:\Python33\python.exe.

You can now compile your source code as usual from the CoolBasic editor.

## Usage

### Conditional compilation
	#define BANANA
	#ifdef BANANA
		print "banaani lienee m‰‰ritelty"
	#endif
	
	#ifndef BANANA
		print "no fruit"
	#else
		print "yummy"
	#endif
	
### Macro expansion
	#define SQUARE(_a) (_a * _a)
	
	print "5^2 = " + SQUARE(5)

Please note that the macro parameter names shouldn't occur in the macro expansion, in other words, this is illegal:
	#define TUPLAT(luku) (luku+luku)
	
	luku = 10
	luku2 = TUPLAT(luku) // stupid preprocessor gets stuck in an infinite loop
	
	
[1]: http://lofibucket.com/download/cbpp_editor_01.zip