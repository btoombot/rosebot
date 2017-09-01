#!/usr/bin/python

from tkinter import *
from tkinter import ttk
from fileworker import *
from views import *
from authorisation import *
import os


def on_closing():

    f = open("configs\\settings.dak", "w")
    if path_to_data.get() != "" or path_to_data.get() != " ":
        f.write("Data path: " + path_to_data.get().__str__())
    else:
        f.write("Data path: " + os.getcwd().__str__())

    if(int(chk_save.get()) == 1 and login_val.get() != ""):
        f.write("\nLogin: " + login_val.get().__str__() +
                "\nPassword: " + password_val.get().__str__() +
                "\nSave: 1")
    f.close()

    if spam_thread_list == []:
            #and fetching_thread_list == [] and spam_thread_list == []:
        root.destroy()
    else:
        output.insert(END, "Sorry, you can't leave unless bot done chatting.")


if __name__ == "__main__":

    try:
        os.makedirs(os.path.dirname("configs\\settings.dak"))
    except FileExistsError:
        pass

    root = Tk()
    root.title("Rosebot v1.5")
    root.resizable(0, 0)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    try:
        root.iconbitmap('configs\\ico.ico')
    except:
        pass
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    path_to_data = StringVar()
    login_val = StringVar()
    password_val = StringVar()
    chk_save = IntVar()

    ttk.Label(mainframe, text="Path for fetched emails:").grid(column=1, row=1, sticky=W)
    data_path = ttk.Entry(mainframe, width=40, textvariable=path_to_data)
    data_path.grid(column=2, row=1, sticky=(W, E))
    data_path.insert(0, getPath())

    ttk.Button(mainframe, text="Settings", command=lambda: set_prefs(root)).grid(column=3, row=1, rowspan=2, sticky=(W, N, E, S))

    # Logbox

    log_frame = Frame(mainframe)
    log_frame_reader = Frame(mainframe)

    sbar_log = Scrollbar(log_frame)
    sbar_log.pack(side=RIGHT, fill=Y)
    sbar_log_reader = Scrollbar(log_frame_reader)
    sbar_log_reader.pack(side=RIGHT, fill=Y)

    ttk.Label(mainframe, text="Log:").grid(column=1, row=3, sticky=W)
    output = Listbox(log_frame, height=10, width=70)
    output_reader = Listbox(log_frame_reader, height=10, width=70)
    output.pack()
    output_reader.pack()
    output.insert(END, "This is spamming log.")
    output_reader.insert(END, "This is reading log.")

    sbar_log.config(command=output.yview)
    output.config(yscrollcommand=sbar_log.set)
    sbar_log_reader.config(command=output_reader.yview)
    output_reader.config(yscrollcommand=sbar_log_reader.set)

    log_frame.grid(column=1, columnspan=2, row=8, rowspan=2, sticky=(W, E))
    log_frame_reader.grid(column=1, columnspan=2, row=4, rowspan=2, sticky=(W, E))

    ttk.Label(mainframe, text="Authorisation:").grid(column=3, row=3, sticky=(W, N))
    login = ttk.Entry(mainframe, width=20, textvariable=login_val)
    login.grid(column=3, row=4, sticky=(W, E, N))
    login.insert(0, getLogin())
    password = ttk.Entry(mainframe, show="*", width=20, textvariable=password_val)
    password.grid(column=3, row=4, sticky=(W, E))
    password.insert(0, getPassword())

    if getSaveCb() != "":
        chk_save.set(1)

    savebox = Checkbutton(mainframe, text="save", variable=chk_save)
    savebox.grid(column=3, row=4, sticky=(W, S))

    ttk.Button(mainframe, text="Read \nincoming \nmessages", command=lambda: read_old(output_reader, login_val, password_val)).grid(
        column=3, row=5, rowspan=3, sticky=(W, E, N, S))
    ttk.Button(mainframe, text="Start \nbot", command=lambda: autopiloting(output, login_val, password_val)).grid(column=3, row=8, sticky=(W, E, N, S))

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()