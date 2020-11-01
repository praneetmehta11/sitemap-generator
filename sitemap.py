from concurrent.futures import ThreadPoolExecutor, wait
import threading
import queue
from scrapers.scraper import connectToBase, getDriver, getUrls
from time import sleep, time


class Crawler(threading.Thread):

    def __init__(self, baseUrl):
        super(Crawler, self).__init__()
        self.yetToCrawelQueue = queue.Queue()
        self.crawledPages = set()
        self.count = 1
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.baseURL = baseUrl
        self.isError = False
        if ":" not in self.baseURL:
            self.baseURL = "https://"+self.baseURL
        self.yetToCrawelQueue.put(self.baseURL+"/")
        return

    def run(self):
        while True:
            if self.count == 0 or self.isError:
                break
            if not self.yetToCrawelQueue.empty():
                url = self.yetToCrawelQueue.get()
                self.crawledPages.add(url)
                self.executor.submit(crawlerWorker, self, url)
        return

    def addToQueue(self, urls):
        filteredUrls = self.filterUrls(urls)
        self.count += len(filteredUrls)
        for url in filteredUrls:
            self.yetToCrawelQueue.put(url)
        return

    def filterUrls(self, urls):
        allowedUrls = []
        baseUrl = self.baseURL
        baseUrlWithoutSubdomain = self.baseURL
        for url in urls:
            if "#" in url:
                continue
            if url.startswith("/"):
                url = baseUrl+url
            if not url.endswith("/"):
                url += "/"
            if url.startswith(baseUrl) == False and url.startswith(baseUrlWithoutSubdomain) == False:
                continue
            if url in self.crawledPages:
                continue
            allowedUrls.append(url)
        return allowedUrls


def crawlerWorker(crawler, url):
    try:
        print("Crawling Page : "+url)
        browser = getDriver()
        if connectToBase(browser, url):
            sleep(2)
            html = browser.page_source
            newUrls = getUrls(html)
            crawler.addToQueue(newUrls)
            crawler.count -= 1
            browser.quit()
        else:
            crawler.isError = True
            print("Error in loading page")
    except:
        crawler.isError = True
        pass


def getSiteMap(url):
    crawler = Crawler(url)
    crawler.start()
    crawler.join()
    if crawler.isError == False:
        return crawler.crawledPages
    else:
        return None


if __name__ == '__main__':
    url = "https://www.signzy.com"
    siteMap = getSiteMap(url)
    if siteMap:
        print(siteMap)
        print(len(siteMap))
    else:
        print("error in crawling page")
    pass
