import threading
from queue import Queue
from spider import Spider
from lib import *
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

PROJECT_NAME = "hongrun"
HOMEPAGE = "https://www.shbs.org.cn/"
QUEUE_FILE = PROJECT_NAME + "/queue.txt"
CRAWLED_FILE = PROJECT_NAME + "/crawled.txt"
NUMBER_OF_THREADS = 4
queue = Queue()

def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

def create_jobs():
    try:
        for link in file_to_set(QUEUE_FILE):
            queue.put(link)
        queue.join()
        crawl()
    except Exception as e:
        logging.error("An error occurred while creating jobs: %s", str(e))

def crawl():
    queue_links = file_to_set(QUEUE_FILE)
    if queue_links is not None:
        if len(queue_links) > 0:
            logging.info("%d links are waiting to be crawled", len(queue_links))
            create_jobs()
        else:
            logging.info("No links to crawl. Exiting...")
    else:
        logging.error("Error: Unable to read queue file or file is empty")

create_workers()
crawl()