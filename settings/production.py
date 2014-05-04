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
