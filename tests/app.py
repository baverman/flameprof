import time


def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    time.sleep(1)
    return [b"Hello World"]
