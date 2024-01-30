import redis
import socket
import time
from cassandra.cluster import Cluster

hostname = socket.gethostname()
master = redis.Redis(host='redis-primary', port=6379)

try:
    cluster = Cluster(['10.128.1.42', '10.128.2.42', '10.128.3.42'])
    session = cluster.connect('urlshortener')
except Exception:
    session = None

stream_name = 'url_stream'
group_name = 'url_group'

try:
    master.xgroup_create(stream_name, group_name, id='0', mkstream=True)
except Exception as e:
    print(e)


def process_messages():
    counter = 0
    total_time = 0
    while True:
        try:
            messages = master.xreadgroup(group_name, hostname, {stream_name: '>'}, count=100, block=0)
            start_time = time.time()
            for stream, stream_message in messages:
                for message in stream_message:

                    msg_id, data = message

                    short_url = data[b'short_url'].decode('utf-8')
                    long_url = data[b'long_url'].decode('utf-8')

                    session.execute("INSERT INTO urls (short_url, long_url) VALUES (%s, %s)", (short_url, long_url))
                    master.xack(stream_name, group_name, msg_id)

                    counter += 1
            end_time = time.time()
            total_time += end_time - start_time
        except Exception as e:
            print(e)
        print("Message Processed: ", counter)
        print("Total Time: ", total_time)


if __name__ == '__main__':
    process_messages()
