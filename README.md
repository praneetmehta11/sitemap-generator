# Sitemap Generator
Sitemap Generator is a python based web crawler that generates sitemap for a given website.

### Prerequisites:
* Python 3
* Google chrome browser Latest (required for selenium)

### Dependencies:
>beautifulsoup4,requests,selenium,Flask

##### For installing dependencies:
    pip3 install -r requirements.txt

### To run the project 
    RUN python3 app.py 
    Now open http://localhost:5000/ in browser

### If you wish to run sitemapGenerator without UI  
    RUN python3 sitemapGenerator.py

### Note
>By default, only 4 threads will concurrently crawl a particular site. If you wish to improve the speed of the sitemap generator, increase the number of concurrent threads by modifying MAX_WORKER variable in sitemapGenerator.py file according to your need.