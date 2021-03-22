#Service.py
import time
from pprint import pprint as pp
TLAST = {0:None}
from threading import Thread
import traceback

class TofaatTevaService(object):
	id = "TofaatTeva"
	name = "🚀TofaatTeva🚀"
	welcome = "Welcome to 🚀TofaatTeva🚀 Service \nUsed for system experiments"
	help = "TofaatTeva TofaatTeva TofaatTeva"
	imageurl = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmaJKloEMiBpQRA9woJw4XnuWXCWeN2BO70w&usqp=CAU"
	shortDescription = "System Experiments 🧪"
	share = None

	examples = {"services":{"text":"Show Public Services","thumbnail":None}}

	def __init__(self,db, api, master):
		TofaatTevaService.share = self

		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! TofaatTeva",TofaatTevaService.share)
		self.db = db
		self.api = api
		self.master = master
		self.coms = ["Scraper"]
		#
		# if "upcoming" not in self.db:
		# 	self.db["upcoming"] = []
		# if "users" not in self.db:
		# 	self.db["users"] = {}
		# self.commands = {"subscribe":None,"group":self.createGroup,"=":self.subscribeToService,"-":self.unsubscribe, "/":self.findElement, "services":self.showServices}
		self.commands = {"אזור":self.newArea}
		self.Q = {}

		qT = Thread(target = self.startQAsync, args = [None])
		qT.start()


	def newArea(self, data, service = "Master", masterGroup = True, emptyNumber ="972543610404"):
		text, chatID, senderID = data
		syns = ["area","אזור","Area"]
		defaultSyn = "area"
		if "areas" not in self.db:
			self.db["areas"] = {}

		area = None
		if text is not None and text is not "":

			''' check synononyms '''
			for k in syns:
				if k in text:
					text = text.replace(k,defaultSyn)

			check = text.split(defaultSyn)[1]
			print("CCCCCCCCCCCCCCCC",check)
			print("CCCCCCCCCCCCCCCC",check)
			print("CCCCCCCCCCCCCCCC",check)
			print("CCCCCCCCCCCCCCCC",check)
			if len(check) > 1:
				if "/" is check[0] or " " is check[0]:
					check = check[1:]
				area = check
				# foundArea = None
				# for serv in self.master.services:
				# 	print(check.lower(), serv.lower())
				# 	if check.lower() == serv.lower():
				# 		foundArea = serv
				# if foundArea is not None:
				# 	service = foundArea

		# if masterGroup:
		# 	senderID = emptyNumber

		target = area
		newArea = True

		groupName = self.name +" "+target
		# path = self.download_image()
		path = self.master.download_image(service=self.id,pic_url=self.imageurl)

		if target not in self.db["areas"]:
			print(
			'''
			===============================================
			 ''' + senderID +" CREATING NEW AREA "+ target +" :D "+'''
			===============================================
			'''
			)

			# obj = None
			# if service in self.master.services and "obj" in self.master.services[service] and self.master.services[service]["obj"] is not None:
			# 	obj = self.master.services[service]["obj"]
			# 	groupName = self.master.services[service]["obj"].name
			# 	imageurl = self.master.services[service]["obj"].imageurl
			# 	if imageurl is not None:
			# 		path = self.download_image(service=service,pic_url=imageurl)



			imagepath = path
			newGroupID, groupInvite = self.master.driver.newGroup(newGroupName = groupName, number = "+"+senderID.split("@")[0], local = self.master.runLocal, image=imagepath)
			# newGroupID = newGroup.id
			welcome = "WELCOME TO WHATSAPP MASTER"

			self.newG = newGroupID
			service = self.id
			self.master.db["users"][senderID][service] = newGroupID
			self.master.db["groups"][newGroupID] = {"service":service, "invite":groupInvite, "link":self.master.newRandomID(), "user":senderID}
			self.db["areas"][target] = {"chatID":newGroupID, "invite":groupInvite}

			# if service is not "Master":
			print(
			'''
			===============================================
			 ''' + senderID +" NEW AREA "+ target +" Created :D "+'''
			===============================================
			''')
		else:
			newArea = False

		if newArea:
			sendBack = "New Area: "+groupName+" \n"+str(groupInvite)+"\nCheck it out :)"
		else:
			groupInvite  = self.db["areas"][target]["invite"]

			sendBack = "Area: "+groupName+" \n"+str(groupInvite)
		res = self.master.driver.send_message_with_thumbnail(path,chatID,url=groupInvite,title="Open  "+groupName,description="BBBBBBBB",text=sendBack)


		self.master.backup()
		self.backup()

	def startQAsync(self, data = None):
		self.startQ(data)

	def startQ(self, data = None):
		while(True):
			# print(self.Q)
			try:
				while(True):
					for area in self.Q:
						# print("area",area)
						q = self.Q[area]
						if len(q) > 0:
							chatID, msgID, isMedia, gName = q.pop()
							self.master.driver.forward_messages(chatID,msgID,isMedia)
							print("======== SENDING TO GROUP ",gName,"=======\n")

			except:
				traceback.print_exc()
	def go(self):
		while(False):
			if "upcoming" not in self.db:
				self.db["upcoming"] = []
			if "users" not in self.db:
				self.db["users"] = {}

			while len(self.db["upcoming"]) > 0:
				item = self.db["upcoming"].pop(0)
				origin, content = item
				self.api.send(origin, content, thumnail = "test")
				# self.api.backup(self.db)

			time.sleep(1)

	def process(self, info):
		origin, user, content, id, mType = None, None, None, None, ""
		if "origin" in info:
			origin = info["origin"]
		if "user" in info:
			user = info["user"]
		if "content" in info:
			content = info["content"]
		if "mID" in info:
			id = info["mID"]
		if "mType" in info:
			mType = info["mType"]

		foundArea = None
		if "areas" not in self.db:
			self.db["areas"] = {}

		for area in self.db["areas"]:
			if origin == self.db["areas"][area]["chatID"]:
				foundArea = area

		if foundArea:
			print("======== SENDING TO AREA",foundArea,"=======\n", content)
			gT = time.time()
			allGroups = self.master.getAllGroups()

			print("======== GETTING GROUPS TIME",str(time.time()-gT),len(allGroups),"=======\n")
			print("LLLLLLLLLLLLLLLLLLLLLLL",len(allGroups))
			self.master.driver.simulateTyping(origin,True)
			if foundArea not in self.Q:
				self.Q[foundArea] = []
			testMax = 10
			testCount = 0
			withTestMax = False
			for group in allGroups:
				# pp(group)
				if group is not None:
					gName = group.name
					if group.name is None:
						prevMsgs = group.get_messages(include_me=True)
						if len(prevMsgs) > 0:
							gName = group.get_messages(include_me=True)[0].get_js_obj()["chat"]["contact"]["name"]
						else:
							gName = ""
						pp(group)
						TLAST[0] = group


					if foundArea in gName and group.id != origin:
						# print(group.id)
						# print(origin)
						# print()
						# print("")
						old = False
						if old:
							self.master.sendMessage(group.id, content)
						elif id:
							if not withTestMax or testCount < testMax:
								# print(id)
								print("FORWARDING to group",gName)
								self.Q[foundArea].append([group.id,id,"video" in mType or "voice" in mType or "ptt" in mType, gName])
								testCount+=1
							else:
								print(testCount)
							# self.master.driver.forward_messages(group.id,id, "video" in mType)
						else:
							print("IIIIIIIIIIIIIIDDDDDDDDDDD IS NONNNEEEEEE")
							print("IIIIIIIIIIIIIIDDDDDDDDDDD IS NONNNEEEEEE")
							print("IIIIIIIIIIIIIIDDDDDDDDDDD IS NONNNEEEEEE")
							print("IIIIIIIIIIIIIIDDDDDDDDDDD IS NONNNEEEEEE")
							print("IIIIIIIIIIIIIIDDDDDDDDDDD IS NONNNEEEEEE")


			self.master.driver.simulateTyping(origin,False)
			print("======== FINISHED SENDING TO GROUPS TIME",str(time.time()-gT),len(allGroups),"=======\n")

		else:
			run = self.runCommands(content, origin, user)
			if not run:
				print("======== NO COMMANDS FOUND =======", content)
		{"masters": ["972545300376","972547932000"],"system": ["972545300376","972547932000"],"users": {"972547932000@c.us": {"Master": "972545300376-1614539822@g.us","TofaatTeva": "972545300376-1614540588@g.us"}},"groups": {},"id": "972545300376-1614534597@g.us","init": 1614540422.0182405,"backupInterval": 0,"backupDelay": 3,"lastBackup": 1614540702.403216,"lastBackupServices": 0,"servicesDB": {},"availableChats": {}}

		# # if "users" not in self.db:
		# # 	self.db["users"] = {}
		# #
		# # if user not in self.db["users"]:
		# # 	self.db["users"][user] = user
		# # 	self.api.send(origin, "WELCOME "+user)
		# # 	self.backup()
		#
		# # sendBack = content
		# #
		# # withLink = True
		# # if withLink:
		# # 	answer = ":answerid:555"
		# # 	myLink = self.api.genLink(origin, answer)
		# # 	sendBack += "\n\n"+answer+":\n"+myLink
		#
		# # self.db["upcoming"].append([origin, sendBack])
		# url = "https://www.youtube.com/watch?v=SD4KgwdjmdI&ab_channel=EngineerMan"
		# text = "Example youtube\n"+url
		# self.master.driver.send_message_with_auto_preview(origin, url, text)
		# return True
		#
		# if origin.split("/")[0] in self.coms:
		# 	lastOrigin = "/".join(origin.split("/")[1:])
		# 	self.api.send(lastOrigin.split("/")[0], "back from Scraper:\n "+content)
		#
		#
		#
		# else:
		#
		# 	''' service-service communicatins '''
		# 	# answer = "yo!"
		# 	# myLink = self.api.genLink(origin, answer, newLink = "yo")
		# 	# idFromLink = myLink.split("?")[1].split["/yo"][0]
		#
		# 	self.api.send("Scraper"+"/"+origin, "yo "+content+" from "+self.name)
		#
		# return True
		#
		# sendBack = content
		# myLink = ""
		# withLink = True
		# if withLink:
		# 	answer = content
		# 	myLink = self.api.genLink(origin, answer, newLink = "a")
		# 	sendBack += "\n\n"+answer+":\n"+myLink
		#
		# #
		# self.master.driver.sendMessage(origin,sendBack)
		#
		# ''' invite tests '''
		# service = "Master"
		# groupName = service
		# myLink = "https://akeyo.io/p?join"
		#
		# path = None
		# if service in self.master.services and "obj" in self.master.services[service] and self.master.services[service]["obj"] is not None:
		# 	groupName = self.master.services[service]["obj"].name
		# 	imageurl = self.master.services[service]["obj"].imageurl
		# 	if imageurl is not None:
		# 		path = self.master.download_image(service=service,pic_url=imageurl)
		# if path is None:
		# 	path = self.master.download_image()
		# imagepath = path
		#
		#
		# for service in self.master.services:
		# 	text, thumb = self.master.inviteToService(service=service)
		# 	print(text, thumb)
		# 	self.master.sendMessage(origin, text, thumbnail = thumb)



	def runCommands(self, text, chatID, senderID):
		foundCommand = False
		cmd = ""
		if text[0] in self.commands:
			cmd = text[0]
		else:
			rep = "/"
			if "/" not in text:
				rep = " "
			cmd = text.split(rep)[0]
		#
		# if "/" in text:
		# 	cmd = text.split("/")[0]

		print("RUNNING COMMANDS....")
		if cmd in self.commands:
			''' RUN COMMAND '''
			print("RUNNING COMMANDS....",cmd)
			res = self.commands[cmd]([text, chatID, senderID])
			foundCommand = True

		return foundCommand


	def backup(self):
		self.api.backup(self.db)

	def updateDB(self, db):
		self.db = db
		# self.db = User.jsonUsersToUsers(db)

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
