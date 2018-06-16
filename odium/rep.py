"""
provides a REP endpoint listening for REQ.
Each REQ connection is handled by a coroutine (asyncio) and REP sent when its work is done.
"""
import logging
import zmq.asyncio
import asyncio
import uvloop

log = logging.getLogger(__name__)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def rep_server(port, req_processor):
    context = zmq.asyncio.Context()
    server = context.socket(zmq.REP)
    server.bind(f"tcp://*:{port}")
    loop = asyncio.get_event_loop()
    loop.create_task(req_handler(server, req_processor))
    loop.run_forever()

async def req_handler(server, req_processor):
    while True:
        req = await server.recv_json()
        rep = await req_processor(req)
        server.send_json(rep, separators=(',',':'))

async def echo(req):
    log.info(req)
    return req

if __name__=='__main__':
    import sys
    from odium import config
    logging.basicConfig(level=20)
    port = config['ports']['REQ_REP']
    rep_server(port, echo)
