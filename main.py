import bs4
import requests
import os
import time

from decor import time_it


class Interface:
    def __init__(self, search):
        self.search = search     # the search string
        self.current_page = 1    # currently displayed page
        self.total_pages = 1     # total number of of available pages
        self.soup = None         # the soup of the page
        self.display_step = 1    # result from how many pages will be displayed
        self.warning = ""        # warning if user tries to go beyond the pages bound
        self.restart = True      # should we stay in the inner loop?
        self.chosen_book = None  # the number of the book to download from a page

    def get_data(self):
        try:
            response = requests.get("https://fulllengthaudiobook.com/page/" + str(self.current_page) + "/?s=" + self.search)

        except requests.exceptions.RequestException as e:
            print("\n"*3 + "  There's a problem with the connetion  ".center(70, "!"), end="\n"*3)
            raise SystemExit(e)

        soup = bs4.BeautifulSoup(response.text, "lxml")
        self.soup = soup

        # Looking for a total number of pages available in this particular search 
        if soup.select(".page-numbers") == []:
            self.total_pages = 1
        elif soup.select(".page-numbers")[-1].text == "»":
            self.total_pages = int(soup.select(".page-numbers")[-2].text)
            # self.display_step = 1
        else:
            self.total_pages = int(soup.select(".page-numbers")[-1].text)
            # self.display_step = 2


    def display(self):
        books = list(enumerate([book.select("p")[0].text for book in self.soup.select(".entry.clearfix")], 1))
        print("\n"*100) # to clear the screen
        print(f"\033[0;31m{self.warning}\033[0m\n") # warning if the user tries to go beyond the pages bound
        self.warning = ""
        print(f"""You were searching for: {self.search}
The page number is \033[42m{self.current_page}\033[0m of {self.total_pages}
Amount of books on this page is {len(books)}

Enter the number of the book or use the following commands:
0     - to turn the page forward
00    - to turn the page backward
000   - to change the search
close - to exit the program

""")
        for index, title in books:
            print("%s) %s" % (index, title))

    def prompt(self):
        command = input("\nENTER YOUR COMMAND: ")

        if command == "0" and self.current_page != self.total_pages:
            self.current_page += 1
            return False # proceed to download

        if command == "0" and self.current_page == self.total_pages:
            self.warning = "!!! ERROR can't exceed the bound !!!"
            return False

        if command == "00" and self.current_page != 1:
            self.current_page -= 1
            return False

        if command == "00" and self.current_page == 1:
            self.warning = "!!! ERROR can't go below the bound !!!"
            return False

        if command == "000":
            self.restart = False
            return False 

        if command == "close":
            print("\nTHE PROGRAM WILL NOW CLOSE")
            time.sleep(1)
            exit()
        
        else:
            try:
                command = int(command) 
                self.chosen_book = command - 1
                return True # proceed to download

            except:
                self.warning = "!!! ERROR the command can't be interpreted !!!"
                return False


    @time_it
    def download(self):
        links = [link.text for link in self.soup.select(".entry.clearfix")[self.chosen_book].select(".wp-audio-shortcode")]
        print(f"\nThe book consists of {len(links)} files")
        
        answer = input("Do you still want to downloabreakd? y/n ")

        if answer[0].lower() == "y":
            print ("\nDownload started. Please, wait...")

            for link in links:
                title = link.split("/")[-2].replace("%20", "_")
                number = link.split("/")[-1].split(".")[-2].replace("%20", "")
                formatt = "."+link.split(".")[-1]

                try:
                    os.mkdir(title)

                except FileExistsError:
                    pass

                with open (title+"/"+number+"_"+title+formatt, "bw") as f:
                    f.write (requests.get(link).content)
                print("File #{} {} of {} is downloaded".format(number, title, len(links)))

if __name__ == "__main__":

    while True:
        search = input ("What do you want to search for?\n")
        # search = input ("What do you want to search for?\n").replace(" ", "+")
        if search == "close":
            exit()

        mysearch = Interface(search)
        while mysearch.restart:
            mysearch.get_data()
            mysearch.display()
            if mysearch.prompt():
                mysearch.download()
                input ("-----------ALL FILES WERE SUCCESSFULLY DOWNLOADED-----------")
            else:
                pass
                









