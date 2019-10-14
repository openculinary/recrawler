from duckpy import Client as ddg
from flask import Flask, abort, jsonify, request
from requests_futures.sessions import FuturesSession

app = Flask(__name__)


@app.route('/', methods=['POST'])
def root():
    products = request.args.getlist('products[]')
    if not products:
        return abort(400)

    products = ' '.join(products)
    results = ddg().search(f'{products} recipes')
    urls = [result['url'] for result in results]

    session = FuturesSession()
    for url in urls:
        session.post(
            url='http://api-service/api/recipes/crawl',
            data={'url': url}
        )

    return jsonify(urls)
