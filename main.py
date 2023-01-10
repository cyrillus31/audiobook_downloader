"""
LOGIC of the main loop
1. Open first page
2. Create soup
3. Find all books on the page
4. Swithcing the pages loop and showing results of all the books present
4. Choose a book
5. Create a list with a links to all files
6. PROFIT!!
"""

import bs4
import requests
import os

input ("""
UPDATED VERSION 11/23/22

____________________!!!!!!!!!!THIS IS NEW INFORMATION!!!!!!!!!!_________________
(in the previous version the link was with "s" at the end https://fulllengthaudiobooks.com/)



This script will allow you to search and bulk download ENGLISH audiobooks from the website:
https://fulllengthaudiobook.com/


All files from one audiobook will be saved to a new dedicated folder created in the same
directory where this script is located.
 
Please, follow the instructions.

---------PRESS ENTER TO CONTINUE---------


""")

mypagenumber = 1
booknumber = ""
totalpages = ""
search = input ("What do you want to search for?\n").replace(" ", "+")

# This function prodcues a list of all the books and writes a total number of available pages to a global variable
def all_books_on_page_func(pagenumber: int) -> list:
    global search

    # Get a response from the page
    response = requests.get("https://fulllengthaudiobook.com/page/" + str(pagenumber) + "/?s=" + search)
    # print ("https://fulllengthaudiobook.com/page/" + str(pagenumber) + "/?s=" + search)
    print("!!!!Should be shown once!!!!!!!!!")

    # Create soup
    soup = bs4.BeautifulSoup(response.text, "lxml")

    # Find a class that contains each book. Name of the class starts with a dot and all spaces are dots
    all_books_on_page = soup.select(".entry.clearfix")

    # Looking for a total number of pages available in this particular search and assign to a global variable
    global totalpages
    if soup.select(".page-numbers") == []:
        totalpages = 1
    elif soup.select(".page-numbers")[-1].text == "»":
        totalpages = soup.select(".page-numbers")[-2].text
    else:
        totalpages = soup.select(".page-numbers")[-1].text

    #     print (totalpages)

    return all_books_on_page

# commented this to test!!
# all_books_on_page_func(mypagenumber) 


# print a list of books on the page
def booknumber_on_the_page(all_books_on_page):
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
    "0) Turn the page forward\n"+
    "00) Turn the page backward\n"+
    "000) Change the search\n")

    for a, b in list_of_enumerated_titles:
        print(str(a) + ")", b)


# booknumber_on_the_page(all_books_on_page_func(mypagenumber))


def switching_pages_and_book_number():
    global mypagenumber
    booknumber_on_the_page(all_books_on_page_func(mypagenumber))
    while True:

        x = input("\nWhich book do you want to download? Enter the number: ")
        print("\n" * 10)
        if x == "0":
            mypagenumber += 1
            booknumber_on_the_page(all_books_on_page_func(mypagenumber))

        elif x == "00":
            mypagenumber -= 1
            booknumber_on_the_page(all_books_on_page_func(mypagenumber))

        elif x == "000":
            global search
            mypagenumber = 1
            search = input("\n\nAre you not satisfied with the search results?\nWhat do you want to search for?\n")
            booknumber_on_the_page(all_books_on_page_func(mypagenumber))

        elif int(x) >= 1 and int(x) <= len(all_books_on_page_func(mypagenumber)):
            return int(x)

# switching_pages_and_book_number()



def listoflinksfiles_func(booknumber):
    book = all_books_on_page_func(mypagenumber)[int(booknumber)-1]
    list_of_links = [] #list of all the links to all the files of the book
    # print(book.select(".wp-audio-shortcode"))
    links_to_files = book.select(".wp-audio-shortcode")
    for item in links_to_files:
    #     print (item.text)
        list_of_links.append (item.text)
#     print (list_of_links)
    return list_of_links

thelist = listoflinksfiles_func(switching_pages_and_book_number())



print ("\nThis book consists of {} files".format(len(thelist)))
answer = input ("Do you still want to download? y/n? ")
if answer[0].lower() == "y":
    print ("\nDownload started. Please, wait...")
    for link in thelist:
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
    input ("-----------RESTART THE PROGRAM AND TRY AGAIN-----------")
