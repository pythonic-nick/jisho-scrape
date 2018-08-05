import random

with open('/Users/Nick/Google_Drive/python/jisho_scrape/common-scrape-output.txt') as f:
	content = f.readlines()

shuffle_filename = "common-all-output-shuffle.txt"

shuffled_list = random.sample(content, len(content))

for words in shuffled_list:
	print(words, end = "", file = open(shuffle_filename, "a"))