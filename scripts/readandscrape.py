import urllib
import json
import unicodedata

with open('read-this.txt') as f:
    content = f.readlines()

kanji_list = []
hiragana_list = []
eng_list2 = []

print("Starting script...")

progress_no = 1

for line_word in content:
	print("Starting word " + str(progress_no) + " of " + (len(content) + 1))
	from urllib.request import urlopen
	query = line_word
	#page = urlopen("http://jisho.org/api/v1/search/words?keyword=%23common&page=" + str(page_num))
	page = urlopen("https://jisho.org/api/v1/search/words?keyword=" + urllib.parse.quote(query, encoding='utf-8') + "&page=" + str(1))
	#Search Japanese word: "https://jisho.org/api/v1/search/words?keyword=家&page="
	#Search tags: http://jisho.org/api/v1/search/words?keyword=%23jlpt-n1&page=
	#Search common: "http://jisho.org/api/v1/search/words?keyword=%23common&page="
	json_data = json.load(page)

	#python2
	#web_page = str("http://jisho.org/api/v1/search/words?keyword=%23jlpt-n1&page=" + str(page_no))
	#page = urllib2.urlopen(web_page)
	#json_data = json.load(page)

	words = json_data['data'][0]

	if "Usually written using kana alone" in words['senses'][0]['tags']:
		kanji = ""
		kanji_list.append(kanji)
	elif 'word' in words['japanese'][0]:
		kanji = words['japanese'][0]['word']
		kanji_list.append(kanji)
	else:
		kanji = ""
		kanji_list.append(kanji)

	#print(words['japanese'][0]['reading'])
	hiragana = words['japanese'][0]['reading']
	hiragana_list.append(hiragana)

	num = 0
	num3 = 1
	eng_num = 1
	eng_list = []

# While the final english definition of the "english" list is not reached,
# Grab each separate list of definitions, and put them in a list. A list of lists.
# For each element in each list within the list, add a number: 1, 2, 3, etc.
	num3 = 1
	while num < len(words['senses']):
		english = words['senses'][num]['english_definitions']
		word_sense = words['senses'][num]['parts_of_speech']
		word_tags = words['senses'][num]['tags']
		word_info = words['senses'][num]['info']
		#str1 = str(num3) + ". " + str('; '.join(english) + "|")
		str2 = str(', '.join(word_sense)) + ":|"
		str3 = str(', '.join(word_sense))
		if not word_tags and not word_info:
			tags_str = ""
			info_str = ""
			str1 = str(num3) + ". " + str('; '.join(english) + "|")
		elif not word_tags and word_info:
			tags_str = ""
			info_str = " " + "(" + str(', '.join(word_info)) + ")"
			str1 = str(num3) + ". " + str('; '.join(english) + info_str + "|")
		elif word_tags and not word_info:
			tags_str = " " + "(" + str(', '.join(word_tags)) + ")"
			info_str = ""
			str1 = str(num3) + ". " + str('; '.join(english) + tags_str + "|")
		else: 
			tags_str = " " + "(" + str(', '.join(word_tags)) + ")"
			info_str = " " + "(" + str(', '.join(word_info)) + ")"
			str1 = str(num3) + ". " + str('; '.join(english) + tags_str + info_str + "|")
		if "Place" in word_sense or "Archaism" in word_tags:
			pass
		elif num == 0:
			eng_list.append(str2 + str1)
			num3 += 1
		elif not words['senses'][num]['parts_of_speech']:
			eng_list.append(str1)
			num3 += 1
		else:
			eng_list.append("|" + str2 + str1)
			num3 += 1
		num += 1
			
	eng_list2.append(eng_list)
	progress_no += 1


filename = "read_it.txt"

num2 = 0
while num2 < len(kanji_list):
	if kanji_list[num2] != "":
		print(kanji_list[num2], end = "	", file = open(filename, "a"))
	print(hiragana_list[num2], end = "	", file = open(filename, "a"))

	for defs in eng_list2[num2][:-1]:
		print(defs, end = "", file = open(filename, "a"))
	print(eng_list2[num2][-1][0:-1], file = open(filename, "a"))
	num2 += 1