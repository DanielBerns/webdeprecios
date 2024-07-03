from webclient import (identifier, password, login_bot, get_token_headers, get_post) 

import pdb

bot = login_bot(identifier, password)
token_json = bot.json()
token = token_json["token"]
auth_headers = get_token_headers(token)
for id_ in range(4):
    pdb.set_trace()
    the_post = get_post(auth_headers, id_)
    print(str(the_post))
