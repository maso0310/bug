from redis import Redis
from rq import Queue

q = Queue(connection=Redis())

from upload import post_image_to_url
result = q.enqueue(post_image_to_url, path=path)