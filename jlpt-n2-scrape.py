import urllib
import json

page_num = 1
final_num = 91

# These lists will populate with kanji, hiragana, and English definitions, and will
# be printed as flashcards in a .txt file at the end.
kanji_list = []
hiragana_list = []
parent_eng_list = []

# By doing <= 1000 (final_num), this will scrape 20,000 commonly-used Japanese words (20 words each page).
# Any more than this will cause strange errors with duplicates. May be an API issue.
while page_num <= final_num:
	print("Starting page " + str(page_num) + " of " + str(final_num) + ".")
	# Go to jisho.org and look through words with "common" as a tag.
	from urllib.request import urlopen
	page = urlopen("http://jisho.org/api/v1/search/words?keyword=%23jlpt-n2&page=" + str(page_num))
	json_data = json.load(page)
	word_data = json_data['data']

	# Grab the Japanese word (in Kanji) and add it to the kanji list.
	# If there's no kanji for it, Kanji is an empty string and still added to the list.
	for words in word_data:
		# Make kanji and empty string (i.e. don't include it) if
		# "Usually written using kana alone" is a tag.
		if "Usually written using kana alone" in words['senses'][0]['tags']:
			kanji = ""
			kanji_list.append(kanji)
		elif 'word' in words['japanese'][0]:
			kanji = words['japanese'][0]['word']
			kanji_list.append(kanji)
		else:
			kanji = ""
			kanji_list.append(kanji)

		# Grab the hiragana and add it to the hiragana list.
		# Sometimes some words don't have hiragana:
		# "No hiragana found" string is added to the list.
		if 'reading' in words['japanese'][0]:
			hiragana = words['japanese'][0]['reading']
			hiragana_list.append(hiragana)
		else:
			hiragana = "No hiragana found"
			hiragana_list.append(hiragana)

		num = 0 # This is the number used to iterate through the list of English definitions.
		num3 = 1 # This is the number the flashcard user sees for English definitions.
		eng_list = []

# While the final english definition of the "english" list is not reached,
# Grab each separate list of definitions, and put them in a list. A list of lists.
# For each element in each list within the list, add a number: 1, 2, 3, etc.
		num3 = 1
		while num != len(words['senses']):
			english = words['senses'][num]['english_definitions']
			word_sense = words['senses'][num]['parts_of_speech']
			word_tags = words['senses'][num]['tags']
			word_info = words['senses'][num]['info']
			str2 = str(', '.join(word_sense)) + ":|"
			str3 = str(', '.join(word_sense))
			
			# Working out what information the English definition has stored with it in the API.
			# Then, neatly printing only the information relevant to that definition.
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
			
			# Don't print definitions with the "Place" tag:
			# So many pointless/redundant English definitions have the "Place" tag.
			# Don't print definitions with the "Archaism" tag:
			# Many archaic words have no real use in modern Japanese, and serve only to confuse new learners.
			# Each definiton is added to the English definition list with the associated info.
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
		
		# Add the list of English definitions for the single word to the parent list
		# containing lists of definitions for all words on the page. It's a list of lists.
		parent_eng_list.append(eng_list)
	page_num += 1

filename = "common-scrape-output.txt" # The output file name.

# Print out Kanji + TAB + hiragana + TAB + English definition into a .txt file.
# Each word is on a separate line.
num2 = 0
while num2 < len(kanji_list):
	if kanji_list[num2] != "":
		print(kanji_list[num2], end = "	", file = open(filename, "a"))
	print(hiragana_list[num2], end = "	", file = open(filename, "a"))

	for defs in parent_eng_list[num2][:-1]:
		print(defs, end = "", file = open(filename, "a"))
	print(parent_eng_list[num2][-1][0:-1], file = open(filename, "a"))
	num2 += 1