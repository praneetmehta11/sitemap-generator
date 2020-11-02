# Sitemap Generator
Sitemap Generator is a python based web crawler that generates sitemap for a given the website.

### Prerequisites:
* Python 3
* Google chrome browser Latest (required for selenium)

### Python dependencies:
>beautifulsoup4,requests,selenium,Flask

### For installing dependencies:
    pip install -r requirements.txt

### To run the project 
    RUN python3 app.py 
    Now open http://127.0.0.1:5000/ in browser
### Note
>If you run the above code,only 4 threads will run concurrently in order to crawl the particular site but if you like to improve the efficiency and speed of the sitemap generator you can increase the number of concurrent thread by modifying MAX_WORKER variable in sitemapGenerator.py file according to your need.