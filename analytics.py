import re, requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urlparse

wordDict = defaultdict(int)
subdomains = defaultdict(set)
def main():
    count = 0
    longestPage = ("link", 0)
    file = open("test.txt", "r")
    output = open("output.txt", 'w')

    for line in file:
        print("new line")
        line = line.split()
        link = line[8].strip(",")

        count += 1

        words = check_words(link)

        print("Checking length of page")
        if len(words) > longestPage[1]:
            longestPage = (link, len(words))

        word_dict(words)

        valid_subdomain(link)

    # Writing to output file
    output.write("Analytics for Web Crawler\n")
    output.write("Unique pages found: " + str(count) + '\n')
    output.write("The longest page in terms of words is: " + longestPage[0] + " with " + str(longestPage[1]) + " words ")

    output.write("The 50 Most Common Words Are:\n")
    counter = 0
    for k, v in sorted(wordDict.items(), key=lambda x: x[1], reverse=True):
        counter += 1

        if counter <= 50:
            output.write(str(k) + " " + str(v) + "\n")
        else:
            break

    output.write("The List of Subdomains Found:\n")
    for k, v in sorted(subdomains.items(), key=lambda x: x[1], reverse=True):
        output.write(str(k) + " " + str(len(v)))

    file.close()
    output.close()

def tokenize(unicode):
    str = unicode.encode('utf-8')
    split_str = re.split('[^A-Za-z]', str.decode('utf-8'))

    tokens = []
    for word in split_str:
        if len(word) > 0:
            word = word.lower()
            tokens.append(word)

    return tokens


def check_words(url):
    try:
        print("inside check_words")
        print(url)
        # send GET request to url
        page = requests.get(url)
        # parse url page for html content
        soup = BeautifulSoup(page.content, 'html.parser')
        # find all text content in given web page
        content = soup.find_all('p')

        # tokenize valid text content
        original_text = []
        for item in content:
            if item.get_text():
                original_text.extend(tokenize(item.get_text()))
        print("finished getting words")
        return original_text

    except:
        print("url not downloaded")
        return []


def word_dict(wordList):
    print("inside word_dict")
    global wordDict

    stop_words = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't",
                  'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
                  "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't",
                  'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have',
                  "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him',
                  'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is',
                  "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself',
                  'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our',
                  'ours\tourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's",
                  'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs',
                  'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're",
                  "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't",
                  'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's",
                  'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't",
                  'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself',
                  'yourselves']

    for word in wordList:
        if word not in stop_words:
            wordDict[word] += 1
    print("filtered words")

def valid_subdomain(link):
    print("checking subdomains")
    global subdomains
    parsed = urlparse((link))

    if 'ics.uci.edu' in parsed.netloc:
        subdomains[parsed.netloc].add(link)

if __name__ == '__main__':
    main()



