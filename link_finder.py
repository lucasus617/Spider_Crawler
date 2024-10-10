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
                if attribute == "href":  # When detected that the tag is href
                    url = parse.urljoin(self.base_url, value)  # Prevent partial URL issues
                    self.links.add(url)  # Add the url to the set

    def error(self, message):  # Handle errors gracefully
        pass

    def page_links(self):
        return self.links  # Add the method that returns found links