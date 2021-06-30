from flask import Flask, Response, json
from flask import request
import time
import redis

"""
FlaskServer class is a class that opens a server and allow to publish messages
get the last message that published, and get list of messages in time interval
"""
class FlaskServer():
    def __init__(self):
        self._app = Flask(__name__)
        self._app.add_url_rule(rule='/publish/', view_func=self._publish, methods=['POST'])
        self._app.add_url_rule(rule='/getLast/', view_func=self._get_last, methods=['GET'])
        self._app.add_url_rule(rule='/getByTime/', view_func=self._get_by_time, methods=['GET'])
        self._redis = None

    """
    run_server function runs the rest api server
    """
    def run_server(self):
        self._app.run(host="0.0.0.0")

    """
    init_redis function inits the redis server
    """
    def init_redis(self, host):
        self._redis = redis.StrictRedis(host=host, charset="utf-8", decode_responses=True)

    """
    publish function gets rest api POST request with message in content argument 
    and set it in redis in sorted set, the key is the timestamp and the value is
    json with the timestamp and the message
    """
    def _publish(self):
        timestamp = float(time.time())
        status = 201
        msg = 'OK'
        message = request.args.get('content')
        if message is not None:
            json_message = {timestamp : message}
            self._redis.zadd('messages', timestamp, json.dumps(json_message))
        else:
            msg = 'Error: content not found'
            status = 400
        return Response(msg, status=status)

    """
    get_last function returns the last message that published
    """
    def _get_last(self):
        last_message = self._redis.zrange('messages', -1, -1)
        if not last_message:
            return Response('Error: there are no messages', status=400)
        return Response(last_message[0], status=200)

    """
    get_by_time function returns all message that published between two timestamps.
    the rest api GET request should include two arguments - start and end with the timestamps.
    """
    def _get_by_time(self):
        start = request.args.get('start')
        end = request.args.get('end')
        if start is None or end is None:
            return Response('Error: cannot get values', status=400)
        if end < start:
            return Response('Error: end value is smaller then start value', status=400)
        num_of_redis_messages = self._redis.zcount('messages', '-inf', '+inf')
        if num_of_redis_messages > 0 :
            list_of_requested_messages = self._redis.zrangebyscore('messages', float(start), float(end))
        else:
            return Response('Error: there are no messages', status=400)
        return Response(json.dumps({'messages': list_of_requested_messages}), status=200)