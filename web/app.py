from cachetools import TTLCache
from flask import Flask, abort, jsonify, request
import httpx

app = Flask(__name__)

query_cache = TTLCache(maxsize=512, ttl=60 * 60 * 4)


@app.route("/", methods=["POST"])
def root():
    include = request.args.getlist("include[]")
    exclude = request.args.getlist("exclude[]")
    equipment = request.args.getlist("equipment[]")
    offset = request.args.get("offset", type=int, default=0)

    # Ensure we can form a positive query
    if not include and not equipment:
        return abort(400)

    # Ignore pagination for now
    if offset > 0:
        return abort(501)

    # Forward up to five terms from each of the include, exclude and equipment lists
    include = include[:5]
    exclude = exclude[:5]
    equipment = equipment[:0]

    # Construct a web search query
    query = " ".join(include)
    query += " -".join([""] + exclude)
    query += " ".join([""] + equipment)
    query += " recipes"

    # Use an in-process time-limited cache to filter repeat queries
    if query in query_cache:
        return abort(501)
    query_cache[query] = True

    # TODO: Restore recipe recrawling
    urls = []
    for url in urls:
        httpx.post(url="http://api-service/api/recipes/crawl", data={"url": url})
    return jsonify(urls)
