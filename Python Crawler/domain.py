from urllib.parse import urlparse#this part is mainly used to get the domains only in the form of xxx.xxx

def get_sub_domain_name(url):
    try: #always remember to use try&except when connecting to a website!!
        return urlparse(url).netloc #use thr netloc method to get the localmethod of the url you just fed
    except:
        return "" #you have to return something


def get_domain_name(url): 
    try:
        results = get_sub_domain_name(url).split(".")# split function is used to split a string with the character you input, like here it is ".", so it is going to chop the string into an item in the list whenever it sees the character
        return results[-2] + "." + results[-1]#"-2" means the second item to the last in this list
    
    except:
        return ""


