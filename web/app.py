import duckduckpy
from flask import Flask, abort, jsonify, request
import requests

app = Flask(__name__)


@app.route('/', methods=['POST'])
def root():
    include = request.args.getlist('include[]')
    exclude = request.args.getlist('exclude[]')
    equipment = request.args.getlist('equipment[]')
    offset = request.args.get('offset', type=int, default=0)

    # Ensure we can form a positive query
    if not include and not equipment:
        return abort(400)

    # Ignore pagination for now
    if offset > 0:
        return abort(501)

    # Construct a web search query
    query = ' '.join(include)
    query += ' -'.join([''] + exclude)
    query += ' '.join([''] + equipment)
    query += ' recipes'

    response = duckduckpy.secure_query(query)
    urls = [result.first_url for result in response.results]
    for url in urls:
        requests.post(
            url='http://api-service/api/recipes/crawl',
            data={'url': url}
        )
    return jsonify(urls)
