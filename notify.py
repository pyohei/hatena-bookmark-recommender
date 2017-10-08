# coding: utf-8
"""Notification recommend feed."""

import requests
import os
from datetime import datetime

class Notify(object):

    def __init__(self, engine):
        pass

    def send_line(self):
        pass

    def _set_as_notified(self):
        pass

def main():
    """Send message with Line"""
    params = {"value1": "{}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}
    url = os.environ.get('HATENA_FEED_NOTIFICATION_URL', '')
    r = requests.post(url, params)
    print(r)

if __name__ == '__main__':
    main()
