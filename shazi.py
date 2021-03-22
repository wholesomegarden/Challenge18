#shazi.py
from ShazamAPI import Shazam
from threading import Thread
import traceback

from pydub import AudioSegment

import time
# class Shazi(object):

'''
None-blocking function to get title, artist, and other shazam data from a file
'''
def shazam(mp3path, outDict = None, checkFull = False):
	if outDict is None:
		outDict = {"out":None}
	sT = Thread(target=shazamAsync,args=[[mp3path, outDict, checkFull]])
	sT.start()
	return outDict

def shazamAsync(data, round = 0):
	print('''%%%%%%%%%%% SHAZAMMING %%%%%%%%%%%''')
	print('''%%%%%%%%%%% SHAZAMMING %%%%%%%%%%%''')
	print('''%%%%%%%%%%% SHAZAMMING %%%%%%%%%%%''')
	t = time.time()
	try:
		mp3path, outDict, checkFull = data

		if checkFull:
			mp3_file_content_to_recognize = open(mp3path, 'rb').read()
		else:
			audio = AudioSegment.from_mp3(mp3path)
			mp3_file_content_to_recognize = audio.export(format="mp3").read()
			start = 0
			seconds = 1.2
			length = len(audio)
			if length > 0:
				if length > seconds:
					seconds = seconds
				else:
					seconds = length/1000

			mp3_file_content_to_recognize = mp3_file_content_to_recognize[start*60*1000:int((start+seconds)*60*1000)]


		# shazam = Shazam(mp3_file_content_to_recognize)
		outDict["out"] = next(Shazam(mp3_file_content_to_recognize).recognizeSong())
		# recognize_generator = shazam.recognizeSong()
		# outDict["out"] = next(recognize_generator)
		if outDict is not None:
			firstRes = None
			try:
				print(firstRes)
				firstRes = outDict["out"][1]["track"]
			except:
				print("EEEEE SHAZAM COULD NOT FIND SONG")
				traceback.print_exc()
			if firstRes is not None and "title" in firstRes and "subtitle" in firstRes:
				outDict["title"] = firstRes["title"]
				outDict["artist"] = firstRes["subtitle"]
				print(outDict["title"] + " - " + outDict["artist"])
		print('''%%%%%%%%%%%   DONE!    %%%%%%%%%%%''', "time",time.time()-t)

		# while True:
		# 	print(next(recognize_generator)) # current offset & shazam response to recognize requests1
	except:
		traceback.print_exc()
