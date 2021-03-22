# ScraperService.py
from User import User
from Reminder import Reminder
from Conv import Conv
# from app import Service
# from ctparse import ctparemidrse
# from datetime import datetime
from bs4 import BeautifulSoup
import requests
import lxml, urllib

import traceback
from dateparser.search import search_dates
from threading import Thread

import time
import datetime
import re


from googlesearch import search


#https://web-capture.net/convert.php?link=google.com
#https://web-capture.net/convert.php?link=https://www.tab4u.com/tabs/songs/68069_%D7%99%D7%A1%D7%9E%D7%99%D7%9F_%D7%9E%D7%95%D7%A2%D7%9C%D7%9D_-_%D7%9E%D7%A1%D7%99%D7%91%D7%94.html

# class ScraperService(Service):
class ScraperService():
	id = "Scraper"
	name = "💚 Scraper 💚"
	welcome =  "*Welcome to Scraper 💚 Service*\n\nYou can now send the name of a song to get its lyrics translations :)\n*תוכלו לשלוח שם של שיר כדי לקבל תרגום למילים שלו :)*\n\nYou could also share a song from Youtube or Spotify!\n*תוכלו גם לשלוח לפה שיר ישר מיוטוב או ספוטיפיי!*"
	help = "Scraper help message"
	shortDescription = "English->Hebrew תרגום שירים"
	imageurl = "https://i.imgur.com/j1SkVVt.png"
	share = None

	examples = {"example1":{"text":"","thumbnail":None, "answer":"sweet child"}}

	sites = {
		"shironet":{"flow":
		[
		{"google":"shironet.mako.co.il"},
		{"get":{"lyrics":["span",{"class":"artist_lyrics_text"}]}}
		]},

		"google":{"flow":
		[
		{"google":"shironet.mako.co.il"},
		{"get":{"lyrics":["span",{"class":"artist_lyrics_text"}]}}
		]},

		}





	def __init__(self,db, api):
		ScraperService.share = self

		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Scraper",ScraperService.share)
		self.db = db
		self.api = api
		if "upcoming" not in self.db:
			self.db["upcoming"] = []
		if "users" not in self.db:
			self.db["users"] = {}


		# self.id = ScraperService.id
		# self.name = ScraperService.name
		# self.welcome = ScraperService.welcome
		# self.help = ScraperService.help
		# self.imageurl = ScraperService.imageurl

	def go(self):
		while(True):
			if "upcoming" not in self.db:
				self.db["upcoming"] = []
			if "users" not in self.db:
				self.db["users"] = {}

			while len(self.db["upcoming"]) > 0:
				item = self.db["upcoming"].pop(0)
				origin, content = item
				# self.backup()

			time.sleep(1)

	def loadPage(self, url):
		page = requests.get(url)
		return BeautifulSoup(page.content, 'html.parser')

	def searchGoogle(self, q, s = 5):
		res = []
		for r in self.google(q, s=s):
			res.append(r)
		return res


	def google(self, q, s = 20, lang = None):
		return search(q,stop = s)

		# text = urllib.parse.quote_plus(q)
		# url = 'https://google.com/search?q=' + text
		# if lang is not None:
		# 	url = url.replace(".com",lang)
		# response = requests.get(url)
		# soup = BeautifulSoup(response.text, 'lxml')
		# # print(soup.text)
		# for g in soup.find("body").findAll("div",{"class":'g'}):
		#     print(g.text)
		#     print('-----')
		# return soup
		# soup = google(None,"כחולת עינים LYRICS")



	def scrape(self, site = "shironet", search = ""):
		sendBack = {}
		if site in self.sites and "flow" in self.sites[site] and self.sites[site] is not None:
			# target = target.replace(" ","+")
			soup = None
			for step in self.sites[site]["flow"]:
				if step is not None:
					print("STEP",step)
					if "google" in step :
						foundG = False
						print("TTTTTTTTTTTTTT:",search)
						lang = None
						if "-.co.il" in step:
							lang = step.split("google-")[1]
						for url in self.google(search, lang = lang):
							print("UUUUUUUU:",url)
							if not foundG:
								if site in url:
									foundG = True
									print("url",url)
									soup = self.loadPage(url)
					if "go" in step:
						soup = self.loadPage(step["go"])
					if "get" in step:
						print("GET")
						for id in step["get"]:
							print(id, step["get"][id])
							try:
								element = step["get"][id][0]
								atrb = step["get"][id][1]
								res = soup.find("body").findNext(element,atrb).text
								sendBack[id] = res
							except:
								traceback.print_exc()


		return sendBack

		# scrape(None,"shironet","כחולת עינים")



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

		# if user not in self.db["users"]:
		# 	self.db["users"][user] = user
		# 	# self.api.send(origin, "WELCOME "+user)
		# 	self.backup()

		# self.db["upcoming"].append([origin, content])
		dbChanged = False
		userID = str(user)
		search = content
		site = ""
		print("CCCCCCCCCCCCCCCCCCCCCCC",content)
		if ":" == content[0]:
			if len(content.split(":")) > 2 and len(content.split(":")[2])>0:
				hasCMD = True
				l = content.split(":")
				site = l[1]
				try:
					search = l[2]
					print("SITE",site,"search",search)
					print("SITE",site,"search",search)
					print("SITE",site,"search",search)
					print("SITE",site,"search",search)
					print("SITE",site,"search",search)
					res = self.scrape(site = site, search = search)
					sendBack = ""
					for key in res:
						sendBack+=res[key]
						self.api.send(origin, sendBack)
						return True
				except:
					traceback.print_exc()

		return True
		''' shironet '''
		res = self.scrape(site = site, search = content)
		sendBack = ""
		for key in res:
			sendBack+=res[key]+"\n"
		self.api.send(origin, sendBack)
		return True

		''' echo '''
		self.api.send(origin, "echo "+content+" from "+self.name)
		return True


		# dbChanged = False
		if userID not in self.db["users"]:
			user = User(userID)
			self.db["users"][userID] = user

			# user.conv.manager("WELCOME "+userID)
			# ScraperService.actuallySend(userID, "*Welcome to Scraper 💚 Service*\nYou can now send a name of a song to get it's lyrics translations :)")
			dbChanged = True

		user = self.db["users"][userID]
		#
		# for a in range(10):
		# 	ScraperService.actuallySend(userID, str(a))
		target = content
		urlChecks = ["http","youtu","spotify.com"]
		url = False
		for check in urlChecks:
			if check.lower() in target.lower():
				url = True
		if url:
			target = str(re.search("(?P<url>https?://[^\s]+)", target).group("url"))

		self.api.send(origin, "Checking Lyrics for:\n*"+target+"*\n"+"Please wait a bit")

		# ScraperService.actuallySend(userID, )

		# import requests
		# from bs4 import BeautifulSoupYO
		# example = "We are the champions"
		# song = example.replace(" ","+")

		target = target.replace(" ","+")
		lyricsLink = "http://Scraper.wholesome.garden/lyrics/"+target
		print (lyricsLink)
		page = requests.get(lyricsLink)
		# if str(page.status_code) == "200":
		soup = BeautifulSoup(page.content, 'html.parser')
		# print(soup.prettify())
		# print(soup.body[""])

		# txt = str(str(P).split('))
		pageLoaded = False

		firstLang = []
		secondLang = []

		try:
			title = soup.findAll("h3")[0].text.replace("                   ","").replace("                ","").replace("\n","")
			while title[-1:] is " ":
				title = title[:-1]

			P = soup.find_all('p')
			lyrics = []
			for pp in P:
				lyrics.append(pp.text.replace("\n","").replace("                ","").replace("              ",""))

			for l in lyrics:
				print("LLL:",l)

			firstLang = lyrics[0::4][:-1]
			secondLang = lyrics[1::4][:-1]
		except Exception as e:
			print("EEEEEEEEEEEEEEEE Scraper could not be loaded",e)
			traceback.print_exc()

		cleanLyrics = "💚 *Scraper* 💚\n"
		cleanLyrics += "*"+title+"*"+"\n\n"

		for i in range(len(firstLang)):
			cleanLyrics += firstLang[i] +"\n"
			if i<len(secondLang):
				cleanLyrics += secondLang[i]+"\n"
			cleanLyrics+="\n"

		if len(firstLang) == 0:
			cleanLyrics += "Could not load Scraper\n\n"

		cleanLyrics+="Made with 💚\n"
		cleanLyrics+="from "+lyricsLink

		# ScraperService.actuallySend(userID, cleanLyrics)
		self.api.send(origin, cleanLyrics)

		if dbChanged:
			self.backup()


	def backup(self):
		self.api.backup(self.db)

	def updateDB(self, db):
		self.db = db
		# self.db = User.jsonUsersToUsers(db)


	def getDB():
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("USERS")
		print(ScraperService.users)

		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("JSON")
		jsonUsers = User.usersToJSONusers(ScraperService.users)
		print(jsonUsers)

		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("recovered USERS")
		print(User.jsonUsersToUsers(jsonUsers))

		return {"users":jsonUsers,"upcoming":ScraperService.upcoming}
		# return {"users":ScraperService.users,"upcoming":ScraperService.upcoming}


	def setDB(db):
		ScraperService.upcoming = db["upcoming"]
		ScraperService.users = User.jsonUsersToUsers(db["users"])

	def backup0():
		ScraperService.backupDelegate(db = ScraperService.getDB(),service = ScraperService.serviceName)

	def loadDB():
		res = ScraperService.backupDelegate(db = None,service = ScraperService.serviceName)
		if res is not None:
			resave = False
			if "upcoming" not in res:
				res["upcoming"] = {}
				resave = True
			if "users" not in res:
				res["users"] = {}
				resave = True
			ScraperService.setDB(res)
			if resave:
				ScraperService.backup()


	def asyncRoll():
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		print("Scraper")
		t = Thread(target = ScraperService.rollUpcoming,args = [None,])
		t.start()

	def rollUpcoming(data):
		"!!!!!!!!!!!!!!!!!!!!!!@@@@@@@@@@@@@@@@@@@@@@@"
		while(True):
			for key in list(ScraperService.upcoming.keys()):
				t = ScraperService.upcoming[key]
				if time.time()-t > 0:
					userID,remID = key.split("_")
					ScraperService.send(userID, remID)
			time.sleep(1)


	# shared = None
	#
	# def __init__(self):
	#     shared = sel
	#     pass #load from back

	def go0(sendDelegate = None, backupDelegate = None):
		## LOAD FROM DAL

		ScraperService.users = {}
		ScraperService.upcoming = {}
		ScraperService.init = True
		ScraperService.asyncRoll()
		ScraperService.sendDelegate = sendDelegate
		ScraperService.backupDelegate = backupDelegate
		ScraperService.loadDB()


	def process0(userID, message):

		print(ScraperService.init,"!!!!!!!!!!!!")
		if not ScraperService.init:
			ScraperService.go()


		dbChanged = False
		userID = str(userID)

		# dbChanged = False
		if userID not in ScraperService.users:
			user = User(userID)
			ScraperService.users[userID] = user

			# user.conv.manager("WELCOME "+userID)
			# ScraperService.actuallySend(userID, "*Welcome to Scraper 💚 Service*\nYou can now send a name of a song to get it's lyrics translations :)")
			dbChanged = True

		user = ScraperService.users[userID]
		#
		# for a in range(10):
		# 	ScraperService.actuallySend(userID, str(a))
		target = content
		urlChecks = ["http","youtu","spotify.com"]
		url = False
		for check in urlChecks:
			if check.lower() in target.lower():
				url = True
		if url:
			target = str(re.search("(?P<url>https?://[^\s]+)", target).group("url"))
		ScraperService.actuallySend(userID, "Checking Lyrics for:\n*"+target+"*\n"+"Please wait a bit")

		# import requests
		# from bs4 import BeautifulSoupYO
		# example = "We are the champions"
		# song = example.replace(" ","+")

		target = target.replace(" ","+")
		lyricsLink = "http://Scraper.wholesome.garden/lyrics/"+target
		print (lyricsLink)
		page = requests.get(lyricsLink)
		# if str(page.status_code) == "200":
		soup = BeautifulSoup(page.content, 'html.parser')
		# print(soup.prettify())
		# print(soup.body[""])

		# txt = str(str(P).split('))

		title = soup.findAll("h3")[0].text.replace("                   ","").replace("                ","").replace("\n","")
		while title[-1:] is " ":
			title = title[:-1]

		P = soup.find_all('p')
		lyrics = []
		for pp in P:
			lyrics.append(pp.text.replace("\n","").replace("                ","").replace("              ",""))

		for l in lyrics:
			print("LLL:",l)

		firstLang = lyrics[0::4][:-1]
		secondLang = lyrics[1::4][:-1]

		cleanLyrics = "💚 *Scraper* 💚\n"
		cleanLyrics += "*"+title+"*"+"\n\n"

		for i in range(len(firstLang)):
			cleanLyrics += firstLang[i] +"\n"+ secondLang[i]+"\n\n"
		cleanLyrics+="Made with 💚\n"
		cleanLyrics+="from "+lyricsLink

		ScraperService.actuallySend(userID, cleanLyrics)
		# if False:
		# 	ScraperService.actuallySend(userID, "Could not fetch lyrics %0AE: "+e)


		#
		# for l in lyrics:
		# 	print(":::"+l+"::::")
		#
		# Made with 💚
		#
		# lyrics
		#
		#
		#
		#
		#
		# user.conv.human(message)
		# timestr = ""
		#
		# if not user.conv.ongoing:
		# # check for commands
		# 	print("AAAAAAAAAAAAAAAAAA")
		# 	m, t, timestr = ScraperService.parseMsg(message)
		# 	if t is None:
		# 		user.conv.manager("When to remind you?")
		# 		ScraperService.actuallySend(userID, "When shall I remind you ?")
		# 		user.conv.ongoing = True
		# 	else:
		# 		ScraperService.convFinished(user, set = True)
		#
		# 	rem = ScraperService.newReminder(userID, m, t)
		#
		#
		#
		# else:
		# 		print("BBBBBBBBBBBBBBBBBBBBB")
		# 		user.conv.tries += 1
		# 		m, t, timestr = ScraperService.parseMsg(message)
		# 		## GET LAST REMINDER
		#
		# 		if t is None:
		# 			user.conv.manager("Sorry I didnt understand when  "+ str(user.conv.tries))
		# 			ScraperService.actuallySend(userID, "Sorry I didn't unserstand when...")
		#
		# 		else:
		# 			rem = user.lastRem
		# 			rem.sendTime = t
		#
		# 			ScraperService.convFinished(user, set = True)
		#
		# if ScraperService.convFinished(user):
		# 	rem = user.lastRem
		#
		# 	if rem.sendTime is not None:
		# 		user.conv.manager(" ".join(["THANK YOU! WILL REMIND YOU TO ",rem.message, "at",time.ctime(rem.sendTime)," (",timestr,")"]))
		# 		ScraperService.actuallySend(userID, " ".join(["THANK YOU! WILL REMIND YOU TO ",rem.message, "at",time.ctime(rem.sendTime)," (",timestr,")"]))
		#
		# 		combID = userID+"_"+rem.id
		# 		ScraperService.upcoming[combID] = rem.sendTime
		# 		dbChanged = True
		# 	else:
		# 		print("XXXXXXXXXXXXXXXXXXXXXXXX", "unhandled")
		#
		# 	ScraperService.convFinished(user, set = None)
		# 	user.conv.ongoing = False
		# else:
		# 	print("***continue conv!!!!!!!!!!!!!!!!!!")
		#
		if dbChanged:
			ScraperService.backup()


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
		if userID in ScraperService.users:
			user = ScraperService.users[userID]
			if remID in user.reminders["unsent"]:
				rem = user.reminders["unsent"][remID]
				print("!!!!!!!",rem)
				if ScraperService.actuallySend(userID,rem.message):
					if user.markSent(remID):
						if combID in ScraperService.upcoming:
							ScraperService.upcoming.pop(combID)
							ScraperService.backup()
						else:
							print("EEEEEEEEE", "wasn't in upcoming")

					else:
						print("EEEEEEEEE", "could not mark!")

				else:
					print("EEEEEEEEE", "could not send!")



	def actuallySend(userID, message):
		print("TRY SENDING ON WHATSAPP! TO:", userID, "MESSAGE:", message)
		return ScraperService.sendDelegate(userID,message)

		# return False #for errors

	def getRE(key):
		return re.compile(re.escape(key.lower()), re.IGNORECASE)


	def formatKnown(txt):
		for key in known:
			keyRE = ScraperService.getRE(key)
			changed = keyRE.sub(known[key],txt)
			if txt != changed:
				print("-------CHANGED",txt,"TO",changed)
				txt = changed
		return txt

	def parseMsg(txt, tries = 0):
		print("============================")
		print(txt)
		formatted = ScraperService.formatKnown(txt)
		timestr = ""
		res = search_dates(formatted, add_detected_language=True)
		when = None
		if res is None:
			return txt, when, timestr
		if True:#try:
			# print("######################",formatted)
			# print(res)
			date = res[0][1].timestamp()
			timestr = res[0][0]
			lang = res[0][2]
			## remove timestr from reminder

			diff = time.time()-date
			# print("DIFF",diff, time.ctime(date))
			if diff > 0 and tries < 3:
				print("RETRY ")
				if tries == 0:
					new = ScraperService.changeDay(formatted)
				else:
					new = formatted.replace(timestr,"in "+timestr)
				return ScraperService.parseMsg(new, tries+1 )
			else:
				when = date
		# if True:#except:
		#     print("EEEEEEEEEEEEEEEEEEEEEE res:",res)
		#     return txt, None, ""

		if timestr is not "":
			formatted = txt.replace(timestr,"")
		return formatted, when, timestr

	def changeDay(txt):
		# print("CCCCCCCCCCCCC C C C C C C, ",txt,"\n")
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
			keyRE = ScraperService.getRE(key)
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

		user = ScraperService.users[userID]
		if user is None:
			print("user not found")
			return None

		user.remCount += 1
		remID = str(user.remCount)
		rem = Reminder(remID, userID, message, when)
		user.reminders["unsent"][remID] = rem
		user.lastRem = rem

		return rem

	def welcomeUser(self, origin):
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		if "users" not in self.db:
			self.db["users"] = {}
		if origin not in self.db["users"]:
			self.db["users"][origin] = origin
			self.backup()
