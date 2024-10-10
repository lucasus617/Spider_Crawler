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
                if attribute == "href": #when detected that the tag is href
                    url = parse.urljoin(self.base_url, value)# prevent the situation when there is a partial url (it can merge the base url and the partial url together without overlapping)
                    self.links.add(url)# add the url to the set for better searching
    def error(self, message):# let the parent class know what it should do if there is any error
        pass
        

    