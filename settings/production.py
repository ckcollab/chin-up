import os

from .base import *


import logging
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)


logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='"%(asctime)s %(levelname)8s %(name)s - %(message)s"',
    datefmt='%H:%M:%S'
)

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", None)
if SECRET_KEY is None:
    assert ValueError("Missing DJANGO_SECRET_KEY environment variable!")
