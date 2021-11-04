def get_ranges(start, stop, n, md5):
	start_num = str_to_num(start)
	stop_num = str_to_num(stop)

	division = (stop_num - start_num) / n
	ranges = []

	for i in range(n):
		start_result = num_to_str(round(start_num + division * i), len(start))
		stop_result = num_to_str(round(start_num + division * (i + 1)), len(start))
		
		ranges.append((start_result, stop_result, md5))

	return ranges

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
