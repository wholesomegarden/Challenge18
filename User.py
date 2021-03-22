# User.py
from Conv import Conv
from Reminder import Reminder
import json

class User():
	id = -1
	isNumber = False
	prefs = {}
	reminders = {}
	remCount = 0
	conv = None
	lastRem = None

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__,
			sort_keys=True, indent=0)

	def checkNum(id):
		return str.isnumeric(id)


	def jsonUsersToUsers(d):
		# print("dddddddddddddddddddd")
		# print(d)
		# print()
		D = {}
		for u in d:

			try:
				D[u] = User.dictToUser(d[u])
			except Exception as e:
				print("EEEEEEEEEEEEEEEEE usersToJSONusers",e)
				print(d)
				print()
				D[u] = d[u]
		return D

	def usersToJSONusers(d):
		D = {}
		for u in d:
			try:
				D[u] = d[u].toJSON()
			except Exception as e:
				print("EEEEEEEEEEEEEEEEE usersToJSONusers",e)
				print(d)
				print()
				D[u] = str(d[u])
		return D

	def dictToUser(d):
		# print("##############################")
		# print(d)
		if "class" not in str(type(d)) and "dict" not in str(type(d)):
			return d

		# print(d)
		# print("QQQQQQQQQQQ")

		d = json.loads(d)
		# print("DDDDDDD")
		# print(d)
		lastRem		= d["lastRem"]
		conv		= Conv.dictToConv(d["conv"])
		remCount	= int(d["remCount"])
		reminders	= Reminder.jsonRemsToRems(d["reminders"])
		prefs		= d["prefs"]
		u = User(id, prefs= prefs, reminders = reminders, remCount = remCount, conv = conv, lastRem = lastRem)
		# print("!!!!!!!!!!!!!!!")
		# print(u)
		# print("!!!!!!!!!!!!!!!")
		return u

	def __init__(self,id, prefs= None, reminders = None, remCount = 0, conv = None,lastRem = None):
		id = str(id)
		number = User.checkNum(id)
		if number is not None:
			self.isNumber = True
		self.id = id
		if prefs is None:
			self.prefs = {}
		else:
			self.prefs = prefs
		if reminders is None:
			self.reminders = {"sent":{},"unsent":{}}
		else:
			self.reminders = reminders
		self.remCount = remCount
		self.lastRem = None
		if conv is None:
			self.conv = Conv(id)
		else:
			self.conv = conv




	def markSent(self, remID):
		if remID in self.reminders["unsent"]:
			self.reminders["sent"][remID] = self.reminders["unsent"].pop(remID)
			self.reminders["sent"][remID].sent = True
			## check for repeat
			print("# REMINDER", remID," MARKED SENT!!!", self.reminders["sent"][remID])
			return True
		return False
