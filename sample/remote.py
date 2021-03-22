import json
import os
import sys
import time
from threading import Thread
from ascii import *
import pathlib


def runReminder():
	from webwhatsapi import WhatsAPIDriver

	print("Environment", os.environ)
	try:
		os.environ["SELENIUM"]
	except KeyError:
		print("Please set the environment variable SELENIUM to Selenium URL")
		sys.exit(1)

	from PIL import Image

	from resizeimage import resizeimage

	##Save session on "/firefox_cache/localStorage.json".
	##Create the directory "/firefox_cache", it's on .gitignore
	##The "app" directory is internal to docker, it corresponds to the root of the project.
	##The profile parameter requires a directory not a file.

	from pyzbar.pyzbar import decode
	dir_path = os.path.dirname(os.path.realpath(__file__))

	print(")(AFYN)(ANY*FU(A*UKFA(E*FU*****************************)))")
	print(")(AFYN)(ANY*FU(A*UKFA(E*FU*****************************)))")
	print(")(AFYN)(ANY*FU(A*UKFA(E*FU*****************************)))")
	print(")(AFYN)(ANY*FU(A*UKFA(E*FU*****************************))),",dir_path)
	returned_value = os.system('export PATH="'+dir_path+':$PATH"')  # returns the exit code in unix


	profiledir = os.path.join(".", "firefox_cache")
	if not os.path.exists(profiledir):
		os.makedirs(profiledir)

	driver = WhatsAPIDriver(
		profile=profiledir, client="remote", command_executor=os.environ["SELENIUM"]
	)


	profiledir = os.path.join(".", "firefox_cache")
	if not os.path.exists(profiledir):
		os.makedirs(profiledir)

	driver = WhatsAPIDriver(
		profile=profiledir, client="remote", command_executor=os.environ["SELENIUM"]
	)

	import timg

	obj = timg.Renderer()

	print("Waiting for QR")
	driver.wait_for_login()
	print("Saving session")


	# from qrtools import qrtools
	# from PIL import Image
	# import zbarlight
	# qr = qrtools.QR()

	#
	# from PIL import Image

	# import os
	# import numpy as np
	# import pyboof as pb

	# # pb.init_memmap() #Optional
	#
	# class QR_Extractor:
	#     # Src: github.com/lessthanoptimal/PyBoof/blob/master/examples/qrcode_detect.py
	#     def __init__(self):
	#         self.detector = pb.FactoryFiducial(np.uint8).qrcode()
	#
	#     def extract(self, img_path):
	#         if not os.path.isfile(img_path):
	#             print('File not found:', img_path)
	#             return None
	#         image = pb.load_single_band(img_path, np.uint8)
	#         self.detector.detect(image)
	#         qr_codes = []
	#         for qr in self.detector.detections:
	#             qr_codes.append({
	#                 'text': qr.message,
	#                 'points': qr.bounds.convert_tuple()
	#             })
	#         return qr_codes


	# qr_scanner = QR_Extractor()

	print("AAA")
	c = 0
	s = 60
	status = "NotLoggedIn"
	while status is not "LoggedIn":
		c+=1
		print("status", status)


		# print("Checking qr, status", driver.get_status())

		print("AAAAAAAAAAAAA")
		# img = driver.get_qr("static/img/newQR.png")
		im_path = os.path.join("newQR.png")
		pathlib.Path().absolute()
		os.system("cp newQR.png sample/static/img/newQR.png")

		img = driver.get_qr("newQR.png")
		# from PIL import Image
		print("BBBBBBBBBBBBBBB")
		decoded = decode(Image.open(im_path))
		# print(decoded, "#######################")
		# print(decoded, "#######################")
		# print(decoded, "#######################")
		# print(decoded, "#######################")
		# print(decoded, "#######################")
		# print(decoded, "#######################")
		# print(decoded, "#######################")

		for barcode in decoded:
			print("@@@@@@@@@@@@@@@@@@@")
					# the barcode data is a bytes object so if we want to draw it
			# on our output image we need to convert it to a string first
			barcodeData = barcode.data.decode("utf-8")
			barcodeType = barcode.type
			# draw the barcode data and barcode type on the image
			text = "{} ({})".format(barcodeData, barcodeType)
			print(text)
			print("@@@@@@@@@@@@@@@@@@@")
			printQR(barcodeData)
			print("@@@@@@@@@@@@@@@@@@@X")


		status = driver.get_status()
		# output = qr_scanner.extract(img)
		# print(output,"!!!!!!!!!!!!!!!!WDIOUSICNOIUCJ)(Z*UCINJ)(ZP*DFJYUF)((P*SUD)(UASIDMUJ))")
		# print(qr.decode(img))
		# print(qr.data)

		# print("BBBB2")
		# with open(img, 'r+b') as f:
		#     with Image.open(f) as image:
		#         cover = resizeimage.resize_cover(image, [57, 57])
		#         cover.save(img, image.format)
		# #
		# qr.decode(img)
		# print (qr.data)
		# print(retval,"!!!!!!!!!!!!!!!!!!!")
		#
		# print("CCC",img)
		# obj.load_image_from_file(img)

		# obj.resize(s,s)
		# s-=1
		# print(obj)
		# obj.render(timg.Ansi24HblockMethod)
		# print("DDD",s,s,s,s)
		# time.sleep(10)
		# driver.save_firefox_profile(remove_old=False)
		# time.sleep(3)
		# try:
		#     driver.reload_qr()
		# except:
		#     print("refresh finised")
	print("Bot started")

	while True:
		time.sleep(.71)
		print("Checking for more messages, status", driver.get_status())
		for contact in driver.get_unread():
			for message in contact.messages:
				print(json.dumps(message.get_js_obj(), indent=4))
				sender = message.get_js_obj()["chat"]["contact"]["formattedName"]

				for contact in driver.get_contacts():
					# print("CCCC",contact.get_safe_name() )
					if  sender in contact.get_safe_name():
						chat = contact.get_chat()
						chat.send_message("Hi "+sender+" !!!*"+message+"*")


				print()
				print()
				print(sender)
				print()
				print()
				print("class", message.__class__.__name__)
				print("message", message)
				print("id", message.id)
				print("type", message.type)
				print("timestamp", message.timestamp)
				print("chat_id", message.chat_id)
				print("sender", message.sender)
				print("sender.id", message.sender.id)
				print("sender.safe_name", message.sender.get_safe_name())
				if message.type == "chat":
					print("-- Chat")
					print("safe_content", message.safe_content)
					print("content", message.content)
					# contact.chat.send_message(message.safe_content)
				elif message.type == "image" or message.type == "video":
					print("-- Image or Video")
					print("filename", message.filename)
					print("size", message.size)
					print("mime", message.mime)
					print("caption", message.caption)
					print("client_url", message.client_url)
					message.save_media("./")
				else:
					print("-- Other")



from flask import Flask, render_template
# app = Flask(__name__)
app=Flask(__name__,template_folder='templates')


import os
arr = os.listdir()
for a in arr:
	# print(a)
	pass
# input()

PEOPLE_FOLDER = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/')
def hello_world():

	full_filename = os.path.join(app.config['UPLOAD_FOLDER'], "newQR.png")
	return render_template("index.html", user_image = full_filename)

def flaskRun():
	t = Thread(target=flaskRunAsync,args=[None,])
	t.start()

def flaskRunAsync(data):
	# input()
	print("AAAAAAAAAAAA ASYNC")
	runReminder()

if __name__ == '__main__':
	flaskRun()
	app.run(debug=True, host='0.0.0.0')
