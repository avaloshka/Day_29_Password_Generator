
import tkinter
from tkinter import END
from tkinter import messagebox
import random
import string
import pyperclip
import json


WEB = None
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = string.ascii_lowercase
    up_letters = string.ascii_uppercase
    numbers = string.digits
    symbols = string.punctuation

    number_of_char_required_in_a_password = 16

    all_char = letters + up_letters + numbers + symbols

    collection = []

    for _ in range(number_of_char_required_in_a_password):
        n = random.choice(all_char)
        collection.append(n)

    random.shuffle(collection)

    password = ''.join(collection)
    password_entry.delete(0, END)
    password_entry.insert(0, password)

    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():

    web = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        web: {
            "email": email,
            "password": password,
        }
    }

    if len(web) == 0 and len(password) == 0:
        messagebox.showinfo(message="Please enter required info")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ----------------------------Retreve a password


def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data Found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="website", message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="No Data", message="No Data Found")
# ---------------------------- UI SETUP -


window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = tkinter.Canvas(width=200, height=189)
logo_img = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Website
website_label = tkinter.Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry = tkinter.Entry(width=32)
website_entry.grid(column=1, row=1)
website_entry.focus()

# Email
email_label = tkinter.Label(text="Email/Username:")
email_label.grid(column=0, row=2)

email_entry = tkinter.Entry(width=51)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "enter your email")


# Password
password_label = tkinter.Label(text="Password:")
password_label.grid(column=0, row=3)

password_entry = tkinter.Entry(width=32)
password_entry.grid(column=1, row=3)
# "Generate Password" button
generate_password_button = tkinter.Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)


# "Add" button
add_button = tkinter.Button(text="Add", width=27, command=save)
add_button.grid(column=1, row=4)

# "Search" button
search_button = tkinter.Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
