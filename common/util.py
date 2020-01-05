
import unicodedata
import re
from dateutil.relativedelta import relativedelta
from datetime import date

def extractAlphanumeric(from_string):
	to_string = ''
	for char in list(from_string):
		# print('{} is {}'.format(char, unicodedata.east_asian_width(char)))
		kind = unicodedata.east_asian_width(char)
		if kind != 'W' and kind != 'A' and kind != 'H':  # 特殊記号、マルチバイト、半角カナを除去
			to_string = to_string + char
	return to_string

def numeric(from_string):
	if '.' in from_string:
		from_string = from_string[:from_string.find('.')]  # 小数点以下は切り捨て
	to_string = ''
	for char in list(from_string):
		kind = unicodedata.east_asian_width(char)
		if kind != 'W' and kind != 'A' and kind != 'H':  # 特殊記号、マルチバイト、半角カナを除去
			if char.isnumeric():
				to_string = to_string + char
	return int(to_string)

def remove_html_symbol(text):
	# HTMLの特殊記号等を指定されたテキストから取り除く
	return text.replace('\xa0','')

def kanji_numeric(strings, last_string):
	count = 0
	data = re.search('[0-9]{1,4}億', strings)
	if data:
		count = count + int(data.group()[:-1]) * 100000000
	data = re.search('[0-9]{1,4}万', strings)
	if data:
		count = count + int(data.group()[:-1]) * 10000
	data = re.search('[0-9]{1,4}' + last_string, strings)
	if data:
		count = count + int(data.group()[:-1])
	return count

if __name__ == '__main__':
	 #西暦2002年11月11日
 	# print(get_age([2002, 11, 11]))
 	print(extract_numeric('170はろーcm'))
