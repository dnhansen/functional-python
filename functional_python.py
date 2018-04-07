###
# Exercises from:
# https://gist.github.com/oskarkv/3168ea3f8d7530ccd94c97c19aafe266
###

from functools import reduce


### clist
# Takes an arbitrary number of inputs and creates a list of them

def clist(*args):
	return list(args)


### add
# Takes an arbitrary number of arguments and adds them

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

def transpose(matrix):
	rows = len(matrix)
	cols = len(matrix[0])
	return [ [matrix[i][j] for i in range(rows) ] for j in range(cols) ]


### partial
# Takes a function and an arbitrary number of arguments, and returns a function
# partially applied to the arguments.

def partial(f, *args):
	partial_args = args
	return lambda *args: f(*(args + partial_args))


### flip
# Takes a function and flips the first and second argument.

def flip(f):
	def f_flip(*args):
		arg_list = clist(*args)		
		arg_list[0], arg_list[1] = arg_list[1], arg_list[0]
		return f(*arg_list)

	return f_flip


### flips
# Takes a function and reverses the arguments to it

def flips(f):
	return lambda *args: f(*reversed(args))


### take
# Takes a number n and a sequence, and returns a list of the first n elements

def take(n, seq):
	return seq[:n]


### drop
# Takes a number n and a sequence, and returns a list with the first n elements removed

def drop(n, seq):
	return seq[n:]


### zip
# Takes an arbitrary number of sequences and zips them

def zip(*seqs):
	return transpose(list(seqs))


### zipmap
# Takes two sequences and creates a dictionary

def zipmap(s1, s2):
	length = len(s1)
	return {s1[i] : s2[i] for i in range(length)}


### interleave
# Takes an arbritrary number of sequences and interleaves them

def interleave(*seqs):
	return add(*zip(*seqs))


### every_pred
# Takes an arbitrary number of predicates and returns true iff all predicates are
# truthy for the argument

def every_pred(*preds):

	def inner_every_pred(arg):
		bools = map(lambda pred: pred(arg), preds)
		print(bools)
		if False not in bools:
			return True
		else:
			return False

	return inner_every_pred


### frequencies
# Takes a sequence and counts how many times the elements appear.

def frequencies(seq):
	dic = {}
	for x in seq:
		if x in dic:
			dic[x] += 1
		else:
			dic[x] = 1

	return dic


### flatten
# Flattens a tree

def flatten(tree):
	flat_list = []
	for x in tree:
		if not type(x) == list:
			flat_list.append(x)
		else:
			flat_list += flatten(x)

	return flat_list


### Partition
# Takes arguments n, step and seq. Takes n elements from seq, wraps them in a list,
# takes a step forward in step steps, then takes another n elements, and so on.

def partition(n, step, seq):
	partitions = []
	length = len(seq)

	for i in range(0, length-n+1, step):
		partitions.append(seq[i:i+n])

	return partitions


### merge_with
# Takes a function and an arbitrary number of dictionaries and merges them,
# combining repeat elements using the given function.

def merge_with(f, *dicts):

	def merge_two(dict1, dict2):
		dict_out = dict(dict1)	# Creates COPY of dict1 to avoid side effects
		for key, val in dict2.items():
			if key in dict_out:
				dict_out[key] = f(dict_out[key], dict2[key])
			else:
				dict_out[key] = dict2[key]
		return dict_out

	return reduce(merge_two, dicts)


### tree_seq
# Takes a function is_branch, a function children and a tree t. Returns a list
# of the nodes of t in depth-first order.

def tree_seq(is_branch, children, t):
	out = [t]

	if is_branch(t):
		for child in children(t):
			out += (tree_seq(is_branch, children, child))

	return out


### memoize
# Takes a function and memoizes it

def memoize(f):

	f.memory = {}

	def new_f(*args):
		if args in f.memory:
			return f.memory[args]
		else:
			out = f(*args)
			f.memory[args] = out
			return out

	return new_f


### group_by
# Takes a function and a sequence and groups the elements by the function.

def group_by(f, seq):
	grouping = {}
	for x in seq:
		val = f(x)
		if val in grouping:
			grouping[val].append(x)
		else:
			grouping[val] = [x]

	return grouping


### update
# Takes a map m, a key k, a function f, and an arbitrary number of additional
# args. Returns a new map with the value of k replaced by f(val, args). If k
# is not in m, creates a new entry.

def update(m, k, f, *args):
	m_new = dict(m)

	if k in m:
		val = m[k]
		m_new[k] = f(val, *args)
	else:
		m_new[k] = f(*args)

	return m_new


### update_in
# Similar to update, but takes a list of keys and updates inside nested maps

def update_in(m, keys, f, *args):
	if not type(keys) == list:
		return update(m, keys, f, *args)
	elif len(keys) == 1:
		return update(m, keys[0], f, *args)
	else:
		m_new = dict(m)
		key0 = keys[0]

		if key0 not in m:
			m_new[key0] = {}
		
		m_new[key0] = update_in(m_new[key0], keys[1:], f, *args)
		return m_new


### balanced
# Takes a string and returns True iff the parentheses in the string are balanced.

def balanced(s):
	parens = list(filter(lambda c: c in '()[]{}', s))

	parens_map = {')': '(',
				  ']': '[',
				  '}': '{'}

	if parens == '':
		return True
	elif len(parens) % 2 != 0:
		return False

	for idx, p in enumerate(parens):
		if p in ')]}':
			if idx == 0:
				return False
			elif parens[idx-1] != parens_map[p]:
				return False
			else:
				del parens[idx-1:idx+1]
				return balanced(''.join(parens))


### map

def map(f, seq):
	out = []
	for x in seq:
		out.append(f(x))
	return out


### filter 

def filter(f, seq):
	out = []
	for x in seq:
		if f(x):
			out.append(x)
	return out


### reduce

def reduce(f, seq):
	out = seq[0]
	for x in seq[1:]:
		out = f(out, x)
	return out