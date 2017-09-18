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
from hatena.bookmark import Bookmark
from hatena.user import User
#from hatena.recommend import Recommend
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

    logging.basicConfig(level=logging.INFO)
    engine = create_engine(ENGINE)

    my_u = User(engine, user)
    my_b = Bookmark(engine, my_u, True)
    my_b.save()
    logging.info('Save Url-->')

    # TODO: create transaction the below process.
    for f in my_b.feeds:
        users = f.extract()
        for u in users:
            logging.info(u.id)
            logging.info(u.name)
            time.sleep(1)
            b = Bookmark(engine, u)
            b.save()
            break
    logging.info('--->Export Result')
    # Recommend
    #r = Recommend(engine)
    #recs = r.select()
    #for r in recs:
    #    print(r)
    logging.info('--->END')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', required=True, help='User name')
    args = parser.parse_args()
    main(args.user)
