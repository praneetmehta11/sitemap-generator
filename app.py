from flask import Flask, render_template, request, jsonify
import uuid
from sitemapGenerator import getSiteMap, Crawler
app = Flask(__name__)

#Flask application for creating wrapper over site

activeCralwer = {}
sitemap = {}


@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html")


@app.route('/generateSitemap', methods=['POST'])
def generateSitemap():
    body = request.json
    baseUrl = body["baseUrl"]
    if not baseUrl.endswith("/"):
        baseUrl+="/"
    if baseUrl in sitemap:
        crawler=sitemap[baseUrl]["crawler"]
        if crawler.stop==False:
            return jsonify({"requestId": sitemap[baseUrl]["requestId"]})
    id = str(uuid.uuid4())
    id = id.replace("-", "")
    activeCralwer[id] = Crawler(baseUrl)
    sitemap[baseUrl] = {"requestId": id, "crawler": activeCralwer[id]}
    activeCralwer[id].start()
    return jsonify({"requestId": id})


@app.route('/getSitemap', methods=['POST'])
def getSitemap():
    body = request.json
    requestId = body["requestId"]
    if requestId not in activeCralwer:
         return jsonify({"error": "Invalid RequestId"})
    crawler = activeCralwer[requestId]
    if crawler.completed:
        if crawler.error:
            return jsonify({"requestId": requestId, "baseUrl": crawler.baseURL, "status": str(crawler.completed),"sitemap":list(crawler.crawledPages),"error":True})
        return jsonify({"requestId": requestId, "baseUrl": crawler.baseURL, "status": str(crawler.completed),"sitemap":list(crawler.crawledPages)})
    else:
        return jsonify({"requestId": requestId, "baseUrl": crawler.baseURL, "status": str(crawler.completed), "message": "Generating sitemap"})

@app.route('/cancle', methods=['POST'])
def stopCrawling():
    body = request.json
    requestId = body["requestId"]
    if requestId not in activeCralwer:
         return jsonify({"error": "Invalid RequestId"})
    crawler = activeCralwer[requestId]
    crawler.kill()
    if crawler.completed:
        if crawler.error:
            return jsonify({"requestId": requestId, "baseUrl": crawler.baseURL, "status": str(crawler.completed),"sitemap":list(crawler.crawledPages),"error":True})
        return jsonify({"requestId": requestId, "baseUrl": crawler.baseURL, "status": str(crawler.completed),"sitemap":list(crawler.crawledPages)})
    else:
        return jsonify({"requestId": requestId, "baseUrl": crawler.baseURL, "status": str(crawler.completed), "message": "Generating sitemap","sitemap":list(crawler.crawledPages)})



if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=False)


