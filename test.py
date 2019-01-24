import requests, os, sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


menustring1 = "(1) Choose download directory"
menustring2 = """(2) Start Scraping
(3) Exit
"""
modestring = """(1) 4Chan
(2) Ylilauta
(3) Back """
spacer = "-----------------------------------"

print(spacer + "\nWelcome to imgboarder!\n" + spacer)

download_dir = ""

def main():
    while True:
        try:
            with open("settings.txt") as conf_file:
                download_dir = conf_file.readline()
        except FileNotFoundError:
            print("Settings.txt not found, creating one...")
            download_dir = "none"
            conf_file = open("settings.txt", 'w')
            conf_file.close()
            print("Done!\n" + spacer)

        try:
            print(menustring1 + " (Set to: " + download_dir + ")")
            userpick = int(input(menustring2 + "Choose action: "))

            if(userpick == 1):
                print(spacer)
                download_dir = dirsetter()
            elif(userpick == 2):
                while True:
                    try:
                        print(spacer)
                        mode = int(input(modestring + "\n" + "Please specify imageboard: "))
                        if(mode == 1):
                            print(spacer)
                            scrape_4chan(download_dir)
                        elif(mode == 2):
                            print(spacer)
                            scrape_Ylilauta(download_dir)
                        elif(mode == 3):
                            print(spacer)
                            main()
                        else:
                            print(spacer+"\nInput not recognized\n"+spacer)
                            continue
                    except ValueError:
                        print(spacer+"\nInput not recognized")
                        continue
            elif(userpick == 3):
                print(spacer + "\nQuitting >>>")
                sys.exit()
            else:
                print(spacer+"\nInput not recognized\n"+spacer)
                continue
        except ValueError:
            print(spacer+"\nInput not recognized\n"+spacer)
            continue

def dirsetter():
    while True:
        new_dir = str(input("Please enter a path to save images to:  "))
        if(os.path.isdir(new_dir) == True):
            with open("settings.txt", 'w') as conf_file:
                conf_file.write(new_dir)
            print("Path set to " + new_dir + "\n" + spacer)
            return new_dir
        else:
            print('Directory "'+new_dir+'" not found\n'+spacer)
            continue

def url_validator():
    while True:
        try:
            url = str(input('Enter page url ("e" to exit): '))
            if(url == "e"):
                main()
            else:
                req = requests.get(url)
                if(req.status_code == 200):
                    print("url ok, proceeding...")
                    return url, req
                else:
                    pass
        except Exception:
            print("Invalid url")
            continue

def scrape_4chan(download_dir):
    while True:
        if(os.path.isdir(download_dir) == True):
            break
        else:
            print("Download directory not found/set")
            download_dir = dirsetter()
            continue

    url, page = url_validator()
    soup = BeautifulSoup(page.content, "html.parser")
    download_links = []

    for a in soup.findAll("a", attrs={"class":"fileThumb"}):
        x = "https:" + (a["href"])
        download_links.append(x)

    print(str(len(download_links)) + " images found.")

    while True:
        try:
            print(spacer+"\n(1) List images\n(2) Download images\n(3) Back")
            pick = int(input("Please choose action: "))

            if(pick == 1):
                print(spacer)
                for link in download_links:
                    print(link)
                continue
            elif(pick == 2):
            	img_downloader(download_links, download_dir)
            elif(pick == 3):
            	main()
            else:
            	print("\nInput not recognized\n"+spacer)
        except ValueError:
        	print("\nInput not recognized\n"+spacer)

def scrape_Ylilauta(download_dir):
    while True:
        if(os.path.isdir(download_dir) == True):
            break
        else:
            print("Download directory not found/set")
            download_dir = dirsetter()
            continue

    while True:
        try:
            url = str(input('Enter page url ("e" to exit): '))
            if(url == "e"):
                main()
            else:
                page = requests.get(url)
                soup = BeautifulSoup(page.content, "html.parser")
                print("url ok, proceeding...")
                break
        except Exception:
            print("url not valid or responding")
            continue
    print("""Launching Firefox in headless mode
    Scraping Javascript, this might take a moment...""")

    options = Options()
    options.headless = True
    ex_path = "geckodriver"
    driver = webdriver.Firefox(options=options, executable_path=ex_path)
    driver.get(url)
    stuff = driver.page_source
    driver.quit()
    parsed_stuff = BeautifulSoup(stuff, features='lxml')
    print("Done!\n" + spacer)

    download_links = []
    for a in parsed_stuff.findAll("a", attrs={"class":"file-content"}):
        x = (a["href"])
        download_links.append(x)

    print(str(len(download_links)) + " images found.")

    while True:
        try:
            print(spacer+"\n(1) List images\n(2) Download images\n(3) Back")
            pick = int(input("Please choose action: "))
            if(pick == 1):
                print(spacer)
                for link in download_links:
                    print(link)
                    continue
            elif(pick == 3):
                main()
            elif(pick == 2):
                img_downloader(download_links)
        except Exception:
            print("Undefined input, try again.")

def img_downloader(download_links, download_dir):
    for link in download_links:
    	print("Downloading image "+ link)
    	filename = link.split("/")[-1]
    	filetosave = download_dir+"/"+filename
    	exists = os.path.isfile(filetosave)

    	if(exists == True):
    		print("File "+filename+" already exists, skipping...")
    		continue
    	f = open(filetosave,"wb")
    	f.write(requests.get(link).content)
    	f.close()

    print(spacer+"\nDownloaded "+str(len(download_links))+" images succesfully!")
    print(spacer)
    main()

    

if __name__ == '__main__':
    main()