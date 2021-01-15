import csv
import pandas as pd
import requests
import sqlite3
from bs4 import BeautifulSoup
import pyttsx3 as pt
import speech_recognition as sr

# Extracting Microsoft Speech API

engine = pt.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)


# Function to make program speak

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


if __name__ == "__main__":
    speak("Hello! How you Doing? Please Name Your Query")


# Function to take commands by user

def command():
    r_1 = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening.....")
        r_1.pause_threshold = 1
        audio = r_1.listen(source)
        q = ''
        try:
            print("recognising.......")
            q = r_1.recognize_google(audio, language="eng-in")
            print(q)
        except Exception:
            speak("Can You Please Repeat?")
            print("can you please repeat?")
            return "None"
        return q


main_list = []  # this is the main list where every list will be appended
title_list = []  # this is the where all the title_2 contents will be
title_2 = []  # this is the list where all the iterated titles will be
detail_list = []  # this is the list where all the author details will be
detail_2 = []  # this is the list where all the iterated author details will be
link_list = []  # this is the list where all the link_2 items will be
link_2 = []  # this is the list where all the iterated links will be
duration_list = []  # this is the list where all the duration_2 contents will be
duration_2 = []  # this is where all the iterated reading time content will be

url_1 = 'https://medium.com/search?q='
url = url_1 + command()
r = requests.get(url)
html_content = r.content
# print(html_content)

soup = BeautifulSoup(html_content, 'html.parser')
# print(soup.prettify())

titles = soup.find_all('h3', class_='graf--title')  # here all titles will be iterated
details = soup.find_all('a', class_='link--darken')  # here all authors will be iterated
links = soup.find_all('div', class_='postArticle-content')  # here all links will be iterated
durations = soup.find_all('span', class_='readingTime')  # here all the reading time will be iterated
for title in titles:
    t = title.text
    # print(title.text)
    title_2 = [t]
    title_list.append(title_2)
for detail in details:
    a = detail.text
    # print(detail.text)
    detail_2 = [a]
    detail_list.append(detail_2)
for link in links:
    l = link.a['href']
    # print(link.a['href'])
    link_2 = [l]
    link_list.append(link_2)
for duration in durations:
    d = duration['title']
    # print(duration['title'])
    duration_2 = [d]
    duration_list.append(duration_2)


# code for extracting author's names

indices_to_access_authors = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27]
a_series_authors = pd.Series(detail_list)
accessed_series_author = a_series_authors[indices_to_access_authors]
accessed_list_authors = list(accessed_series_author)

# code for extracting dates

indices_to_access_dates = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]
a_series_dates = pd.Series(detail_list)
accessed_series_dates = a_series_dates[indices_to_access_dates]
accessed_list_dates = list(accessed_series_dates)

# code for extracting websites on which author wrote

indices_to_access_websites = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28]
a_series_websites = pd.Series(detail_list)
accessed_series_websites = a_series_websites[indices_to_access_websites]
accessed_list_websites = list(accessed_series_websites)
# print(detail_list)
print(title_list)
print(link_list)
# print(duration_list)
print(accessed_list_authors)
print(accessed_list_dates)
print(accessed_list_websites)

main_list.append(title_list)
main_list.append(accessed_list_authors)
main_list.append(accessed_list_websites)
main_list.append(accessed_list_dates)
main_list.append(link_list)
main_list.append(duration_list)
# print(main_list)


# Creating a Database
conn = sqlite3.connect('scraped_data.bd')
c = conn.cursor()

#  Creating a Table

c.execute('''CREATE TABLE contents(Title TEXT, Author TEXT, Website TEXT, Date TEXT, Link TEXT, Duration Text)''')

# Since data here is in form os lists, so I cannot add them directly to the columns of the table, hence we have to iterate within the list or say we have to fetch the length of the list

n = len(title_list)
for i in range(n):
    c.execute('''INSERT INTO contents VALUES(?,?,?,?,?,?)''', (title_list[i][0], accessed_list_authors[i][0], accessed_list_websites[i][0], accessed_list_dates[i][0], link_list[i][0], duration_list[i][0]))
conn.commit()

# Conversion in the form of .csv file
with open('medium_data.csv', 'w') as file:
    writer = csv.writer(file)
    for item_1 in main_list:
        writer.writerow(item_1)
