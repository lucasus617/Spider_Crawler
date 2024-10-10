from urllib.request import urlopen
from link_finder import LinkFinder
from lib import *


class Spider:
    project_name = "hongrun"
    base_url = "https://www.shbs.org.cn/"
    domain_name = "shbs.org.cn"
    queue_file = "/queue.txt"
    crawled_file = "/crawled.txt"
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.queue_file = Spider.project_name + "/queue.txt"
        Spider.crawled_file = Spider.project_name + "/crawled.txt"
        self.boot()
        self.crawl_page("First spider", Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url:
            if page_url not in Spider.crawled:
                print(thread_name + " is crawling " + page_url)

    @staticmethod
    def gather_links(page_url):
        html_string = ""
        try:
            response = urlopen(page_url)
            if response.getheader("Content-Type") == "text/html":
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
                finder = LinkFinder(Spider.base_url, page_url)
                finder.feed(html_string)
        except:
            print("Error: cannot crawl page")
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url:
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)