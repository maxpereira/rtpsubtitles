import re
import requests
from bs4 import BeautifulSoup

startIndex = 0
endIndex = 7500
while startIndex <= endIndex:
	# Set up BS4
	req = requests.get('https://www.rtp.pt/play/p'+str(startIndex)+'/')
	bs = BeautifulSoup(req.text, 'html.parser')

	vodString = str(startIndex)+": "

	# Check for invalid
	invalid_vod = bs.find(class_='vod-no-result')
	if invalid_vod:
		vodString = vodString + "Invalid VOD."
		print(vodString)

		with open("output.txt", "a") as outp:
			outp.write(vodString+'\n')
		startIndex = startIndex+1
	else:
		file = open('out','w')
		file.write(req.text)
		file.close()

		file2 = open('out','r')

		capUrl = ""

		pat = "vtt: "
		for line in file2:
			if re.search(pat,line):
				capUrl = line

		# Get program title
		try:
			try:
				program_title = bs.find(class_='h3').find_all('a')
				vodString = vodString + program_title[0].contents[0] + " - "
			except:
				program_title = bs.find(class_='h3')
				vodString = vodString + program_title.contents[0] + " - "
		except:
			program_title = bs.find('h1')
			vodString = vodString + program_title.contents[0] + " - "

		if not capUrl == "":
			vodString = vodString + "CC Available."
		else:
			vodString = vodString + "NO Captions."
		print(vodString)
		with open("output.txt", "a") as outp:
			outp.write(vodString+'\n')

		startIndex = startIndex+1
