import os

from cachetools import TTLCache
from flask import Flask, abort, jsonify, request
import httpx
from pymojeek import Search

app = Flask(__name__)

query_cache = TTLCache(maxsize=512, ttl=60 * 60 * 4)


@app.route("/", methods=["POST"])
def root():
    include = request.args.getlist("include[]")
    exclude = request.args.getlist("exclude[]")
    equipment = request.args.getlist("equipment[]")
    offset = request.args.get("offset", type=int, default=0)

    # Forward up to five terms from each of the include and exclude lists;
    # equipment terms are ignored currently, to increase the cache hit ratio
    include = include[:5]
    exclude = exclude[:5]
    equipment = equipment[:0]

    # Ensure we can form a positive query
    if not include and not equipment:
        return abort(400)

    # Ignore pagination for now
    if offset > 0:
        return abort(501)

    # Construct a web search query
    query = " ".join(include)
    query += " ".join([""] + equipment)
    query += " recipes"

    # Use an in-process time-limited cache to filter repeat queries
    cache_key = query + " -".join([""] + exclude)
    if cache_key in query_cache:
        return abort(501)
    query_cache[cache_key] = True

    client = Search(api_key=os.environ.get("MOJEEK_API_KEY"), safe_search=True)
    results = client.search(query, exclude_words=exclude)
    urls = [result.url for result in results]
    for url in urls:
        httpx.post(url="http://backend-service/recipes/crawl", data={"url": url})
    return jsonify(urls)
