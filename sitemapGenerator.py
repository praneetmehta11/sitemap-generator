from concurrent.futures import ThreadPoolExecutor, wait
import threading
import queue
from scrapers.scraper import connectToBase, getDriver, getUrls
from time import sleep, time
from urllib.parse import urlsplit, urlunsplit, urljoin, urlparse
import re

MAX_WORKER = 4


class Crawler(threading.Thread):

    def __init__(self, baseUrl):
        super(Crawler, self).__init__()
        self.yetToCrawelQueue = queue.Queue()
        self.crawledPages = set()
        self.count = 1
        self.executor = ThreadPoolExecutor(max_workers=MAX_WORKER)
        self.baseURL = self.normalizeUrl(baseUrl)
        scheme = urlparse(self.baseURL).scheme
        if scheme == "":
            self.baseURL = "https://"+self.baseURL
        scheme, netloc, path, qs, anchor = urlsplit(self.baseURL)
        self.baseURL = urlunsplit((scheme, netloc, "", "", ""))
        self.host = urlparse(self.baseURL).netloc
        self.error = False
        self.completed = False
        self.excludedPattern = r".(gif|jpg|jpeg|png|ico|bmp|ogg|webp|mp4|webm|mp3|ttf|woff|json|rss|atom|gz|zip|rar|7z|css|js|gzip|exe|svg)$"
        self.yetToCrawelQueue.put(self.baseURL)
        self.stop = False
        print("BASE URL : ", self.baseURL)
        return

    def kill(self):
        self.stop = True

    def run(self):
        self.stop=False
        while True and self.stop == False:
            if self.count == 0 or self.error:
                break
            if not self.yetToCrawelQueue.empty():
                url = self.yetToCrawelQueue.get()
                self.crawledPages.add(url)
                self.executor.submit(crawlerWorker, self, url)
        self.completed = True
        return

    def addToQueue(self, urls):
        filteredUrls = self.filterUrls(urls)
        self.count += len(filteredUrls)
        for url in filteredUrls:
            self.yetToCrawelQueue.put(url)
        return

    def filterUrls(self, urls):
        allowedUrls = []
        for url in urls:
            if url.startswith("/"):
                url = self.baseURL+url
            if "#" in url:
                continue
            url = self.normalizeUrl(url)
            if url.endswith("/"):
                url = url[0:-1]
            if self.isInternal(url) == False:
                continue
            if re.search(self.excludedPattern, url):
                continue
            if url.endswith("/"):
                tempUrl = url[0:-1]
                if tempUrl in self.crawledPages:
                    continue
            tempUrl = url+"/"
            if url in self.crawledPages or tempUrl in self.crawledPages:
                continue
            allowedUrls.append(url)
        return allowedUrls

    def normalizeUrl(self, url):
        scheme, netloc, path, qs, anchor = urlsplit(url)
        return urlunsplit((scheme, netloc, path, qs, anchor))

    def isInternal(self, url):
        host = urlparse(url).netloc
        return host == self.host


def crawlerWorker(crawler, url):
    if crawler.stop:
        return
    try:
        print("Crawling page")
        browser = getDriver()
        if connectToBase(browser, url):
            sleep(2)
            html = browser.page_source
            newUrls = getUrls(html)
            crawler.addToQueue(newUrls)
            crawler.count -= 1
            browser.quit()
        else:
            crawler.error = True
            print("Error while Crawling page : "+url)
    except:
        crawler.error = True
        pass


def getSiteMap(url):
    crawler = Crawler(url)
    crawler.start()
    crawler.join()
    if crawler.error == False:
        return crawler.crawledPages
    else:
        return None


if __name__ == '__main__':
    url = "https://www.google.com"
    siteMap = getSiteMap(url)
    if siteMap:
        print(siteMap)
        print(len(siteMap))
    else:
        print("Error while generating sitemap")
    pass
