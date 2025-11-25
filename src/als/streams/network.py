import asyncio
from concurrent.futures import Future
import ipaddress
import json
import os
import socket
from logging import getLogger
from types import MappingProxyType
from typing import Any, Iterable, List, Mapping, Optional, Sequence

from aiohttp import hdrs, web
import psutil

from als import config
from als.code_utilities import log, AlsLogAdapter

_LOGGER = AlsLogAdapter(getLogger(__name__), {})

WEB_SERVER_BIND_HOST = "0.0.0.0"
ADVERTISED_ADDRESS_AUTO = "auto"
ADVERTISED_ADDRESS_IP_PREFIX = "ip:"


class NetworkAddress:
    """Candidate IPv4 address that can be advertised to browser clients."""

    @log
    def __init__(
            self, interface_name: str, ip: str, url: str, is_loopback: bool,
            is_link_local: bool, is_private: bool, score: int,
            label: str) -> None:
        """
        Builds a display-ready local IPv4 address candidate.

        :param interface_name: OS-provided network interface name
        :param ip: IPv4 address to advertise
        :param url: Browser URL built from the IP address and server port
        :param is_loopback: True when the address is loopback-only
        :param is_link_local: True when the address is link-local
        :param is_private: True when the address is in a private range
        :param score: Ranking score used for Auto selection
        :param label: Human-readable label for UI dropdowns
        """
        self._interface_name = interface_name
        self._ip = ip
        self._url = url
        self._is_loopback = is_loopback
        self._is_link_local = is_link_local
        self._is_private = is_private
        self._score = score
        self._label = label

    @property
    @log
    def interface_name(self) -> str:
        """
        Returns the OS-provided network interface name.

        :return: network interface name
        """
        return self._interface_name

    @property
    @log
    def ip(self) -> str:
        """
        Returns the candidate IPv4 address.

        :return: IPv4 address
        """
        return self._ip

    @property
    @log
    def url(self) -> str:
        """
        Returns the browser URL for this address candidate.

        :return: browser URL
        """
        return self._url

    @property
    @log
    def is_loopback(self) -> bool:
        """
        Returns whether the candidate is loopback-only.

        :return: True when the candidate is loopback-only
        """
        return self._is_loopback

    @property
    @log
    def is_link_local(self) -> bool:
        """
        Returns whether the candidate is link-local.

        :return: True when the candidate is link-local
        """
        return self._is_link_local

    @property
    @log
    def is_private(self) -> bool:
        """
        Returns whether the candidate is in a private address range.

        :return: True when the candidate is private
        """
        return self._is_private

    @property
    @log
    def score(self) -> int:
        """
        Returns the Auto-selection ranking score.

        :return: ranking score
        """
        return self._score

    @property
    @log
    def label(self) -> str:
        """
        Returns the UI label for this address candidate.

        :return: display label
        """
        return self._label


@log
def _interface_name_score(interface_name: str) -> int:
    """
    Scores weak interface-name hints without filtering any candidates.

    :param interface_name: OS-provided network interface name
    :return: ranking adjustment for the interface name
    """
    normalized_name = interface_name.lower()
    physical_hints = (
        "wi-fi", "wifi", "wireless", "wlan", "wl",
        "ethernet", "eth", "enp", "ens", "eno",
    )
    virtual_hints = (
        "virtual", "vmware", "vbox", "hyper-v", "vethernet",
        "docker", "bridge", "br-", "vpn", "tun", "tap", "utun",
        "tailscale", "zerotier",
    )

    if any(hint in normalized_name for hint in physical_hints):
        return 10
    if any(hint in normalized_name for hint in virtual_hints):
        return -10
    return 0


@log
def _display_interface_name(interface_name: str) -> str:
    """
    Builds a conservative display name for an interface.

    :param interface_name: OS-provided network interface name
    :return: display name for address dropdown labels
    """
    normalized_name = interface_name.lower()
    if (
            "wi-fi" in normalized_name
            or "wifi" in normalized_name
            or "wireless" in normalized_name
            or normalized_name.startswith(("wlan", "wl"))):
        return "Wi-Fi"
    if (
            "ethernet" in normalized_name
            or normalized_name.startswith(("eth", "enp", "ens", "eno"))):
        return "Ethernet"
    if not interface_name:
        return ""
    return interface_name


@log
def _score_ip_address(
        ip_address: ipaddress.IPv4Address, interface_name: str) -> int:
    """
    Scores an IPv4 address for Auto advertised-address selection.

    :param ip_address: parsed IPv4 address
    :param interface_name: OS-provided network interface name
    :return: ranking score for the address
    """
    score = 0
    if ip_address.is_private:
        score += 100
    if ip_address.is_link_local:
        score -= 100
    if ip_address.is_loopback:
        score -= 200
    score += _interface_name_score(interface_name)
    return score


@log
def _network_address(interface_name: str, ip: str, port: int) -> NetworkAddress:
    """
    Converts an interface/IP pair into a normalized address candidate.

    :param interface_name: OS-provided network interface name
    :param ip: IPv4 address to advertise
    :param port: Web server port number used to build the URL
    :return: normalized network address candidate
    """
    ip_address = ipaddress.ip_address(ip)
    url = f"http://{ip}:{port}"
    display_name = _display_interface_name(interface_name)
    return NetworkAddress(
        interface_name=interface_name,
        ip=ip,
        url=url,
        is_loopback=ip_address.is_loopback,
        is_link_local=ip_address.is_link_local,
        is_private=ip_address.is_private,
        score=_score_ip_address(ip_address, interface_name),
        label=f"{display_name} - {ip}" if display_name else ip,
    )


@log
def get_network_address_candidates(
        port: int,
        interface_addresses: Optional[
            Mapping[str, Sequence[Any]]] = None) -> List[NetworkAddress]:
    """
    Retrieves local IPv4 addresses that can be advertised to web clients.

    :param port: Web server port number used to build candidate URLs
    :param interface_addresses: Optional psutil-style address mapping for tests
    :return: ranked list of network address candidates
    :rtype: list[NetworkAddress]
    """
    if interface_addresses is None:
        interface_addresses = psutil.net_if_addrs()
    candidates = []
    seen_ips = set()

    for interface_name, addresses in interface_addresses.items():
        for address in addresses:
            if address.family != socket.AF_INET:
                continue
            try:
                ip_address = ipaddress.ip_address(address.address)
            except ValueError:
                continue
            if ip_address.version != 4 or address.address in seen_ips:
                continue
            seen_ips.add(address.address)
            candidates.append(
                _network_address(interface_name, address.address, port))

    if not candidates:
        candidates.append(_network_address("Loopback", "127.0.0.1", port))

    return sorted(
        candidates, key=lambda candidate: (-candidate.score, candidate.ip))


@log
def advertised_address_preference(ip: str) -> str:
    """
    Builds the persisted preference value for an advertised IP address.

    :param ip: IP address
    :return: persisted preference value
    :rtype: str
    """
    return f"{ADVERTISED_ADDRESS_IP_PREFIX}{ip}"


@log
def select_advertised_address(
        preference: Optional[str],
        candidates: Iterable[NetworkAddress]) -> NetworkAddress:
    """
    Selects the advertised address from a persisted preference and candidates.

    :param preference: persisted preference value, either auto or ip:<address>
    :param candidates: ranked NetworkAddress candidates
    :return: selected candidate
    :rtype: NetworkAddress
    """
    candidates = list(candidates)
    if not candidates:
        candidates = get_network_address_candidates(
            config.get_www_server_port_number(), {})

    by_ip = {candidate.ip: candidate for candidate in candidates}
    if preference and preference.startswith(ADVERTISED_ADDRESS_IP_PREFIX):
        preferred_ip = preference[len(ADVERTISED_ADDRESS_IP_PREFIX):]
        preferred_candidate = by_ip.get(preferred_ip)
        if preferred_candidate:
            return preferred_candidate

    return candidates[0]


class Server:

    _NO_CACHE_HEADERS: Mapping[str, str] = MappingProxyType({
        'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
        'Pragma': 'no-cache',
        'Expires': '0'
    })

    @staticmethod
    def _no_cache_file_response(path: str) -> web.FileResponse:
        """
        Builds a file response with aggressive no-cache directives.

        :param path: filesystem path to serve
        :return: prepared HTTP response
        """
        response = web.FileResponse(path)
        response.headers.update(Server._NO_CACHE_HEADERS)
        response.headers.pop(hdrs.ETAG, None)
        response.headers.pop(hdrs.LAST_MODIFIED, None)
        return response

    @log
    def __init__(self, static_path):
        self._static_path = static_path
        self._app = web.Application()
        self._app.add_routes([web.get('/ws', self._websocket_handler)])
        self._app.add_routes([web.get('/', self._index_handler)])
        self._app.add_routes([web.get('/data.json', self._data_handler)])
        self._app.add_routes([web.get('/web_image.jpg', self._image_handler)])

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
    async def _index_handler(self, _: web.Request) -> web.StreamResponse:
        """Serve the main webview page."""
        return web.FileResponse(os.path.join(self._static_path, 'index.html'))

    @log
    async def _data_handler(self, _: web.Request) -> web.StreamResponse:
        """Serve exposition data without caching."""
        return self._no_cache_file_response(os.path.join(self._static_path, 'data.json'))

    @log
    async def _image_handler(self, _: web.Request) -> web.StreamResponse:
        """Serve the latest web image without caching."""
        return self._no_cache_file_response(os.path.join(self._static_path, 'web_image.jpg'))

    @log
    async def _send_message_to_clients(self, message):
        for ws in self._clients:
            await ws.send_str(json.dumps(message))

    @log
    def _set_startup_exception(
            self, startup_future: Optional[Future], error: Exception) -> None:
        """
        Stores server startup failure for the controller thread.

        :param startup_future: future shared with the controller
        :param error: startup error to report
        """
        if startup_future is not None and not startup_future.done():
            startup_future.set_exception(error)

    @log
    def _set_startup_success(self, startup_future: Optional[Future]) -> None:
        """
        Stores server startup success for the controller thread.

        :param startup_future: future shared with the controller
        """
        if startup_future is not None and not startup_future.done():
            startup_future.set_result(None)

    @log
    async def _start_server(
            self, host: str, port: int,
            startup_future: Optional[Future] = None) -> None:
        """
        Starts the aiohttp server and reports bind success or failure.

        :param host: host address to bind
        :param port: port number to bind
        :param startup_future: optional future shared with the controller
        """
        try:
            self._runner = web.AppRunner(self._app)
            await self._runner.setup()
            site = web.TCPSite(self._runner, host, port)
            await site.start()
        except Exception as error:
            self._set_startup_exception(startup_future, error)
            if self._runner:
                await self._runner.cleanup()
            raise

        self._set_startup_success(startup_future)

        try:
            while True:
                await asyncio.sleep(3600)
        except asyncio.CancelledError:
            pass

    @log
    def _on_server_task_done(
            self, task: asyncio.Task, startup_future: Optional[Future]) -> None:
        """
        Stops the event loop when startup fails before normal server shutdown.

        :param task: server coroutine task
        :param startup_future: future shared with the controller
        """
        if task.cancelled():
            return

        error = task.exception()
        if error is not None:
            self._set_startup_exception(startup_future, error)
            self._loop.stop()

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
    def start(
            self, host: str = WEB_SERVER_BIND_HOST, port: Optional[int] = None,
            startup_future: Optional[Future] = None) -> None:
        """
        Starts the web server event loop.

        :param host: host address to bind
        :param port: port number to bind
        :param startup_future: optional future used to report startup result
        """
        asyncio.set_event_loop(self._loop)
        if port is None:
            port = config.get_www_server_port_number()
        self._server_task = self._loop.create_task(
            self._start_server(host, port, startup_future))
        self._server_task.add_done_callback(
            lambda task: self._on_server_task_done(task, startup_future))
        self._loop.run_forever()
