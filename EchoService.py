#Service.py
import time

class EchoService(object):
	id = "Echo"
	name = "Echo!"
	welcome = "Welcome to Echo! Service \nWe echo what you send..."
	help = "send a message to get it back"
	imageurl = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmaJKloEMiBpQRA9woJw4XnuWXCWeN2BO70w&usqp=CAU"
	shortDescription = "Echo Echo Echo"
	share = None

	examples = {"services":{"text":"Show Public Services","thumbnail":None}}

	def __init__(self,db, api):
		EchoService.share = self

		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Echo",EchoService.share)
		self.db = db
		self.api = api
		if "upcoming" not in self.db:
			self.db["upcoming"] = []
		if "users" not in self.db:
			self.db["users"] = {}

	def go(self):
		while(True):
			if "upcoming" not in self.db:
				self.db["upcoming"] = []
			if "users" not in self.db:
				self.db["users"] = {}

			while len(self.db["upcoming"]) > 0:
				item = self.db["upcoming"].pop(0)
				origin, content = item
				self.api.send(origin, content, autoPreview = True)
				# self.api.send(origin, content, thumnail = "test")
				# self.api.backup(self.db)

			time.sleep(1)

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

		if user not in self.db["users"]:
			self.db["users"][user] = user
			self.api.send(origin, "WELCOME "+user)
			self.backup()

		sendBack = content

		withLink = True
		if withLink:
			answer = ":answerid:555"
			myLink = self.api.genLink(origin, answer)
			sendBack += "\n\n"+answer+":\n"+myLink

		self.db["upcoming"].append([origin, content])
		# self.db["upcoming"].append([origin, sendBack])


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
