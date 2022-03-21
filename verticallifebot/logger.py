import logging
import os

TEST = os.environ.get('TEST')

if TEST == 'True':
    logging_level = logging.INFO
else:
    logging_level = logging.WARN

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging_level,
                    datefmt='%Y-%m-%d %H:%M:%S')
