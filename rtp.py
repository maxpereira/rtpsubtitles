import re
import requests
import sys
from bs4 import BeautifulSoup

startIndex = int(sys.argv[1])
endIndex = int(sys.argv[2])

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

		with open("output"+sys.argv[1]+".txt", "a") as outp:
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

		# Look for caption link in page source
		if (req.text.find('vtt: ') != -1):
			# Has captions
			vodString = vodString + "CC Available."
		else:
			# Does not have captions
			vodString = vodString + "NO Captions."

		print(vodString)
		with open("output"+sys.argv[1]+".txt", "a") as outp:
			outp.write(vodString+'\n')

		startIndex = startIndex+1
