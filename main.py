"""Hatena bookmark recommender.

This script create articles which you have interested.
The ingredient of script is Hatena user. After you give your hatena user name, this script
create your interested articles.

Usage:
    The target user can direct from argument.

      python main.py `your hatena user name`

"""

import logging
import time
from hatena.my_bookmark import MyBookmark
from hatena.bookmark import Bookmark
from hatena.user import User
from hatena.recommend import Recommend
from notify import Notification
from sqlalchemy import create_engine


ENGINE = 'sqlite:///hatena.db'


def main(user_name):
    """Main script.

    The outline of this script is the below.
      - Fetch your bookmarked urls
      - Search users from the urls 
      - Search bookmarked urls of its users
      - Recommend url from all bookmarked urls

    """
    logging.basicConfig(level=logging.INFO)
    engine = create_engine(ENGINE)

    # Cahce user date not to access duplicate.
    user_cache = []

    my_u = User(engine, user_name)
    my_b = MyBookmark(engine, my_u)
    my_b.save()

    user_cache.append(my_u.id)

    for f in my_b.new_feeds:
        users = f.extract()
        for u in users:
            time.sleep(1)
            if u.id in user_cache:
                continue
            b = Bookmark(engine, u)
            b.save()
            user_cache.append(u.id)
            break

    r = Recommend(engine)
    n = Notification(engine)
    for rec in r.select():
        n.send_line(rec)
        logging.info('--->')

    logging.info('--->END')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('hatena_user', help='Hatena user name')
    args = parser.parse_args()
    main(args.hatena_user)
