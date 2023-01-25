from tkinter import *
from tkinter import messagebox
from ttkwidgets import autocomplete
import random
import string
import pyperclip
import json

JSON_FILE = "passwords.json"
websites = []
emails = []


# ---------------------------- AUTOCOMPLETE GENERATOR ------------------------------- #
def generate_autocomplete():
    global websites
    global emails
    try:
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        websites = []
        emails = []
    else:
        websites = list(dict.fromkeys(data.keys()))
        sub_list = list(data.values())
        emails = list(dict.fromkeys([x["Email/Username"] for x in sub_list]))
    return websites


# ---------------------------- JSON GENERATOR ------------------------------- #
def dump_new_json(json_data, json_file):
    with open(json_file, "w") as file:
        # Saving updated data
        json.dump(json_data, file, indent=4)


# ---------------------------- WEBSITE SEARCH ------------------------------- #
def website_search():
    search = web_entry.get()
    with open(JSON_FILE, "r") as file:
        try:
            data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            messagebox.showwarning(title="Warning", message="No passwords saved.")
        else:
            if search in data:
                user = data[search]['Email/Username']
                password = data[search]['Password']
                messagebox.showinfo(title=f"{search} Password Info",
                                    message=f"Email/Username: {user} "
                                            f"\nPassword: {password}")
            else:
                messagebox.showwarning(title="Warning", message="No password corresponding to this website.")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
    alphabet = list(string.ascii_uppercase) + list(string.ascii_lowercase)
    numbers = list(string.digits)
    symbols = ["!", "#", "$", "%", "&", "*", "(", ")", "+"]

    password_letters = [random.choice(alphabet) for _ in range(random.randint(6, 8))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(4, 5))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(4, 5))]

    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = web_entry.get()
    user = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "Email/Username": user,
            "Password": password
        }
    }

    if len(website) == 0 or len(user) == 0 or len(password) == 0:
        messagebox.showwarning(title="Warning", message="Do not leave any fields empty")
    else:
        is_ok = messagebox.askokcancel(message=f"Details entered: \nEmail/Username: {user} \nPassword: {password}"
                                               f"\nWould you like to save this password?",
                                       title="Save?")
        if is_ok:
            try:
                with open(JSON_FILE, "r") as password_file:
                    # Reading the old data
                    data = json.load(password_file)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                dump_new_json(json_data=new_data, json_file=JSON_FILE)
            else:
                data.update(new_data)
                dump_new_json(json_data=data, json_file=JSON_FILE)
            finally:
                pyperclip.copy(password)
                web_entry.delete(0, 'end')
                password_entry.delete(0, 'end')
                generate_autocomplete()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

generate_autocomplete()

# Display logo
logo_canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
logo_canvas.create_image(100, 100, image=logo_img)
logo_canvas.grid(column=1, row=0)

# ---- Labels ---- #

# 'Website' Label
web_label = Label(text="Website:")
web_label.grid(column=0, row=1)

# 'Email/Username' Label
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

# 'Password' Label
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# ---- Entries ---- #

# Website Entry
web_entry = autocomplete.AutocompleteCombobox(width=19,
                                              completevalues=generate_autocomplete()
                                              )
web_entry.grid(column=1, row=1)
web_entry.focus()

# Email/Username Entry
email_entry = autocomplete.AutocompleteCombobox(width=33,
                                                completevalues=emails
                                                )
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "claytonjarretteng@gmail.com")

# Password Entry
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# ---- Buttons ---- #

# 'Generate Password' Button
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)

# 'Add' Button
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

# 'Search' Button
search_button = Button(text="Search", width=13, command=website_search)
search_button.grid(column=2, row=1)
window.mainloop()
