#!/bin/env python3
from pyquery import PyQuery as pq
from lxml import etree
import urllib
import requests
import os
import re
import stat
import json
import argparse
import getpass

SMILEY_DIR = os.path.join(os.path.expanduser("~"), ".purple", "smileys", "hipchat")
CONF_FILE = os.path.join(SMILEY_DIR, "hipchat_pidgin_smilies.conf")

def setup(interactive_setup=False):
    """Load the config file, if it doesn't exist, exit with error.

    If interactive_setup==True, instead of erroring run an interactive
    setup process to get started as a first time user.
    """
    try:
        os.makedirs(SMILEY_DIR)
    except FileExistsError:
        pass
    # Find if the config file exists:
    try:
        with open(CONF_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        if not interactive_setup:
            raise AssertionError("No configuration found, run with --setup to perform first time setup")
        # First time setup:
        print("This looks like the first time you've run this, let me help get you setup!")
        data = {}
        data['hipchat_org_name'] = input("What is your organization's hipchat name? : ")
        data['hipchat_username'] = input("What is your hipchat login email address? : ")
        while True:
            passwd = getpass.getpass("\nWhat is your hipchat password? : ")
            if len(passwd) == 0:
                print("Password can't be blank, try again..")
                continue
            passwd_confirm = getpass.getpass("Please confirm your password : ")
            if passwd == passwd_confirm:
                data['hipchat_password'] = passwd
                break
            print("Passwords didn't match, try again..")
            
        with open(CONF_FILE, 'w') as f:
            json.dump(data, f)
        os.chmod(CONF_FILE, stat.S_IREAD | stat.S_IWRITE)
        return data

def login():
    conf = setup()
    s = requests.Session()
    #get xsrf_token then login:
    login_page = pq(s.get("https://www.hipchat.com/sign_in").text)
    xsrf_token = login_page.find("form.signupForm").find(
        "input[name=xsrf_token]").attr('value')
    r = s.post(
        "https://www.hipchat.com/sign_in",
        headers={
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.125 Safari/537.36",
            "Referer":"https://www.hipchat.com/sign_in"
        },
        data={
            "email": conf['hipchat_username'],
            "password": conf['hipchat_password'],
            "xsrf_token": xsrf_token,
            "stay_signed_in": 1,
            "signin": "Log in"
        })
    assert r.status_code == 200
    return s
    
def get_emoticons_page(session=None):
    """Download the emoticons page, return as a pyquery object"""
    conf = setup()
    if not session:
        session = login()
    return pq(session.get('https://{org_name}.hipchat.com/emoticons'.format(org_name=conf['hipchat_org_name'])).text)

def get_emoticons_list(session=None):
    """Parse the emoticon shortcut and image URLs from the hipchat.com page"""
    if not session:
        session = login()
    # Org specific emoticons:
    emoticons = [] # [(shortcut, url), ...]
    page = get_emoticons_page()
    for row in page.find("table#currentemoticons").find("tr.data"):
        row = pq(row)
        img_url = row.find("img.emoticon")[0].get("src")
        shortcut_text = row.find("td.shortcut").text()
        emoticons.append((shortcut_text, img_url))

    # Hipchat standard emoticons:
    for block in page.find("div.emoticon-block"):
        block = pq(block)
        img_url = block.find("img")[0].get("src")
        shortcut_text = block.attr("data-clipboard-text")
        emoticons.append((shortcut_text, img_url))

    return emoticons

def update_emoticons_on_disk():
    conf = setup()
    session = login()
    emoticons = get_emoticons_list(session)
    #Download emoticon images:
    for shortcut_text, img_url in emoticons:
        img_name = re.sub("-[0-9]+", "", img_url.split("/")[-1])
        img_path = os.path.join(SMILEY_DIR, "{}".format(img_name))
        if not os.path.exists(img_path):
            print("Downloading {} ...".format(img_url))
            r = session.get(img_url, stream=True)
            with open(img_path,'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
    #Create theme file:
    with open(os.path.join(SMILEY_DIR, "theme"), "w") as f:
        f.write("Name=hipchat\n")
        f.write("Description=Hipchat emoticon theme\n")
        f.write("Icon=hipchat.png\n")
        f.write("\n")
        f.write("[XMPP]\n")
        for shortcut_text, img_url in emoticons:
            img_name = re.sub("-[0-9]+", "", img_url.split("/")[-1])
            f.write("{img_name}    {shortcut_text}\n".format(
                img_name=img_name, shortcut_text=shortcut_text))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='hipchat_pidgin_smilies.py')
    parser.add_argument('--setup', help='Run firsttime setup', action="store_true")
    args = parser.parse_args()

    if args.setup:
        setup(interactive_setup=True)
    else:
        update_emoticons_on_disk()
