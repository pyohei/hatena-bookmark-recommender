"""Hatena bookmark recommender.

This script create articles which you have interested .
The ingredient of script is Hatena user. After you give your hatena user name, this script
create your interested articles.

Usage:
    The target user can direct from argument.

      python main.py -u xxxxx

"""

import logging
import time
from hatena.mybook import Mybook
from hatena.bookmark import Bookmark
from hatena.feed import Feed
from hatena.recomend import Recommend
from sqlalchemy import create_engine


ENGINE = 'sqlite:///hatena.db'


def main(user):
    """Main script.

    The outline of this script is the below.
      - Fetch your bookmarked urls
      - Search users from the urls 
      - Search bookmarked urls of its users
      - Recommend url from all bookmarked urls

    """

    # Process Flow 
    logging.basicConfig(level=logging.INFO)
    logging.info('Start-->')
    engine = create_engine(ENGINE)

    my_f = Bookmark(engine, user)
    urls = my_f.load()
    my_f.save(urls, 1)
    logging.info('Fetch Url-->')

    mb = Mybook(engine)
    mb.register(urls)

    b = Feed(engine, urls)
    users = b.extract()
    b.save(users)

    # Load feed data of my reading feed users
    for user in users:
        user_no = b.load_user_no(user)
        if not user_no:
            continue
        recFeed = Bookmark(engine, user)
        urls = recFeed.load()
        recFeed.save(urls, user_no)
        time.sleep(1)
        break
    logging.info('--->Export Result')
    r = Recommend(engine)
    recs = r.select()
    for r in recs:
        print(r)
    logging.info('--->END')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', required=True, help='User name')
    args = parser.parse_args()
    main(args.user)
