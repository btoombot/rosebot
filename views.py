from authorisation import *
from preferences import create_window
from pagefetcher import *
from messages import *
from spammer import *
from reader import *
import threading


autopilot_is_on = False
dont_start_auto = True
thread_autopilot_list = []
thread_reader_list = []

def fetch_ids(output, login_val, password_val):
    if spam_thread_list ==[] and fetching_thread_list == []:
        iniciate_fetching(output, login_val, password_val)
    else:
        output.insert(END, "Im busy.")


def spam(output, login_val, password_val):
    if spam_thread_list == []:
        start_spam_thread(output, login_val, password_val)
    else:
        output.insert(END, "Im busy.")


def on_closing(window):
    window.grab_release()


def set_prefs(root):
    window = tk.Toplevel(root)

    window.grab_set()
    window.protocol("WM_DELETE_WINDOW", on_closing(root))
    window.title("Settings")
    window.resizable(0, 0)

    create_window(window)
    MsgWindow(window)


def autopiloting(output, login_val, password_val):
    if thread_autopilot_list == []:
        global autopilot_is_on
        if not autopilot_is_on:
            autopilot_is_on = True
        else:
            autopilot_is_on = False

        global dont_start_auto
        if autopilot_is_on:
            dont_start_auto = False
            output.insert(END, "!!!Autobot was switched on!!!")
            thread_autoomg = threading.Thread(target=dosomeomg, args=(output, login_val, password_val))
            thread_autoomg.start()
            thread_autopilot_list.append(thread_autoomg)

        else:
            dont_start_auto = True
            output.insert(END, "!!!Autobot will be turned off, after finishing current iteration!!!")
    else:
        output.insert(END, "Autobot is currently working. It will be off, once it finish.")
        dont_start_auto = True


def dosomeomg(output, login_val, password_val):
    skip_to_spam = False

    while not dont_start_auto:

        output.insert(END, "==========!!! STARTING FETCHING !!!==========")
        if not skip_to_spam:
            iniciate_fetching(output, login_val, password_val)

            time.sleep(10)
            while fetching_thread_list != []:
                time.sleep(1)

        output.insert(END, "==========!!! DONE FETCHING !!!==========")
        time.sleep(10)

        output.insert(END, "==========!!! STARTING SPAM !!!==========")

        start_spam_thread(output, login_val, password_val)

        while spam_thread_list != []:
            time.sleep(1)

        output.insert(END, "==========!!! DONE SPAMMING !!!==========")
        time.sleep(300)

        skip_to_spam = False


def read_old(output, login_val, password_val):
    if thread_reader_list == []:
            thread_reader = threading.Thread(target=read_msg, args=(output, login_val, password_val))
            thread_reader.daemon = True
            thread_reader_list.append(thread_reader)
            thread_reader.start()
            output.insert(END, "Reader started...")
    else:
        output.insert(END, "Reader is working.")




