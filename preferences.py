from tkinter import *
from tkinter import ttk
import tkinter as tk
from fileworker import *

# Some very dirty magic
window = Tk()

gen_var = StringVar()
trip_val = StringVar()
country_val = StringVar()
job_val = StringVar()
budget_val = StringVar()
all_budget_val = StringVar()

window.update()
window.destroy()

def on_closing(window):
    window.grab_release()


def add(listbox, value):
    if value.get() != "":
        listbox.insert(END, value.get())


def addTrip(listbox, value, addvalue):
    if value.get() != "":
        listbox.insert(END, value.get() + " | " + addvalue.get())


def remove(listbox):
    try:
        listbox.delete(listbox.curselection())
    except:
        pass


def create_window(window):
    prefframe = ttk.Frame(window, name="prefs", padding="3 3 12 12")
    prefframe.grid(column=0, row=0, sticky=(N, W))
    prefframe.columnconfigure(0, weight=1)
    prefframe.rowconfigure(0, weight=1)

    ttk.Label(prefframe, text="Gender: ").grid(column=1, row=1, sticky=W)
    gender = ttk.Combobox(prefframe, name="gender", textvariable=gen_var, state="readonly", width=10)
    gender['values'] = ('male', 'female')
    gender.current(0)
    gender.grid(column=2, row=1, sticky=W)

    try:
        gender.current(gender['values'].index(getGender()))
    except ValueError:
        pass

    ttk.Label(prefframe, text="Age from/to: ").grid(column=1, row=2, sticky=W)
    age = Spinbox(prefframe, name="age", from_=18, to=99, width=10)
    age.grid(column=2, row=2, sticky=(W, E))
    age.delete(0, END)
    age.insert(0, getAgeFrom())

    ageTo = Spinbox(prefframe, name="ageTo", from_=19, to=100, width=10)
    ageTo.grid(column=3, row=2, sticky=(W, E))
    ageTo.delete(0, END)
    try:
        ageTo.insert(0, getAgeTo())
    except:
        ageTo.insert(0, 100)
        pass

    ttk.Label(prefframe, text="Include ppl that has no: ").grid(column=1, row=3, sticky=W)

    chk_nocountry = IntVar(prefframe)
    no_country = ttk.Checkbutton(prefframe, name="chk_nocountry", text="countries", variable=chk_nocountry)
    no_country.grid(column=2, row=3, sticky=(W, N))
    try:
        chk_nocountry.set(int(getNoCountryCb()))
    except:
        chk_nocountry.set(1)
        pass

# Lists =====================

    ttk.Label(prefframe, text="Exclude countries(born at):").grid(column=1, row=6, sticky=W)

    frame_contry = ttk.Frame(prefframe, name="frame_country")

    sbar_country = Scrollbar(frame_contry)
    sbar_country.pack(side=RIGHT, fill=Y)

    pobirth = Listbox(frame_contry, name="pobirth", height=5)
    pobirth.pack()

    sbar_country.config(command=pobirth.yview)
    pobirth.config(yscrollcommand=sbar_country.set)

    frame_contry.grid(column=3, row=7, rowspan=2, columnspan=2, sticky=(W, E))

    try:
        loaded_pobirth = getBirth()
        for item in loaded_pobirth:
            pobirth.insert(END, item)
    except:
        pass

    textbox = ttk.Entry(prefframe, width=20, textvariable=country_val)
    textbox.grid(column=1, columnspan=1, row=7, sticky=(W, E, N))

    ttk.Button(prefframe, text=">>>", command=lambda: add(pobirth, textbox)).grid(column=2, row=7, sticky=(W, S))
    ttk.Button(prefframe, text="<<<", command=lambda: remove(pobirth)).grid(column=2, row=8, sticky=(W, N))

    for child in prefframe.winfo_children():
        child.grid_configure(padx=5, pady=5)
