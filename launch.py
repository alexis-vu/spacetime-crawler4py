from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler
import scraper


def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    crawler = Crawler(config, restart)
    crawler.start()

if __name__ == "__main__":
    output = open("analytics.txt", "w")
    output.write("Analytics for Web Crawler\n")

    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)

    output.write("Unique pages found: " + str(len(scraper.unique_pages)) + '\n')
    output.write( "The longest page in terms of words is: " + scraper.longest_page[0] + " with " + str(scraper.longest_page[1]) + " words\n")

    output.write("The 50 Most Common Words Are:\n")
    counter = 0
    for k, v in sorted(scraper.words_dict.items(), key=lambda x: x[1], reverse=True):
        counter += 1
        if counter <= 50:
            output.write(str(k) + " " + str(v) + "\n")
        else:
            break

    output.write("The List of Subdomains Found:\n")
    for k, v in sorted(scraper.subdomains.items(), key=lambda x: x[1], reverse=True):
        output.write(str(k) + " " + str(len(v)) + "\n")

