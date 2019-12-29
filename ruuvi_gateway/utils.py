import logging
import time
import sys

logging.Formatter.converter = time.gmtime
logging.basicConfig(
        stream=sys.stdout,
        format='%(asctime)s %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%SZ',
        level=logging.INFO
)
logger = logging.getLogger()