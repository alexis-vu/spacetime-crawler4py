from urllib.parse import urlparse
import sys
import re

def main():
    links = open(sys.argv[-1])
    for link in links:
        parsed = urlparse(link)

        extensions = "(\.)?(css|js|bmp|gif|jpe?g|ico|png|tiff?|mid|mp2|mp3|mp4|wav|avi|mov|mpeg|ram|" \
                     "m4v|mkv|ogg|ogv|pdf|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|" \
                     "bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1|thmx|mso|arff|rtf|jar|csv|" \
                     "rm|smil|wmv|swf|wma|zip|rar|gz)"

        if re.search(extensions, parsed.path) != None:
            print("path check")
            print(link)
            return False

        if re.search(extensions, parsed.netloc) != None:
            print("netloc check")
            print(link)
            return False

if __name__ == '__main__':
    main()
