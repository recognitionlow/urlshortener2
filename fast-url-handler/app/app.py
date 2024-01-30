from redis import Redis
from cassandra.cluster import Cluster
from flask import Flask, request, redirect


app = Flask(__name__)
master = Redis(host='redis-primary', port=6379)
slave = Redis(host='redis-replica', port=6379)

cluster = Cluster(['10.128.1.42', '10.128.2.42', '10.128.3.42'])
try:
    session = cluster.connect('urlshortener')
except Exception:
    session = None


@app.route('/', methods=['PUT'])
def save_long_url():
    short_url = request.args.get('short')
    long_url = request.args.get('long')

    if not short_url or not long_url:
        return 'bad request', 400

    try:
        master.set(short_url, long_url)
        master.xadd('url_stream', {'short_url': short_url, 'long_url': long_url})
        master.xadd('log_stream', {'short_url': short_url, 'long_url': long_url})
        return 'accepted', 200
    except Exception as e:
        print(e)
        return 'internal server error', 500


@app.route('/', methods=['GET'])
def invalid_method():
    return 'bad request', 400


@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    redis_down = False
    try:
        long_url = slave.get(short_url)
    except Exception:
        long_url = None
        redis_down = True

    if not long_url:
        try:
            rows = session.execute("SELECT long_url FROM urls WHERE short_url = %s", (short_url,))
        except Exception:
            if redis_down:
                return 'page not found', 404

        if not rows:
            return 'page not found', 404

        long_url = rows[0].long_url
        try:
            master.set(short_url, long_url)
        except Exception:
            pass

    return redirect(long_url, code=307)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
