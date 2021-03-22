# pastebin.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import os, time
import requests
import json


runFlask = True


from flask import Flask, render_template, redirect
# app = Flask(__name__)
app=Flask(__name__,template_folder='templates')

refs = {}
refs["yo"] = "ALLRIGHT!"
refs["fuckyea"] = "nice"
refs["dani"] = "is cool!"



@app.route('/<path:text>', methods=['GET', 'POST'])
def all_routes(text):
	if text in refs:
		return redirect("https://api.WhatsApp.com/send?phone=+972512170493&text="+refs[text])
	else:
		return redirect("https://error.com")

@app.route('/')
def hello_world():
	# full_filename = os.path.join(app.config['UPLOAD_FOLDER'], "QR"+str(reminder.lastQR)+".png")
	full_filename = "xxx"
	if "reminder.status" == "LoggedIn":
		return render_template("loggedIn.html", user_image = full_filename, status = "reminder.status")
	else:
		return render_template("index.html", user_image = full_filename, status = "reminder.status")


if runFlask:
	app.run(debug=True, host='0.0.0.0')

# chrome_options.add_argument("user-data-dir=session.default");

# driver1 = webdriver.Firefox(firefox_profile="session.default")


from webwhatsapi import WhatsAPIDriver
driver = WhatsAPIDriver(username="wholesomegarden",profile=None)


db = driver.getDB()

db["update"] = True
driver.updateDB(db)

newDB =  driver.getDB()
newDB
db = driver.getDB()

db["update"] = True
driver.updateDB(db)

newDB =  driver.getDB()
newDB

# dbChat = driver.getChat("DB")


#
# send = dictToJson(refs)
# send


#
# updateDB(refs)
#
# driver = WhatsAPIDriver(username="wholesomegarden",profile=None)
#
# db = getDB()
# db
#



json_msg = json.dumps(lastMsg, indent = 0)
json_msg

db = getDB()


driver1 = webdriver.Firefox()
from selenium.webdriver.common.by import By



def tryOut(target, args, timeout = 3, click = False):
	res = None
	t = time.time()
	while(res is None and time.time() - t < timeout):
		try:
			res = target(args)
		except Exception as e:
			print("EEEEEEEEEEEEE",args,"---",e)
			# print(e)
			# print()
			time.sleep(1)
	if click and res is not None:
		again = True
		t2 = time.time()
		while(again and time.time() - t2 < timeout):
			try:
				res.click()
				again = False
			except Exception as e:
				again = True
				print("EEEEEEEEEEEEE","click","---",e)
			# print()
	return res



driver1.get("https://web.whatsapp.com")
driver1.get("https://web.whatsapp.com/send?phone=+972585222444")
'''
<li tabindex="-1" class="_1uAPO _2AkAt _14FXT" data-animate-dropdown-item="true" style="opacity: 1;">
<div class="_1OwwW _3oTCZ" role="button" title="New group">New group</div></li>

# newgroup = driver.find_element_by_xpath("//span[@title='{}']".format(name))
# newgroup.click()
<div aria-disabled="false" role="button" tabindex="0" title="Menu"><span data-testid="menu" data-icon="menu" class=""><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="currentColor" d="M12 7a2 2 0 1 0-.001-4.001A2 2 0 0 0 12 7zm0 2a2 2 0 1 0-.001 3.999A2 2 0 0 0 12 9zm0 6a2 2 0 1 0-.001 3.999A2 2 0 0 0 12 15z"></path></svg></span></div>
'''
# dots = driver.find_element_by_xpath("//form[input/@name='emailId/mobileNo']")

dots = driver1.find_element_by_xpath("//span[@data-testid='menu']")
dots.click()


# panel = tryOut(driver1.find_element_by_class_name,'_3LtPa',click=True)

def newGroup(driver1,
f = 1,
newGroupName = 'New Group Name',
number = "+972512170493"
):
	for a in range(f):
		dots = tryOut(driver1.find_element_by_xpath,"//span[@data-testid='menu']",click=True)
		newgroup = tryOut(driver1.find_element_by_tag_name,'li', click=True)
		input = tryOut(driver1.find_element_by_tag_name,'input',click=True)
		input.send_keys(number+Keys.ENTER+Keys.ENTER)
		# txt = tryOut(input.send_keys,"+972512170493")
		# txt = tryOut(input.send_keys,Keys.ENTER)
		# contact = tryOut(driver1.find_element_by_class_name,'q2PP6',click=True)
		# next = tryOut(driver1.find_element_by_class_name,'_2_g1_',click=True)
		nameInput = tryOut(driver1.find_element_by_class_name,'_1awRl',click=True)
		nameInput.send_keys(newGroupName+Keys.ENTER)




# create = tryOut(driver1.find_element_by_class_name,'_3kOoC',click=True)
newGroup(driver1, f = 3)

newGroup(driver1, f = 3, newGroupName = '<3',
number = "+972549147262")

'''
https://api.WhatsApp.com/send?phone='+972585222444'
https://web.WhatsApp.com/send?phone='+972585222444&text=ho yea'
'''

# input.send_keys("+972512170493")

heading = driver1.find_element_by_tag_name('li')
heading.click()
# heading.send_keys("+972512170493")

input = driver1.find_element_by_tag_name('input')


input.send_keys("+972512170493")
first1 = driver1.find_element_by_class_name('_1MZWu')
first1.click()



first2 = driver1.find_element_by_class_name('q2PP6')
first2.click()

first3 = driver1.find_element_by_class_name('_2_g1_')
first3.click()

firstx = driver1.find_element_by_class_name('_1awRl')
firstx.click()
firstx.send_keys("+972512170493")


first4 = driver1.find_element_by_class_name('_3kOoC')
first4.click()


input()
print("ARE YOU THIN YET ?")


if False:
	driver1.get("https://accounts.random.org/")

	print(driver1.page_source)

	try:
		block = driver1.find_element_by_id("account-overview-block")
		print("==========================")
		print(" LOGGED IN!!!!!!!!! A",block)
		print("==========================")
	except:
		print("==========================")
		print(" NO BLOCK LOGGED OUT A ")
		print("==========================")


	username = driver1.find_element_by_id("login-login")
	password = driver1.find_element_by_id("login-password")
	# btn   = driver1.find_element_by_css_selector("button.btn btn-primary")

	username.send_keys("takeyo")
	password.send_keys("12345678abcd")
	password.send_keys(Keys.ENTER)
	# Step 4) Click Login
	time.sleep(5)
	block = driver1.find_element_by_id("account-overview-block")


	try:
		block = driver1.find_element_by_id("account-overview-block")
		print("==========================")
		print(" LOGGED IN!!!!!!!!! B",block)
		print("==========================")
	except:
		print("==========================")
		print(" NO BLOCK LOGGED OUT B")
		print("==========================")
