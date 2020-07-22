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
	#with open("debug", "a") as deb:
	#	deb.write(req.text)

	lnkString = "<a href='https://www.rtp.pt/play/p" + str(startIndex) + "/'>"
	vodString = str(startIndex) + ": "

	# Check for invalid
	invalid_vod = req.text.find('vod-no-result')
	if (invalid_vod != -1):
		vodString = vodString + "Invalid VOD"
		print(vodString)

		startIndex = startIndex+1
	else:
		# Get content title
		title_check = req.text.find('content_title : ')
		if (title_check != -1):
			titleStr = req.text[title_check+16:]
			titleStr = titleStr.replace('\\\"', 'YY')
			stopIndex = titleStr.replace('\"', 'XXX', 1).find('\"')
			titleStr = titleStr.replace('YY', '\\\"')
			vod_title = titleStr[+1:stopIndex-2]
			vod_title = vod_title.replace('\\', '')
			vodString = vodString + vod_title + " , "
		else:
			# It is a Zig Zag video
			zig_title_check = req.text.find('twitter:title')
			if (zig_title_check != -1):
				zigStr = req.text[zig_title_check+23:]
				zigStopIndex = zigStr.replace('\"', 'XXX', 1).find('\"')
				zig_title = zigStr[+1:zigStopIndex-2]
				vodString = vodString + zig_title + " , Zig Zag , "

		# Get content type
		type_check = req.text.find('content_type : ')
		if (type_check != -1):
			vod_type = req.text[type_check+16:type_check+21]
			vodString = vodString + vod_type + " , "

		# Get content air date
		date_check = req.text.find('content_date: ')
		if (date_check != -1):
			air_date = req.text[date_check+15:date_check+25]
			vodString = vodString + air_date

		# Look for caption link in page source
		if (req.text.find('vtt: ') != -1):
			# Has captions
			with open(outFile+"_CC.html", "a") as outp:
				outp.write(lnkString+vodString+"</a><br>"+'\n')
		else:
			# Does not have captions
			with open(outFile+"_NoCC.html", "a") as outp:
				outp.write(lnkString+vodString+"</a><br>"+'\n')

		print(vodString)

		startIndex = startIndex+1
