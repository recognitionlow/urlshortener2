import redis
import os
from datetime import datetime

master = redis.Redis(host='redis-primary', port=6379)

stream_name = 'log_stream'
group_name = 'log_group'
data_dir = '/root/logs'

try:
    master.xgroup_create(stream_name, group_name, id='0', mkstream=True)
except Exception as e:
    print(e)


def process_messages():
    while True:
        try:
            messages = master.xreadgroup(group_name, 'log_consumer', {stream_name: '>'}, count=100, block=0)
            with open(os.path.join(data_dir, "logfile"), 'a+') as log:
                for stream, stream_message in messages:
                    for message in stream_message:
                        msg_id, data = message

                        short_url = data[b'short_url'].decode('utf-8')
                        long_url = data[b'long_url'].decode('utf-8')

                        log.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]   short: {short_url},   long: {long_url}\n')

                        master.xack(stream_name, group_name, msg_id)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    process_messages()
