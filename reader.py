import requests
import time
import json
import pycountry
import os
from tkinter import *
from tkinter import ttk
from fileworker import getPath
import lxml.html as html
import urllib.request as url
import threading
from random import randint
from authorisation import *


def get_msgs():
    try:
        f = open("configs\\messages.dak", "r")
        msg_list = []
        stri = ""

        for line in f.readlines():
            if line.__contains__("Message: ") or line.__contains__("Delay: "):
                msg_list.append(stri)
                stri = line.replace("Message: ", "")
            else:
                stri = stri + line

        # self.msg_list.append(str)
        f.close()
        return msg_list[1:]
    except FileNotFoundError as err:
        return []


def get_delay():
    try:
        f = open("configs\\messages.dak", "r")
        for line in f.readlines():
            if line.__contains__("Delay: ") == True:
                f.close()
                return line.replace("\n", "").split(": ")[1].__str__()
        f.close()
        return 1
    except FileNotFoundError as err:
        return 1


def read_msg(output, login_val, password_val):

    while True:
        time.sleep(int(get_delay()))
        auth = authorizeOnSite(output, login_val, password_val)
        output.insert(END, "Checking new messages...")
        # <-------------------------------------- READING

        header = {'Cookie': "SESS=" + auth}

        rRead = None
        while rRead is None:
            try:
                rRead = requests.get("https://www.rosebrides.com/member/messages/", headers=header)
            except:
                continue

        page = html.document_fromstring(rRead.text)

        new_messages_list = page.find_class('msg-th-unread')

        todo_list = []

        while todo_list == [] and new_messages_list != []:
            try:
                for item in new_messages_list:
                    link = item.find_class('ma-msg-sub-unread').pop().get("href").replace("&amp;", "&")
                    todo_list.append(link)
            except:
                continue

        if todo_list:
            for item in todo_list:
                my_messages = []
                email = None
                sender_url = None

                rRead = requests.get("https://www.rosebrides.com" + item, headers=header)
                message_page = html.document_fromstring(rRead.text)
                messages = message_page.find_class('message')

                for msg in messages:
                    sender_url = msg.find_class('member').pop().find_class('photo').pop().getchildren()[0].get('href')
                    message_content = msg.find_class('content').pop().find_class('message-content message-view').pop().text_content()

                    if sender_url is None:
                        sender_url = "me"
                        my_messages.append(message_content.__str__())
                    else:
                        word_list = message_content.replace("\t", "").replace("\r\n", " ").replace("  ", " ").split(" ")

                        pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
                        pattern2 = re.compile("(^[a-zA-Z0-9_.+-]+ [a-zA-Z0-9-] +\.[a-zA-Z0-9-.]+$)")
                        pattern3 = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-])")

                        for word in word_list:
                            if pattern.match(word) or pattern2.match(word) or pattern3.match(word):
                                email = word

                if sender_url != "me":
                    if email:
                        save_email(output, email, sender_url)
                    else:
                        answer(output, sender_url, my_messages, auth)



def answer(output, sender_url, my_messages, auth):
    recipient = sender_url.split("-")[1].split(".")[0]
    gotten_msg_list = get_msgs()

    if my_messages.__len__() >= gotten_msg_list.__len__():
        return 0

    gotten_msg_list = gotten_msg_list[my_messages.__len__():]

    message = gotten_msg_list[0]
    print(gotten_msg_list[0])

    bound_str = ""
    for i in range(0, randint(13, 14)):
        bound_str += randint(0, 9).__str__()

    header = {'Cookie': "SESS=" + auth, 'Content-Type': "multipart/form-data; boundary=---------------------------" + bound_str}
    payload = "-----------------------------" + bound_str + \
        "\nContent-Disposition: form-data; name=\"sub_action\"\n\n" + \
        "process" + \
        "\n-----------------------------" + bound_str + \
        "\nContent-Disposition: form-data; name=\"asn\"\n\n" + \
        "conversation" + \
        "\n-----------------------------" + bound_str + \
        "\nContent-Disposition: form-data; name=\"tid\"\n\n" + \
        recipient + \
        "\n-----------------------------" + bound_str + \
        "\nContent-Disposition: form-data; name=\"msg[body]\"\n\n" + \
        message + \
        "\n-----------------------------" + bound_str + "--"


    try:
        rP = requests.post("https://www.rosebrides.com/member/messages/new/", headers=header, data=payload)
        output.insert(END, "Reply was send to user " + recipient.__str__())
        f = open("configs\\history.dak", "a+")
        f.write("0" + recipient + "\n")
    except:
        output.insert(END, "Couldn't send message to user " + recipient.__str__())
        pass


def save_email(output, email, sender_url):
    recipient = {}
    recipient['id'] = sender_url.split("-")[1].split(".")[0]
    recipient['name'] = sender_url.split("-")[0].split("/").pop()
    save_path = getPath()

    output.insert(END, "Reader successfully fetched an e-mail from " + recipient['name'] + "(" + recipient['id'] + ")")
    path = save_path.replace("\n", "") + "\\fetched_emails\\" + recipient['name'] + "-" + recipient['id'] + "\\"
    if os.path.isfile(path + recipient['name'] + recipient['id'] + ".txt") is False:
        os.makedirs(os.path.dirname(path + recipient['name'] + recipient['id'] + ".txt"))

    f = open(path + recipient['name'] + recipient['id'] + ".txt", "w")
    f.write("mail: " + email + "\n")
    f.write("name: " + recipient['name'] + "\n")
    f.write("page: " + "https://www.rosebrides.com" + sender_url.__str__() + "\n")

    img = None
    while img is None:
        try:
            page = html.parse(url.urlopen("https://www.rosebrides.com" + sender_url)).getroot()
            info = page.find_class('details-basics').pop().getchildren().pop().getchildren()

            for item in info:
                tmp = item.drop_tag()
                if tmp:
                    f.write(item.drop_tag())
            f.close()
            img = page.get_element_by_id("pPhotoMain").getchildren().pop().get("href")
        except:
            continue


    try:
        img = requests.get("https://rosebrides.com" + img, stream=True)
        with open(path + "photo" + ".jpg", 'wb') as f:
            for chunk in img.iter_content(1024):
                f.write(chunk)
    except:
        pass

    try:
        f = open("configs\\fetched_ids.dak", "a+")
        f.write("0" + sender_url.replace("https://www.rosebrides.com", "") + "\n")
        f.close()

    except FileNotFoundError as err:
        print(err.__str__())
        pass
















    # message_list = messages_html.find_class('message')
    # for m_item in message_list:
    #     m_item.find_class('message-content message-view')

    # save_path = getPath()
    # token = int(time.time())
    # #time.sleep(1800)
    # sender_info = json.JSONDecoder().decode(auth.text)
    # header = {'authorization': "Token token=\"" + auth.headers['X-Token'] + "\""}
    #
    # email = None
    # m_sender = None
    # pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    # pattern2 = re.compile("(^[a-zA-Z0-9_.+-]+ [a-zA-Z0-9-] +\.[a-zA-Z0-9-.]+$)")
    #
    # while True:
    #     try:
    #         response = requests.get(
    #             "https://api.triptogether.com/events/" + sender_info['id'] + "?token=" + token.__str__(),
    #             headers=header)
    #     except ConnectionError as err:
    #         output.insert(END, "!!! " + err.__str__())
    #         pass
    #
    #     if response.text != "[]" and response:
    #         message = json.JSONDecoder().decode(response.text)
    #         for item in message:
    #             try:
    #                 if item['type'] == "added:event":
    #                     if 'details' in item:
    #                         if 'payload' in item['details']:
    #                             if 'text' in item['details']['payload']:
    #                                 t_item = item['details']['payload']['text']
    #                                 if t_item.split(" ").__len__() > 1:
    #                                     t_item = t_item.split(" ")
    #
    #                                 if type(t_item) is list:
    #                                     for word in t_item:
    #                                         if pattern.match(word) or pattern2.match(word):
    #                                             email = word
    #                                             m_sender = item['details']['payload']['sender-id']
    #                                 else:
    #                                     if pattern.match(t_item) or pattern2.match(t_item):
    #                                         email = t_item
    #                                         m_sender = item['details']['payload']['sender-id']
    #
    #                 token = message[0]['token']
    #                 break
    #             except:
    #                 m_sender = ""
    #                 pass
    #     else:
    #         m_sender = ""
    #
    #     info = None
    #     try:
    #         info = requests.get('https://api.triptogether.com/users/' + m_sender)
    #         info = json.JSONDecoder().decode(info.text)
    #     except:
    #         pass
    #
    #     if email and info:
    #         output.insert(END, "Reader successfully fetched an e-mail from " + info['name'] + "(" + m_sender + ")")
    #         path = save_path.replace("\n", "") + "\\fetched_emails\\" + info['name'] + info['id'] + "\\"
    #         if os.path.isfile(path + info['name'] + info['id'] + ".txt") is False:
    #             os.makedirs(os.path.dirname(path + info['name'] + info['id'] + ".txt"))
    #
    #         f = open(path + info['name'] + info['id'] + ".txt", "w")
    #         f.write("mail: " + email + "\n")
    #
    #         if 'name' in info:
    #             f.write("name: " + info['name'] + "\n")
    #
    #         if 'id' in info:
    #             f.write("page: www.triptogether.com/travellers/#" + info['id'] + "\n")
    #
    #         if 'gender' in info:
    #             if info['gender'] == "mal":
    #                 f.write("gender: male\n")
    #             else:
    #                 if info['gender'] == "fem":
    #                     f.write("gender: female\n")
    #                 else:
    #                     f.write("gender: -bender\n")
    #
    #         if 'birthday' in info:
    #             f.write("birthday: " + info['birthday'] + "\n")
    #
    #         if 'country' in info:
    #             f.write("country: " + pycountry.countries.get(alpha_2=info['country']).name + "\n")
    #
    #         if 'occupation' in info:
    #             f.write("job: " + info['occupation'] + "\n")
    #
    #         f.close()
    #         img = None
    #         try:
    #             img = requests.get("https://api.triptogether.com/users/" + info['id'] + "/photos", stream=True)
    #         except:
    #             pass
    #         if img:
    #             img_list = json.JSONDecoder().decode(img.text)
    #             for item in img_list:
    #                 try:
    #                     r = requests.get(
    #                         "https://api7.triptogether.com/users/" + info['id'] + "/photos/" + item + ".310x455")
    #                 except:
    #                     pass
    #                 with open(path + item + ".jpg", 'wb') as f:
    #                     for chunk in r.iter_content(1024):
    #                         f.write(chunk)
    #         email = None
    #
    #         try:
    #             f = open("configs\\fetched_ids.dak", "a+")
    #             f.write("0" + info['id'] + "\n")
    #             f.close()
    #
    #         except FileNotFoundError as err:
    #             print(err.__str__())
    #             pass

