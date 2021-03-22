'''

    WAPY - PYTHON - V.1.3
+------------------------+
WhatsApp Python automation.
Developed by qq8 & robby.
+------------------------+

'''

# Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colors import printc
import os
import time
import random
import json

# Variables
class Variables:
    executable_path = 'chromedriver.exe'
    old_element = None
var = Variables()

# WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=var.executable_path, options=options)

# Functions
def init(driver=driver):
    '''
    Initialized WAPY.
    Firstly starts chromedriver and gets https://web.whatsapp.com/.
    Secondly waits until QR-CODE is scanned.
    '''

    printc('[W] Initializing WAPY...', 'magenta')

    driver.get('https://web.whatsapp.com/')

    try:
        qr_code_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[2]/div[1]/div/div[2]/div/canvas'))
        )
    except:
        return printc('[-] ERROR: QR-CODE cannot get found.', 'red')
    

    while True:
        time.sleep(0.5)
        try:
            qr_code_box = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/div/div[2]/div/canvas')
            qr_code_box
        except:
            break
    time.sleep(1)
    printc('[+] Successfully initialized WAPY.', 'green')

def send(message, contact=None, driver=driver):
    '''
    Sends a message to specific contact or to focused contact.
    Add contact to send to specific contact.
    If no contact was given it will send message to focused contact.
    '''

    if contact == None:
        try:
            message_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            message_box.clear()
            message_box.send_keys(message)
            message_box.send_keys(u'\ue007')
        except:
            return printc('[-] ERROR: Message Box was not found.', 'red')
        printc('[+] Successfully send message.', 'green')

    if not contact == None:
        try:
            search_contact = driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
            search_contact.click()
            search_contact.clear()
            search_contact.send_keys(contact)
        except:
            return printc('[-] ERROR: Cannot search contact.', 'red')
        time.sleep(0.5)
        try:
            contact_box = driver.find_element_by_class_name('eJ0yJ')
            contact_box.click()
        except:
            return printc('[-] ERROR: Contact could not be found.', 'red')

        message_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        
        message_box.clear()
        message_box.send_keys(message)
        message_box.send_keys(u'\ue007')
        printc('[+] Successfully send message.', 'green')

def send_image(image, contact=None, driver=driver):
    '''
    Sends a image to specific contact or to focused contact.
    Add contact to send to specific contact.
    If no contact was given it will send image to focused contact.
    '''

    if contact == None:
        try:
            attachment_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div')
            attachment_box.click()
        except:
            return printc('[-] ERROR: Attachment box cannot be found.', 'red')
        time.sleep(0.1)
        try:
            image_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input')
            image_box.send_keys(image)
        except:
            return printc('[-] ERROR: Image could not be send.', 'red')
        time.sleep(0.1)
        try:
            send_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div'))
            )
            send_box.click()
        except:
            return printc('[-] ERROR: Image could not be send.', 'red')
        time.sleep(1)
        printc('[+] Successfully send image.', 'green')

    if not contact == None:
        try:
            search_contact = driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
            search_contact.click()
            search_contact.clear()
            search_contact.send_keys(contact)
        except:
            return printc('[-] ERROR: Cannot search contact.', 'red')
        time.sleep(0.5)
        try:
            contact_box = driver.find_element_by_class_name('eJ0yJ')
            contact_box.click()
        except:
            return printc('[-] ERROR: Contact could not be found.', 'red')

        try:
            attachment_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div')
            attachment_box.click()
        except:
            return printc('[-] ERROR: Attachment box cannot be found.', 'red')
        time.sleep(0.1)
        try:
            image_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input')
            image_box.send_keys(image)
        except:
            return printc('[-] ERROR: Image could not be send.', 'red')
        time.sleep(0.1)
        try:
            send_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div'))
            )
            send_box.click()
        except:
            return printc('[-] ERROR: Image could not be send.', 'red')
        time.sleep(1)
        printc('[+] Successfully send image.', 'green')

def send_attachment(attachment, contact=None, driver=driver):
    '''
    Sends a attachment to specific contact or to focused contact.
    Add contact to send to specific contact.
    If no contact was given it will send attachment to focused contact.
    '''

    if contact == None:
        try:
            attachment_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div')
            attachment_box.click()
        except:
            return printc('[-] ERROR: Attachment box cannot be found.', 'red')
        time.sleep(0.1)
        try:
            attach_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input')
            attach_box.send_keys(attachment)
        except:
            return printc('[-] ERROR: Attachment could not be send.', 'red')
        time.sleep(0.1)
        try:
            send_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div'))
            )
            send_box.click()
        except:
            return printc('[-] ERROR: Attachment could not be send.', 'red')
        time.sleep(1)
        printc('[+] Successfully send attachment.', 'green')

    if not contact == None:
        try:
            search_contact = driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
            search_contact.click()
            search_contact.clear()
            search_contact.send_keys(contact)
        except:
            return printc('[-] ERROR: Cannot search contact.', 'red')
        time.sleep(0.5)
        try:
            contact_box = driver.find_element_by_class_name('eJ0yJ')
            contact_box.click()
        except:
            return printc('[-] ERROR: Contact could not be found.', 'red')

        try:
            attachment_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div')
            attachment_box.click()
        except:
            return printc('[-] ERROR: Attachment box cannot be found.', 'red')
        time.sleep(0.1)
        try:
            attach_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input')
            attach_box.send_keys(attachment)
        except:
            return printc('[-] ERROR: Attachment could not be send.', 'red')
        time.sleep(0.1)
        try:
            send_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div'))
            )
            send_box.click()
        except:
            return printc('[-] ERROR: Attachment could not be send.', 'red')
        time.sleep(1)
        printc('[+] Successfully send attachment.', 'green')

def contact(contact, driver=driver):
    '''
    Opens chat of specific contact.
    '''

    try:
        search_contact = driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
        search_contact.click()
        search_contact.clear()
        search_contact.send_keys(contact)
    except:
        return printc('[-] ERROR: Cannot search contact.', 'red')
    time.sleep(0.5)
    try:
        contact_box = driver.find_element_by_class_name('eJ0yJ')
        contact_box.click()
    except:
        return printc('[-] ERROR: Contact could not be found.', 'red')

def contact_name(driver=driver):
    '''
    Gets the contact name of current open chat.
    '''
    try:
        contact_span = driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div/div/span')
        return contact_span.text
    except:
        return None

def refresh(driver=driver):
    '''
    Refreshes WhatsApp.
    '''
    time.sleep(1)
    driver.refresh()
    time.sleep(1)
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'pane-side'))
        )
    except:
        return printc('[-] ERROR: WhatsApp refreshed with errors.', 'red')
    printc('[+] Successfully refreshed WhatsApp.', 'green')

def message_in(message_index, driver=driver):
    '''
    Fetches a message from contact from open chat with given index.
    Index '-1' is last message.
    Messages contains 'type', 'text', 'image', 'time', 'author', 'element'.
    '''

    message = {
        'type': None,
        'text': None,
        'image': None,
        'time': None,
        'author': None,
        'element': None
    }

    try:
        messages_in = driver.find_elements_by_class_name('message-in')
        message_in = messages_in[message_index]
    except:
        return message
    message['element'] = driver.find_elements_by_class_name('message-in')[message_index]

    try:
        message['text'] = message_in.find_element_by_class_name('copyable-text').text
        message['type'] = 'text'
    except:
        try:
            message['image'] = message_in.find_element_by_tag_name('img').get_attribute('src')
            message['type'] = 'media'
        except:
            try:
                message_in.find_element_by_class_name('_1ZYID')
                message['type'] = 'attachment'
            except:
                message['type'] = None
    
    try:
        message['time'] = message_in.find_element_by_class_name('_18lLQ').text
    except:
        message['time'] = None
    
    message['author'] = contact_name()

    return message

def message_out(message_index, driver=driver):
    '''
    Fetches a message from yourself from open chat with given index.
    Index '-1' is last message.
    Messages contains 'type', 'text', 'image', 'time', 'author'.
    '''

    message = {
        'type': None,
        'text': None,
        'image': None,
        'time': None,
        'author': None
    }

    try:
        messages_out = driver.find_elements_by_class_name('message-out')
        message_out = messages_out[message_index]
    except:
        return message

    try:
        message['text'] = message_out.find_element_by_class_name('copyable-text').text
        message['type'] = 'text'
    except:
        message['text'] = None
        try:
            message['image'] = message_out.find_element_by_tag_name('img').get_attribute('src')
            message['type'] = 'media'
        except:
            try:
                message_out.find_element_by_class_name('_1ZYID')
                message['type'] = 'attachment'
            except:
                message['type'] = None
    
    try:
        message['time'] = message_out.find_element_by_class_name('_18lLQ').text
    except:
        message['time'] = None
    
    message['author'] = contact_name()

    return message         
 
def contact_presence(driver=driver):
    '''
    Gets the presence from open chat.
    Presence can be 'online', 'offline' or None if no chat is open.
    '''

    try:
        presence = driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div[2]/span').text
        if presence == 'online':
            return 'online'
        if '…' in presence:
            return 'online'
        
    except:
        return 'offline'

def commandHandler(dictionary, index=-1, driver=driver):
    '''
    Responses on specific messages with specific message, image or attachment.
    Command handler runs only 1 time.
    \n
    Command handler formation: '{command}': '{type}={text/path}'
    \n
    {command} = a message to be replied to
    \n
    {type} = 'text', 'image' or 'attach'
    \n
    {text} = text message
    \n
    {path} = path of file
    '''

    for i in dictionary:

        if message_in(index)['text'] == i:
            if var.old_element == message_in(index)['element']:
                pass
            elif message_in(index)['text'] == i:
                if 'image=' in dictionary[i]:
                    send_image(dictionary[i].replace('image=', ''))
                elif 'attach=' in dictionary[i]:
                    send_attachment(dictionary[i].replace('attach=', ''))
                elif 'text=' in dictionary[i]:
                    send(dictionary[i].replace('text=', ''))
                else:
                    printc('[-] Wrong command handler formation.', 'red')
                var.old_element = message_in(index)['element']

def response(command, response_type, text=None, path=None, index=-1, driver=driver):
    '''
    Responses on specific messages with specific message, image, attachment or returns 'True' boolean.
    \n
    Response types are 'text', 'image', 'attach' or 'bool'.
    '''

    if message_in(index)['text'] == command:
        if var.old_element == message_in(index)['element']:
            pass
        elif message_in(index)['text'] == command:
            if response_type == 'image':
                send_image(path)
            elif response_type == 'attach':
                send_attachment(path)
            elif response_type == 'bool':
                var.old_element = message_in(index)['element']
                return True
            elif response_type == 'text':
                send(text)
            else:
                printc('[-] Response type is incorrect.', 'red')
            var.old_element = message_in(index)['element']

def unread(driver=driver):
    '''
    Checks if you got new message from contact.
    If you got new message from contact it will open chat from contact.
    '''
    try:
        unread_message = driver.find_element_by_class_name('ZKn2B')
        unread_message.click()
    except:
        pass
