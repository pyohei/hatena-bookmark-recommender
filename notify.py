"""Notification recommend feed."""

import requests
import os
from datetime import datetime

def main():
    """Send message with Line"""
    params = {"value1": "{}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}
    url = os.environ.get('HATENA_FEED_NOTIFICATION_URL', '')
    r = requests.post(url, params)
    print(r)

if __name__ == '__main__':
    main()
