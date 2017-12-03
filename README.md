# Simplified Logger Client
Python GUI that allows the user to log message and optional extra data
to a configurable webservice using basic auth.

# Getting Started
1. Clone the project
2. Set the server configuration in `config.ini`
3. Run the standard `python setup.py install`
4. `python logger_client`

**NOTE**: if the client is being ran as an external dependency, you can
set the environment variables `SIMPLIFIED_LOGGER_SERVER_URI` and
`MESSAGES_ENDPOINT`. The client will look for these variables before
consulting `config.ini`

# Usage
Using the client, you can send a log message, log type, and optional email
with basic auth to a webservice. For this prototype, the only user is an
admin user with the credentials:
* username: `admin1`
* password: `pass1`

The client is designed to handle user error such as not entering a message,
or not entering authentication information. The Response textbox is
designed to inform the user of how to use the app as well as how the
server is responding.

# Improvements
Being able to send ar arbitrary amount of optional parameters would be a
great feature for the next iteration.

The client could also use some basic testing.