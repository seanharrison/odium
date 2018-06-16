"""
provides a SUB endpoint.
"""
import logging
import json
import zmq.asyncio
import asyncio
import uvloop

log = logging.getLogger(__name__)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def sub_subscriber(host, port, processor, subscription=''):
    context = zmq.asyncio.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect(f"tcp://{host}:{port}")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, subscription)

    loop = asyncio.get_event_loop()
    task = loop.create_task(sub_handler(subscriber, processor))
    loop.run_until_complete(task)

async def sub_handler(subscriber, processor):
    while True:
        msg_string = await subscriber.recv_string()
        msg = json.loads(msg_string)
        await processor(msg)

async def echo(msg):
    log.info(msg)

if __name__=='__main__':
    import sys
    from odium import config
    logging.basicConfig(level=20)
    host = 'localhost'
    port = config['ports']['PUB_SUB']
    subscriber = sub_subscriber(host, port, echo, subscription="")
