# app.py
import os, sys, time
import json
from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webwhatsapi import WhatsAPIDriver

from pprint import pprint

# from ServiceImporter import *
import requests
# export PATH="$HOME/wholesomegarden/WhatsappReminder:$PATH"
from ServiceLoader import *

# self.runLocal = False
class MasterService(object):
	# shares = []
	# db = {
	# 	"masters":["972512170493", "972547932000"],
	# 	"users":{"id":{"services":{"groupID":None}}},
	# 	"services":{"Reminders":{"dbID":None,"incomingTarget":None},"Proxy":{"dbID":None,"incomingTarget":None},"Danilator":{"dbID":None,"incomingTarget":None}},
	# 	"groups": {"id":"service"},
	# 	"id":"972547932000-1610379075@g.us"}
	# services = {}
	id = "Master"
	name = "✨WhatsappMaster✨"
	welcome = "Welcome to ✨WhatsappMaster✨ \nCheck out our services!"
	help = "send a message to get it back"
	# imageurl = "https://businesstech.co.za/news/wp-content/uploads/2020/09/WhatsApp-logo.png"
	imageurl = "https://www.nicepng.com/png/detail/5-52288_colores-del-logo-de-whatsapp-whatsapp-icon-red.png"
	shortDescription = "Whatsapp Service Platform"
	share = None

	examples = {"services":{"text":"Show Public Services","thumbnail":None}}

	# publicServices =  ["Danilator", "Reminders", "Music"]

	''' start master driver and log in '''
	def __init__(self, db, api, master):
		MasterService.share = self
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! MasterService",MasterService.share)

		self.db = db
		self.api = api
		self.runLocal = master.runLocal
		# self.master.db = db
		# self.master.services = services
		# self.master.driver = driver
		self.master = master

		self.commands = {"subscribe":None,"group":self.createGroup,"=":self.subscribeToService,"-":self.unsubscribe, "/":self.findElement, "services":self.showServices}


	def findElement(self, data):
		text, chatID, senderID = data
		# if text[0] is "/":
		# "//div[@class='VPvMz']/div/div/span[@data-testid='menu']"
		print("##################################")
		print("##################################")
		print("#####                      #######")
		print("##################################")
		print("##################################", text)
		dotsSide = self.master.driver.tryOut(self.master.driver.driver.find_element_by_xpath,text,click=True)

	def showServices(self, data):
		text, chatID, senderID = data

		# self.master.sendMessage(chatID, text)
		# time.sleep(1)

		self.master.sendMessage(chatID, "*List of Public Services:*")
		time.sleep(1.5)
		for service in self.master.publicServices:
			time.sleep(0.2)
			text, thumb = self.master.inviteToService(service=service,fromChat = chatID, public = True)
			print("TTTTTTTTTTTTTTTTTT")
			print(text, thumb)

			self.master.sendMessage(chatID, text, thumbnail = thumb)


	def subscribeToService(self, data):
		text, chatID, senderID = data

		''' person registering service with ='''
		target = text[1:]
		dbChanged = False
		now = False

		''' check target service in db '''
		serviceFound = False

		serviceChat = ""
		for service in self.master.services:
			print("______________ ----------"+service)
			print("")
			if not serviceFound and target.lower() == service.lower():
				target = service


				''' service found '''
				serviceFound = True
				if "users" not in  self.master.db:
					self.master.db["users"] = {}
				if "groups" not in  self.master.db:
					self.master.db["groups"] = {}
				if senderID not in self.master.db["users"]:
					self.master.db["users"][senderID] = {}
					dbChanged = True
					''' first time user '''
					# self.master.db["users"][senderID] = {'services': {'Reminders': {'groupID': None}}}
				else:
					pass
					''' known user '''


				foundChat = None
				if service in self.master.db["users"][senderID]:
					serviceChat = self.master.db["users"][senderID][service]
					print("#########################################################")

					# self.master.driver.sendMessage(senderID,"You are already subscirbed to: "+target+" \nYou can unsubscribe with -"+target.lower())
					if serviceChat is not None:
						try:
							foundChat = self.master.driver.get_chat_from_id(serviceChat)
						except:
							print('chat could not be found')


				chatName = target
				welcome = "Thank you for Subscribing to "+target
				try:
					chatName = self.master.services[service]["obj"].name
					welcome = "Thank you for Subscribing to "+chatName
					welcome = self.master.services[service]["obj"].welcome
				except:
					pass

				if foundChat is not None:
					# check_participents = False
					# if check_participents:
					# 	if senderID in foundChat.get_participants_ids() or True:
					# 		'''##### check that user is participant '''
					# 		self.master.driver.sendMessage(chatID,"You are already subscirbed to: "+chatName+" \nYou can unsubscribe with -"+target.lower())
					# 		self.master.driver.sendMessage(serviceChat,"subscirbed to: "+chatName)
					# 	else:
					# 		foundChat = None
					if serviceChat in self.master.db["groups"]:
						gotLink = False
						groupName = service
						path = self.download_image()
						inviteLink = ""

						print("$$$$$$$$$$$$$$$$$$$$$$$")
						print(serviceChat, self.master.db["groups"][serviceChat]  )
						if serviceChat in self.master.db["groups"] and self.master.db["groups"][serviceChat] is not None and "invite" in self.master.db["groups"][serviceChat]:
							if self.master.db["groups"][serviceChat]["invite"] is not None:
								inviteLink = self.master.db["groups"][serviceChat]["invite"]
								gotLink = True
								if service in self.master.services and "obj" in self.master.services[service] and self.master.services[service]["obj"] is not None:
									groupName = self.master.services[service]["obj"].name
									imageurl = self.master.services[service]["obj"].imageurl
									if imageurl is not None:
										path = self.download_image(service=service,pic_url=imageurl)


						content = "You are already subscirbed to:\n"+chatName+" \n"
						if gotLink:
							content+= inviteLink
						# content+="\n"+"You can unsubscribe with -"+target.lower()

						if gotLink:
							res = self.master.driver.send_message_with_thumbnail(path,chatID,url=inviteLink,title="Open  "+groupName,description="xxx",text=content)
						else:
							self.master.driver.sendMessage(chatID,content)
						self.master.driver.sendMessage(serviceChat,"subscirbed to: "+chatName)
					else:
						foundChat = None

				''' create new group '''
				if foundChat is None: #NGN
					print(
					'''
					===============================================
					 ''' + senderID +" CREATING NEW GROUP "+ target +" :D "+'''
					===============================================
					'''
					)
					self.master.driver.sendMessage(chatID,"Creating group: "+chatName+" \nPlease wait a moment :)")

					groupName = service
					path = self.download_image()
					obj = None
					if service in self.master.services and "obj" in self.master.services[service] and self.master.services[service]["obj"] is not None:
						obj = self.master.services[service]["obj"]
						groupName = obj.name
						imageurl = obj.imageurl
						if imageurl is not None:
							path = self.download_image(service=service,pic_url=imageurl)


					imagepath = path
					newGroupID, groupInvite = self.master.driver.newGroup(newGroupName = groupName, number = "+"+senderID.split("@")[0], local = self.runLocal, image=imagepath)
					# newGroupID = newGroup.id

					self.newG = newGroupID
					# if  self.master.db
					link = self.master.newRandomID()

					self.master.db["users"][senderID][service] = newGroupID
					self.master.db["groups"][newGroupID] = {"service":target, "invite":groupInvite, "user":senderID, "link":link}
					dbChanged = True
					now = True
					print(
					'''
					===============================================
					 ''' + senderID +" is NOW SUBSCRIBED TO "+ target +" :D "+'''
					===============================================
					'''
					)

					res = self.master.driver.send_message_with_thumbnail(path,chatID,url=groupInvite,title="Open  "+groupName,description="BBBBBBBB",text="Thank you! you are now subscribed to: "+chatName+" \n"+str(groupInvite)+"\nPlease check your new group :)")

					# self.master.driver.sendMessage(senderID,"Thank you! you are now subscribed to: "+chatName+" \n"+str(groupInvite)+"\nPlease check your new group :)")

					toAdd = ""
					if obj is not None:
						if len(obj.examples) > 0:
							toAdd += "\n\n"
							toAdd += "See Examples: (click the link or type)\n"
							for example in obj.examples:
								key = example
								answer = key
								text = ""
								if "answer" in obj.examples[key]:
									answer = obj.examples[key]["answer"]
								if "text" in obj.examples[key]:
									text = obj.examples[key]["text"]
								toAdd += "*"+answer+"* : "+text+"\n"
								toAdd += self.master.baseURL + link +"/"+key + "\n\n"
					self.master.driver.sendMessage(newGroupID,welcome+toAdd)
					# self.master.driver.sendMessage(serviceChat,"subscirbed to: "+target)

		if not serviceFound:
			self.master.driver.sendMessage(chatID,target+" : is not recognized as a service "+target)
			print(
			'''
			===============================================
			  SERVICE '''+ target +" IS NOT AVAILABLE"+'''
			===============================================
			'''
			)
		if dbChanged:
			self.master.backup()

	def unsubscribe(self,data):
		text, chatID, senderID = data

		''' person unsubscribing service with -'''
		target = text[1:]
		dbChanged = False
		now = False

		''' check target service in db '''
		serviceFound = False
		for service in self.master.services:
			print("______________ ----------"+service)
			print("")
			if not serviceFound and target.lower() == service.lower():
				target = service

				''' service found '''
				serviceFound = True

				if senderID not in self.master.db["users"]:
					self.master.db["users"][chatID] = {}
					dbChanged = True
					''' first time user '''
					# self.master.db["users"][senderID] = {'services': {'Reminders': {'groupID': None}}}
				else:
					pass
					''' known user '''

				foundChat = None
				if chatID in self.master.db["groups"]:
					if "service" in self.master.db["groups"][chatID] and target == self.master.db["groups"][chatID]["service"]:
						self.master.db["groups"][chatID]["service"] = None

				if service in self.master.db["users"][senderID]:
					serviceChat = self.master.db["users"][senderID][service]

					# self.master.driver.sendMessage(senderID,"You are already subscirbed to: "+target+" \nYou can unsubscribe with -"+target.lower())
					if serviceChat is not None:
						try:
							oldGroup = self.master.db["users"][senderID].pop(service)
							if oldGroup in self.master.db["groups"]:
								self.master.db["groups"].pop(oldGroup)
								self.master.driver.sendMessage(oldGroup,"Unsubscribing from: *"+service+"*")

							self.master.driver.sendMessage(chatID,"Unsubscribing from: *"+service+"*")
							print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
							print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
							print("UUUUUUU    UNSUBSCRIBING       UUUUUUUUUUUU")
							print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
							print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
							print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",chatID,service)
							dbChanged = True
							now = True

						except:
							print('chat could not be found')
				else:
					self.master.driver.sendMessage(chatID,"you are not subscirbed to: *"+service+"*"+"\n"+chatID+" / "+senderID)

		if not serviceFound:
			self.master.driver.sendMessage(chatID,"you are not subscirbed to: *"+service+"*")

		if dbChanged:
			self.master.backup()

	def createGroup(self, data, service = "Master", masterGroup = True, emptyNumber ="972543610404"):
		text, chatID, senderID = data

		if text is not None and len(text.split("group")) > 1:

			check = text.split("group")[1]
			print("CCCCCCCCCCCCCCCC",check)
			print("CCCCCCCCCCCCCCCC",check)
			print("CCCCCCCCCCCCCCCC",check)
			print("CCCCCCCCCCCCCCCC",check)
			if len(check) > 1:
				if "/" is check[0]:
					check = check[1:]

				foundService = None
				for serv in self.master.services:
					print(check.lower(), serv.lower())
					if check.lower() == serv.lower():
						foundService = serv
				if foundService is not None:
					service = foundService

		if masterGroup:
			senderID = emptyNumber

		target = service

		print(
		'''
		===============================================
		 ''' + senderID +" CREATING NEW GROUP "+ target +" :D "+'''
		===============================================
		'''
		)

		groupName = service
		path = self.download_image()
		obj = None
		if service in self.master.services and "obj" in self.master.services[service] and self.master.services[service]["obj"] is not None:
			obj = self.master.services[service]["obj"]
			groupName = self.master.services[service]["obj"].name
			imageurl = self.master.services[service]["obj"].imageurl
			if imageurl is not None:
				path = self.download_image(service=service,pic_url=imageurl)



		imagepath = path
		newGroupID, groupInvite = self.master.driver.newGroup(newGroupName = groupName, number = "+"+senderID.split("@")[0], local = self.runLocal, image=imagepath)
		# newGroupID = newGroup.id
		welcome = "WELCOME TO WHATSAPP MASTER"

		self.newG = newGroupID

		# if service is not "Master":
		# 	self.master.db["users"][senderID][service] = newGroupID
		# 	self.master.db["groups"][newGroupID] = {"service":target, "invite":groupInvite, "link":self.master.newRandomID(), "user":senderID}
		# print(
		# '''
		# ===============================================
		#  ''' + senderID +" is NOW SUBSCRIBED TO "+ target +" :D "+'''
		# ===============================================
		# '''
		# )
		# self.master.driver.sendMessage(senderID,"Thank you! you are now subscribed to: "+chatName+" \n"+str(groupInvite)+"\nPlease check your new group :)")

		if obj is not None:
			# print("WAIT 5")
			# time.sleep(1)
			# imageurl = "https://scontent.ftlv6-1.fna.fbcdn.net/v/t1.0-9/s960x960/90941246_10158370682234287_4145441832110653440_o.jpg?_nc_cat=110&ccb=2&_nc_sid=825194&_nc_ohc=8s_3FhJStQUAX-yKU8c&_nc_ht=scontent.ftlv6-1.fna&tp=7&oh=cc43986a0035414deb90a706d7b7fc2b&oe=602D4239"
			#
			# time.sleep(5)
			# self.master.setGroupIcon(newGroupID, obj.imageurl)
			# print("WAIT 5")
			pass
		if masterGroup:
			if "availableChats" not in self.master.db:
				self.master.db["availableChats"] = {}
			if service not in self.master.db["availableChats"]:
				self.master.db["availableChats"][service] = {}
			# time.sleep(1)
			# self.master.driver.remove_participant_group(newGroupID,senderID+"@c.us")
			code = "WAPI.removeParticipantGroup('"+newGroupID+"', '"+senderID+"@c.us"+"')"
			self.master.driver.driver.execute_script(script=code)

			if obj is not None:
				imageurl = obj.imageurl
				# imageurl = "https://aux2.iconspalace.com/uploads/whatsapp-flat-icon-256.png"
				# imageurl = ""
				self.master.setGroupIcon(newGroupID, imageurl)


			# time.sleep(1)
			# code = "WAPI.getMetadata('"+newGroupName+"', '"+number+"@c.us"+"')"

			# time.sleep(10)
			self.master.driver.sendMessage(newGroupID,welcome)
			# print("##############################")
			self.master.db["availableChats"][service][newGroupID] = groupInvite
			# print("##############################")
			# print(self.master.db["availableChats"])
			# self.waitForNewParticipant(newGroupID)
		if chatID is not None:
			res = self.master.driver.send_message_with_thumbnail(path,chatID,url=groupInvite,title="Open  "+groupName,description="BBBBBBBB",text="Creating empty group: "+groupName+" \n"+str(groupInvite)+"\nCheck it out :)")


		self.master.backup()


	def runCommands(self, text, chatID, senderID):
		foundCommand = False
		cmd = ""
		if text[0] in self.commands:
			cmd = text[0]
		else:
			cmd = text.split("/")[0]
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

	def ProcessChat(self,message):
		print("MMMMMMMMMMX",message.content)
		chatID = ""
		if self.runLocal and False: #for firefox
			chatID = message.chat_id["_serialized"]
		else:
			chatID = message.chat_id

		print("!!!!!!!!!!!!!!!!!!!")
		try:
			chat = self.master.driver.get_chat_from_id(chatID)
		except Exception as e:
			print(" ::: ERROR - _serialized chatID ::: "+chatID+" ::: ","\n",e,e.args,"\n")

		''' incoming from: '''
		''' Personal Chat  '''
		print("!!!!!!!!!!!!!!!!!!!!!")
		senderName = message.get_js_obj()["chat"]["contact"]["formattedName"]
		senderID = message.sender.id
		fromGroup = False
		print("!!!!!!!!!!!!!!!!!!!",chatID)
		if "c" in chatID or True:
			print(
			'''
			===================================
			   Incoming Messages from '''+senderID+" "+senderName+'''
			===================================
			'''
			)
			print("!!!!!!!!!!!!!!!!!!!")
			if message.type == "chat":
				text = message.content
				run = self.runCommands(text, chatID, senderID)

				if not run:
					print("======== NO COMMANDS FOUND =======", text)
				''' SENT FROM GROUP CHAT '''

	def go(self):
		while(False):
			time.sleep(1)

	def process(self, info):
		origin, user, content = None, None, None
		if "origin" in info:
			origin = info["origin"]
		if "user" in info:
			user = info["user"]
		if "content" in info:
			content = info["content"]
		print("@@@@@@")
		print("@@@@@@")
		print("@@@@@@")

		run = self.runCommands(content, origin, user)

		if not run:
			print("======== NO COMMANDS FOUND =======", content)

		print("@@@@@@")
		print("@@@@@@")
		# self.api.send(origin, "WHATSAPPMASTER SERVICE\n"+content, thumnail = "test")

		print("XXXXXXXXXXXXXXXZ")
		print("XXXXXXXXXXXXXXXZ")
		print("XXXXXXXXXXXXXXXZ")
		print("XXXXXXXXXXXXXXXZ")
		print("XXXXXXXXXXXXXXXZ")
		# if "users" not in self.db:
		# 	self.db["users"] = {}
		#
		# if user not in self.db["users"]:
		# 	self.db["users"][user] = user
		# 	self.api.send(origin, "WELCOME "+user)
		# 	self.backup()

		#
		# res = self.master.driver.send_message_with_thumbnail(path,origin,url=myLink,title="Invite to "+groupName,description="BBBBBBBB",text="This is a link to join: "+groupName+" \n"+str(myLink)+"\nPlease check it out :)")


		# self.api.send(origin, sendBack)

		# self.db["upcoming"].append([origin, sendBack])


	def backup(self):
		self.api.backup(self.db)

	def updateDB(self, db):
		self.db = db


	def makeDirs(self, filename):
		if not os.path.exists(os.path.dirname(filename)):
		    try:
		        os.makedirs(os.path.dirname(filename))
		    except OSError as exc: # Guard against race condition
		        if exc.errno != errno.EEXIST:
		            raise

	def download_image(self, service="test", pic_url="https://img-authors.flaticon.com/google.jpg", img_name = 'thumnail.jpg'):
		if service is None or pic_url is None or img_name is None:
			return None

		final_path = service+"/"+img_name
		self.makeDirs(final_path)
		with open(final_path, 'wb') as handle:
		        response = requests.get(pic_url, stream=True)
		        if not response.ok:
		            print(response)
		        for block in response.iter_content(1024):
		            if not block:
		                break
		            handle.write(block)

		return os.path.abspath(final_path)

	# def send(self, api, service, target, content, thumnail = None):
	# 	sendThread = Thread(target = self.sendAsync, args = [[api, service, target, content, thumnail]])
	# 	sendThread.start()
	# #UX WELCOME AFTER SUBSCIBING TO
	# def sendAsync(self, data):
	# 	api, service, target, content, thumbnail = data
	# 	print("!!!!!!!!!!!!")
	# 	if service in self.master.services:
	# 		if self.master.services[service]["api"] is api:
	# 			if target in self.master.db["groups"] and "service" in self.master.db["groups"][target] and service.lower() == self.master.db["groups"][target]["service"].lower():
	# 				if thumbnail is not None:
	# 					print("T T T T T T")
	# 					print("T T T T T T")
	# 					print("T T T T T T")
	# 					imageurl = "https://media1.tenor.com/images/7528819f1bcc9a212d5c23be19be5bf6/tenor.gif"
	# 					title = "AAAAAAAAAA"
	# 					desc = "BBBBBBB"
	# 					link = imageurl
	# 					if "imageurl" in thumbnail:
	# 						imageurl = thumbnail["imageurl"]
	# 					if "title" in thumbnail:
	# 						title = thumbnail["title"]
	# 					if "desc" in thumbnail:
	# 						desc = thumbnail["desc"]
	# 					if "link" in thumbnail:
	# 						link = thumbnail["link"]
	#
	# 					path = self.download_image(service = service, pic_url=imageurl)
	#
	# 					# metadata = self.master.driver.get_group_metadata(target)
	# 					# print()
	# 					# print(metadata)
	# 					# print()
	#
	# 					res = self.master.driver.send_message_with_thumbnail(path,target,url=link,title=title,description=desc,text=content)
	# 					print(res)
	# 					print("!!!!!!!!!!!!!!")
	# 					return res
	# 				return self.master.driver.sendMessage(target, content)

	def loadDB(self, number = None):
		if number is None:
			number = self.master.db["id"]
		return self.master.driver.loadDB(number = number)
	#
	# def backupService(self, db = None, service = None, api = None):
	# 	data = [db,service]
	# 	# self.backupServiceAsync(data)
	# 	if service in self.master.services:
	# 		if self.master.services[service]["api"] is api:
	# 			bT = Thread(target = self.backupServiceAsync,args = [data])
	# 			bT.start()
	#
	# def backupServiceAsync(self,data):
	# 	time.sleep(self.master.db["backupDelay"])
	# 	db, service = data
	# 	print("SSSSSSSSS",service,db)
	# 	if time.time() - self.master.db["lastBackupServices"] < self.master.db["backupInterval"]:
	# 		return False
	#
	# 	if service is None or len(service) == 0:
	# 		return None
	#
	# 	backupChat = None
	# 	if service in self.master.db["servicesDB"]:
	# 		chatID = self.master.db["servicesDB"][service]["dbID"]
	# 		if chatID is not None:
	# 			bchat = None
	# 			try:
	# 				bchat = self.master.driver.getChat(chatID)
	# 			except Exception as e:
	# 				print(" ::: ERROR - COULD NOT GET BACKUPCHAT",e," ::: ","\n")
	# 				traceback.print_exc()
	# 			if bchat is not None:
	# 				print("FFFFFFFFFFFFFFFUCKKK")
	# 				# self.master.driver.sendMessage(chatID,"FFFFFFFFFFFFFFFUCKKK")
	#
	# 				backupChat = chatID
	# 		else:
	# 			print(" ::: ERROR - SERVICE HAS NO BACKUPCHAT"+" ::: ","\n")
	#
	#
	# 	if backupChat is not None:
	# 		if db is not None:
	# 			return self.master.driver.updateDB(db,number=backupChat)
	# 		else:
	# 			return self.loadDB(backupChat)
	# 	else:
	# 		print(" ::: ERROR - BackupChat NOT FOUND for :"+service+": service ::: \n")
	# 	self.master.db["lastBackupServices"] = time.time()

	# def backup(self, now = None):
	# 	bT = Thread(target = self.backupAsync,args = [now])
	# 	bT.start()
	#
	# def backupAsync(self,data):
		now = data
		if now is None:
			time.sleep(self.master.db["backupDelay"])
			if time.time() - self.master.db["lastBackup"] < self.master.db["backupInterval"]:
				return False
		self.master.db["lastBackup"] = time.time()
		return self.master.driver.updateDB(self.master.db,number=self.master.db["id"])




	def quit(self):
		self.master.driver.quit()

	def Nothing(data):
		print(":::Nothign::: DATA=",data)

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
	# def ProcessIncoming0(self, data):
	# 	print(
	# 	'''
	# 	===================================
	# 		Processing Incoming Messages
	# 	===================================
	# 	'''
	# 	)
	# 	lastm = None
	# 	loopc = 0
	# 	delay = 0.5
	# 	while True:
	# 		# try:
	# 		if True:
	# 			if loopc % 20 == 0:
	# 				''' ::: rechecking status ::: '''
	# 				try:
	# 					self.status = status = self.master.driver.get_status()
	# 					print(" ::: status is",status,"::: ")
	# 				except Exception as e:
	# 					self.status = status = "XXXXXXXX"
	# 					print(" ::: ERROR - Status Fetching ::: ","\n",e,e.args,"\n")
	#
	#
	# 			''' all unread messages '''
	# 			for contact in self.master.driver.get_unread():
	#
	# 				self.Process(contact)
	#
	#
	# 				'''
	# 				lastm = message
	# 				print(json.dumps(message.get_js_obj(), indent=4))
	# 				for contact in self.master.driver.get_contacts():
	# 					# print("CCCC",contact.get_safe_name() )
	# 					if  sender in contact.get_safe_name():
	# 						chat = contact.get_chat()
	# 						# chat.send_message("Hi "+sender+" !!!*"+message.content+"*")
	# 				print()
	# 				print()
	# 				print(sender)
	# 				print()
	# 				print()
	# 				print("class", message.__class__.__name__)
	# 				print("message", message)
	# 				print("id", message.id)
	# 				print("type", message.type)
	# 				print("timestamp", message.timestamp)
	# 				print("chat_id", message.chat_id)
	# 				print("sender", message.sender)
	# 				print("sender.id", message.sender.id)
	# 				print("sender.safe_name", message.sender.get_safe_name())
	# 				if message.type == "chat":
	# 					print("-- Chat")
	# 					print("safe_content", message.safe_content)
	# 					print("content", message.content)
	# 					# Manager.process(message.sender.id,message.content)
	# 					# contact.chat.send_message(message.safe_content)
	# 				elif message.type == "image" or message.type == "video":
	# 					print("-- Image or Video")
	# 					print("filename", message.filename)
	# 					print("size", message.size)
	# 					print("mime", message.mime)
	# 					print("caption", message.caption)
	# 					print("client_url", message.client_url)
	# 					message.save_media("./")
	# 				else:
	# 					print("-- Other type:",str(message.type))
	# 				print("PROCESSING MESSAGE:",message)
	# 				'''
	#
	# 		else:
	# 			pass
	# 		# except Exception as e:
	# 		# 	print(" ::: ERROR - CHECKING MESSAGES ::: ","\n",e,e.args,"\n")
	#
	# 		loopc += 1; loopc = loopc % 120
	# 		time.sleep(delay)
	#
	# def initServicesDB0(self):
	# 	for service in self.master.services:
	# 		# try:
	# 		if True:
	# 			if "servicesDB" not in self.master.db:
	# 				self.master.db["servicesDB"] = {}
	#
	# 			if service not in self.master.db["servicesDB"]:
	# 				self.master.db["servicesDB"][service] = {}
	#
	# 			if "dbID" not in self.master.db["servicesDB"][service]:
	# 				self.master.db["servicesDB"][service]["dbID"] = None
	#
	# 			dbID = self.master.db["servicesDB"][service]["dbID"]
	# 			''' create new db group '''
	# 			db = {}
	# 			if dbID is None:
	# 				print("-------------------------------")
	# 				print("     CREATING NEW DB GROUP   "+service)
	# 				print("-------------------------------")
	# 				groupName = service
	#
	# 				newGroup = self.master.driver.newGroup(newGroupName = service+"_DB", number = "+"+self.master.db["masters"][1], local = self.runLocal)
	# 				newGroupID = newGroup.id
	# 				self.master.db["servicesDB"][service]["dbID"] = newGroupID
	# 				db = {"init":True}
	# 				self.master.driver.sendMessage(newGroupID, json.dumps(db))
	# 				self.backup()
	# 			else:
	# 				db = self.loadDB(dbID)
	#
	# 			print("-------------------------------")
	# 			print("service: ",service,"  dbID: ",dbID)
	# 			print("-------------------------------")
	# 			print(db)
	# 			# while()
	# 			self.master.services[service]["obj"].updateDB(db)
	#
	# 		# except Exception as e:
	# 		else:
	# 			print(" ::: ERROR - LOAD SERVICES ::: ","\n",e,e.args,"\n")
	#
	# def LoadServices0(self):
	# 	# load list of services
	# 	for service in self.master.db["services"]:
	#
	#
	# 		if "reminders".lower() == service.lower():
	# 			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
	# 			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
	# 			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
	# 			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
	# 			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
	# 			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
	# 			ReminderService.go(sendDelegate=self.master.driver.sendMessage,backupDelegate=self.backupService)
	# 			self.serviceFuncs["services"][service]=ReminderService.process
	# 			groupName = "🔔 Reminders 🔔"
	# 			self.serviceGroupNames[service] = groupName
	# 			self.master.db["services"][service]["welcome"] = ReminderService.welcome
	# 			self.master.db["services"][service]["groupName"] = groupName
	# 			# self.serviceGroupNames[service] = "Reminders"
	#
	#
	# 		if "danilator".lower() == service.lower():
	# 			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
	# 			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
	# 			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
	# 			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
	# 			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
	# 			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
	# 			DanilatorService.go(sendDelegate=self.master.driver.sendMessage,backupDelegate=self.backupService)
	# 			self.serviceFuncs["services"][service]=DanilatorService.process
	# 			groupName = "💚 Danilator 💚"
	# 			self.serviceGroupNames[service] = groupName
	# 			self.master.db["services"][service]["welcome"] = DanilatorService.welcome
	# 			self.master.db["services"][service]["groupName"] = groupName
	#
	#
	# 			# self.serviceGroupNames[service] = "Danilator"
	#
	# 		try:
	# 			if "dbID" not in self.master.db["services"][service]:
	# 				self.master.db["services"][service]["dbID"] = None
	#
	# 			dbID = self.master.db["services"][service]["dbID"]
	# 			''' create new db group '''
	# 			if dbID is None:
	# 				print("-------------------------------")
	# 				print("     CREATING NEW DB GROUP   "+service)
	# 				print("-------------------------------")
	# 				groupName = service
	#
	# 				newGroup = self.master.driver.newGroup(newGroupName = service+"_DB", number = "+"+self.master.db["masters"][1], local = self.runLocal)
	# 				newGroupID = newGroup.id
	# 				self.master.db["services"][service]["dbID"] = newGroupID
	# 				self.master.driver.sendMessage(newGroupID, json.dumps({"init":True}))
	# 				self.backup()
	# 			else:
	# 				print("-------------------------------")
	# 				print("service: ",service,"  dbID: ",dbID)
	# 				print("-------------------------------")
	#
	# 		except Exception as e:
	# 			print(" ::: ERROR - LOAD SERVICES ::: ","\n",e,e.args,"\n")
	#
	# def initAsync0(self, profileDir = "/app/session/rprofile2"):
	#
	# 	''' init driver variables '''
	# 	if len(Master.shares) > 1:
	# 		profileDir += "-"+str(len(Master.shares))
	# 	chrome_options = webdriver.ChromeOptions()
	# 	chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
	# 	chrome_options.add_argument("--headless")
	# 	chrome_options.add_argument("--disable-dev-shm-usage")
	# 	chrome_options.add_argument("--no-sandbox")
	# 	chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
	# 	chrome_options.add_argument("user-data-dir="+profileDir);
	# 	chrome_options.add_argument('--profile-directory='+profileDir)
	#
	# 	if not self.runLocal:
	# 		self.master.driver = WhatsAPIDriver(profile = profileDir, client='chrome', chrome_options=chrome_options,username="wholesomegarden")
	# 	else:
	# 		self.master.driver = WhatsAPIDriver(username="wholesomegarden",profile=None)
	# 	driver = self.master.driver
	#
	# 	print(''' ::: waiting for login ::: ''')
	# 	driver.wait_for_login()
	# 	try:
	# 		self.status = status = driver.get_status()
	# 	except Exception as e:
	# 		print(" ::: ERROR - Status Init ::: ","\n",e,e.args,"\n")
	#
	# 	''' preping for qr '''
	# 	if status is not "LoggedIn":
	# 		img = None
	# 		triesCount = 0
	# 		maxtries = 40
	#
	# 		while status is not "LoggedIn" and triesCount < maxtries:
	# 			triesCount+=1
	#
	# 			print("-------------------------------")
	# 			print("status:",status,"tries:",triesCount,"/",maxtries)
	# 			print("-------------------------------")
	#
	# 			self.lastQR += 1
	# 			try:
	# 				img = driver.get_qr("static/img/QR"+str(self.lastQR)+".png")
	# 				print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
	# 				print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
	# 				print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
	# 				print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
	# 				print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
	# 				print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
	# 				print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ",str(img)[17:130])
	#
	# 			except Exception as e:
	# 				print(" ::: ERROR - QR Fetching ::: ","\n",e,e.args,"\n")
	#
	# 			# im_path = os.path.join("static/img/newQR.png")
	#
	# 			print(''' ::: rechecking status ::: ''')
	# 			try:
	# 				self.status = status = driver.get_status()
	# 			except Exception as e :
	# 				self.status = status = "XXXXXXXX"
	# 				print(" ::: ERROR - Status Fetching ::: ","\n",e,e.args,"\n")
	#
	# 	if status is "LoggedIn":
	# 		print(''' :::::::::::::::::::::::::::::::::::: ''')
	# 		print(''' :::::::::::::::::::::::::::::::::::: ''')
	# 		print(''' ::::                           ::::: ''')
	# 		print(''' ::::   MASTER IS LOGGED IN!    ::::: ''')
	# 		print(''' ::::                           ::::: ''')
	# 		print(''' :::::::::::::::::::::::::::::::::::: ''')
	# 		print(''' :::::::::::::::::::::::::::::::::::: ''')
	# 		# if self.runLocal:
	# 		# 	self.master.driver.save_firefox_profile(remove_old=False)
	#
	# 		''' load DB '''
	# 		## overwrite to init db
	# 		initOverwrite = False
	# 		if initOverwrite:
	# 			self.backup(now = True)
	# 		# driver.updateDB(self.master.db,number=self.master.db["id"])
	# 		lastDB = self.loadDB()
	# 		self.master.db = lastDB
	# 		self.master.db["init"] = time.time()
	# 		self.master.db["backupInterval"] = 10*60
	# 		if self.runLocal:
	# 			self.master.db["backupInterval"] = 0
	#
	# 		self.master.db["backupDelay"] = 10
	# 		if self.runLocal:
	# 			self.master.db["backupDelay"] = 3
	#
	# 		self.master.db["lastBackup"] = 0
	# 		self.master.db["lastBackupServices"] = 0
	# 		self.backup()
	# 		print(''' :::::::::::::::::::::::::::::::::::: ''')
	# 		print(''' :::::::::::::::::::::::::::::::::::: ''')
	# 		print(''' ::::                           ::::: ''')
	# 		print(''' ::::     DATABASE LOADED       ::::: ''')
	# 		print(''' ::::                           ::::: ''')
	# 		print(''' :::::::::::::::::::::::::::::::::::: ''')
	# 		print(''' :::::::::::::::::::::::::::::::::::: ''')
	# 		print(self.master.db)
	# 		print()
	# 		#
	# 		''' Load Services '''
	# 		# print("SSSSSSSSSSSSSSSSSSSSs")
	# 		self.LoadServices()
	# 		# print("SSSSSSSSSSSSSSSSSSSSs")
	#
	# 		''' process incoming '''
	# 		process = Thread(target = self.ProcessIncoming, args=[None])
	# 		process.start()
	# 	else:
	# 		print(" ::: ERROR - COULD NOT LOG IN  ::: ","\n")
	#
	# def ProcessServiceAsync0(self, obj, info):
	# 	serviceT = Thread(target = self.ProcessService, args = [[obj,info]])
	# 	serviceT.start()
	#
	# def ProcessService0(self, data):
		# try:
		# service, chatID, text = data
		# obj, info = data
		# obj.process(info)
		# self.serviceFuncs["services"][service](chatID, text)

		# except Exception as e:
		# 	print(" ::: ERROR - Processing Service ::: ",serice,":::",chatID,":::",text,":::","\n",e,e.args,"\n")


# ''' running master '''
# master = None
# timeout = time.time()
# maxtimeout = 30
# while master is None and time.time()-timeout < maxtimeout:
# try:
# # if True:
# 	# master = Master()
# 	# print("9999999999999999999999999999")
# 	# print("9999999999999999999999999999")
# 	# print("9999999999999999999999999999")
# 	# print("9999999999999999999999999999")
#
# 	maxtimeout = 0
#
# # else:
# # 	pass
# except Exception as e:
# 	print(" ::: ERROR - init Master ::: ","\n",e,e.args,"\n")


#
# ''' running front server '''
# from flask import Flask, render_template, redirect
#
# app = Flask(__name__,template_folder='templates')
#
# qrfolder = os.path.join('static', 'img')
# app.config['QR_FOLDER'] = qrfolder
#
# ''' setting referals '''
# refs = {"yo":"https://api.WhatsApp.com/send?phone=+972512170493"}
# refs["yoo"] = "https://web.WhatsApp.com/send?phone=+972512170493"
#
# @app.route('/')
# def hello_world():
# 	master = Master.shares[0]
# 	full_filename = os.path.join(app.config['QR_FOLDER'], "QR"+str(master.lastQR)+".png")
# 	if master.status == "LoggedIn":
# 		return render_template("loggedIn.html", user_image = full_filename, status = master.status)
# 	else:
# 		return render_template("index.html", user_image = full_filename, status = master.status)
#
# @app.route('/<path:text>', methods=['GET', 'POST'])
# def all_routes(text):
# 	if "exit" in text:
# 		print("EXITTT")
# 		print("EXITTT")
# 		print("EXITTT")
# 		print("EXITTT")
# 		return redirect("https://chat.whatsapp.com/JmnYDofCd7v0cXzfBgcVDO")
# 		return render_template("exit.html", user_image = "full_filename", status = "s")
#
#
# 	if text in refs:
# 		return redirect(refs[text])
# 	else:
# 		return redirect("/")
#
#
# #
# # if __name__ == '__main__':
# # 	print(
# # 	'''
# # 	===================================
# # 		   Running Front Server
# # 	===================================
# # 	'''
# # 	)
# # 	app.run(debug=True, host='0.0.0.0',use_reloader=False)
# # else:
# # 	print("################################")
# # 	print("################################")
# # 	print("################################")
# # 	print("################################")
# # 	print("################################")
# # 	print("################################")
# #
#
# def flaskRun(master):
# 	print("GONNA RUN ASYNC")
# 	print("GONNA RUN ASYNC")
# 	print("GONNA RUN ASYNC")
# 	print("GONNA RUN ASYNC")
# 	print("GONNA RUN ASYNC")
# 	print("GONNA RUN ASYNC")
# 	print("GONNA RUN ASYNC")
# 	print("GONNA RUN ASYNC")
# 	global running
# 	# if reminder.runners < 1 and running < 1:
# 	if True:
# 		# running += 1
# 		# reminder.runners += 1
# 		t = Thread(target=flaskRunAsync,args=[master,])
# 		t.start()
# 	else:
# 		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
# 		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
# 		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
# 		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
# 		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
# 		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
# 		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
# 	print("AFTER GONNA RUN ASYNC")
# 	print("AFTER GONNA RUN ASYNC")
# 	print("AFTER GONNA RUN ASYNC")
# 	print("AFTER GONNA RUN ASYNC")
#
#
# def flaskRunAsync(data):
# 	master = data
# 	# input()
# 	print("AAAAAAAAAAAA ASYNC")
# 	print("AAAAAAAAAAAA ASYNC")
# 	print("AAAAAAAAAAAA ASYNC")
# 	print("AAAAAAAAAAAA ASYNC")
# 	print("AAAAAAAAAAAA ASYNC")
# 	print("AAAAAAAAAAAA ASYNC")
# 	print("AAAAAAAAAAAA ASYNC")
# 	master = Master()
# 	master = Master.shares[0]
# 	print("9999999999999999999999999999")
# 	print("9999999999999999999999999999")
# 	print("9999999999999999999999999999")
# 	print("9999999999999999999999999999")
#
#
#
# if __name__ == '__main__':
# 	flaskRun(master)
# 	print("STARTING APP")
# 	# print("STARTING APP")
# 	# print("STARTING APP")
# 	# print("STARTING APP")
# 	# print("STARTING APP")
# 	if self.runLocal :
# 		pass
# 		app.run(debug=True, host='0.0.0.0',use_reloader=False)
# 	# app.run(debug=True, host='0.0.0.0',use_reloader=False)
# else:
# 	flaskRun(master)
# 	if self.runLocal :
# 		pass
# 		app.run(debug=True, host='0.0.0.0',use_reloader=False)
# 	# app.run(debug=True, host='0.0.0.0',use_reloader=False)
# 	print("STARTING APP22222222222")
# 	# print("STARTING APP22222222222")
# 	# print("STARTING APP22222222222")
# 	# print("STARTING APP22222222222")
# 	# print("STARTING APP22222222222")
# 	# print("STARTING APP22222222222")
