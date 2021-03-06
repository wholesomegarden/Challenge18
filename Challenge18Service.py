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
import random
import json

import emoji

from threading import Thread
import traceback
from pprint import pprint as pp

import C18Tasks

from flask import Flask, render_template, redirect, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

# from Challenge18Manager import Challenge18Manager

from urllib.request import urlopen, Request, quote

known = {"morning": "at 08:00", "afternoon": "at 16:00", "evening": "at 18:00",
		 "in in": "in", "at at": "at", "בבוקר": "08:00", "בצהריים": "12:00", "בערב": "18:00"}
days = "Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday".split(",")
cFormat = {"today": -1, "upcoming": {}}


# class Challenge18Service(Service):


'''
# at 20:00
Monday		: Day 1
Tuesday		: Day 2
Wednesday	: Day 3
Thursday	: Day 4
Friday		: Day 4.5
Saturday	: Day 5

Sunday		: Day 6
Monday		: Day 7
Tuesday		: Day 8
Wednesday	: Day 9
Thursday	: Day 10
Friday		: Day 10.5
Saturday	: Day 11

Sunday		: Day 12
Monday		: Day 13
Tuesday		: Day 14
Wednesday	: Day 15
Thursday	: Day 16
Friday		: Day 16.5
Saturday	: Day 17

Sunday		: Day 18
'''
# from Challenge18Service import *
# site = "https://www.youtube.com/watch?v=QkF3oxziUI4&ab_channel=LedZeppelin"
# views(site)

def views(url):
	# url = "https://www.youtube.com/watch?v=QkF3oxziUI4&ab_channel=LedZeppelin"
	t = time.time()
	headers_Get = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate',
			'DNT': '1',
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1'
		}
	with requests.Session() as session:
		res=session.get(url, headers=headers_Get,cookies={'CONSENT': 'YES+cb.20210328-17-p0.en-GB+FX+{}'.format(random.randint(100, 999))})
	numOfViews = -1
	try:
		x = res.text.split("viewCount")[4][2:].split(",\"")[0]
		numOfViews = json.loads(x)["simpleText"]
	except :
		traceback.print_exc()
		return -1

	# res = urlopen(url)
	# html = res.read()
	# wordBreak = ['<','>']
	# for i in range(len(html)):
	# 	if html[i] in wordBreak:
	# 		html[i] = ' '
	#
	# html = html.split()
	# dataSwitch = False
	# numOfViews = ''
	# for element in html:
	# 	if element == '/div':
	# 		dataSwitch = False
	# 	if dataSwitch:
	# 		numOfViews += str(element)
	# 	if "view-count" in str(element):
	# 		dataSwitch = True
	# print(numOfViews, " Views - Time: ",time.time()-t)
	return numOfViews


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

	daysToSkip = [4,10,16]
	push = {"international": C18Tasks.international, "Hebrew": C18Tasks.hebrew, "Family": C18Tasks.familyEng, "FamilyHeb": C18Tasks.familyHeb, "SongValuesHeb":C18Tasks.songValuesHeb}
	debug = False
	simulation = False

	def __init__(self, db, api, master):
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
		self.commands = {"#totalPoints":self.sendTotal,"#totalPointsHeb":self.sendTotalHeb, "#public":self.sendPublic}
		# self.manager = Challenge18Manager.share
		self.manager = None
		self.master = master
		self.excludeNumbers = ["972559721123@c.us"]
		# self.excludeNumbers = []


	def halfday(self, day):
		return day/.5 % 2 == 1

	def updateDay(self, current, ch = None):
		if ch is not None and ch in self.db["challenges"]:
			challenge = self.db["challenges"][ch]
			if "skipShabbat" in challenge and str(challenge["skipShabbat"]).lower() in ["true","1"]: #Edit/skipShabbat/true
				if current in self.daysToSkip :
					return current + .5 # SKIPS SHABBAT

		if self.halfday(current):
			return int(current + .5)
		return int(current + 1)

	def managePush(self):
		p = Thread(target=self.managePushAsync, args=[None])
		p.start()

	def getChallenge(self,info):
		res = {}
		origin, user, content = None, None, None
		if "origin" in info:
			origin = info["origin"]
		# if "user" in info:
		# 	user = info["user"]
		# if "content" in info:
		# 	content = info["content"]
		res["users"] = {}
		res["total"] = 0
		res["scores"] = []
		res["day"] = None
		if origin in self.db["challenges"]:
			if "today" in self.db["challenges"][origin]:
				res["day"] = self.db["challenges"][origin]["today"]
			if "template" in self.db["challenges"][origin]:
				res["template"] = self.db["challenges"][origin]["template"]
		try:
			print("OOOOOOOOOOOOOOOOOOOOO",info)
			print("OOOOOOOOOOOOOOOOOOOOO")
			print("OOOOOOOOOOOOOOOOOOOOO")
			print(":"+origin+":")
			print("OOOOOOOOOOOOOOOOOOOOO")
			print("OOOOOOOOOOOOOOOOOOOOO")
			participants = self.master.driver.group_get_participants_ids(origin)
		except :
			traceback.print_exc()
			participants = {}
		if participants:
			for user in participants:
				userData = res["users"][user] = {}
				if user in self.db["users"]:
					u = self.db["users"][user]
					if "score" in u:
						res["scores"].append(u["score"])
						res["total"]+=u["score"]
					else:
						res["scores"].append(0)

		return res

	def getChallengeScore(self,info):
		res = {}
		origin, user, content = None, None, None
		if "origin" in info:
			origin = info["origin"]
		# if "user" in info:
		# 	user = info["user"]
		# if "content" in info:
		# 	content = info["content"]
		res["users"] = {}
		res["total"] = 0
		# res["scores"] = []
		res["day"] = None
		if origin in self.db["challenges"]:
			if "today" in self.db["challenges"][origin]:
				res["day"] = self.db["challenges"][origin]["today"]
			if "template" in self.db["challenges"][origin]:
				res["template"] = self.db["challenges"][origin]["template"]
		try:
			print("OOOOOOOOOOOOOOOOOOOOO",info)
			print("OOOOOOOOOOOOOOOOOOOOO")
			print("OOOOOOOOOOOOOOOOOOOOO")
			print(":"+origin+":")
			print("OOOOOOOOOOOOOOOOOOOOO")
			print("OOOOOOOOOOOOOOOOOOOOO")
			participants = self.master.driver.group_get_participants_ids(origin)
		except :
			traceback.print_exc()
			participants = {}
		if participants:
			for user in participants:
				# userData = res["users"][user] = {}
				if user in self.db["users"]:
					u = self.db["users"][user]
					if "username" in u:
						if "score" not in u:
							self.db["users"][user]["score"] = 0
						res["users"][u["username"]] = u["score"]
						if "score" in u:
							# res["scores"].append(u["score"])
							res["total"]+=u["score"]
					# else:
						# res["scores"].append(0)

		return res

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
				if "template" not in challenge:
					challenge["template"] = "international"
				sent = []
				for up in challenge["upcoming"]:
					# print("UP",up)

					timeDiff = time.time() - search_dates(up)[0][1].timestamp()
					passedTime = timeDiff > 0 and timeDiff < lastHour
					if passedTime:
						try:
							day = challenge["today"]
							# if day in self.push and up in self.push[day]:
							if day in self.push[challenge["template"]] and up in self.push[challenge["template"]][day]:
								content = self.push[challenge["template"]][day][up]
								if content is not None:
									content = content.replace(
										"DDD", str(day)).replace("TTT", up)
									print(
										"#################### SENDING PUSH TO C18", ch, "DAY", day, "time", up)
									sent.append(up)
									# send to user
									if self.isCommand(content):
										tCommand = Thread(target = self.commands[content.split("/")[0]], args = [{"origin":ch, "content":content}])
										tCommand.start()
									else:
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

	def isCommand(self, content):
		return content.split("/")[0] in self.commands

	def sendTotalHeb(self, data, ret = False):
		return self.sendTotal(data,ret=ret, defaultLanguage = "hebrew")

	def sendPublic(self, data, ret = False, defaultLanguage = "internetional", strings = {"default": "{0}"}):
		origin, content = None, ""
		if "origin" in data:
			origin = data["origin"]
			res = self.getChallengeScore(data)
			if res is not None:
				self.api.send(
					origin, strings["default"].format(res), autoPreview=True)



	def sendTotal(self, data, ret = False, defaultLanguage = "internetional", strings = {
	"international":
	'''
🌴🌴🌴🌴🌴🌴🌴
*Total Points in the group: {0}*
🐋🌸🙏
	'''
	,
	"hebrew":
	'''
🌴🌴🌴🌴🌴🌴🌴🌴
*ניקוד קבוצתי מצטבר: {0}*
🙏🌍 *אתגר 18* 🐋🌸
	''',
	"family":
	'''
🌴🌴🌴🌴🌴🌴🌴
*Total Points in the group: {0}*
🐋🌸🙏
	'''
	,
	"familyheb":
	'''
🌴🌴🌴🌴🌴🌴🌴🌴
*ניקוד קבוצתי מצטבר: {0}*
🙏🌍 *אתגר 18* 🐋🌸
	''',
	}):
		print("DDDDDDDDDDd")
		print(data)
		print("DDDDDDDDDDd")
		origin, content = None, ""
		if "origin" in data:
			origin = data["origin"]

		total = 0
		if self.manager is None:
			print("XXXXXXXXXXX NO MANAGER")
			# self.manager = self.Challenge18Manager.share
		# res = self.manager.getChallenge({"origin":origin})
		res = self.getChallenge({"origin":origin})
		print("RRRRRRRRRRRRRRRRRRRRR")
		print("RRRRRRRRRRRRRRRRRRRRRoooooooo")
		print(res)
		print("RRRRRRRRRRRRRRRRRRRRR")
		print("RRRRRRRRRRRRRRRRRRRRR")
		if "template" in res:
			defaultLanguage = res["template"].lower()
			if defaultLanguage not in strings:
				if "heb" in defaultLanguage:
					defaultLanguage = "hebrew"
				else:
					defaultLanguage = "international"
			print("RRRRRRRRRRRRRRRRRRRRRoooooooo", "template",defaultLanguage)
		if "total" in res:
			total += res["total"]
			content = strings[defaultLanguage].format(str(total))
			# content += str(total)+"*"
			# content += "\n"
		else:
			content = ""

		if not ret and content != "":
			self.api.send(
				origin, content, autoPreview=True)
		else:
			return content


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

					for ch in self.db["challenges"]:
						challenge = self.db["challenges"][ch]
					# for challenge in self.db["challenges"]:

						# self.db["challenges"][challenge]["today"] += 1
						self.db["challenges"][ch]["today"] = self.updateDay(self.db["challenges"][ch]["today"], ch = ch)

						# if self.db["challenges"][challenge]["today"] == 0:
						# 	self.db["challenges"][challenge]["today"] += 1
						day = self.db["challenges"][ch]["today"]
						if self.debug:
							# send to user
							self.api.send(
								ch, "CHALLENGE CHANGED TO DAY " + str(day)+"\n"+self.db["challenges"][ch])

						if "template" not in challenge:
							challenge["template"] = "international"
						if day in self.push[challenge["template"]]:
							for tm in self.push[challenge["template"]][day]:
								self.db["challenges"][ch]["upcoming"][tm] = "_"

						print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", ch,
							  "DAY: ", challenge["today"])
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

	def loadDay(self, ch, origin = None):
		if ch in self.db["challenges"]:
			challenge = self.db["challenges"][ch]
		# for challenge in self.db["challenges"]:

			# self.db["challenges"][challenge]["today"] += 1
			# self.db["challenges"][ch]["today"] = self.updateDay(self.db["challenges"][ch]["today"])

			# if self.db["challenges"][challenge]["today"] == 0:
			# 	self.db["challenges"][challenge]["today"] += 1
			day = self.db["challenges"][ch]["today"]


			if "template" not in challenge:
				challenge["template"] = "international"

			print("LOADING DAYYYYYYYYYYYYYYYYYYYYYYYYYY")
			print("LOADING DAYYYYYYYYYYYYYYYYYYYYYYYYYY")
			print("LOADING DAYYYYYYYYYYYYYYYYYYYYYYYYYY")
			print("LOADING DAYYYYYYYYYYYYYYYYYYYYYYYYYY")
			print("LOADING DAYYYYYYYYYYYYYYYYYYYYYYYYYY")
			self.db["challenges"][ch]["upcoming"] = {}
			if day in self.push[challenge["template"]]:
				for tm in self.push[challenge["template"]][day]:
					self.db["challenges"][ch]["upcoming"][tm] = "_"
					print(day, self.push[challenge["template"]][day][tm] , "_____________________________")

			print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", ch,
				  "DAY: ", challenge["today"])
			if origin:
				# send to user
				self.api.send(
					origin, "CHALLENGE CHANGED TO DAY " + str(day)+"\n"+str(self.db["challenges"][ch]))

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
		print("RATE1")
		challenge = None
		if group in self.db["challenges"]:
			print("RATE2")
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

			if score > 0:
				''' for now just thankyou - later add custom message based on score / random '''
				# sendBack = "🙏🌍 *Challenge18* 🐋🌸"+"\n\n*Thank you!* "+user.split("@")[0]+"\n*your current score is now "+str(self.db["users"][user]["score"])+"*"
				sendBack = "🙏🌍 *Challenge18* 🐋🌸" + "\n" + "Day " + \
					str(day) + " - " + backmsg + "\n*Thank you!* " + \
					"\n*your current score is now " + \
					str(self.db["users"][user]["score"]) + "*"

				''' for now send directly to user - later in group '''

				print("RATE3",user,sendBack)
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


		challenge = self.db["challenges"][origin]

		if "template" not in challenge:
			challenge["template"] = "international"

		if "day=" in content.lower():
			for m in self.addMasters:
				if user.split("@")[0] in m:
					gotDay = None
					res = re.findall("[-\d]+", content)
					if len(res) > 0:
						try:
							gotDay = int(res[0])
						except:
							traceback.print_exc()
					if "template" not in self.db["challenges"][origin]:
						self.db["challenges"][origin]["template"] = "international"
					self.db["challenges"][origin] = self.formatChallenge(
						day=gotDay, template = self.db["challenges"][origin]["template"])
					# self.loadDay(origin)
					self.api.send(origin, "CHALLENGE CHANGED TO DAY " + str(self.db["challenges"][origin]["today"]) + "\n" + str(self.db["challenges"][origin]))  # send to user
					dbChanged = True
		if "template=" in content.lower() or "tem=" in content.lower():
			for m in self.addMasters:
				if user.split("@")[0] in m:
					gotTemplate = None
					# res = re.findall("[-\d]+", content)
					res = content.split("=")[1]
					if len(res) > 0 and res in self.push:
						try:
							self.db["challenges"][origin]["template"] = res
							self.db["challenges"][origin] = self.formatChallenge(
								day=self.db["challenges"][origin]["today"], template = self.db["challenges"][origin]["template"])
							self.api.send(origin, "CHALLENGE TEMPLATE TO " + self.db["challenges"][origin]["template"])  # send to user
							dbChanged = True
						except:
							traceback.print_exc()
							self.api.send(origin, "COULD NOT CHANGE TEMPLATE ERROR"+traceback.format_exc())  # send to user
					else:
						txt = "COULD NOT CHANGE TEMPLATE to "+res
						txt+= "\n\nAvailable templates:\n"
						for k in self.push:
							txt+=k+"\n"
						self.api.send(origin, txt)  # send to user

		elif "sim" == content.split("/")[0].lower():
			for m in self.addMasters:
				if user.split("@")[0] in m:
					self.simulation = True
					emptyContent = False
					noTimes = True
					allDays = False
					showDay = 3
					if "all" in content:
						allDays = True
					elif len(content.split("/")) > 1:
						try:
							simDay = int(content.split("/")[1])
							showDay = simDay
						except :
							pass
					currentDay = self.db["challenges"][origin]["today"]
					# send to user
					self.api.send(
						origin, "SIMULATING ALL DAYS OF THE CHALLENGE !!!!!!! READY? GO!")
					for d in self.push[challenge["template"]]:
						if (d > (showDay-1) and d < (showDay+1)) or allDays:
							self.db["challenges"][origin] = self.formatChallenge(
								day=d, template = self.db["challenges"][origin]["template"])
							self.api.send(origin, "=====================\n(Simulation) DAY " + str(self.db["challenges"][origin]["today"]) + "\n" + str(
								self.db["challenges"][origin]) + "\n\n=====================")  # send to user
							print("_____________________________________")
							print("_____________________________________")
							print("_____________________________________")
							print("DAY ", d)
							time.sleep(.5)
							print(self.push[challenge["template"]][d].keys())
							print(str(self.db["challenges"]
									  [origin]["upcoming"]))
							for atTime, v in self.db["challenges"][origin]["upcoming"].items():
								print("_____________________________________")
								print()
								print(d, "AT TIME:::", atTime)
								sendTxt = str(self.push[challenge["template"]][d][atTime])
								if "#totalPointsHeb" in sendTxt:
									sendTxt = self.sendTotal({"origin":origin, "content":""},ret=True)
								elif "#totalPoints" in sendTxt:
									sendTxt = self.sendTotal({"origin":origin, "content":""},ret=True)
								if noTimes:
									self.api.send(origin, sendTxt, autoPreview=True)
								elif not emptyContent:
									self.api.send(origin, "DAY " + str(d) + " " + atTime +
												  "\n\n\n" + sendTxt, autoPreview=True)
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
			if userID not in self.excludeNumbers:
				firstWord = content.split("\n")[0].split(" ")[0]
				if firstWord not in self.commands:
					goRate = True
					if "username" not in self.db["users"][userID] or self.db["users"][userID]["username"] is None:
						if "user=" not in firstWord.lower():
							self.signupUser(userID, origin)
						else:
							regRes = self.registerUsername(firstWord.split("=")[1], userID)
							goRate = False
							if regRes:
								dbChanged = True
				else:
					tCommand = Thread(target = self.commands[content.split("/")[0]], args = [{"origin":origin, "content":content}])
					tCommand.start()
					goRate = False
					dbChanged = False





				if thisDay < 0 or thisDay>9999:
					print("DONT RATE BEFORE FIRSTDAY", thisDay)
					goRate = False

				if goRate:
					self.rate(origin, content, userID)
					dbChanged = True

			else:
				print("SHARON!!!!!!!!!!!!")
				print("SHARON!!!!!!!!!!!!")
				print("SHARON!!!!!!!!!!!!")
				print("SHARON!!!!!!!!!!!!")
				print("SHARON!!!!!!!!!!!!")
				print("SHARON!!!!!!!!!!!!")
				print("SHARON!!!!!!!!!!!!")

		# user = self.db["users"][userID]

		if dbChanged:
			self.backup()
		# self.api.backup(self.db)

	def signupUser(self, userID, challengeGroup):
		signupMessage = "To show up on the scoreboard please choose a username, and send back:\n\n*user=MyUserName*"
		self.api.send(userID, signupMessage, autoPreview=True)

	def registerUsername(self, username, userID, fullData):
		res = self.usernameLegal(username, userID)
		if res[0]:
			res2 = self.checkPhone(userID)
			if not res2[0]:
				return res2
			if userID not in self.db["users"]:
				self.db["users"][userID] = {}
			self.db["users"][userID]["username"] = username #xxx
			if "register" in fullData:
				for k in fullData["register"]:
					self.db["users"][userID][k] = fullData["register"][k]
			elif fullData is not None and "dict" in str(type(fullData)) and len(fullData) > 1:
				for k in fullData:
					self.db["users"][userID][k] = fullData[k]
			self.backup()
		else:
			return res

		sendBack = res[1]
		self.api.send(userID, sendBack, autoPreview=True)
		return res

	def usernameLegal(self, username, userID):
		for user in self.db["users"]:
			if "username" in self.db["users"][user]:
				# print("#####################")
				# print(user["username"], userID)
				if self.db["users"][user]["username"] == username and user != userID:
					return False, "Oops! This username is already taken,\nplease choose another :)"
		return True, "Great! your username is now: *{0}*".format(username)

	def checkUsername(self, username):
		for user in self.db["users"]:
			if "username" in self.db["users"][user]:
				if self.db["users"][user]["username"].lower() == username.lower():
					return False, "Oops! This username is already taken,\nplease choose another :)"
		return True, "Great! you can register with username: *{0}*".format(username)

	def checkPhone(self, userID):
		userID = userID.split("@")[0].strip("+")+"@c.us"
		if userID in self.db["users"]:
			if "username" in self.db["users"][userID] and self.db["users"][userID]["username"] is not None and len(self.db["users"][userID]["username"]) > 1:
				return False, "Oops! This phone is already taken,\nplease choose another :)"

		return True, "Great! you can register with this phone *{0}*".format(userID)

# https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
	def getToken(self, userID):
		access_token = create_access_token(identity=userID)


	def signIn(self, username, userID):
		print("SIGN IN {0},{1}".format(username,userID))
		for user in self.db["users"]:
			if "username" in self.db["users"][user]:
				if self.db["users"][user]["username"] == username and user == userID:
					print("FUCK YEA")
					print("FUCK YEA")
					print("FUCK YEA")
					print("FUCK YEA")
					return True, userID
		return False, userID


	def backup(self):
		self.api.backup(self.db)
		# self.api.backup({"upcoming":self.db["upcoming"],"users":User.usersToJSONusers(self.db["users"])})

	def formatChallenge(self, day=None, template = "international"):
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

		nc = {"today": day, "upcoming": {}, "template": template}
		# for k in cFormat:
		# 	nc[k] = cFormat[k]
		#
		# nc["today"] = day
		# if "upcoming" not in nc:
		# 	nc["upcoming"] = {}

		if day in self.push[template]:
			for tm in self.push[template][day]:
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
