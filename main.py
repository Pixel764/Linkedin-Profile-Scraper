from dotenv import load_dotenv
from Chrome import chrome
import sys


def main(time_per_page=5):
    path_to_urls_file = input('File (Full path): ')
    urls = []
    try:
        with open(path_to_urls_file, 'r') as file:
            for url in file.readlines():
                urls.append(url.strip())
    except FileNotFoundError:
        print('File Not Found!')
        exit()

    print('None = Html element is not found\n')
    chrome.start(urls, time_per_page)


if __name__ == '__main__':
    load_dotenv()

    if sys.argv[1]:
        main(int(sys.argv[1]))
    else:
        main()

