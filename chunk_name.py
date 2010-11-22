def getchunkname(x, y):
	def base36encode(number):
		sign = ''
		if not isinstance(number, (int, long)):
			raise TypeError('number must be an integer')
		if number < 0:
			#raise ValueError('number must be positive')
			sign = '-'
			number = number * -1

		alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'

		base36 = ''
		while number:
			number, i = divmod(number, 36)
			base36 = alphabet[i] + base36

		return sign + base36 or sign + alphabet[0]

	chunk_x = -13
	chunk_y = 44
		
	filename = base36encode(divmod(chunk_x, 64)[1])  + "\\" + base36encode(divmod(chunk_y, 64)[1]) + "\\c." + base36encode(chunk_x) + "." + base36encode(chunk_y) + ".dat"

	return filename