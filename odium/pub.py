"""
provides a PUB endpoint.
"""
import json
import logging
import zmq.asyncio
import asyncio
import uvloop

log = logging.getLogger(__name__)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def pub_publisher(port):
    context = zmq.asyncio.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(f"tcp://*:{port}")
    return publisher

async def publish(publisher, msg):
    await publisher.send_string(json.dumps(msg, separators=(',',':')))

if __name__=='__main__':
    import sys, time
    from odium import config
    logging.basicConfig(level=20)
    port = config['ports']['PUB_SUB']
    publisher = pub_publisher(port)
    loop = asyncio.get_event_loop()
    start_time = time.time()
    while True:
        time.sleep(1)
        task_time = round(time.time()-start_time, 2)
        task = loop.create_task(publish(publisher, {'t': task_time, 'argv': sys.argv[1:]}))
        loop.run_until_complete(task)
