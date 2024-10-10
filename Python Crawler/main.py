import threading 
from queue import Queue
from spider import Spider
from domain import *
from lib import *

PROJECT_NAME = "hongrun"
HOMEPAGE = "https://www.shbs.org.cn/"
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + "/queue.txt"
CRAWLED_FILE = PROJECT_NAME + "/crawled.txt"
NUMBER_OF_THREADS = 4
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME) #boot the system, setting directories and stuff, and call out the first spider to crawl to home page url

def create_workers():
    for _ in range(NUMBER_OF_THREADS): # if not using the _ in any formula but just want the function to loop for a certain amount of time, we use "_" as a convention
        t = threading.Thread(target = work) #the target means the function it needs to work on
        t.daemon = True
        t.start()
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()
#each link in the queue would be a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put (link)
    queue.join()
    crawl()
#check in there are links in the queue, if wo crawl them
def crawl():
    queue_links = file_to_set(QUEUE_FILE)
    if len(queue_links) > 0: #check if there are still links to be craled
        print(str(len(queue_links))+ "links are waiting to be crawled")
        create_jobs()

create_workers()
crawl()

 

