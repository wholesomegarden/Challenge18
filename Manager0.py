# Manager.py
from User import User
from Reminder import Reminder
from Conv import Conv
from app import Service
# from ctparse import ctparemidrse
# from datetime import datetime
from dateparser.search import search_dates

import time
import datetime
import re

from threading import Thread

known = {"Morning":"at 08:00", "evening":"at 18:00", "in in":"in","at at":"at", "בבוקר":"08:00"}
days = "Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday".split(",")

class Manager(Service):
	users = {}
	upcoming = {}
	init = False

	def getDB():
		return {"users":users,"upcoming":upcoming}

	def setDB(db):
		Manager.upcoming = db["upcoming"]
		Manager.users = db["users"]

	def asyncRoll():
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		t = Thread(target = Manager.rollUpcoming,args = [None,])
		t.start()

	def rollUpcoming(data):
		"!!!!!!!!!!!!!!!!!!!!!!@@@@@@@@@@@@@@@@@@@@@@@"
		while(True):
			for key in list(Manager.upcoming.keys()):
				t = Manager.upcoming[key]
				if time.time()-t > 0:
					userID,remID = key.split("_")
					Manager.send(userID, remID)
			time.sleep(1)


	# shared = None
	#
	# def __init__(self):
	#     shared = sel
	#     pass #load from back

	def go(driver = None):
		## LOAD FROM DAL
		Manager.users = {}
		Manager.upcoming = {}
		Manager.init = True
		Manager.asyncRoll()
		Manager.driver = driver

	def process(userID, message):
		print(Manager.init,"!!!!!!!!!!!!")
		if not Manager.init:
			Manager.go()

		userID = str(userID)
		if userID not in Manager.users:

			user = User(userID)
			Manager.users[userID] = user

			user.conv.manager("WELCOME "+userID)
			Manager.actuallySend(userID, "WELCOME "+userID)

		user = Manager.users[userID]
		user.conv.human(message)
		timestr = ""

		if not user.conv.ongoing:
		# check for commands
			print("AAAAAAAAAAAAAAAAAA")
			m, t, timestr = Manager.parseMsg(message)
			if t is None:
				user.conv.manager("When to remind you?")
				Manager.actuallySend(userID, "When shall I remind you ?")
				user.conv.ongoing = True
			else:
				Manager.convFinished(user, set = True)

			rem = Manager.newReminder(userID, m, t)



		else:
				print("BBBBBBBBBBBBBBBBBBBBB")
				user.conv.tries += 1
				m, t, timestr = Manager.parseMsg(message)
				## GET LAST REMINDER

				if t is None:
					user.conv.manager("Sorry I didnt understand when  "+ str(user.conv.tries))
					Manager.actuallySend(userID, "Sorry I didn't unserstand when...")

				else:
					rem = user.lastRem
					rem.sendTime = t

					Manager.convFinished(user, set = True)

		if Manager.convFinished(user):
			rem = user.lastRem
			user.conv.manager(" ".join(["THANK YOU! WILL REMIND YOU TO ",rem.message, "at",time.ctime(rem.sendTime)," (",timestr,")"]))
			Manager.actuallySend(userID, " ".join(["THANK YOU! WILL REMIND YOU TO ",rem.message, "at",time.ctime(rem.sendTime)," (",timestr,")"]))

			if rem.sendTime is not None:
				combID = userID+"_"+rem.id
				Manager.upcoming[combID] = rem.sendTime
			else:
				print("XXXXXXXXXXXXXXXXXXXXXXXX", "unhandled")

			Manager.convFinished(user, set = None)
			user.conv.ongoing = False
		else:
			print("***continue conv!!!!!!!!!!!!!!!!!!")


	def convFinished(user, set = -1):
		if set is -1:
			convFin = True
			for key in user.conv.fin:
				if user.conv.fin[key] is None:
					convFin = False
			return convFin
		else:
			for key in user.conv.fin:
				user.conv.fin[key] = set

	def send(userID, remID):
		userID, remID = str(userID), str(remID)
		combID = userID+"_"+remID
		if userID in Manager.users:
			user = Manager.users[userID]
			if remID in user.reminders["unsent"]:
				rem = user.reminders["unsent"][remID]

				if Manager.actuallySend(userID,rem.message):
					if user.markSent(remID):
						if combID in Manager.upcoming:
							Manager.upcoming.pop(combID)
						else:
							print("EEEEEEEEE", "wasn't in upcoming")

					else:
						print("EEEEEEEEE", "could not mark!")

				else:
					print("EEEEEEEEE", "could not send!")



	def actuallySend(userID, message):
		print("TRY SENDING ON WHATSAPP! TO:", userID, "MESSAGE:", message)
		if Manager.driver is not None:
			print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
			print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
			print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
			print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
			print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
			Manager.driver.send_message_to_id(userID, message)
			print("SENT!!!!!!!!!!!!!!!!!!!!!!!!")
			return True

		print("NO WHATSAPP DRIVER")
		return False
		# return False #for errors

	def getRE(key):
		return re.compile(re.escape(key.lower()), re.IGNORECASE)


	def formatKnown(txt):
		for key in known:
			keyRE = Manager.getRE(key)
			changed = keyRE.sub(known[key],txt)
			if txt != changed:
				print("-------CHANGED",txt,"TO",changed)
				txt = changed
		return txt

	def parseMsg(txt, tries = 0):
		print("============================")
		print(txt)
		formatted = Manager.formatKnown(txt)
		timestr = ""
		res = search_dates(formatted, add_detected_language=True)
		when = None
		if res is None:
			return txt, when, timestr
		if True:#try:
			print("######################",formatted)
			print(res)
			date = res[0][1].timestamp()
			timestr = res[0][0]
			lang = res[0][2]
			## remove timestr from reminder

			diff = time.time()-date
			print("DIFF",diff, time.ctime(date))
			if diff > 0 and tries < 3:
				print("RETRY ")
				if tries == 0:
					new = Manager.changeDay(formatted)
				else:
					new = formatted.replace(timestr,"in "+timestr)
				return Manager.parseMsg(new, tries+1 )
			else:
				when = date
		# if True:#except:
		#     print("EEEEEEEEEEEEEEEEEEEEEE res:",res)
		#     return txt, None, ""

		if timestr is not "":
			formatted = txt.replace(timestr,"")
		return formatted, when, timestr

	def changeDay(txt):
		print("CCCCCCCCCCCCC C C C C C C, ",txt,"\n")
		temp = txt + ""
		today = datetime.date.today().strftime("%A")
		currday = days.index(today)
		dates = []
		for d in range(7):
			c = (d+currday+1)%7
			dates.append(days[c])
		print("DATES::::::::::::::::::")
		print(dates)

		kc = 0
		for key in dates:
			kc+=1
			realday = "in "+str(kc)+" day"
			if c>1:
				realday+="s"
			print("DDDDDD ",realday)
			keyRE = Manager.getRE(key)
			changed = keyRE.sub(realday,txt)
			print("TTTTTTTT",changed)
			print
			txt = changed
		if temp != txt:
			print("CHANGED FROM -",temp," TO -",txt)
		else:
			print("NOT CHANGED DAY")
		return txt

	def newReminder(userID, message, when = None):

		user = Manager.users[userID]
		if user is None:
			print("user not found")
			return None

		user.remCount += 1
		remID = str(user.remCount)
		rem = Reminder(remID, userID, message, when)
		user.reminders["unsent"][remID] = rem
		user.lastRem = rem

		return rem
