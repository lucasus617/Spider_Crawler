from html.parser import HTMLParser
from urllib import parse

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for (attribute, value) in attrs:
                if attribute == "href":  # When detecting href tags
                    url = parse.urljoin(self.base_url, value)  # Merge base URL
                    self.links.add(url)  # Add to the set

    def error(self, message):  # Handle errors gracefully
        pass