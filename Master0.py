# app.py
import os, sys, time
import json
from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webwhatsapi import WhatsAPIDriver

from pprint import pprint

from ServiceImporter import *

# export PATH="$HOME/wholesomegarden/WhatsappReminder:$PATH"
from ServiceLoader import *
from MasterService import *

runLocal = False
print(
'''
:::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::
::::                         ::::
::::    WHATSAPP MASTER      ::::
::::                         ::::
:::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::
'''
)

# runLocal = True
if runLocal:
	print(
	'''
	:::::::::::::::::::::::::::::::::
	::::    RUNNING LOCALLY      ::::
	:::::::::::::::::::::::::::::::::
	'''
	)
	print('export PATH="$HOME/wholesomegarden/WhatsappReminder:$PATH"')


class Master(object):
	shares = []
	db = {
		"masters":["972512170493", "972547932000"],
		"users":{"id":{"services":{"groupID":None}}},
		"services":{"Reminders":{"dbID":None,"incomingTarget":None},"Proxy":{"dbID":None,"incomingTarget":None},"Danilator":{"dbID":None,"incomingTarget":None}},
		"groups": {"id":"service"},
		"id":"972547932000-1610379075@g.us"}
	services = {}

	''' start master driver and log in '''
	def __init__(self, profileDir = "/app/session/rprofile2"):
		Master.shares.append(self)
		self.db = Master.db
		# self.services = ServiceLoader.LoadServices(self)

		self.status = "INIT"
		self.lastQR = 0
		self.driver = None
		self.masterService = None

		asyncInit = Thread(target = self.initAsync,args = [profileDir])
		asyncInit.start()

	def initAsync(self, profileDir = "/app/session/rprofile2"):

		''' init driver variables '''
		if len(Master.shares) > 1:
			profileDir += "-"+str(len(Master.shares))
		chrome_options = webdriver.ChromeOptions()
		chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument("--no-sandbox")
		chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
		chrome_options.add_argument("user-data-dir="+profileDir);
		chrome_options.add_argument('--profile-directory='+profileDir)

		if not runLocal:
			self.driver = WhatsAPIDriver(profile = profileDir, client='chrome', chrome_options=chrome_options,username="wholesomegarden")
		else:
			self.driver = WhatsAPIDriver(username="wholesomegarden",profile=None)
		driver = self.driver

		''' RUNNING MASTER SERVICE '''
		self.masterService = MasterService(runLocal, self.db, self.services, self.driver, self)


		print(''' ::: waiting for login ::: ''')
		driver.wait_for_login()
		try:
			self.status = status = driver.get_status()
		except Exception as e:
			print(" ::: ERROR - Status Init ::: ","\n",e,e.args,"\n")

		''' preping for qr '''
		if status is not "LoggedIn":
			img = None
			triesCount = 0
			maxtries = 40

			while status is not "LoggedIn" and triesCount < maxtries:
				triesCount+=1

				print("-------------------------------")
				print("status:",status,"tries:",triesCount,"/",maxtries)
				print("-------------------------------")

				self.lastQR += 1
				try:
					img = driver.get_qr("static/img/QR"+str(self.lastQR)+".png")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ",str(img)[17:130])

				except Exception as e:
					print(" ::: ERROR - QR Fetching ::: ","\n",e,e.args,"\n")

				# im_path = os.path.join("static/img/newQR.png")

				print(''' ::: rechecking status ::: ''')
				try:
					self.status = status = driver.get_status()
				except Exception as e :
					self.status = status = "XXXXXXXX"
					print(" ::: ERROR - Status Fetching ::: ","\n",e,e.args,"\n")

		if status is "LoggedIn":
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' ::::   MASTER IS LOGGED IN!    ::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			# if runLocal:
			# 	self.driver.save_firefox_profile(remove_old=False)

			''' load DB '''
			## overwrite to init db
			initOverwrite = True
			if initOverwrite:
				self.backup(now = True)
			# driver.updateDB(self.db,number=self.db["id"])
			lastDB = self.loadDB()
			self.db = lastDB
			self.db["init"] = time.time()
			self.db["backupInterval"] = 10*60
			if runLocal:
				self.db["backupInterval"] = 0

			self.db["backupDelay"] = 10
			if runLocal:
				self.db["backupDelay"] = 3

			self.db["lastBackup"] = 0
			self.db["lastBackupServices"] = 0
			self.backup()
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' ::::     DATABASE LOADED       ::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(self.db)
			print()

			self.services = ServiceLoader.LoadServices(self.send, self.backupService)
			self.initServicesDB()
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' ::::     SERVICES LOADED       ::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(self.services)
			print()
			#
			# ''' Load Services '''
			# # print("SSSSSSSSSSSSSSSSSSSSs")
			# self.LoadServices()
			# # print("SSSSSSSSSSSSSSSSSSSSs")

			''' process incoming '''
			process = Thread(target = self.ProcessIncoming, args=[None])
			process.start()
		else:
			print(" ::: ERROR - COULD NOT LOG IN  ::: ","\n")

	def send(self, api, service, target, content):
		print("!!!!!!!!!!!!")
		if service in self.services:
			if self.services[service]["api"] is api:
				if target in self.db["groups"] and service.lower() == self.db["groups"][target].lower():
					return self.driver.sendMessage(target,content)


	def Process(self,contact):
		for message in contact.messages:
			print("MMMMMMMMMM",message)

			if runLocal:
				chatID = message.chat_id["_serialized"]
			else:
				chatID = message.chat_id

			try:
				chat = self.driver.get_chat_from_id(chatID)
			except Exception as e:
				print(" ::: ERROR - _serialized chatID ::: "+chatID+" ::: ","\n",e,e.args,"\n")

			''' incoming from: '''
			''' Personal Chat  '''
			senderName = message.get_js_obj()["chat"]["contact"]["formattedName"]
			senderID = message.sender.id
			fromGroup = False
			if "c" in chatID:

				''' SEND TO MASTER SERVICE '''
				self.masterService.Process(message)

				#
				# print(
				# '''
				# ===================================
				#    Incoming Messages from '''+senderID+" "+senderName+'''
				# ===================================
				# '''
				# )
				# if message.type == "chat":
				# 	text = message.content
				#
				# 	print("TTTTTXXXXXXXXXTTTTTTT",text)
				# 	''' subscribe to service '''
				#
				# 	''' SENT FROM GROUP CHAT '''
				#
				# 	if "%%%!%%%" in text:
				# 		target = text.split(u"%%%!%%%")[1]
				# 		self.driver.sendMessage(chatID,"Adding Service to DB: "+target)
				# 		self.db["services"][target] = {"dbID":None,"incomingTarget":None}
				# 		self.LoadServices()
				# 		# self.serviceFuncs["services"][target] = None
				#
				# 		self.backup(now = True)
				# 	else:
				# 		print("XXXXXXXXXXXXXXXXXXX")
				# 		print("XXXXXXXXXXXXXXXXXXX")
				# 		print("XXXXXXXXXXXXXXXXXXX")
				#
				# 	if text[0] is "=":
				# 		''' person registering service with ='''
				# 		target = text[1:]
				# 		dbChanged = False
				# 		now = False
				#
				# 		''' check target service in db '''
				# 		serviceFound = False
				# 		for service in self.services:
				# 			print("______________ ----------"+service)
				# 			print("")
				# 			if not serviceFound and target.lower() == service.lower():
				# 				target = service
				# 				''' service found '''
				# 				serviceFound = True
				#
				# 				if chatID not in self.db["users"]:
				# 					self.db["users"][chatID] = {}
				# 					dbChanged = True
				# 					''' first time user '''
				# 					# self.db["users"][senderID] = {'services': {'Reminders': {'groupID': None}}}
				# 				else:
				# 					pass
				# 					''' known user '''
				#
				#
				# 				foundChat = None
				# 				if service in self.db["users"][chatID]:
				#
				# 					serviceChat = self.db["users"][chatID][service]
				#
				# 					# self.driver.sendMessage(senderID,"You are already subscirbed to: "+target+" \nYou can unsubscribe with -"+target.lower())
				# 					if serviceChat is not None:
				# 						try:
				# 							foundChat = self.driver.get_chat_from_id(serviceChat)
				# 						except:
				# 							print('chat could not be found')
				#
				#
				# 				chatName = target
				# 				welcome = "Thank you for Subscribing to "+target
				# 				try:
				# 					chatName = self.services[service]["obj"].name
				# 					welcome = "Thank you for Subscribing to "+chatName
				# 					welcome = self.services[service]["obj"].welcome
				# 				except:
				# 					pass
				#
				# 				if foundChat is not None:
				# 					check_participents = False
				# 					if check_participents:
				# 						if senderID in foundChat.get_participants_ids() or True:
				# 							'''##### check that user is participant '''
				# 							self.driver.sendMessage(senderID,"You are already subscirbed to: "+chatName+" \nYou can unsubscribe with -"+target.lower())
				# 							self.driver.sendMessage(serviceChat,"subscirbed to: "+chatName)
				# 						else:
				# 							foundChat = None
				# 					else:
				# 						self.driver.sendMessage(senderID,"You are already subscirbed to:\n"+chatName+" \n<Link>\nYou can unsubscribe with -"+target.lower())
				# 						self.driver.sendMessage(serviceChat,"subscirbed to: "+chatName)
				#
				#
				# 				''' create new group '''
				# 				if foundChat is None:
				# 					groupName = service
				# 					if service in self.services and "obj" in self.services[service] and self.services[service]["obj"] is not None:
				# 						groupName = self.services[service]["obj"].name
				#
				# 					newGroup = self.driver.newGroup(newGroupName = groupName, number = "+"+senderID.split("@")[0], local = runLocal)
				# 					newGroupID = newGroup.id
				# 					self.newG = newGroupID
				#
				# 					self.db["users"][chatID][service] = newGroupID
				# 					self.db["groups"][newGroupID] = target
				# 					dbChanged = True
				# 					now = True
				# 					print(
				# 					'''
				# 					===============================================
				# 					 ''' + senderID +" is NOW SUBSCRIBED TO "+ target +" :D "+'''
				# 					===============================================
				# 					'''
				# 					)
				#
				# 					self.driver.sendMessage(senderID,"Thank you! you are now subscribed to: "+chatName+" \n<Link>\nPlease check your new group :)")
				# 					self.driver.sendMessage(newGroupID,welcome)
				# 					# self.driver.sendMessage(serviceChat,"subscirbed to: "+target)
				#
				# 		if not serviceFound:
				# 			self.driver.sendMessage(chatID,target+" : is not recognized as a service "+target)
				# 			print(
				# 			'''
				# 			===============================================
				# 			  SERVICE '''+ target +" IS NOT AVAILABLE"+'''
				# 			===============================================
				# 			'''
				# 			)
				# 		if dbChanged:
				# 			self.backup(now=now)


			# ''' Group Chat '''
			elif "g" in chatID:
				fromGroup = True
				print(
				'''
				===============================================
				   Incoming Messages in Group \"'''+senderName+" from "+senderID+'''
				===============================================
				'''
				)
				if message.type == "chat":
					text = message.content

					''' GOT REGISTRATION COMMAND '''
					if text[0] is "=":
						foundService = None
						target = text[1:]

						''' register group to service '''
						for service in self.services:
							if target.lower() == service.lower():
								foundService = service

								foundChat = False
								if chatID in self.db["groups"]:
									targetService = self.db["groups"][chatID]
									print("TTTTTTTTTTTTTTTTTTTT")
									print(targetService, service)
									if targetService is not None:
										if targetService.lower() == service.lower():
											foundChat = True
											self.driver.sendMessage(chatID,"You are already subscirbed to: "+target+" \nYou can unsubscribe with -"+target.lower())

								if not foundChat:
									print("SSSSSSSSSSSSSSSSSSSSSSsxxxxx")
									print("SSSSSSSSSSSSSSSSSSSSSSsxxxxx")
									print("SSSSSSSSSSSSSSSSSSSSSSsxxxxx")
									self.driver.sendMessage(chatID,"Subscribing to service: "+service)
									self.db["groups"][chatID] = service
									self.backup()

						if foundService is None:
							self.driver.sendMessage(chatID,"service: "+target+" Not Found")

					''' Chat is not registered first time'''
					if chatID not in self.db["groups"]:
						# print("SSSSSSSSSSSSSSSSSSSSSS")
						self.driver.sendMessage(chatID,"This chat is not registered with any service yet\nYou can register it by sending =service_name")
						# print("JJJJJJJJJJJJJJ")
						self.db["groups"][chatID] = None
						# print("SSSSSSSSSSSSSSSSSSSSSS")
						self.backup()

					if self.db["groups"][chatID] is not None:
						''' Chat is known '''
						target = self.db["groups"][chatID]
						print("MMMMMMMMMMMMMMMM",target)
						''' adding new user to service from group'''

						foundService = None
						for service in self.services:
							if target.lower() == service.lower():
								foundService = service

								''' CHAT IS REGISTERED TO SERVICE! '''
								''' PROCESS INCOMNG MESSAGE in SERVICE '''
								if foundService is not None and text[0] is not "=":

									''' this is where the magic happens - send to service'''

									if "obj" in self.services[foundService]:
										obj = self.services[foundService]["obj"]
										if obj is not None:
											#Get Nicknames

											self.ProcessServiceAsync(obj,{"origin":chatID, "user":senderID, "content":text})
											# obj.process({"origin":chatID, "user":senderID, "content":text})

									# self.ProcessServiceAsync(service,chatID,text)


						if foundService is None:
							self.driver.sendMessage(chatID,target+" : is not recognized as a service "+target)



	def ProcessIncoming(self, data):
		print(
		'''
		===================================
			Processing Incoming Messages
		===================================
		'''
		)
		lastm = None
		loopc = 0
		delay = 0.5
		while True:
			# try:
			if True:
				if loopc % 20 == 0:
					''' ::: rechecking status ::: '''
					try:
						self.status = status = self.driver.get_status()
						print(" ::: status is",status,"::: ")
					except Exception as e:
						self.status = status = "XXXXXXXX"
						print(" ::: ERROR - Status Fetching ::: ","\n",e,e.args,"\n")


				''' all unread messages '''
				for contact in self.driver.get_unread():

					self.Process(contact)


					'''
					lastm = message
					print(json.dumps(message.get_js_obj(), indent=4))
					for contact in self.driver.get_contacts():
						# print("CCCC",contact.get_safe_name() )
						if  sender in contact.get_safe_name():
							chat = contact.get_chat()
							# chat.send_message("Hi "+sender+" !!!*"+message.content+"*")
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
						# Manager.process(message.sender.id,message.content)
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
						print("-- Other type:",str(message.type))
					print("PROCESSING MESSAGE:",message)
					'''

			else:
				pass
			# except Exception as e:
			# 	print(" ::: ERROR - CHECKING MESSAGES ::: ","\n",e,e.args,"\n")

			loopc += 1; loopc = loopc % 120
			time.sleep(delay)






# class Master0(object):
	# print(
	# '''
	# :::::::::::::::::::::::::::::::::
	# :::::::::::::::::::::::::::::::::
	# ::::                         ::::
	# ::::     MASTER DRIVER       ::::
	# ::::                         ::::
	# :::::::::::::::::::::::::::::::::
	# :::::::::::::::::::::::::::::::::
	# '''
	# )

	def initServicesDB(self):
		for service in self.services:
			# try:
			if True:
				if "servicesDB" not in self.db:
					self.db["servicesDB"] = {}

				if service not in self.db["servicesDB"]:
					self.db["servicesDB"][service] = {}

				if "dbID" not in self.db["servicesDB"][service]:
					self.db["servicesDB"][service]["dbID"] = None

				dbID = self.db["servicesDB"][service]["dbID"]
				''' create new db group '''
				db = {}
				if dbID is None:
					print("-------------------------------")
					print("     CREATING NEW DB GROUP   "+service)
					print("-------------------------------")
					groupName = service

					newGroup = self.driver.newGroup(newGroupName = service+"_DB", number = "+"+self.db["masters"][1], local = runLocal)
					newGroupID = newGroup.id
					self.db["servicesDB"][service]["dbID"] = newGroupID
					db = {"init":True}
					self.driver.sendMessage(newGroupID, json.dumps(db))
					self.backup()
				else:
					db = self.loadDB(dbID)

				print("-------------------------------")
				print("service: ",service,"  dbID: ",dbID)
				print("-------------------------------")
				print(db)
				# while()
				self.services[service]["obj"].updateDB(db)

			# except Exception as e:
			else:
				print(" ::: ERROR - LOAD SERVICES ::: ","\n",e,e.args,"\n")




	def LoadServices0(self):
		# load list of services
		for service in self.db["services"]:


			if "reminders".lower() == service.lower():
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				ReminderService.go(sendDelegate=self.driver.sendMessage,backupDelegate=self.backupService)
				self.serviceFuncs["services"][service]=ReminderService.process
				groupName = "🔔 Reminders 🔔"
				self.serviceGroupNames[service] = groupName
				self.db["services"][service]["welcome"] = ReminderService.welcome
				self.db["services"][service]["groupName"] = groupName
				# self.serviceGroupNames[service] = "Reminders"


			if "danilator".lower() == service.lower():
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				DanilatorService.go(sendDelegate=self.driver.sendMessage,backupDelegate=self.backupService)
				self.serviceFuncs["services"][service]=DanilatorService.process
				groupName = "💚 Danilator 💚"
				self.serviceGroupNames[service] = groupName
				self.db["services"][service]["welcome"] = DanilatorService.welcome
				self.db["services"][service]["groupName"] = groupName


				# self.serviceGroupNames[service] = "Danilator"

			try:
				if "dbID" not in self.db["services"][service]:
					self.db["services"][service]["dbID"] = None

				dbID = self.db["services"][service]["dbID"]
				''' create new db group '''
				if dbID is None:
					print("-------------------------------")
					print("     CREATING NEW DB GROUP   "+service)
					print("-------------------------------")
					groupName = service

					newGroup = self.driver.newGroup(newGroupName = service+"_DB", number = "+"+self.db["masters"][1], local = runLocal)
					newGroupID = newGroup.id
					self.db["services"][service]["dbID"] = newGroupID
					self.driver.sendMessage(newGroupID, json.dumps({"init":True}))
					self.backup()
				else:
					print("-------------------------------")
					print("service: ",service,"  dbID: ",dbID)
					print("-------------------------------")

			except Exception as e:
				print(" ::: ERROR - LOAD SERVICES ::: ","\n",e,e.args,"\n")

	def initAsync0(self, profileDir = "/app/session/rprofile2"):

		''' init driver variables '''
		if len(Master.shares) > 1:
			profileDir += "-"+str(len(Master.shares))
		chrome_options = webdriver.ChromeOptions()
		chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument("--no-sandbox")
		chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
		chrome_options.add_argument("user-data-dir="+profileDir);
		chrome_options.add_argument('--profile-directory='+profileDir)

		if not runLocal:
			self.driver = WhatsAPIDriver(profile = profileDir, client='chrome', chrome_options=chrome_options,username="wholesomegarden")
		else:
			self.driver = WhatsAPIDriver(username="wholesomegarden",profile=None)
		driver = self.driver

		self.masterService = MasterService(runLocal, self.db, self.services, self.driver, self)

		print(''' ::: waiting for login ::: ''')
		driver.wait_for_login()
		try:
			self.status = status = driver.get_status()
		except Exception as e:
			print(" ::: ERROR - Status Init ::: ","\n",e,e.args,"\n")

		''' preping for qr '''
		if status is not "LoggedIn":
			img = None
			triesCount = 0
			maxtries = 40

			while status is not "LoggedIn" and triesCount < maxtries:
				triesCount+=1

				print("-------------------------------")
				print("status:",status,"tries:",triesCount,"/",maxtries)
				print("-------------------------------")

				self.lastQR += 1
				try:
					img = driver.get_qr("static/img/QR"+str(self.lastQR)+".png")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ",str(img)[17:130])

				except Exception as e:
					print(" ::: ERROR - QR Fetching ::: ","\n",e,e.args,"\n")

				# im_path = os.path.join("static/img/newQR.png")

				print(''' ::: rechecking status ::: ''')
				try:
					self.status = status = driver.get_status()
				except Exception as e :
					self.status = status = "XXXXXXXX"
					print(" ::: ERROR - Status Fetching ::: ","\n",e,e.args,"\n")

		if status is "LoggedIn":
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' ::::   MASTER IS LOGGED IN!    ::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			# if runLocal:
			# 	self.driver.save_firefox_profile(remove_old=False)

			''' load DB '''
			## overwrite to init db
			initOverwrite = False
			if initOverwrite:
				self.backup(now = True)
			# driver.updateDB(self.db,number=self.db["id"])
			lastDB = self.loadDB()
			self.db = lastDB
			self.db["init"] = time.time()
			self.db["backupInterval"] = 10*60
			if runLocal:
				self.db["backupInterval"] = 0

			self.db["backupDelay"] = 10
			if runLocal:
				self.db["backupDelay"] = 3

			self.db["lastBackup"] = 0
			self.db["lastBackupServices"] = 0
			self.backup()
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' ::::     DATABASE LOADED       ::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(self.db)
			print()
			#
			''' Load Services '''
			# print("SSSSSSSSSSSSSSSSSSSSs")
			self.LoadServices()
			# print("SSSSSSSSSSSSSSSSSSSSs")

			''' process incoming '''
			process = Thread(target = self.ProcessIncoming, args=[None])
			process.start()
		else:
			print(" ::: ERROR - COULD NOT LOG IN  ::: ","\n")


	def loadDB(self, number = None):
		if number is None:
			number = self.db["id"]
		return self.driver.loadDB(number = number)


	def backupService(self, db = None, service = None, api = None):
		data = [db,service]
		# self.backupServiceAsync(data)
		if service in self.services:
			if self.services[service]["api"] is api:
				bT = Thread(target = self.backupServiceAsync,args = [data])
				bT.start()

	def backupServiceAsync(self,data):
		time.sleep(self.db["backupDelay"])
		db, service = data
		print("SSSSSSSSS",service,db)
		if time.time() - self.db["lastBackupServices"] < self.db["backupInterval"]:
			return False

		if service is None or len(service) == 0:
			return None

		backupChat = None
		if service in self.db["servicesDB"]:
			chatID = self.db["servicesDB"][service]["dbID"]
			if chatID is not None:
				bchat = None
				try:
					bchat = self.driver.getChat(chatID)
				except Exception as e:
					print(" ::: ERROR - COULD NOT GET BACKUPCHAT",e," ::: ","\n")
				if bchat is not None:
					print("FFFFFFFFFFFFFFFUCKKK")
					# self.driver.sendMessage(chatID,"FFFFFFFFFFFFFFFUCKKK")

					backupChat = chatID
			else:
				print(" ::: ERROR - SERVICE HAS NO BACKUPCHAT"+" ::: ","\n")


		if backupChat is not None:
			if db is not None:
				return self.driver.updateDB(db,number=backupChat)
			else:
				return self.loadDB(backupChat)
		else:
			print(" ::: ERROR - BackupChat NOT FOUND for :"+service+": service ::: \n")
		self.db["lastBackupServices"] = time.time()



	def backup(self, now = None):
		bT = Thread(target = self.backupAsync,args = [now])
		bT.start()

	def backupAsync(self,data):
		now = data
		if now is None:
			time.sleep(self.db["backupDelay"])
			if time.time() - self.db["lastBackup"] < self.db["backupInterval"]:
				return False
		self.db["lastBackup"] = time.time()
		return self.driver.updateDB(self.db,number=self.db["id"])

	def ProcessServiceAsync(self, obj, info):
		serviceT = Thread(target = self.ProcessService, args = [[obj,info]])
		serviceT.start()

	def ProcessService(self, data):
		# try:
		# service, chatID, text = data
		obj, info = data
		obj.process(info)
		# self.serviceFuncs["services"][service](chatID, text)

		# except Exception as e:
		# 	print(" ::: ERROR - Processing Service ::: ",serice,":::",chatID,":::",text,":::","\n",e,e.args,"\n")


	def ProcessIncoming0(self, data):
		print(
		'''
		===================================
			Processing Incoming Messages
		===================================
		'''
		)
		lastm = None
		loopc = 0
		delay = 0.5
		while True:
			# try:
			if True:
				if loopc % 20 == 0:
					''' ::: rechecking status ::: '''
					try:
						self.status = status = self.driver.get_status()
						print(" ::: status is",status,"::: ")
					except Exception as e:
						self.status = status = "XXXXXXXX"
						print(" ::: ERROR - Status Fetching ::: ","\n",e,e.args,"\n")


				''' all unread messages '''
				for contact in self.driver.get_unread():
					# print("MMMMMMMMMMXXX",contact)
					# print("MMMMMMMMMMXXX",contact)
					# print("MMMMMMMMMMXXX",contact)
					# print("MMMMMMMMMMXXX",contact)
					# print("MMMMMMMMMMXXX",contact)
					for message in contact.messages:
						print("MMMMMMMMMM",message)

						# print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
						# pprint(vars(contact))
						# print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
						# pprint(vars(message))
						# print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
						# print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
						# print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
						if runLocal:
							chatID = message.chat_id["_serialized"]
						else:
							chatID = message.chat_id
						try:
							chat = self.driver.get_chat_from_id(chatID)
						except Exception as e:
							print(" ::: ERROR - _serialized chatID ::: "+chatID+" ::: ","\n",e,e.args,"\n")

						''' incoming from: '''
						''' Personal Chat  '''
						senderName = message.get_js_obj()["chat"]["contact"]["formattedName"]
						senderID = message.sender.id
						fromGroup = False
						if "c" in chatID:
							print(
							'''
							===================================
							   Incoming Messages from '''+senderID+" "+senderName+'''
							===================================
							'''
							)
						# ''' Group Chat '''
						elif "g" in chatID:
							fromGroup = True
							print(
							'''
							===============================================
							   Incoming Messages from \"'''+senderID+" in "+senderName+'''\" GROUP
							===============================================
							'''
							)

						if message.type == "chat":
							text = message.content

							print("TTTTTXXXXXXXXXTTTTTTT",text)
							''' subscribe to service '''

							''' SENT FROM GROUP CHAT '''

							if "%%%!%%%" in text:

								print("YYYYYYYYYYYYYYYYYYYY")
								print("YYYYYYYYYYYYYYYYYYYY")
								print("YYYYYYYYYYYYYYYYYYYY")
								target = text.split(u"%%%!%%%")[1]
								self.driver.sendMessage(chatID,"Adding Service to DB: "+target)
								self.db["services"][target] = {"dbID":None,"incomingTarget":None}
								self.LoadServices()
								# self.serviceFuncs["services"][target] = None

								self.backup(now = True)
							else:
								print("XXXXXXXXXXXXXXXXXXX")
								print("XXXXXXXXXXXXXXXXXXX")
								print("XXXXXXXXXXXXXXXXXXX")



							if fromGroup is True:
								''' GOT REGISTRATION COMMAND '''
								if text[0] is "=":
									foundService = None
									target = text[1:]

									''' register group to service '''
									for service in self.db["services"]:
										if target.lower() == service.lower():
											foundService = service

											foundChat = False
											if chatID in self.db["groups"]:
												targetService = self.db["groups"][chatID]
												print("TTTTTTTTTTTTTTTTTTTT")
												print(targetService, service)
												if targetService is not None:
													if targetService.lower() == service.lower():
														foundChat = True
														self.driver.sendMessage(chatID,"You are already subscirbed to: "+target+" \nYou can unsubscribe with -"+target.lower())

											if not foundChat:
												print("SSSSSSSSSSSSSSSSSSSSSSsxxxxx")
												print("SSSSSSSSSSSSSSSSSSSSSSsxxxxx")
												print("SSSSSSSSSSSSSSSSSSSSSSsxxxxx")
												self.driver.sendMessage(chatID,"Subscribing to service: "+service)
												self.db["groups"][chatID] = service
												self.backup()

									if foundService is None:
										self.driver.sendMessage(chatID,"service: "+target+" Not Found")

								''' Chat is not registered first time'''
								if chatID not in self.db["groups"]:
									# print("SSSSSSSSSSSSSSSSSSSSSS")
									self.driver.sendMessage(chatID,"This chat is not registered with any service yet\nYou can register it by sending =service_name")
									# print("JJJJJJJJJJJJJJ")
									self.db["groups"][chatID] = None
									# print("SSSSSSSSSSSSSSSSSSSSSS")
									self.backup()
								elif self.db["groups"][chatID] is not None:
									''' Chat is known '''
									target = self.db["groups"][chatID]
									print("MMMMMMMMMMMMMMMM",target)
									''' adding new user to service from group'''

									foundService = None
									for service in self.db["services"]:
										if target.lower() == service.lower():
											foundService = service


											''' CHAT IS REGISTERED TO SERVICE! '''
											''' PROCESS INCOMNG MESSAGE in SERVICE '''
											if foundService is not None and text[0] is not "=":
												# self.driver.sendMessage(chatID,text+" ::: GONNA BE PROCESSED BY "+target)

												''' this is where the magic happens - send to service'''
												self.ProcessServiceAsync(service,chatID,text)



									if foundService is None:
										self.driver.sendMessage(chatID,target+" : is not recognized as a service "+target)


								else:
									''' service is None '''
									self.driver.sendMessage(chatID,"You can register this chat by sending =service_name")



							elif text[0] is "=":
								''' person registering service with ='''
								target = text[1:]
								dbChanged = False
								now = False

								''' check target service in db '''
								serviceFound = False
								for service in self.db["services"]:
									print("______________ ----------"+service)
									print("")
									if not serviceFound and target.lower() == service.lower():
										''' service found '''
										serviceFound = True

										if chatID not in self.db["users"]:
											self.db["users"][chatID] = {'services': {}}
											dbChanged = True
											''' first time user '''
											# self.db["users"][senderID] = {'services': {'Reminders': {'groupID': None}}}
										else:
											''' known user '''


										foundChat = None
										if service in self.db["users"][chatID]["services"]:

											serviceChat = self.db["users"][chatID]["services"][service]

											# self.driver.sendMessage(senderID,"You are already subscirbed to: "+target+" \nYou can unsubscribe with -"+target.lower())
											try:
												foundChat = self.driver.get_chat_from_id(serviceChat)

											except:
												print('chat could not be found')


										chatName = target
										welcome = "Thank you for Subscribing to "+target
										try:
											chatName = 	self.db["services"][service]["groupName"]
											welcome = "Thank you for Subscribing to "+chatName
											welcome = self.db["services"][service]["welcome"]
										except:
											pass
										if foundChat is not None:


											check_participents = False
											if check_participents:
												if senderID in foundChat.get_participants_ids() or True:
													'''##### check that user is participant '''
													self.driver.sendMessage(senderID,"You are already subscirbed to: "+chatName+" \nYou can unsubscribe with -"+target.lower())
													self.driver.sendMessage(serviceChat,"subscirbed to: "+chatName)
												else:
													foundChat = None
											else:
												self.driver.sendMessage(senderID,"You are already subscirbed to:\n"+chatName+" \nYou can unsubscribe with -"+target.lower())
												self.driver.sendMessage(serviceChat,"subscirbed to: "+chatName)

										''' create new group '''
										if foundChat is None:
											groupName = service
											if service in self.serviceGroupNames:
												groupName = self.serviceGroupNames[service]

											newGroup = self.driver.newGroup(newGroupName = groupName, number = "+"+senderID.split("@")[0], local = runLocal)
											newGroupID = newGroup.id
											self.newG = newGroupID

											self.db["users"][chatID]['services'][service] = newGroupID
											self.db["groups"][newGroupID] = target
											dbChanged = True
											now = True
											print(
											'''
											===============================================
											 ''' + senderID +" is NOW SUBSCRIBED TO "+ target +" :D "+'''
											===============================================
											'''
											)

											self.driver.sendMessage(senderID,"Thank you! you are now subscribed to: "+chatName+" \nPlease check your new group :)")
											self.driver.sendMessage(newGroupID,welcome)
											# self.driver.sendMessage(serviceChat,"subscirbed to: "+target)

								if not serviceFound:
									self.driver.sendMessage(chatID,target+" : is not recognized as a service "+target)
									print(
									'''
									===============================================
									  SERVICE '''+ target +" IS NOT AVAILABLE"+'''
									===============================================
									'''
									)
								if dbChanged:
									self.backup(now=now)



						'''
						lastm = message
						print(json.dumps(message.get_js_obj(), indent=4))
						for contact in self.driver.get_contacts():
							# print("CCCC",contact.get_safe_name() )
							if  sender in contact.get_safe_name():
								chat = contact.get_chat()
								# chat.send_message("Hi "+sender+" !!!*"+message.content+"*")
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
							# Manager.process(message.sender.id,message.content)
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
							print("-- Other type:",str(message.type))
						print("PROCESSING MESSAGE:",message)
						'''

			else:
				pass
			# except Exception as e:
			# 	print(" ::: ERROR - CHECKING MESSAGES ::: ","\n",e,e.args,"\n")

			loopc += 1; loopc = loopc % 120
			time.sleep(delay)

	def quit(self):
		self.driver.quit()

	def Nothing(data):
		print(":::Nothign::: DATA=",data)



''' running master '''
master = None
timeout = time.time()
maxtimeout = 30
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



''' running front server '''
from flask import Flask, render_template, redirect

app = Flask(__name__,template_folder='templates')

qrfolder = os.path.join('static', 'img')
app.config['QR_FOLDER'] = qrfolder

''' setting referals '''
refs = {"yo":"https://api.WhatsApp.com/send?phone=+972512170493"}
refs["yoo"] = "https://web.WhatsApp.com/send?phone=+972512170493"

@app.route('/')
def hello_world():
	master = Master.shares[0]
	full_filename = os.path.join(app.config['QR_FOLDER'], "QR"+str(master.lastQR)+".png")
	if master.status == "LoggedIn":
		return render_template("loggedIn.html", user_image = full_filename, status = master.status)
	else:
		return render_template("index.html", user_image = full_filename, status = master.status)

@app.route('/<path:text>', methods=['GET', 'POST'])
def all_routes(text):
	if "exit" in text:
		print("EXITTT")
		print("EXITTT")
		print("EXITTT")
		print("EXITTT")
		return redirect("https://chat.whatsapp.com/JmnYDofCd7v0cXzfBgcVDO")
		return render_template("exit.html", user_image = "full_filename", status = "s")


	if text in refs:
		return redirect(refs[text])
	else:
		return redirect("/")


#
# if __name__ == '__main__':
# 	print(
# 	'''
# 	===================================
# 		   Running Front Server
# 	===================================
# 	'''
# 	)
# 	app.run(debug=True, host='0.0.0.0',use_reloader=False)
# else:
# 	print("################################")
# 	print("################################")
# 	print("################################")
# 	print("################################")
# 	print("################################")
# 	print("################################")
#

def flaskRun(master):
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	global running
	# if reminder.runners < 1 and running < 1:
	if True:
		# running += 1
		# reminder.runners += 1
		t = Thread(target=flaskRunAsync,args=[master,])
		t.start()
	else:
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
	print("AFTER GONNA RUN ASYNC")
	print("AFTER GONNA RUN ASYNC")
	print("AFTER GONNA RUN ASYNC")
	print("AFTER GONNA RUN ASYNC")


def flaskRunAsync(data):
	master = data
	# input()
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	master = Master()
	master = Master.shares[0]
	print("9999999999999999999999999999")
	print("9999999999999999999999999999")
	print("9999999999999999999999999999")
	print("9999999999999999999999999999")



if __name__ == '__main__':
	flaskRun(master)
	print("STARTING APP")
	# print("STARTING APP")
	# print("STARTING APP")
	# print("STARTING APP")
	# print("STARTING APP")
	if runLocal :
		pass
		app.run(debug=True, host='0.0.0.0',use_reloader=False)
	# app.run(debug=True, host='0.0.0.0',use_reloader=False)
else:
	flaskRun(master)
	if runLocal :
		pass
		app.run(debug=True, host='0.0.0.0',use_reloader=False)
	# app.run(debug=True, host='0.0.0.0',use_reloader=False)
	print("STARTING APP22222222222")
	# print("STARTING APP22222222222")
	# print("STARTING APP22222222222")
	# print("STARTING APP22222222222")
	# print("STARTING APP22222222222")
	# print("STARTING APP22222222222")
