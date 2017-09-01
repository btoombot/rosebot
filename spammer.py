from views import *
import requests
from authorisation import authorizeOnSite
import threading
import time
from fileworker import getPath
from tkinter import *
from random import randint
from tkinter import ttk

spam_thread_list = []

def get_ids():
    try:
        f = open("configs\\curr_victims.dak", "r")      # <--------------------------------------CHANGE FILENAME HERE!
        id_list = []
        for line in f.readlines():
            if line[0] == "0":
                id_list.append(line.replace("\n", "")[1:])

        return id_list
    except FileNotFoundError as err:
        return []


def get_timeout():
    try:
        f = open("configs\\messages.dak", "r")
        for line in f.readlines():
            if line.__contains__("Timeout: ") == True:
                f.close()
                return line.replace("\n", "").split(": ")[1].__str__()
        f.close()
        return 1
    except FileNotFoundError as err:
        return 0


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
        return 0


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


def send(recipient, auth, output, message):
    recipient = recipient.split("-")[1].split(".")[0]

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
        output.insert(END, "Message was send to user " + recipient.__str__())
    except:
        output.insert(END, "Couldn't send message to user " + recipient.__str__())
        pass


def get_threads():
    try:
        f = open("configs\\messages.dak", "r")
        for line in f.readlines():
            if line.__contains__("Threads: ") == True:
                f.close()
                return line.replace("\n", "").split(": ")[1].__str__()
        f.close()
        return 1
    except FileNotFoundError as err:
            return 1


def initiate_spam(output, auth_r, id_list):
    gotten_msg_list = get_msgs()
    for id_ in id_list:
        time.sleep(3)
        send(id_, auth_r, output, gotten_msg_list[0])

    spam_thread_list.clear()
    f = open("configs\\curr_victims.dak", "w")
    f.close()


def start_spam_thread(output, login_val, password_val):
    auth_r = authorizeOnSite(output, login_val, password_val)

    if auth_r:
        output.insert(END, "Looking through history...")
        id_list = get_ids()

        if id_list:
            output.insert(END, "Initiating spam...")

            spam_thread = threading.Thread(target=initiate_spam, args=(output, auth_r, id_list))
            spam_thread.daemon = True
            spam_thread_list.append(spam_thread)
            spam_thread.start()
            output.insert(END, "Done! You may go and drink some coffee.")
            output.insert(END, "Meanwhile bot will be doing your dirty work ;)")

        else:
            output.insert(END, "Could not find ids. Try fetching some first.")