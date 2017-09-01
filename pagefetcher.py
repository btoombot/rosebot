from views import *
import requests
import json
from datetime import datetime
import pycountry
from fileworker import *
from multiprocessing.pool import ThreadPool
import threading
import lxml.html as html

SITE = "https://www.rosebrides.com/"

fetching_thread_list = []


def get_budget_weight(word):
    if word == 'low':
        return 0
    if word == 'medium':
        return 1
    if word == 'high':
        return 2
    if word == 'very-high':
        return 3


def iniciate_fetching(output, login_val, password_val):
    auth_r = authorizeOnSite(output, login_val, password_val)

    if auth_r:
        output.insert(END, "\n==============================================")
        output.insert(END, "Fetching IDs from " + SITE + "...")

        fetching_thread = threading.Thread(target=get_page_ids, args=(output, auth_r))
        fetching_thread.daemon = True
        fetching_thread_list.append(fetching_thread)
        fetching_thread.start()
        output.insert(END, "Now wait until thread will finish fetching IDs...")
        output.insert(END, "I will let you now, when its done ;)")


def get_page_ids(output, auth):
    header = {'Cookie': "SESS=" + auth}
    ids_to_save = []
    profile_list = []
    page = None
    r = None

    while r is None:
        try:
            r = requests.get(SITE + "member/matches/online/", headers=header)
            page = html.document_fromstring(r.text)
            profile_list = page.find_class('profile')
        except:
            output.insert(END, "Couldn't connect to site. Check your internet.")
            continue
        if page is None:
            continue

    victim_list = []
    for item in profile_list:
        victim = {}

        children = item.getchildren()
        if children.__len__() >= 4:
            victim['id'] = children[1].getchildren().pop().get("href")
            victim['name'] = children[2].text_content().split(" ")[:1].pop()
            victim['age'] = children[2].text_content().split(" ")[1:-1].pop()
            victim['country'] = children[3].text_content().split(",")[-1:].pop()[1:]
            victim_list.append(victim)

    ids_to_save = []
    for item in victim_list:
        output.delete(END)
        output.insert(END, "Checking user " + item['id'] + " (" + item['name'] + ")")

        if 'age' in item:
            if not (int(getAgeFrom()) <= int(item['age']) <= int(getAgeTo())):
                continue
        else:
            continue

        if getBirth():
            if 'country' in item:
                if item['country'] in getBirth():
                    continue
            else:
                continue

        output.delete(END)
        output.insert(END, "User " + item['name'] + " (" + item['id'] + ") was added to check list!")
        output.insert(END, "")
        ids_to_save.append(item['id'])

    if ids_to_save != []:
        counter = save_id(ids_to_save)
    else:
        counter = 0

    output.delete(END)
    output.insert(END, "Done! New IDs: " + counter.__str__())
    if counter == 0:
        output.insert(END, "New IDs: " + counter.__str__() + ". Try lowering your preferences.")

    fetching_thread_list.clear()

