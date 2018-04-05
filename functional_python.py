### clist
# Takes an arbitrary number of inputs and creates a list of them

def clist(*args):
	arg_list = list(args)
	return arg_list


### add
# Takes an arbitrary number of arguments and adds them

from functools import reduce
def add(*args):
	return reduce((lambda x,y: x+y), args)


### compose
# Takes two functions and returns their composition

def compose(f1, f2):
	return lambda *args: f1(f2(*args))


### compose with var args
# Takes an arbitrary number of functions and returns their composition

def compose2(*args):
	return reduce(compose, args)


### transpose
# Transposes matrices (lists of lists)

#


