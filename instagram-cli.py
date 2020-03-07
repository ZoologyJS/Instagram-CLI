import os
import tkinter
import requests
import json
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
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.365'

def access_instagram():
    with requests.Session() as req:
        req.headers = {"user-agent": user_agent}
        req.headers.update({'Referer': "https://www.instagram.com/"})
        get_response = req.get("https://www.instagram.com/")
        #  Handler for sniffing csrf cookie token from initial request
        if get_response.cookies['csrftoken']:
            csrf_token = get_response.cookies['csrftoken']
        elif get_response.cookies['csrf']:
            csrf_token = get_response.cookies['csrf']
        elif get_response.cookies['csrf_token']:
            csrf_token = get_response.cookies['csrf_token']
        else:
            print("Failed to retrieve csrf token")

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
    soup = BeautifulSoup(response.text, 'html.parser')  #  Initiating instance of BS4 on response from GET request
    settings_data_raw = soup.find_all("script", type="text/javascript")[3]  #  Object in script with user settings data
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

access_instagram()





# import requests
#
# main_url = 'https://www.instagram.com/'
# login_url = main_url+'accounts/login/ajax'
# user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.365'
#
# session = requests.session()
# session.headers = {"user-agent": user_agent}
# session.headers.update({'Referer': main_url})
#
# req = session.get(main_url)
# #session.headers.update({'set-cookie': req.cookies['csrftoken']})
# print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
# print(f"CSRF Token: {req.cookies['csrftoken']}")
# print(f"Loading home page - Status Code: {req.status_code}")
# req.close()
#
# login_data = {"csrfmiddlewaretoken": req.cookies["csrftoken"]}
#
#
# login = session.post(login_url, data=login_data, allow_redirects=True)
# #print(f"CSRF Token: {login.cookies['csrftoken']}")
# print(f"Logging in - Status code: {login.status_code}")
# #session.headers.update({'set-cookie': login.cookies['csrftoken']})
# if login.status_code == 200 and req.status_code == 200:
#     print("Success!")
# cookies = login.cookies
#
# print(login.headers)
# print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
# print(dir(login))
# print(login.ok)
# print(login.url)
# login.close()




# import requests
#
# url = 'https://www.instagram.com/accounts/login/'
# url_main = url + 'ajax/'
# auth = {'username': 'chrisfradellaf', 'password': 'm0g0Juniper_'}
# headers = {'referer': "https://www.instagram.com/accounts/login/"}
#
# with requests.Session() as s:
#     req = s.get(url)
#     headers['x-csrftoken'] = req.cookies['csrftoken']
#     s.post(url_main, data=auth, headers=headers)
#     # Now, you can use 's' object to 'get' response from any instagram url
#     # as a logged in user.
#     r = s.get('https://www.instagram.com/accounts/edit/')
#     # If you want to check whether you're getting the correct response,
#     # you can use this:
#
#     print(r.text)
#     print(r.status_code)
#     print(auth['username'] in r.text)  # which returns 'True'
