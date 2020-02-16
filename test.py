import re
from urllib.parse import urlparse
import sys

parsed_paths = dict()

def is_redirect(root, end):
    if root in parsed_paths.keys():
        if parsed_paths[root] != end:
            print(root)
            print(parsed_paths[root])
            return True
    else:
        parsed_paths[root] = end
        return False

def main():
    urls = open(sys.argv[-1])
    for url in urls:
        url = url.rstrip('/\n')
        parsed = urlparse(url)
        path = parsed.path.split('/')
        root = parsed.netloc + '/'
        home = parsed.netloc + '/'

        for i in range (1, len(path) - 1):
            root += path[i]
            root += '/'

        end = path[-1]

        if root == home:
            parsed_paths[path] = ''
        else:
            if is_redirect(root, end):
                print("redirect found")
                print(root)
                print(end)

    for k, v in parsed_paths.items():
        print(k + " : " + v)

if __name__ == '__main__':
    main()

# print(root_path)
# print(end_path)
