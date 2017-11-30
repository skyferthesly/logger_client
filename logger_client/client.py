import json
import requests
from tkinter import Tk, Label, Button, Entry, BOTTOM, LEFT, Text, END, TOP

base_url = "http://127.0.0.1:5000/"
messages_endpoint = "%smessages/" % base_url
users_endpoint = "%susers/" % base_url


def get_auth_payload():
    return username_textbox.get(), password_textbox.get()


def get():
    return requests.get(base_url).text


def post_message(message):
    payload = {'message': message}
    return requests.post(messages_endpoint, data=json.dumps(payload), auth=get_auth_payload())


def send():
    message = message_textbox.get()
    if message:
        response_textbox.insert(END, post_message(message))


root = Tk()
root.title('Logger Client')
root.geometry('500x200')

response_textbox = Text(root, width=25, height=2)
response_textbox.pack(side=BOTTOM)

send_button = Button(root, text='Send', command=send)
send_button.pack(side=BOTTOM)

message_textbox = Entry(root, width=50)
message_textbox.pack(side=BOTTOM)

message_label = Label(root, text='Message')
message_label.pack(side=BOTTOM)

username_label = Label(root, text='Username')
username_label.pack(side=TOP)
username_textbox = Entry(root, width=25)
username_textbox.pack(side=TOP)

password_label = Label(root, text='Password')
password_label.pack(side=TOP)
password_textbox = Entry(root, width=25, show="*")
password_textbox.pack(side=TOP)
root.mainloop()
