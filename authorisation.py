from views import *
import requests
from requests.auth import HTTPBasicAuth
from tkinter import *


SITE = "https://rosebrides.com"
s = requests.session()


def authorizeOnSite(output, login, password):
    output.insert(END, "Authorising at " + SITE + "...")
    r = None

    if login.get() == "" or password.get() == "":
        output.insert(END, "You forgot your login or password!")

    while r is None:
        try:
            req_params = {'sub_action': "processLogin", 'login[user]': login.get(), 'login[password]': password.get()}
            r = s.post(SITE + "/login/", params=req_params)
        except:
            output.insert(END, "Error connecting to server.")
            output.insert(END, "Retrying...")
            continue

        if r and r.cookies.get(name="SESS", domain="www.rosebrides.com"):
            output.insert(END, "\nInfiltration successful!")
        else:
            output.insert(END, "Something went wrong :(")
            output.insert(END, "Try to check your login info and try again...")

    return r.cookies.get(name="SESS", domain="www.rosebrides.com")