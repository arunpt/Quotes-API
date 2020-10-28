from flask import Flask, jsonify
from goodreads import GoodReads

api = Flask(__name__)

@api.route('/')
def index():
    res = {
      'status': 200,
      'about': 'Quotes api by W4RR10R',
      'usage': [
         '/random',
         '/search/query/no of pages'
       ]
    }
    return jsonify(res)
 
@api.route('/random')
def random_quotes():
    return jsonify(GoodReads().random)

@api.route('/search')
def search():
    res = {
       "error": {
          'status': 400,
          'detail': 'No search query found'
       }
    }
    return jsonify(res)
 
@api.route('/search/<query>', defaults= {"pages": 1})  
@api.route('/search/<query>/<pages>')
def search_quotes(query, pages):
    results = GoodReads.search_all(query, int(pages))
    return jsonify(results)
       
if __name__ == '__main__':
    api.run(host="0.0.0.0", port=5000, debug=True)