import pdb
from markdown2 import markdown

from webclient import (
    identifier, password, login_bot, get_token_headers, 
    get_post,
    delete_post,
    publish_post,
    get_all_the_posts
) 



dirty_posts_txt = "/home/dberns/Info/athena/webclient/dirty_posts.txt"
clean_posts_txt = "/home/dberns/Info/athena/webclient/clean_posts.txt"

bot = login_bot(identifier, password)
token_json = bot.json()
token = token_json["token"]
auth_headers = get_token_headers(token)
pdb.set_trace()
with open(dirty_posts_txt, "w") as target:
    response = get_all_the_posts(auth_headers)
    all_the_posts = response.json()
    for key, value in all_the_posts.items():
        id_ = int(key)
        the_post = get_post(auth_headers, id_)
        target.write(f"{the_post.text:s}\n")
        deleted = delete_post(auth_headers, id_)
        target.write(f"{deleted.text:s}\n")

with open(clean_posts_txt, "r") as origin:        
    for line in origin:
        title, link = line.split("|")
        content = f"{title:s}\nInforme: {link:s}\n\n"
        html_content = markdown(content)
        print(content)
        print(html_content)
        published = publish_post(auth_headers, content)
        print(f"{published.text:s}")        
