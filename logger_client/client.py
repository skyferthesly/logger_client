import json
import requests
from requests.exceptions import ConnectionError
from tkinter import Tk, Label, Button, Entry, Text, Frame, OptionMenu, StringVar, END


class LoggerClient(object):
    def __init__(self, messages_endpoint):
        self.messages_endpoint = messages_endpoint

        # main window
        self.container = Tk()
        self.container.title('Logger Client')
        self.width = 402
        self.height = 267
        self.container.geometry('%sx%s' % (self.width, self.height))
        self.container.config(bg='grey')
        # required fields frame
        self.fields_frame = Frame(self.container)
        self.fields_frame.grid(row=0, column=0, sticky="W", padx=5, pady=5)
        self.fields_frame.config(highlightthickness=3)
        self.fields_frame.config(highlightbackground='grey')

        self.message_type_label = Label(self.fields_frame, text='Type', font="bold")
        self.message_type_label.grid(row=0, column=0)
        self.message_label = Label(self.fields_frame, text='Log Message', font="bold")
        self.message_label.grid(row=0, column=1)

        var = StringVar(self.container)
        var.set("INFO")
        self.message_type_optionmenu = OptionMenu(self.fields_frame, var, "INFO", "ERROR",
                                                  command=self.set_message_type)
        self.message_type_optionmenu.grid(row=1, column=0)

        self.message_textbox = Entry(self.fields_frame, width=51)
        self.message_textbox.grid(row=1, column=1)

        # optional fields frame
        self.optionals_frame = Frame(self.container)
        self.optionals_frame.grid(row=1, column=0, sticky="W", padx=5, pady=5)
        self.optionals_frame.config(highlightthickness=3)
        self.optionals_frame.config(highlightbackground='grey')
        self.email_label = Label(self.optionals_frame, text="Email", font="bold")
        self.email_label.grid(row=2, column=0)
        self.email_textbox = Entry(self.optionals_frame, width=55)
        self.email_textbox_default = 'This field is optional'
        self.email_textbox.insert(0, self.email_textbox_default)
        self.email_textbox.grid(row=2, column=1)

        # login frame
        self.login_frame = Frame(self.container)
        self.login_frame.grid(row=2, column=0, columnspan=20, sticky="W", padx=5, pady=5)
        self.login_frame.config(highlightthickness=3)
        self.login_frame.config(highlightbackground='grey')

        self.username_label = Label(self.login_frame, text='Username', font="bold")
        self.username_label.grid(row=0, column=0)
        self.username_textbox = Entry(self.login_frame, width=33)
        self.username_textbox.grid(row=0, column=1)

        self.password_label = Label(self.login_frame, text='Password', font="bold")
        self.password_label.grid(row=1, column=0)
        self.password_textbox = Entry(self.login_frame, width=33, show="*")
        self.password_textbox.grid(row=1, column=1)

        self.send_button = Button(self.login_frame, text='Send', command=self.send, width=10, font="bold", bg="green")
        self.send_button.grid(row=1, column=2, sticky="W")

        # response frame
        self.response_frame = Frame(self.container)
        self.response_frame.grid(row=3, column=0, sticky="W", padx=5, pady=5)
        self.response_frame.config(highlightthickness=3)
        self.response_frame.config(highlightbackground='grey')
        self.response_label = Label(self.response_frame, text="Response", font="bold")
        self.response_label.grid(row=0, column=0)
        self.response_textbox = Text(self.response_frame, width=47, height=2)
        self.response_textbox.grid(row=1, column=0)

        self.message_type = None

    def set_message_type(self, value):
        self.message_type = value

    def clear_response(self):
        self.response_textbox.delete(self.response_textbox.index("end-1c linestart"), END)

    def get_auth_payload(self):
        username = self.username_textbox.get()
        password = self.password_textbox.get()
        if not username or not password:
            return None
        return username, password

    def post_message(self, data):
        return requests.post(self.messages_endpoint, auth=data.pop('auth'), data=json.dumps(data))

    def send(self):
        self.clear_response()

        message = self.message_textbox.get()
        if not message:
            self.response_textbox.insert(END, "Please enter a Log Message.")
            return

        auth = self.get_auth_payload()
        if not auth:
            self.response_textbox.insert(END, "Please enter a username and password.")
            return

        email_text = self.email_textbox.get()
        email = email_text if email_text != self.email_textbox_default else None

        payload = dict()
        payload['message'] = message
        payload['message_type'] = self.message_type
        payload['auth'] = auth
        if email:
            payload['email'] = email

        try:
            res = self.post_message(payload)
        except ConnectionError:
            self.clear_response()
            self.response_textbox.insert(END, "Could not connect to server. Please contact your system administrator.")
        else:
            if res.status_code == 401:
                self.response_textbox.insert(END, "Invalid username/password.")
            elif res.status_code == 400:
                self.response_textbox.insert(END, json.loads(res.text)['message'])
            elif res.status_code == 200:
                self.response_textbox.insert(END, "Log message saved.")
                self.message_textbox.delete(0, END)
                self.email_textbox.delete(0, END)
                self.email_textbox.insert(END, self.email_textbox_default)
            elif res.status_code == 500:
                self.response_textbox.insert(END,
                                             "The server didn't understand how to handle the request. Please contact your system administrator.")
            else:
                self.response_textbox.insert(END, "Unknown response code: %s" % res.status_code)

    @classmethod
    def run(cls):
        import os
        import configparser
        env_uri = os.environ.get('SIMPLIFIED_LOGGER_SERVER_URI')
        env_messages_ep = os.environ.get('MESSAGES_ENDPOINT')
        if env_uri and env_messages_ep:
            base_url = os.environ['SIMPLIFIED_LOGGER_SERVER_URI']
            messages_endpoint = os.environ['MESSAGES_ENDPOINT']
        else:
            config = configparser.ConfigParser()
            config.read('config.ini')
            base_url = config['DEFAULT'].get('SERVER_URI')
            messages_endpoint = config['DEFAULT'].get("MESSAGES_ENDPOINT")

        client = cls("%s%s" % (base_url, messages_endpoint))
        client.container.mainloop()
