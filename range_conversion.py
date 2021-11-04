def str_to_num(string):
	number = 0
	numbers = []

	for c in string[::-1]:
		numbers.append(ord(c)-97)

	for i, n in zip(numbers, range(len(numbers))):
		number += i*(26**n)

	return number

def num_to_str(number, padding):
	lst = []
	while number != 0:
		lst.append(chr((number % 26) + 97))
		number //=26

	return ''.join(lst[::-1]).rjust(padding, 'a')
