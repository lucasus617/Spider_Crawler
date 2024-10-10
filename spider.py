from urllib.request import urlopen
from link_finder import LinkFinder
from lib import *
import os


class Spider:
    project_name = "hongrun"
    base_url = "https://www.shbs.org.cn/"
    domain_name = "shbs.org.cn"
    queue_file = f"{project_name}/queue.txt"
    crawled_file = f"{project_name}/crawled.txt"
    queue = set()
    crawled = set()
    output_dir = ""

    def __init__(self, project_name, base_url):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.queue_file = f"{Spider.project_name}/queue.txt"
        Spider.crawled_file = f"{Spider.project_name}/crawled.txt"
        Spider.output_dir = self.create_output_dir(Spider.project_name)  # Create Output directory
        self.boot()
        self.crawl_page("First spider", Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def create_output_dir(project_name):
        output_dir = os.path.join(project_name, "Output")
        if not os.path.exists(output_dir):
            print("Creating Output directory: " + output_dir)
            os.makedirs(output_dir)
        return output_dir

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url:
            if page_url not in Spider.crawled:
                print(thread_name + " is crawling " + page_url)
                Spider.crawled.add(page_url)

                content = Spider.get_page_content(page_url)  # Get the page content
                if content:  # Check if content is retrieved
                    Spider.save_page_content(page_url, content)  # Save content to file
                else:
                    print(f"No content retrieved for {page_url}")  # Log if no content

                links = Spider.gather_links(page_url)
                Spider.add_links_to_queue(links)
                Spider.update_files()

    @staticmethod
    def get_page_content(page_url):
        try:
            response = urlopen(page_url)
            if response.getheader("Content-Type") == "text/html":
                html_bytes = response.read()
                return html_bytes.decode("utf-8")
        except Exception as e:
            print(f"Error: cannot crawl page {page_url} - {str(e)}")
        return ""

    @staticmethod
    def save_page_content(page_url, content):
        # Create a safe filename from the URL
        safe_filename = page_url.replace("https://", "").replace("http://", "").replace("/", "_") + ".txt"
        file_path = os.path.join(Spider.output_dir, safe_filename)

        print(f"Attempting to save content to {file_path}")  # Log the saving attempt
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Content successfully saved to {file_path}")  # Log successful save
        except Exception as e:
            print(f"Error saving content for {page_url} - {str(e)}")

    @staticmethod
    def gather_links(page_url):
        html_string = ""
        finder = None
        try:
            response = urlopen(page_url)
            if response.getheader("Content-Type") == "text/html":
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
                finder = LinkFinder(Spider.base_url, page_url)
                finder.feed(html_string)
        except Exception as e:
            print(f"Error: cannot crawl page {page_url} - {str(e)}")
            return set()
        if finder is not None:
            return finder.page_links()  # Call the method to get the links
        return set()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue or url in Spider.crawled:  # Avoid duplicates
                continue
            if Spider.domain_name not in url:
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)