from urllib.parse import urlparse

def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc  # Get the sub-domain name
    except:
        return ""

def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split(".")  # Split to get domain
        return results[-2] + "." + results[-1]
    except:
        return ""