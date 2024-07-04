import pdb
from markdown2 import markdown

from webclient import (
    identifier, password, login_bot, get_token_headers, 
    get_post,
    delete_post,
    publish_post
) 



dirty_posts_txt = "/home/dberns/Info/athena/webclient/dirty_posts.txt"
clean_posts_txt = "/home/dberns/Info/athena/webclient/clean_posts.txt"

bot = login_bot(identifier, password)
token_json = bot.json()
token = token_json["token"]
auth_headers = get_token_headers(token)
pdb.set_trace()
with open(dirty_posts_txt, "w") as target, \
     open(clean_posts_txt, "r") as origin:
    for id_ in [1, 2, 3, 4, 5, 6, 7, 8]:
        # the_post = get_post(auth_headers, id_)
        # target.write(f"{the_post.text:s}\n")
        # deleted = delete_post(auth_headers, id_)
        # target.write(f"{deleted.text:s}\n")
        title = origin.readline()
        link = origin.readline()
        skip = origin.readline()
        content = f"{title:s}\nInforme: {link:s}\n\n"
        html_content = markdown(content)
        print(content)
        print(html_content)
        published = publish_post(auth_headers, content)
        target.write(f"{published.text:s}\n")        
