from webclient import (
    create_bot,
    get_auth_headers,
    get_messages,
    clear_messages,
    publish_post
)

from consumers import Consumer
from producers import Producer


def execute(identifier: str, 
            consumer: Consumer, 
            producer: Producer
    ) -> None:
    auth_headers = get_auth_headers(identifier)
    if auth_headers:
        message_count = 0
        for message in get_messages(auth_headers):
            consumer.update(message)
            message_count += 1
        if message_count:
            clear_messages(auth_headers)
        for content in producer.content():
            publish_post(auth_headers, content) 
   
