import re
import requests
import sys

# Get arguments
startIndex = int(sys.argv[1])
endIndex = int(sys.argv[2])
outFile = sys.argv[3]

while startIndex <= endIndex:
	# Request the video page
	req = requests.get('https://www.rtp.pt/play/p'+str(startIndex)+'/')

	# File output for debugging
	with open("debug", "a") as deb:
		deb.write(req.text)

	vodString = str(startIndex)+": "

	# Check for invalid
	invalid_vod = req.text.find('vod-no-result')
	if (invalid_vod != -1):
		vodString = vodString + "Invalid VOD"
		print(vodString)

		with open(outFile, "a") as outp:
			outp.write(vodString+'\n')

		startIndex = startIndex+1
	else:
		# Get content title
		title_check = req.text.find('content_title : ')
		if (title_check != -1):
			titleStr = req.text[title_check+16:]
			stopIndex = titleStr.replace('\"', 'XXX', 1).find('\"')
			vod_title = titleStr[+1:stopIndex-2]
			vodString = vodString + vod_title + " - "
		else:
			# It is a Zig Zag video
			zig_title_check = req.text.find('twitter:title')
			if (zig_title_check != -1):
				zigStr = req.text[zig_title_check+23:]
				zigStopIndex = zigStr.replace('\"', 'XXX', 1).find('\"')
				zig_title = zigStr[+1:zigStopIndex-2]
				vodString = vodString + zig_title + " - Zig Zag - "

		# Get content type
		type_check = req.text.find('content_type : ')
		if (type_check != -1):
			vod_type = req.text[type_check+16:type_check+21]
			vodString = vodString + vod_type + " - "

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
