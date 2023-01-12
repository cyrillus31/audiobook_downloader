# English Audiobooks Downloader

## Description/ Описание

This program will allow you to search and bulk download english audiobooks from the website:  
https://fulllengthaudiobook.com/

All files from one audiobook will be saved to a new dedicated folder created in the same
directory as this program.
___

Данная программа позволяет осуществлять поиск аудиокниг сайта https://fulllengthaudiobook.com/ и скачивать сразу всё файлы одной аудиокниги.

Все файлы одной аудиокниги будут сохранены в отдельную папку, созданную в той же директории, где находится программа.


## Under the hood/ Под капотом
Various webscraping techniques are utilized.
The program searches the website for audiobooks using [query strings](https://en.wikipedia.org/wiki/Query_string) via [requests](https://requests.readthedocs.io/en/latest/) library, receives an html file and parses it with [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io/en/latest/), looking for the titles and links to the audio files. A user is presented with a list of books gathered on a current webpage in accordance with the initial request. From then on user can move forwards and backwards from page to page. Once the user finds the desired audiobook, he can select it and download all audiofiles to a new dedicated folder. Error handling is impemented.
___
Для поиска аудиокниг используется вебскрейпинг. Перемещение по сайту осуществляется через [query strings](https://en.wikipedia.org/wiki/Query_string) с помощью библиотеки [requests](https://requests.readthedocs.io/en/latest/). Для парсинга получаемых html файлов используется библиотека [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io/en/latest/). В результате парсинга формируется список книг, предсталенных на конкретной веб странице (в соответствии с запросом), который демонстрируется пользователю. Далее пользователь может перемещаться со страницы на страницу, просматривая имеющиеся аудиокниги. Пользователь может выбрать понравившуюся книгу и скачать все аудиофайлы в папку, создаваемую по адресу расположения программы. Обработка ошибок производится.


## ToDo
. . .  

## About the author
[LinkedIn](https://www.linkedin.com/in/kirill-fedtsov-a37209159/)  
[Telegram](https://t.me/idoubledareu31)  