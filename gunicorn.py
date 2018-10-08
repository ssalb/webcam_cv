from multiprocessing import cpu_count
from os import environ

def max_workers():
    return cpu_count()

bind = "0.0.0.0:{}".format(environ.get("API_PORT", 5000))
max_requests = 1024
workers = max_workers()

# certfile=""
# keyfile=""

accesslog = "./logs/gunicorn-access.log"
errorlog = "./logs/gunicorn-error.log"
loglevel = "info"
