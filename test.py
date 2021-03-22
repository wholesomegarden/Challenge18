# test.py
from dateparser.search import search_dates
from ServiceImporter import *
id = "0547772000"

#
# msg = "send message to Omer tomorrow morning "
# Manager.process(id, msg)
#
#

msg = "call omer thursday morning"
Manager.process(id, msg)

export PATH="$HOME/wholesomegarden/WhatsappReminder:$PATH"

#
# import wapy
#
# wapy.init()
# while True:
#     wapy.unread()
#     wapy.response('-wapy', 'text', text='Hello World!')
import os
import time
import json
import os
import sys

from QRMatrix import *

from skimage import data, color
from skimage.transform import rescale, resize, downscale_local_mean
from webwhatsapi import WhatsAPIDriver
from skimage import io

driver = WhatsAPIDriver(username="mkhase")
Manager.go(driver)
# driver.get_status()
img = driver.get_qr("i.png")
print(img)
# time.sleep(4)
QRCode = QRMatrix("decode", img)
print(QRCode.decode())
print("@@@@@@@@@@@@@@@@@@")
print("XXXXXXXX")
# # i = io.imread(img)
# # image = color.rgb2gray(i)
#
# image_rescaled = rescale(image, 0.25, anti_aliasing=False)
# io.imsave(img, image_rescaled)
print("XXXXXXXX")
import timg
obj = timg.Renderer()
obj.load_image_from_file(img)
obj.resize(106,106)
obj.render(timg.Ansi24HblockMethod)
#
#
# for contact in driver.get_contacts():
#     print("CCCC",contact.get_safe_name() )
#     if  "@@@@@@@@@@@@@@@@@@@@@@@@@" in contact.get_safe_name():
#         chat = contact.get_chat()
#         chat.send_message("Hi Jack")

lastm = None
while True:
	time.sleep(.71)
	print("Checking for more messages, status", driver.get_status())
	for contact in driver.get_unread():
		for message in contact.messages:
			lastm = message
			print(json.dumps(message.get_js_obj(), indent=4))
			sender = message.get_js_obj()["chat"]["contact"]["formattedName"]
			for contact in driver.get_contacts():
				# print("CCCC",contact.get_safe_name() )
				if  sender in contact.get_safe_name():
					chat = contact.get_chat()
					chat.send_message("Hi "+sender+" !!!*"+message.content+"*")
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
			print("PROCESSING MESSAGE:",message)
			Manager.process(message.sender.id,message.content)


# 4. In case the QR code expires, you can use the reload_qr function to reload it
# driver.reload_qr()
# driver.view_unread()
# driver.get_all_chats()
# 7. To send a message, get a Contact object, and call the send_message function with the message.
# <Contact Object>.send_message("Hello")
# 8. Sending a message to an ID, whether a contact or not.
# driver.send_message_to_id(id, message)
