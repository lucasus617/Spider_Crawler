from urllib.request import urlopen
response = urlopen("https://www.shbs.org.cn/")
read_bytes = response.read()
string = ""
string = read_bytes.decode("utf-8")
print(string)