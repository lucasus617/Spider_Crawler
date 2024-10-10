import os

# automatically help you create a folder for project you crawl

def create_project_dir(directory):
    if not os.path.exists(directory):
        print("creating directory" + directory )
        os.makedirs(directory )

#create_project_dir("hongrun")

def create_data_files(project_name, base_url):
    queue = project_name + "/queue.txt"
    crawled = project_name + "/crawled.txt" # create the directory for queue and crawled links
    if not os.path.isfile(queue):
        write_file(queue, base_url)# create the files but with its first queued link to crawl
    if not os.path.isfile(crawled):
        write_file(crawled, "")

def write_file(path,data):
    f = open(path, 'w')# switch the file to write mode
    f.write(data)
    f.close()

#create_data_files("hongrun", "https://www.hongrun.ink/")

#append data
def append_to_file(path,data):
    with open(path, "a") as file:
        file.write(data+ "/n")

#delete data by creating a new file to override
# Delete data by creating a new file to override
def delete_file_contents(path):
    with open(path, "w") as file:  # Open the file in write mode to clear its contents
        pass  # Pass does nothing; this effectively empties the file

#file to set in order to run the program faster with varariables
def file_to_set(file_name):
    result = set()
    try:
        with open(file_name, 'r') as file:
            for line in file:
                result.add(line.strip())
    except FileNotFoundError:
        print("Error: File not found")
    except Exception as e:
        print("Error reading file:", str(e))
    return result
#set to file in order to save your data whenever you need to tempertarily close your crawler
def set_to_file(links, file): # links represents set, file represents file
    delete_file_contenets(file) #in case any remain data
    for link in links:
        append_to_file(file, link)

