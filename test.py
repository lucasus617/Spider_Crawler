from urllib.request import urlopen
response = urlopen("http://htmltemp.vteamer.cc/")
read_bytes = response.read()
string = ""
string = read_bytes.decode("utf-8")
print(string)