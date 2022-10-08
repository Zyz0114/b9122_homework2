from bs4 import BeautifulSoup
import urllib.request


def main():
    seed_url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"
    keyword = "covid"
    min_num_url = 10
    urls = [seed_url]       # queue of the urls to crawl
    seen = [seed_url]       # stack of urls seen so far
    opened = []             # keep track of seen urls so that we don't revisit them

    print("Starting with URL = " + str(urls))

    while len(urls) > 0 and len(opened) < min_num_url:
        try:
            curr_url = urls.pop()
            # print("Number of URLS in stack: %d" % (len(urls)))
            # print("Trying to access: " + curr_url)
            req = urllib.request.Request(curr_url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urllib.request.urlopen(req).read()
            # opened.append(curr_url)
        except Exception as e:
            print("Unable to access: " + curr_url)
            print(e)
            continue

        if keyword in str(webpage).lower():
            opened.append(curr_url)
            print("The %d URL contains %s: %s" % (len(opened), keyword, curr_url))

        # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
        # ADD THE URLS FOUND TO THE QUEUE url AND seen
        soup = BeautifulSoup(webpage, features="html.parser")
        # Put child URLs into the stack
        for tag in soup.find_all('a', href=True):
            child_url = urllib.parse.urljoin(seed_url, tag['href'])
            # print("Seed URL: " + seed_url)
            # print("Original Child URL: " + tag['href'])
            # print("Child URL: " + child_url)
            # print("Seed URL in Child URL: " + str(seed_url in child_url))
            if seed_url not in child_url and child_url not in seen:
                urls.append(child_url)
                seen.append(child_url)

    print("========================================")
    print("The following URLs contain " + keyword)
    for i, url in enumerate(opened):
        print(str.format("{}: {}", i + 1, url))


if __name__ == '__main__':
    main()
