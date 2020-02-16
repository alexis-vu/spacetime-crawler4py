# Write an function to test the quality of the content given
# Function should take in a URL
# First filter out the stop words
# count the amount of unique words and the total amount of words (minus the stopwords)
# return true if ratio is in range (0.25,0.65)
import requests
import bs4
import re
from bs4 import BeautifulSoup

def compute_word_freq(url_text):
    stopwords = open('stopwords.txt', 'r')
    word_freq = defaultdict(int)
    regEx = '[A-Z|a-z|0-9]+'

    url_text = url_text.split()
    for word in url_text:
        if word in stopwords:
            break
        if re.match(regEx, word):
            word_freq[word] += 1
    return word_freq

def printFrequencies(token_freq):
    token_freq = sorted(token_freq.items(), key = lambda t: t[1], reverse = True)
    for token in token_freq:
        print("%s -> %d" % (token[0], token[1]))

def tokenize(unicode):
    str = unicode.encode('utf-8')
    split_str = re.split('[^A-Za-z]', str)

    tokens = []
    for word in split_str:
        if len(word) > 0:
            word = word.lower()
            tokens.append(word)

    return tokens


def check_value(url):
    stop_words = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours\tourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find_all('p')

    original_text = []
    for item in content:
        if item.get_text():
            original_text.extend(tokenize(item.get_text()))

    filtered_text = []
    for text in original_text:
        if text not in stop_words:
            filtered_text.append(text)

    measure = float(len(filtered_text)) / float(len(original_text))

    return True if 0.25 < measure < 0.65 else False





def main():
    url = 'https://wics.ics.uci.edu/wics-fall-quarter-week-6-mentorship-reveal/'

    url2 = 'https://medium.com/@helen_zhang/the-4-week-plan-to-nailing-your-next-coding-technical-interview-internship-level-c5368c47e1d'

    url3 = 'https://www.informatics.uci.edu/impact/graduate-alumni-spotlights/amanda-williams/'

    url4 = 'https://wics.ics.uci.edu/events/'

    print(check_value(url4))

if __name__ == '__main__':
    main()






# #high or low value page
# def high_value_page_tester(resp_object):
#     stopwords = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours\tourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']
#
#
#     #code inspiration source: https://stackoverflow.com/questions/30565404/remove-all-style-scripts-and-html-tags-from-an-html-page/30565420
#
#     raw_html = resp_object.raw_response.content
#     soup = BeautifulSoup(raw_html, features= "lxml")
#     for script in soup(["script", "style"]):
#         script.extract()
#
#
#     lines = (line.strip() for line in soup.get_text().splitlines())
#     chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
#     text = '\n'.join(chunk for chunk in chunks if chunk)
#
#
#     original_text = [word.translate(str.maketrans('', '', string.punctuation)) for word in text.split() if word in stopwords or word.isalpha()]
#     filtered_text = set([word for word in original_text if word not in stopwords and word.isalpha()])
#
#   # Analytics
#     for word in filtered_text:
#         seen_words[word] += 1
#
#     return True if 0.25 < len(filtered_text)/len(original_text) < 0.5 else False
