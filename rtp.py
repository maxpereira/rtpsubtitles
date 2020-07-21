import re
import requests
import sys
from bs4 import BeautifulSoup

startIndex = int(sys.argv[1])
endIndex = int(sys.argv[2])
outFile = sys.argv[3]

while startIndex <= endIndex:
	# Set up BS4
	req = requests.get('https://www.rtp.pt/play/p'+str(startIndex)+'/')
	bs = BeautifulSoup(req.text, 'html.parser')

	# File output for debugging
	with open("debug", "a") as deb:
		deb.write(req.text)

	vodString = str(startIndex)+": "

	# Check for invalid
	invalid_vod = bs.find(class_='vod-no-result')
	if invalid_vod:
		vodString = vodString + "Invalid VOD."
		print(vodString)

		with open(outFile, "a") as outp:
			outp.write(vodString+'\n')

		startIndex = startIndex+1
	else:
		# Get program title
		try:
			try:
				# Standard title
				program_title = bs.find(class_='h3').find_all('a')
				vodString = vodString + program_title[0].contents[0].strip() + " - "
			except:
				# Palco title
				program_title = bs.find(class_='h3')
				vodString = vodString + program_title.contents[0].strip() + " - "
		except:
			# Zigzag title
			program_title = bs.find('h1')
			vodString = vodString + program_title.contents[0].strip() + " - "

		# Get content air date
		date_check = req.text.find('content_date: ')
		if (date_check != -1):
			air_date = req.text[date_check+15:date_check+25]
			vodString = vodString + air_date + " - "

		# Look for caption link in page source
		if (req.text.find('vtt: ') != -1):
			# Has captions
			vodString = vodString + "CC Available"
		else:
			# Does not have captions
			vodString = vodString + "NO Captions"

		print(vodString)
		with open(outFile, "a") as outp:
			outp.write(vodString+'\n')

		startIndex = startIndex+1
