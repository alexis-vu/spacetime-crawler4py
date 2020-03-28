from bs4 import BeautifulSoup
import re, requests
from urllib.parse import urlparse, parse_qs
from collections import defaultdict

subdomains = defaultdict(set)
words_dict = defaultdict(int)
longest_page = ("link", 0)
unique_pages = set()


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links]


def extract_next_links(url, resp):
    # Implementation required.
    next_links = set()
    if resp.status in range(200, 300):
        html = resp.raw_response.content
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            if link.get('href') is not None:
                link = is_abs_url(url, link.get('href'))
                if is_valid(link):
                    next_links.add(link)

    return next_links


def is_valid(url):
    valid_domains = ["www.ics.uci.edu",
                     "www.cs.uci.edu",
                     "www.informatics.uci.edu",
                     "www.stat.uci.edu",
                     "today.uci.edu/department/information_computer_sciences"]
    try:
        parsed = urlparse(url)

        # Checks if scheme is valid
        if parsed.scheme not in set(["http", "https"]):
            return False

        # Checks if domain or if subdomain is valid
        # Need to edit and accept subdomains ie.e visions.ics.uci.edu
        domain = "(ics\.uci\.edu|cs\.uci\.edu|informatics\.uci\.edu|stat\.uci\.edu|today\.uci\.edu\/department\/information_computer_sciences)"
        if not re.search(domain, parsed.netloc):
            # print(parsed.netloc + " domain regex does not work")
            return False

        # cannot crawl to sites with the following in their url
        # i.e. /about/pdf/textbook.html is not a valid url
        # i.e. /about/hello/textbook.pdf is not a valid url
        extensions = "(css|js|bmp|gif|jpe?g|ico|png|tiff?|mid|mp2|mp3|mp4|wav|avi|mov|mpeg|ram|" \
                     "m4v|mkv|ogg|ogv|pdf|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|" \
                     "bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1|thmx|mso|arff|rtf|jar|csv|" \
                     "rm|smil|wmv|swf|wma|zip|rar|gz)"

        if re.search(("(/)" + extensions), parsed.path):
            # print(parsed.path + " wrong extension in path")
            return False

        if re.search("(.)" + extensions, parsed.netloc):
            # print(parsed.netloc + " wrong extension in domain")
            return False

        # Check if the URL has more than 1 query parameter
        if len(parse_qs(parsed.query)) > 1:
            # print(url + " too many params")
            return False
        if 'reply' in str(parsed.query) or 'share' in str(parsed.query):
            # print(parsed.query + " reply/share inside query")
            return False

        # Checks the len of the URL, if it has more than 250, it is not valid
        if len(url) > 250:
            # print(url + "len is too long")
            return False

        # Check if URL is an anchor or a calendar
        if '#' in url or 'calendar' in url:
            # print(url + " calendar/anchor trap")
            return False

        # Check if the subdirectories in the path do not repeat
        path_directory = parsed.path[1:].split('/')
        if len(path_directory) != len(set(path_directory)):
            # print(url + " repeating directories")
            return False

        # Write an function to test the quality of the content given
        # Function should take in a URL
        # First filter out the stop words
        # count the amount of unique words and the total amount of words (minus the stopwords)
        # return true if ratio is in range (0.20,0.80)
        if not check_value(url):
            # print(url + " low value content")
            return False

        else:
            unique_pages.add(url)
            netloc = parsed.netloc.split(".")
            domain = ".".join(netloc[1:4])
            subdomain = ".".join(netloc[0:4])
            if domain == "ics.uci.edu":
                subdomains[subdomain].add(url)
            return True

    except TypeError:
        raise


def tokenize(unicode):
    str = unicode.encode('utf-8')
    split_str = re.split('[^A-Za-z]', str.decode('utf-8'))

    tokens = []
    for word in split_str:
        if len(word) > 0:
            word = word.lower()
            tokens.append(word)

    return tokens


def check_value(url):
    global words_dict, longest_page
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

    try:
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

        if len(original_text) == 0:
            return False

        # filter stop words out original text
        filtered_text = []
        for text in original_text:
            if text not in stop_words:
                filtered_text.append(text)

        # compute measure for usefulness of webpage content
        measure = float(len(filtered_text)) / float(len(original_text))

        # return true if usefulness measure beteween 25%-75%
        if 0.20 < measure < 0.80:
            if longest_page[0] < len(original_text):
                longest_page = (url, len(original_text))
            for word in filtered_text:
                words_dict[word] += 1
            return True
        else:
            return False
    except:
        return False


def is_abs_url(base_url, found_url):
    parsed_found = urlparse(found_url)
    parsed_base = urlparse(base_url)

    if parsed_found.scheme == '' and parsed_found.netloc == '':
        missing = parsed_base.scheme + '://' + parsed_base.netloc
        found_url = missing + found_url

    elif parsed_found.scheme == '':
        missing = parsed_base.scheme + '://'
        found_url = missing + found_url

    if parsed_found.fragment != '':
        found_url = found_url.replace(('#' + parsed_found.fragment), '')

    return found_url
