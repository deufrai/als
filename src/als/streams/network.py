import asyncio
import json
import os
import socket
from logging import getLogger

from aiohttp import web

from als import config
from als.code_utilities import log, AlsLogAdapter

_LOGGER = AlsLogAdapter(getLogger(__name__), {})

@log
def get_host_ip():
    """
    Retrieves machine's IP address.

    :return: IP address
    :rtype: str
    """
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        test_socket.connect(('10.255.255.255', 1))
        ip_address = test_socket.getsockname()[0]
    except OSError:
        ip_address = '127.0.0.1'
    finally:
        test_socket.close()
    return ip_address

@log
def is_port_in_use(ip, port):
    """
    Checks if a given port on a given IP is in use.

    :param ip: IP address to check
    :param port: Port number to check
    :return: True if port is in use, False otherwise
    :rtype: bool
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex((ip, port))
        return result == 0

class Server:

    @log
    def __init__(self, static_path):
        self._static_path = static_path
        self._app = web.Application()
        self._app.add_routes([web.get('/ws', self._websocket_handler)])
        self._app.add_routes([web.get('/', self._index_handler)])

        # Catch-all route for static files
        self._app.router.add_static('/', self._static_path)

        self._clients = []
        self._runner = None
        self._loop = asyncio.new_event_loop()
        self._server_task = None

    @log
    async def _websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self._clients.append(ws)
        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    await ws.send_str(msg.data)
        finally:
            self._clients.remove(ws)
        return ws

    @log
    async def _index_handler(self, _):
        return web.FileResponse(os.path.join(self._static_path, 'index.html'))

    @log
    async def _send_message_to_clients(self, message):
        for ws in self._clients:
            await ws.send_str(json.dumps(message))

    @log
    async def _start_server(self, host, port):
        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, host, port)
        await site.start()

        try:
            while True:
                await asyncio.sleep(3600)
        except asyncio.CancelledError:
            pass

    @log
    async def _stop_server(self):
        # Notify clients to disconnect
        await self._send_message_to_clients({'type': 'disconnect'})

        # Wait for a short time to allow clients to disconnect
        await asyncio.sleep(2)

        if self._runner:
            await self._runner.cleanup()
        self._server_task.cancel()
        try:
            await self._server_task
        except asyncio.CancelledError:
            pass

    @log
    def stop(self):
        future = asyncio.run_coroutine_threadsafe(self._stop_server(), self._loop)
        future.result()  # Ensure the coroutine is awaited and completed
        self._loop.call_soon_threadsafe(self._loop.stop)

    @log
    def send_message(self, message):
        future = asyncio.run_coroutine_threadsafe(self._send_message_to_clients(message), self._loop)
        future.result()  # Ensure the coroutine is awaited and completed

    @log
    def start(self):
        asyncio.set_event_loop(self._loop)
        self._server_task = self._loop.create_task(self._start_server(get_host_ip(), config.get_www_server_port_number()))
        self._loop.run_forever()