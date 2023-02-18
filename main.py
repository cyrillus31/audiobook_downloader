import bs4
import requests
import os
import time


class Interface:
    def __init__(self, search):
        self.search = search     # the search string
        self.current_page = 1    # currently displayed page
        self.total_pages = 1     # total number of of available pages
        self.soup = None         # the soup of the page
        self.display_step = 1    # result from how many pages will be displayed
        self.warhning = ""       # warning if user tries to go beyond the pages bound
        self.restart = True      # if we should do the search again

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
            self.total_pages = soup.select(".page-numbers")[-2].text
            # self.display_step = 1
        else:
            self.total_pages = soup.select(".page-numbers")[-1].text
            # self.display_step = 2


    def display(self):
        books = list(enumerate([book.select("p")[0].text for book in self.soup.select(".entry.clearfix")], 1))
        print("\n"*100) # to clear the screen
        print(self.warning) # warning if the user tries to go beyond the pages bound
        print(f"""You were searching for: {self.search}
The page number is {self.current_page} of {self.total_pages}
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
        command = input("Enter your command: ")

        if command == "0" and self.current_page != self.total_pages:
            self.current_page += 1
            return 0

        elif command == "00" and self.current_page != 1:
            self.current_page -= 1
            return 0

        elif command == "000":
            return 0
        
        else:
            try:
                command = int(command) 









if __name__ == "__main__":

    while True:
        search = input ("What do you want to search for?\n").replace(" ", "+")

        mysearch = Interface(search)
        mysearch.get_data()
        mysearch.display()
        if mysearch.prompt()









