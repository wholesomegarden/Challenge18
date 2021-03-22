# Challenge18Service.py
# from app import Service
# from ctparse import ctparemidrse
# from datetime import datetime
from bs4 import BeautifulSoup
import requests

from dateparser.search import search_dates

import time
import datetime
import re

import emoji

from threading import Thread
import traceback
from pprint import pprint as pp

import C18Tasks


known = {"morning": "at 08:00", "afternoon": "at 16:00", "evening": "at 18:00",
		 "in in": "in", "at at": "at", "בבוקר": "08:00", "בצהריים": "12:00", "בערב": "18:00"}
days = "Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday".split(",")
cFormat = {"today": -1, "upcoming": {}}


# class Challenge18Service(Service):


class Challenge18Service():
	id = "Challenge18"
	name = "🙏🌍 Challenge18 🐋🌸 "
	welcome = "*Welcome to 🙏🌍 Challenge18 🐋🌸* \n*שלחו* הודעה ואנחנו כבר נזכיר לכם :)"
	help = "Challenge18 help message"
	shortDescription = "Get your Challenge18 as whatsapp messages!"
	imageurl = "https://i.imgur.com/YdXGl4K.jpg"

	share = None

	addMasters = ["972547932000", "972559721123"]

	# examples = {"example1":{"text":"","thumbnail":None, "answer":"This is awesome in 5 seconds"}, "example2":{"text":"","thumbnail":None, "answer":"להתקשר לברוך מחר בבוקר"}}
	examples = {}

	emojiValues = {1: "@🧡❤️💛💚💙💜🖤🤍🤎💔❣️💕💞💓💗💖💘💝💐🌷🌹🥀🌺🌸🌼🌻🪴🎍🍀☘️🌱🌿🌴🎋🍃🌳🌲🎄🌵",
				   2: "🍒",
				   3: "🌎🌍🌏🌐⚽👂🏃🏃‍♀️👟💸💵💴💶💷💰💳💎💲🤑📱🤳📲📞☎️📴📳📵💡🏐🏀🏈⚾🥎🎾🏉🎱🏓🥍🏏⛹️‍♀️⛹️🏌️‍♀️🏌️🥥🐜",
				   18: "🤹‍♀️🤹‍♂️🥇⌛",
				   10: "🎥",
				   17: "️👣",
				   180: "🕉️"}

	push = C18Tasks.international
	debug = False
	simulation = False

	def __init__(self, db, api):
		Challenge18Service.share = self
		self.db = db
		self.api = api
		# if "upcoming" not in self.db or "dict" not in str(type(self.db["upcoming"])):
		# 	self.db["upcoming"] = {}
		# if "users" not in self.db:
		# 	self.db["users"] = {}

		self.id = Challenge18Service.id
		self.name = Challenge18Service.name
		self.welcome = Challenge18Service.welcome
		self.imageurl = Challenge18Service.imageurl
		# self.emojiValues = Challenge18Service.emojiValues
		# self.help = Challenge18Service.help
		self.managePush()

	def managePush(self):
		p = Thread(target=self.managePushAsync, args=[None])
		p.start()

	def managePushAsync(self, data):
		needsBackup = False
		while "challenges" not in self.db:
			time.sleep(1)
		print("##################################")
		print("##################################")
		print("##################################")
		print("MANAGING PUSH FOR C18")
		lastHour = 60 * 60
		while(True):
			simCounter = 0
			while self.simulation:
				if simCounter < 10:
					simCounter += 1
					time.sleep(0.1)
					print("SIMULATION")
				else:
					time.sleep(1)
			for ch in self.db["challenges"]:
				challenge = self.db["challenges"][ch]
				if "upcoming" not in challenge:
					challenge["upcoming"] = {}

				sent = []
				for up in challenge["upcoming"]:
					# print("UP",up)

					timeDiff = time.time() - search_dates(up)[0][1].timestamp()
					passedTime = timeDiff > 0 and timeDiff < lastHour
					if passedTime:
						try:
							day = challenge["today"]
							if day in self.push and up in self.push[day]:
								content = self.push[day][up]
								if content is not None:
									content = content.replace(
										"DDD", str(day)).replace("TTT", up)
									print(
										"#################### SENDING PUSH TO C18", ch, "DAY", day, "time", up)
									sent.append(up)
									# send to user
									self.api.send(
										ch, content, autoPreview=True)
									needsBackup = True
						except:
							traceback.print_exc()
				for up in sent:
					challenge["upcoming"].pop(up)
				# challenge["today"] += 1

			time.sleep(5)
			if needsBackup:
				self.backup()
				needsBackup = False

	def go(self):
		resetLast2000 = False
		while "challenges" not in self.db:
			print("C18 waiting for db")
			time.sleep(2)
		if "last2000" not in self.db or resetLast2000:
			self.db["last2000"] = 0
			# self.backup()
			print("22222222222222222222222222222222222222222222000")
		while(True):
			# if "upcoming" not in self.db or "0dict" not in str(type(self.db["upcoming"])):
			# 	self.db["upcoming"] = {}
			if "users" not in self.db:
				self.db["users"] = {}

			''' UPDATE CHALLENGE DAYS '''
			''' SEND DAYLIES '''
			''' USER engagment '''

			''' check time after 20:00 '''
			dayly = 60 * 60 * 23
			# dayly = 60*60*13
			# dayly = 60
			atTime = "19:30"
			# passed2000 = time.time() - search_dates("20:00")[0][1].timestamp() > 0
			# print("C18",time.time(),"\nc18",search_dates(atTime)[0][1].timestamp(),"\n",self.db["last2000"])
			passed2000 = time.time() - \
				search_dates(atTime)[0][1].timestamp() > 0
			try:
				# print(passed2000, time.time() ,"\n", self.db["last2000"] ,"\n", dayly)
				if passed2000 and time.time() - self.db["last2000"] > dayly:
					self.db["last2000"] = time.time()
					for challenge in self.db["challenges"]:
						self.db["challenges"][challenge]["today"] += 1
						# if self.db["challenges"][challenge]["today"] == 0:
						# 	self.db["challenges"][challenge]["today"] += 1
						day = self.db["challenges"][challenge]["today"]
						if self.debug:
							# send to user
							self.api.send(
								challenge, "CHALLENGE CHANGED TO DAY " + str(day))
						if day in self.push:
							for tm in self.push[day]:
								self.db["challenges"][challenge]["upcoming"][tm] = "_"

						print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", challenge,
							  "DAY: ", self.db["challenges"][challenge]["today"])
					self.backup()
			except:
				traceback.print_exc()
			# passed2000 update day += 1

			# while len(self.db["upcoming"]) > 0:
			# 	key = self.db["upcoming"].pop(0)
			# 	origin, content = item
			# for key in list(self.db["upcoming"].keys()):
			# 	t = self.db["upcoming"][key]
			# 	if time.time()-t > 0:
			# 		userID,remID = key.split("_")
			# 		self.remind(userID, remID)

			#
			#
			#
			time.sleep(3)

	def prepUser(self, user, day):
		if "days" not in self.db["users"][user]:
			self.db["users"][user]["days"] = {}
		if day not in self.db["users"][user]["days"]:
			self.db["users"][user]["days"][day] = 0
		if "score" not in self.db["users"][user]:
			self.db["users"][user]["score"] = 1

	def hasDay(self, msg):
		return False, -1, msg

	def emojiValue(self, char):
		''' get emoji values '''
		''' strip all characters '''

		for k in self.emojiValues:
			if char in self.emojiValues[k]:
				return k
			print(char + " in " + str(self.emojiValues[k]))
		return 1

	def char_is_emoji(self, character):
		return character in emoji.UNICODE_EMOJI

	def getScore(self, msg, max=6):
		''' count hearts and emoji values '''

		# nmsg = ''.join(c for c in msg if c.isprintable())
		# if len(msg) != len(nmsg):
		# 	print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
		# 	print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
		# 	print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
		# 	print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
		# 	print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
		# 	msg = nmsg

		sum = 0
		backmsg = ""
		for char in msg:
			if self.char_is_emoji(char) or char is "@":
				print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC", msg)
				print("x" + char + "x")
				sum += self.emojiValue(char)
				backmsg += char
		return sum, backmsg.replace("@", "❤️")

	def rate(self, group, msg, user):
		challenge = None
		if group in self.db["challenges"]:
			challenge = self.db["challenges"][group]
			day = challenge["today"]
			isDay, d, m = self.hasDay(msg)
			if isDay:
				day = d
				msg = m

			''' max by day '''
			score, backmsg = self.getScore(
				msg.replace(" ", "").replace("❤️", "@"), max=6)
			self.prepUser(user, day)

			''' get score - later check by task'''
			self.db["users"][user]["score"] += score
			self.db["users"][user]["days"][day] += score

			''' for now just thankyou - later add custom message based on score / random '''
			# sendBack = "🙏🌍 *Challenge18* 🐋🌸"+"\n\n*Thank you!* "+user.split("@")[0]+"\n*your current score is now "+str(self.db["users"][user]["score"])+"*"
			sendBack = "🙏🌍 *Challenge18* 🐋🌸" + "\n" + "Day " + \
				str(day) + " - " + backmsg + "\n*Thank you!* " + \
				"\n*your current score is now " + \
				str(self.db["users"][user]["score"]) + "*"

			''' for now send directly to user - later in group '''
			self.api.send(user, sendBack)  # send to user
			# self.api.send(group,sendBack) # send to user

	def process(self, info):
		origin, user, content = None, None, None
		if "origin" in info:
			origin = info["origin"]
		if "user" in info:
			user = info["user"]
		if "content" in info:
			content = info["content"]

		if "users" not in self.db:
			self.db["users"] = {}
		if "challenges" not in self.db:
			self.db["challenges"] = {}

		dbChanged = False

		userID = str(user)
		if userID not in self.db["users"]:
			self.db["users"][userID] = {}
			dbChanged = True
		if origin not in self.db["challenges"]:
			self.db["challenges"][origin] = self.formatChallenge()
			dbChanged = True

		if "day=" in content:
			for m in self.addMasters:
				if user.split("@")[0] in m:
					gotDay = None
					res = re.findall("[-\d]+", content)
					if len(res) > 0:
						try:
							gotDay = int(res[0])
						except:
							traceback.print_exc()
					self.db["challenges"][origin] = self.formatChallenge(
						day=gotDay)
					self.api.send(origin, "CHALLENGE CHANGED TO DAY " + str(self.db["challenges"][origin]["today"]) + "\n" + str(self.db["challenges"][origin]))  # send to user
					dbChanged = True

		elif "sim" == content.lower():
			for m in self.addMasters:
				if user.split("@")[0] in m:
					self.simulation = True
					emptyContent = False
					allDays = True

					currentDay = self.db["challenges"][origin]["today"]
					# send to user
					self.api.send(
						origin, "SIMULATING ALL DAYS OF THE CHALLENGE !!!!!!! READY? GO!")
					for d in self.push:
						self.db["challenges"][origin] = self.formatChallenge(
							day=d)
						self.api.send(origin, "=====================\n(Simulation) DAY " + str(self.db["challenges"][origin]["today"]) + "\n" + str(
							self.db["challenges"][origin]) + "\n\n=====================")  # send to user
						print("_____________________________________")
						print("_____________________________________")
						print("_____________________________________")
						print("DAY ", d)
						time.sleep(.5)
						print(self.push[d].keys())
						if d > -2 or allDays:
							print(str(self.db["challenges"]
									  [origin]["upcoming"]))
							for atTime, v in self.db["challenges"][origin]["upcoming"].items():
								print("_____________________________________")
								print()
								print(d, "AT TIME:::", atTime)
								if not emptyContent:
									self.api.send(origin, "DAY " + str(d) + " " + atTime +
												  "\n\n\n" + str(self.push[d][atTime]), autoPreview=True)
								else:
									self.api.send(
										origin, "DAY " + str(d) + " " + atTime + "\n", autoPreview=True)
								time.sleep(.5)

					self.db["challenges"][origin] = self.formatChallenge(
						day=currentDay)
					self.api.send(origin, "FIN - SIMULATING - BACK TO DAY " + str(
						self.db["challenges"][origin]["today"]) + "\n" + str(self.db["challenges"][origin]))
					self.simulation = False

		else:
			thisDay = self.db["challenges"][origin]["today"]
			if thisDay > 0:
				self.rate(origin, content, userID)
				dbChanged = True
			else:
				print("DONT RATE BEFORE FIRSTDAY", thisDay)
		# user = self.db["users"][userID]

		if dbChanged:
			self.backup()
		# self.api.backup(self.db)

	def backup(self):
		self.api.backup(self.db)
		# self.api.backup({"upcoming":self.db["upcoming"],"users":User.usersToJSONusers(self.db["users"])})

	def formatChallenge(self, day=None):
		if day is None:
			today = datetime.date.today()
			if today == today + datetime.timedelta((0 - today.weekday()) % 7, weeks=0):
				day = today + \
					datetime.timedelta((0 - today.weekday()) % 7, weeks=1)
			else:
				day = today + \
					datetime.timedelta((0 - today.weekday()) % 7, weeks=0)

			day = (0 - today.weekday()) % 7
			if day is 0:
				day = -7
			else:
				day = -1 * day

			day = day - 7

		nc = {"today": day, "upcoming": {}}
		# for k in cFormat:
		# 	nc[k] = cFormat[k]
		#
		# nc["today"] = day
		# if "upcoming" not in nc:
		# 	nc["upcoming"] = {}

		if day in self.push:
			for tm in self.push[day]:
				nc["upcoming"][tm] = "_"

		return nc

	def updateDB(self, db):
		self.db = db

	def nextNextMonday(self):
		return day

	def welcomeUser(self, origin):
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		if "users" not in self.db:
			self.db["users"] = {}
		# if origin not in self.db["users"]:
		# 	self.db["users"][origin] = origin
		# 	self.backup()

		if "challenges" not in self.db:
			self.db["challenges"] = {}

		if origin not in self.db["challenges"]:

			# res = search_dates("next monday 20:00", add_detected_language=True)
			# if res is not None:
			# 	res= res[0][1]
			# else:
			# 	pass
			self.db["challenges"][origin] = self.formatChallenge()
			self.api.send(origin, "CHALLENGE SET TO DAY " + str(
				self.db["challenges"][origin]["today"]) + "\n" + str(self.db["challenges"][origin]))  # send to user
			dbChanged = True
