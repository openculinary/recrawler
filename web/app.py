from duckpy import Client as ddg
from flask import Flask, abort, jsonify, request
from requests_futures.sessions import FuturesSession

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

    results = ddg().search(query)
    urls = [result['url'] for result in results]

    session = FuturesSession()
    for url in urls:
        session.post(
            url='http://api-service/api/recipes/crawl',
            data={'url': url}
        )

    return jsonify(urls)
