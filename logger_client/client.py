import json
import requests
from tkinter import Tk, Label, Button, Entry, BOTTOM, LEFT, Text, END

base_url = "http://127.0.0.1:5000/"


def get():
    return requests.get(base_url).text


def post(message):
    payload = {'message': message}
    return requests.post(base_url, data=json.dumps(payload))


def send():
    message = message_textbox.get()
    if message:
        response_textbox.insert(END, post(message))


root = Tk()
root.title('Logger Client')
root.geometry('400x100')

message_label = Label(root, text='Message')
message_label.pack(side=LEFT)

message_textbox = Entry(root, width=50)
message_textbox.pack(side=LEFT)

send_button = Button(root, text='Send', command=send)
send_button.pack(side=LEFT)

response_textbox = Text(root)
response_textbox.pack(side=BOTTOM)
root.mainloop()
