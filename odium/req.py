
import logging
import zmq.asyncio
import asyncio
import uvloop

log = logging.getLogger(__name__)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def send_req(host, port, req):
    context = zmq.asyncio.Context()
    client = context.socket(zmq.REQ)
    client.connect(f"tcp://{host}:{port}")
    await client.send_json(req, separators=(',',':'))
    rep = await client.recv_json()
    return rep

if __name__=='__main__':
    from odium import config
    import json, sys
    logging.basicConfig(level=20)
    host = 'localhost'
    port = config['ports']['REQ_REP']
    loop = asyncio.get_event_loop()
    task = loop.create_task(send_req(host, port, {'argv': sys.argv[1:]}))
    rep = loop.run_until_complete(task)
    log.info(json.dumps(rep, separators=(',',':')))
