import os
import tkinter
import requests
import json
import time
import ast
import lxml
from getpass import getpass
from bs4 import BeautifulSoup

print(" _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
print("|                                                       |")
print("|          I N S T A G R A M   C L I   V 1 . 0          |")
print("|_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _|")

#  Credentials used for logging in
USERNAME = input("\nUsername: ")
PASSWORD = getpass("Password: ")
print("Connecting...")
headers = {'referer': "https://www.instagram.com/accounts/login/"}
#  My personal user agent; Replace with your for use.
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.365'

def access_instagram():
    with requests.Session() as req:
        req.headers = {"user-agent": user_agent}
        req.headers.update({'Referer': "https://www.instagram.com/"})
        get_response = req.get("https://www.instagram.com/")
        #  Handler for sniffing anti-csrf cookie token from initial request
        if get_response.cookies['csrftoken']:
            csrf_token = get_response.cookies['csrftoken']
        elif get_response.cookies['csrf']:
            csrf_token = get_response.cookies['csrf']
        elif get_response.cookies['csrf_token']:
            csrf_token = get_response.cookies['csrf_token']
        else:
            print("Failed to retrieve csrf token")

        #  Login data to be sent in the POST request
        login_data = dict(csrfmiddlewaretoken=csrf_token, username=USERNAME, password=PASSWORD, next="/")
        post_response = req.post("https://www.instagram.com/accounts/login/ajax/", data=login_data)

        if post_response.status_code == 200:
            get_response2 = req.get("https://www.instagram.com/accounts/edit/")
        else:
            print(f"Error: {post_response.status_code} -- Could not log in.")
            return

        if (USERNAME in get_response2.text):
            print(f"Successfully logged in to Instagram as '{USERNAME}'")
        else:
            print(f"Error -- Failed to log in as '{USERNAME}'!")
            return

        getJSON(get_response2)



def getJSON(response):
    #  Instagram renders their web app content with Javascript. Because of this, the raw data on the site is in the form
    #  of a JavaScript array nested inside of an HTML <script> tag.
    soup = BeautifulSoup(response.text, 'html.parser')  #  Initiating instance of BS4 on response from GET request
    settings_data_raw = soup.find_all("script", type="text/javascript")[3]  #  Finding object in script with user settings data
    settings_info = json.loads(str(settings_data_raw)[52:-10])  #  Converting JSON string to JSON Object
    user_obj = {
        'scraped_all' : str(settings_info["entry_data"]),
        'scraped_name' : str(settings_info["entry_data"]["SettingsPages"][0]["form_data"]["first_name"]),
        'scraped_username' : str(settings_info["entry_data"]["SettingsPages"][0]["form_data"]["username"]),
        'scraped_email' : str(settings_info["entry_data"]["SettingsPages"][0]["form_data"]["email"]),
        'scraped_phone' : str(settings_info["entry_data"]["SettingsPages"][0]["form_data"]["phone_number"]),
        'scraped_birthday' : str(settings_info["entry_data"]["SettingsPages"][0]["form_data"]["birthday"]),
        'scraped_bio' : f'"{str(settings_info["entry_data"]["SettingsPages"][0]["form_data"]["biography"])}"'
        }
    menu_init(settings_info=settings_info, obj=user_obj)

def menu_init(settings_info, obj):
    def menu(settings_info, obj):
        menu_choice = input(
        """
        Select a number below to access account info:
        1 : Account Settings
        2 : Feed
        3 : Exit
        """)
        if menu_choice == '1':
            user_info_display =  f"Name: {obj['scraped_name']}\nUsername: {obj['scraped_username']}\nEmail: {obj['scraped_email']}\nPhone Number: {obj['scraped_phone']}\nBirthday: {obj['scraped_birthday']}"
            print(user_info_display)
        else:
            return
    menu(settings_info, obj)
menu(settings_info, obj)

access_instagram()
