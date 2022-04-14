import requests
import csv
import time
start_time = time.time()

with open('gutenberg100.csv') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        url = row['link href']
        # get the id from the url
        bookId = url[33:]

        # to download the book, we need to download from the url
        # http://aleph.gutenberg.org/ , adding the id to the end as
        # subdirectories. Each digit in the id is a subdirectory.
        # The book is the .txt file in the subdirectory.
        subdirectoriesPath = bookId[0: -1].replace("", "/")[1: -1]

        # Make a request and get the content as text
        bookUrl = "http://aleph.gutenberg.org/" + subdirectoriesPath + "/" + bookId
        response = requests.get(bookUrl)
        s = response.text

        # Find the name of the .txt file (this is needed as they sometimes
        # have extra digits in the filename)
        # This is a little hacky, but it works
        positionOfTxt = s.find(".txt")
        subString = s[positionOfTxt - 18: positionOfTxt]
        start = '<a href="'
        txtPath = subString[subString.find(start) + len(start):] + '.txt'

        # download the book
        downloadUrl = bookUrl + "/" + txtPath
        title = row['title']
        print('start download of ' + title)
        with open('./books/' + title + ".txt", 'w', encoding='utf-8') as file:
            # fetch
            response = requests.get(downloadUrl)
            response.encoding = 'utf-8'
            file.write(response.text)

        # wait for a bit
        print('download finished')
        print('waiting 1 seconds')
        time.sleep(1)

print("--- %s seconds ---" % (time.time() - start_time))
