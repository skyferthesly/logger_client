import os
import configparser
from logger_client.client import LoggerClient

if 'SIMPLIFIED_LOGGER_SERVER_URI' in os.environ and 'MESSAGES_ENDPOINT' in os.environ:
    base_url = os.environ['SIMPLIFIED_LOGGER_SERVER_URI']
    messages_endpoint = os.environ['MESSAGES_ENDPOINT']
else:
    config = configparser.ConfigParser()
    config.read('config.ini')
    base_url = config['DEFAULT'].get('SERVER_URI')
    messages_endpoint = config['DEFAULT'].get("MESSAGES_ENDPOINT")

if __name__ == '__main__':
    client = LoggerClient("%s%s" % (base_url, messages_endpoint))
    client.run()
