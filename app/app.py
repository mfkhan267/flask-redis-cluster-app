import time
import redis
from flask import Flask, render_template
import socket
from redis.cluster import RedisCluster

app = Flask(__name__)

# Redis Cluster setup using environment variables
startup_nodes = [{"host": "redis-cluster", "port": "6379"}]

cache = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route("/")
def index():
    count = get_hit_count()
    hostname = socket.gethostname()
    return render_template('index.html', hostname=hostname, count=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

