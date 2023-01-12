import bs4
import requests
import os
import time

# Establish global variables
mypagenumber = 1
booknumber = ""
totalpages = ""

# Introduction to the program
input ("""REFACTORED VERSION 12/01/23

author: kirill.olegovich31@gmail.com
github: github.com/IdoubledareU31/

This program will allow you to search and bulk download ENGLISH audiobooks from the website:
https://fulllengthaudiobook.com/

All files from one audiobook will be saved to a new dedicated folder created in the same
directory as this program.
 
Please, follow the instructions.

---------PRESS ENTER TO CONTINUE---------


""")


search = input ("What do you want to search for?\n").replace(" ", "+")

def all_books_on_page_func(pagenumber: int) -> list:
    """This function returns a list of all the books and writes a total number of 
    available pages to a global variable
    """

    global search

    # Get a response from the page
    response = requests.get("https://fulllengthaudiobook.com/page/" + str(pagenumber) + "/?s=" + search)
    # print ("https://fulllengthaudiobook.com/page/" + str(pagenumber) + "/?s=" + search)
    print("!!!!Should be shown once!!!!!!!!!")

    # Create soup
    soup = bs4.BeautifulSoup(response.text, "lxml")

    # Find a class that contains each book. Name of the class starts with a dot and all spaces are dots
    list_of_books_on_page = soup.select(".entry.clearfix")

    # Looking for a total number of pages available in this particular search and assign to a global variable
    global totalpages
    if soup.select(".page-numbers") == []:
        totalpages = 1
    elif soup.select(".page-numbers")[-1].text == "»":
        totalpages = soup.select(".page-numbers")[-2].text
    else:
        totalpages = soup.select(".page-numbers")[-1].text

    #     print (totalpages)

    return list_of_books_on_page

def booknumber_on_the_page(all_books_on_page: list) -> None:
    """The following fuction prints a menu and lits available books on the current web page"""

    global pagenumber
    global totalpages
    list_of_titles_per_page = []
    list_of_enumerated_titles = []
    for book in all_books_on_page:
        if len(book.select("p")[0].text) == 1:
            list_of_titles_per_page.append(book.select("p")[1].text)
        else:
            list_of_titles_per_page.append(book.select("p")[0].text)

    # print (list_of_titles_per_page)
    for a, b in enumerate(list_of_titles_per_page, start=1):
        list_of_enumerated_titles.append((a, b))

    # Following statments explain navigation for the user
    print("\nThe page number is {} of {}\n".format(mypagenumber, totalpages)+
    "Amount of books on the page is {}\n".format(len(list_of_enumerated_titles))+
    "Use the following inputs:"+
    "0     - to turn the page forward\n"+
    "00    - to turn the page backward\n"+
    "000   - to change the search\n"+
    "close - to exit the program")

    for a, b in list_of_enumerated_titles:
        print(str(a) + ")", b)

def switching_pages_and_book_number() -> str:
    """This function switches pages and allowes you to quit the program"""

    global mypagenumber
    
    list_of_books_on_page = all_books_on_page_func(mypagenumber)  
    booknumber_on_the_page(list_of_books_on_page)
    total_amount_of_books_on_page = len(list_of_books_on_page)

    while True:
        try:
            x = input("\nWhich book do you want to download? Enter the number: ")
            print("\n" * 10)

            # Go one page forward
            if x == "0":
                mypagenumber += 1
                list_of_books_on_page = all_books_on_page_func(mypagenumber)  
                booknumber_on_the_page(list_of_books_on_page)
                total_amount_of_books_on_page = len(list_of_books_on_page)

            # Go one page backward
            elif x == "00":
                mypagenumber -= 1
                list_of_books_on_page = all_books_on_page_func(mypagenumber)  
                booknumber_on_the_page(list_of_books_on_page)
                total_amount_of_books_on_page = len(list_of_books_on_page)

            # Search for another title
            elif x == "000":
                global search
                mypagenumber = 1
                search = input("\n\nAre you not satisfied with the search results?\nWhat do you want to search for?\n")
                list_of_books_on_page = all_books_on_page_func(mypagenumber)  
                booknumber_on_the_page(list_of_books_on_page)
                total_amount_of_books_on_page = len(list_of_books_on_page)

            # Return the number of the chosen title 
            elif int(x) >= 1 and int(x) <= total_amount_of_books_on_page:
                return int(x)
        
            # User wants to exit the program
            elif x == "close":
                return x

            # User's input is invalid
            else:
                print("The input is invalid. Try again.")
                booknumber_on_the_page(all_books_on_page_func(mypagenumber))
        
        except ValueError as e:
            # User's input is invalid
            print(str(e) + "\nThe input is invalid. Try again.")
            time.sleep(0.5)
            booknumber_on_the_page(all_books_on_page_func(mypagenumber))

        

def listoflinksfiles_func(booknumber: str) -> list:
    """The fuction take a number of a book on a current web page and returns 
    a list of links to the files of the books
    """

    book = all_books_on_page_func(mypagenumber)[int(booknumber)-1]
    list_of_links = [] #list of all the links to all the files of the book
    # print(book.select(".wp-audio-shortcode"))
    links_to_files = book.select(".wp-audio-shortcode")
    for item in links_to_files:
    #     print (item.text)
        list_of_links.append (item.text)
#     print (list_of_links)
    return list_of_links


def main():
    while True:
        booknumber = switching_pages_and_book_number()
        if booknumber == "close":
            print("The program will close.")
            input()
            break
        else:
            print("here!")
            list_of_links = listoflinksfiles_func(booknumber)
            print ("\nThis book consists of {} files".format(len(list_of_links)))
            answer = input ("Do you still want to download? y/n? ")

            if answer[0].lower() == "y":
                print ("\nDownload started. Please, wait...")
                for link in list_of_links:
                    title = link.split("/")[-2].replace("%20", " ")
                    number = link.split("/")[-1].split(".")[-2].replace("%20", "")
                    formatt = "."+link.split(".")[-1]

                    try:
                        os.mkdir(title)
                    except Exception:
                        pass

                    with open (title+"/"+number+" "+title+formatt, "bw") as f:
                        f.write (requests.get(link).content)

                input ("-----------ALL FILES WERE SUCCESSFULLY DOWNLOADED-----------")

            else:
                return


if __name__ == "__main__":
    main()