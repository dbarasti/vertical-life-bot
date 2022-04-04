from dotenv import load_dotenv

from verticallifebot.scraper import launch
from verticallifebot.logger import logging
import sys

load_dotenv()


def main():
    try:
        launch()
    except Exception as e:
        logging.error("Error executing application. Shutting down...")
        logging.exception(e)
        sys.exit()


if __name__ == "__main__":
    main()
